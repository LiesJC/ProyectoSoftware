import cv2
import base64
import asyncio
import json
import threading
import time
from ultralytics import YOLO
from channels.generic.websocket import AsyncWebsocketConsumer
from queue import Queue
from sistema.basefirebase.firebase import *

class CameraConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.running = False
        self.mode = "raw"
        self.loop = asyncio.get_running_loop()
        self.model = YOLO("yolo11n.pt")
        self.frame_queue = Queue(maxsize=1)

    async def disconnect(self, close_code):
        self.running = False

    async def receive(self, text_data):
        if text_data == "start" and not self.running:
            self.running = True
            # Iniciar threads
            threading.Thread(target=self.capture_loop, daemon=True).start()
            threading.Thread(target=self.process_loop, daemon=True).start()
        elif text_data == "stop":
            self.running = False
        elif text_data in ("raw", "yolo"):
            self.mode = text_data

    # Captura continua de la cámara
    def capture_loop(self):
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        cap.set(cv2.CAP_PROP_FPS, 30)

        while self.running:
            ret, frame = cap.read()
            if not ret:
                continue

            # Mantener solo el último frame
            if not self.frame_queue.empty():
                try: self.frame_queue.get_nowait()
                except: pass
            self.frame_queue.put(frame)
            time.sleep(0.01)

        cap.release()

    # Procesamiento y envío
    def process_loop(self):
        while self.running:
            if self.frame_queue.empty():
                time.sleep(0.01)
                continue

            frame = self.frame_queue.get()
            counts = {}

            if self.mode == "yolo":
                yolo_frame = cv2.resize(frame, (416, 416))
                results = self.model(yolo_frame, conf=0.4, verbose=False)

                h, w, _ = frame.shape
                scale_x = w / 416
                scale_y = h / 416

                for box in results[0].boxes:
                    # Coordenadas escaladas al frame original
                    x1, y1, x2, y2 = map(float, box.xyxy[0])
                    x1 = int(x1 * scale_x)
                    x2 = int(x2 * scale_x)
                    y1 = int(y1 * scale_y)
                    y2 = int(y2 * scale_y)

                    cls = int(box.cls[0])
                    name = self.model.names[cls]

                    conf = float(box.conf[0])
                    conf_pct = int(conf * 100)

                    label = f"{name} {conf_pct}%"

                    # Contador con promedio de confianza (último frame)
                    counts[name] = {"count": counts.get(name, {"count":0})["count"] + 1,
                                    "conf": conf_pct}

                    # Dibujar caja y texto
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
                    cv2.putText(frame, label, (x1, y1-5),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)

            # Enviar frame siempre
            _, buffer = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 50])
            frame_b64 = base64.b64encode(buffer).decode("utf-8")

            asyncio.run_coroutine_threadsafe(
                self.send(text_data=json.dumps({"type":"frame","data":frame_b64})),
                self.loop
            )

            # Enviar conteos
            if counts:
                asyncio.run_coroutine_threadsafe(
                    self.send(text_data=json.dumps({"type":"counts","data":counts})),
                    self.loop
                )

            # Controlar FPS
            time.sleep(0.03 if self.mode=="raw" else 0.08)

class VisionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.model = YOLO("yolo11n.pt")

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        if text_data == "procesar":
            await self.process_frame()

    async def process_frame(self):
        # Toma un fotograma
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        ret, frame = cap.read()
        cap.release()
        if not ret:
            return

        # YOLO
        results = self.model(frame, conf=0.4, verbose=False)
        frame_detected = results[0].plot()

        # Conteo
        counts = {}
        for box in results[0].boxes:
            cls = int(box.cls[0])
            name = self.model.names[cls]
            conf = float(box.conf[0]) * 100
            counts[name] = counts.get(name, []) + [round(conf, 1)]

        # Imagen base64
        _, buffer = cv2.imencode(".jpg", frame_detected, [cv2.IMWRITE_JPEG_QUALITY, 70])
        frame_b64 = base64.b64encode(buffer).decode("utf-8")

        # Enviar al cliente
        await self.send(text_data=json.dumps({
            "type": "frame",
            "data": frame_b64,
            "counts": counts
        }))

        # 🔹 Cambiar vision a False después de procesar
        desactivar_vision()