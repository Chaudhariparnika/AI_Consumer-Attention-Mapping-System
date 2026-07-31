import os
from typing import Any, Dict, List, Optional

try:
    import cv2
except ImportError:  # pragma: no cover - optional dependency
    cv2 = None

try:
    from ultralytics import YOLO
except ImportError:  # pragma: no cover - optional dependency
    YOLO = None


class YOLOService:
    def __init__(self, model_name: Optional[str] = None, device: str = "cpu"):
        self.model_name = model_name or os.getenv("YOLO_MODEL", "yolov8n.pt")
        self.device = device
        self.model = None

    def _load_model(self):
        if self.model is not None:
            return self.model

        if cv2 is None:
            raise RuntimeError("opencv-python is not installed. Install it with: pip install opencv-python")

        if YOLO is None:
            raise RuntimeError("ultralytics is not installed. Install it with: pip install ultralytics")

        model_path = os.getenv("YOLO_MODEL_PATH")
        if model_path and os.path.exists(model_path):
            self.model = YOLO(model_path)
        else:
            self.model = YOLO(self.model_name)

        self.model.to(self.device)
        return self.model

    def predict_frame(self, frame, conf_threshold: float = 0.25) -> List[Dict[str, Any]]:
        model = self._load_model()
        results = model(frame, conf=conf_threshold, stream=False, verbose=False)

        detections: List[Dict[str, Any]] = []
        for result in results:
            boxes = result.boxes
            if boxes is None:
                continue

            for box in boxes:
                cls_id = int(box.cls[0].item()) if hasattr(box.cls[0], "item") else int(box.cls[0])
                class_name = result.names.get(cls_id, str(cls_id))
                confidence = float(box.conf[0].item()) if hasattr(box.conf[0], "item") else float(box.conf[0])
                x1, y1, x2, y2 = [float(v) for v in box.xyxy[0].tolist()]

                detections.append(
                    {
                        "class_name": class_name,
                        "confidence": round(confidence, 4),
                        "x1": int(x1),
                        "y1": int(y1),
                        "x2": int(x2),
                        "y2": int(y2),
                    }
                )

        return detections

    def process_rtsp_url(self, rtsp_url: str, conf_threshold: float = 0.25) -> List[Dict[str, Any]]:
        if cv2 is None:
            raise RuntimeError("opencv-python is not installed. Install it with: pip install opencv-python")

        cap = cv2.VideoCapture(rtsp_url)
        if not cap.isOpened():
            raise RuntimeError(f"Unable to open RTSP stream: {rtsp_url}")

        success, frame = cap.read()
        cap.release()

        if not success or frame is None:
            raise RuntimeError("Unable to read a frame from the RTSP stream")

        return self.predict_frame(frame, conf_threshold=conf_threshold)
