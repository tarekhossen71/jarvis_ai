import webbrowser
import urllib.parse
import time
import pyautogui
import win32gui
import win32con

def open_whatsapp():
    try:
        webbrowser.open("whatsapp://")
        return "WhatsApp Desktop app opened successfully."

    except Exception as e:
        return f"Failed to open WhatsApp app: {e}"


def open_email():
    try:
        webbrowser.open("https://mail.google.com/")
        return "Email opened successfully."
    except Exception as e:
        return f"Failed to open email: {e}"


def compose_email(to="", subject="", body=""):
    try:
        params = {
            "view": "cm",
            "to": to,
            "su": subject,
            "body": body,
        }

        query = urllib.parse.urlencode(params)
        url = f"https://mail.google.com/mail/?{query}"

        webbrowser.open(url)

        return "Email compose window opened."

    except Exception as e:
        return f"Failed to compose email: {e}"

def open_whatsapp_chat(phone_number, message=""):
    try:
        phone_number = (
            phone_number
            .replace(" ", "")
            .replace("-", "")
            .replace("(", "")
            .replace(")", "")
        )

        if phone_number.startswith("01"):
            phone_number = "880" + phone_number[1:]

        phone_number = phone_number.replace("+", "")

        if not phone_number.isdigit():
            return "Please provide a valid phone number."

        if not message:
            return "Please provide a message."

        url = (
            f"whatsapp://send"
            f"?phone={phone_number}"
            f"&text={urllib.parse.quote(message)}"
        )

        webbrowser.open(url)

        time.sleep(3)

        return (
            f"WhatsApp message is ready for {phone_number}. "
            "Please confirm before sending."
        )

    except Exception as e:
        return f"Failed to open WhatsApp chat: {e}"

    
# def send_whatsapp_message():
#     try:
#         pyautogui.press("enter")
#         return "WhatsApp message sent successfully."

#     except Exception as e:
#         return f"Failed to send WhatsApp message: {e}"

def send_whatsapp_message():
    try:
        # WhatsApp window activate
        activate_whatsapp_window()

        time.sleep(1)

        # Message send
        pyautogui.press("enter")

        return "WhatsApp message sent successfully."

    except Exception as e:
        return f"Failed to send WhatsApp message: {e}"

def activate_whatsapp_window():
    whatsapp_hwnd = None

    def find_window(hwnd, extra):
        nonlocal whatsapp_hwnd

        if not win32gui.IsWindowVisible(hwnd):
            return

        title = win32gui.GetWindowText(hwnd)

        if "WhatsApp" in title:
            whatsapp_hwnd = hwnd

    win32gui.EnumWindows(find_window, None)

    if not whatsapp_hwnd:
        return False

    try:
        win32gui.ShowWindow(
            whatsapp_hwnd,
            win32con.SW_RESTORE
        )

        time.sleep(1)
        win32gui.BringWindowToTop(whatsapp_hwnd)
        time.sleep(1)
        win32gui.SetForegroundWindow(whatsapp_hwnd)
        time.sleep(1)

    except Exception:
        # Windows focus restriction holeo
        # WhatsApp already open thakte pare
        pass

    return True