class CameraIntents:

    def __init__(self, tools):
        self.tools = tools

    def normalize(self, text):
        return text.lower().strip()

    def open_camera(self, command):
        text = self.normalize(command)

        commands = [
            "open camera",
            "start camera",
            "launch camera",
            "camera open",
            "camera start",
            "turn on camera",
        ]

        if text in commands:
            return self.tools.open_camera()

        return None

    def close_camera(self, command):
        text = self.normalize(command)

        commands = [
            "close camera",
            "stop camera",
            "camera close",
            "camera stop",
            "turn off camera",
        ]

        if text in commands:
            return self.tools.close_camera()

        return None

    def execute(self, command):
        result = self.open_camera(command)
        if result is not None:
            return result

        result = self.close_camera(command)
        if result is not None:
            return result

        result = self.take_photo(command)
        if result is not None:
            return result

        result = self.camera_status(command)
        if result is not None:
            return result

        result = self.live_preview(command)
        if result is not None:
            return result

        result = self.stop_preview(command)
        if result is not None:
            return result

        return None

    def take_photo(self, command):
        text = self.normalize(command)

        commands = [
            "take photo",
            "take a photo",
            "capture photo",
            "capture a photo",
            "take picture",
            "take a picture",
            "capture picture",
            "capture a picture",
            "snap photo",
            "snap a photo",
        ]

        if text in commands:
            return self.tools.take_photo()

        return None

    def camera_status(self, command):
        text = self.normalize(command)

        commands = [
            "camera status",
            "check camera",
            "check camera status",
            "is camera working",
            "is the camera working",
            "is camera available",
            "is the camera available",
            "camera available",
        ]

        if text in commands:
            return self.tools.camera_status()

        return None

    def live_preview(self, command):
        text = self.normalize(command)

        commands = [
            "live camera",
            "camera preview",
            "live camera preview",
            "start camera preview",
            "show camera",
            "show live camera",
            "open camera preview",
            "start live camera",
        ]

        if text in commands:
            return self.tools.start_live_preview()

        return None


    def stop_preview(self, command):
        text = self.normalize(command)

        commands = [
            "stop camera preview",
            "stop live camera",
            "close camera preview",
            "close live camera",
            "stop camera",
            "stop preview",
        ]

        if text in commands:
            return self.tools.stop_live_preview()

        return None