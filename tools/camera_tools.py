import subprocess
import cv2
import os
import threading
from datetime import datetime


# Camera preview state
_camera_thread = None
_camera_running = False


def open_camera():

    try:

        os.startfile(
            "microsoft.windows.camera:"
        )

        return "Camera opened successfully."

    except Exception:

        try:

            subprocess.Popen([
                "explorer.exe",
                "microsoft.windows.camera:"
            ])

            return "Camera opened successfully."

        except Exception as e:

            return (
                f"Failed to open camera: {e}"
            )


def close_camera():
    try:
        global _camera_running

        _camera_running = False

        subprocess.run(
            ["taskkill", "/F", "/IM", "WindowsCamera.exe"],
            capture_output=True,
            text=True
        )

        return "Camera closed successfully."

    except Exception as e:
        return f"Failed to close camera: {e}"


def take_photo():
    try:
        camera = cv2.VideoCapture(0)

        if not camera.isOpened():
            return "I could not access the camera."

        ret, frame = camera.read()
        camera.release()

        if not ret:
            return "Failed to capture photo."

        pictures_path = os.path.join(
            os.path.expanduser("~"),
            "Pictures"
        )

        os.makedirs(pictures_path, exist_ok=True)

        filename = datetime.now().strftime(
            "JARVIS_%Y%m%d_%H%M%S.jpg"
        )

        file_path = os.path.join(
            pictures_path,
            filename
        )

        cv2.imwrite(file_path, frame)

        return f"Photo captured successfully. Saved as {filename}."

    except Exception as e:
        return f"Failed to capture photo: {e}"


def camera_status():
    try:
        camera = cv2.VideoCapture(0)

        if not camera.isOpened():
            camera.release()
            return "Camera is not available."

        ret, frame = camera.read()
        camera.release()

        if ret:
            return "Camera is connected and working."

        return "Camera is connected but I could not access the video."

    except Exception as e:
        return f"Failed to check camera: {e}"


def _camera_preview_worker():
    global _camera_running

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        _camera_running = False
        return

    cv2.namedWindow("JARVIS Camera", cv2.WINDOW_NORMAL)

    while _camera_running:

        ret, frame = camera.read()

        if not ret:
            break

        cv2.imshow("JARVIS Camera", frame)

        # Q = stop preview
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    _camera_running = False

    camera.release()
    cv2.destroyAllWindows()


def start_live_preview():
    global _camera_thread
    global _camera_running

    if _camera_running:
        return "Camera preview is already running."

    _camera_running = True

    _camera_thread = threading.Thread(
        target=_camera_preview_worker,
        daemon=True
    )

    _camera_thread.start()

    return "Live camera preview started."


def stop_live_preview():
    global _camera_running

    if not _camera_running:
        return "Camera preview is not running."

    _camera_running = False

    return "Stopping camera preview."