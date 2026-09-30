
import os
import re
import subprocess
import time
import urllib.parse
import requests
import pythoncom
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from winrt.windows.devices.radios import Radio, RadioKind, RadioState


# ============================================================
# ADB CONFIGURATION
# ============================================================

ADB_PATH = (
    r"C:\Users\pandu\Downloads"
    r"\platform-tools-latest-windows"
    r"\platform-tools"
    r"\adb.exe"
)
PHONE_SERVER_URL = "http://192.168.29.193:8080"

# ============================================================
# ADB DEVICE
# ============================================================
def get_adb_devices():
    result = subprocess.run(
        [ADB_PATH, "devices"],
        capture_output=True,
        text=True
    )

    lines = result.stdout.strip().splitlines()

    devices = []

    for line in lines[1:]:
        line = line.strip()

        if not line:
            continue

        parts = line.split()

        if len(parts) >= 2 and parts[1] == "device":
            devices.append(parts[0])

    if devices:
        return (
            "Android phone connected. "
            f"Device count: {len(devices)}"
        )

    return "No Android phone is connected."
def get_wireless_device():
    """
    Find a connected Android phone through Wireless ADB.
    """

    try:
        # Make sure the ADB server is running
        subprocess.run(
            [ADB_PATH, "start-server"],
            capture_output=True,
            text=True,
            timeout=10
        )

        result = subprocess.run(
            [ADB_PATH, "devices"],
            capture_output=True,
            text=True,
            timeout=10
        )

        lines = result.stdout.splitlines()
        devices = []

        for line in lines:
            line = line.strip()

            if not line:
                continue

            if line.startswith("List of devices"):
                continue

            parts = line.split()

            if len(parts) >= 2 and parts[1] == "device":
                devices.append(parts[0])

        # Prefer direct IP:PORT connection
        for device in devices:
            if ":" in device and "_adb-" not in device:
                return device

        # Otherwise use Wireless ADB mDNS connection
        for device in devices:
            if "_adb-tls-connect._tcp" in device:
                return device

        return None

    except Exception:
        return None


# ============================================================
# ADB COMMAND
# ============================================================

def adb_command(arguments):
    """
    Run an ADB command using the currently connected
    wireless Android phone.
    """

    device = get_wireless_device()

    if device is None:
        return (
            "No wireless Android phone is connected. "
            "Please turn on Wireless debugging."
        )

    try:
        command = [ADB_PATH, "-s", device] + arguments

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=30
        )

        output = result.stdout.strip()
        error = result.stderr.strip()

        if output:
            return output

        if error:
            return error

        return "ADB command completed."

    except subprocess.TimeoutExpired:
        return "ADB command timed out."

    except Exception as error:
        return f"ADB error: {error}"


# ============================================================
# PHONE APPS
# ============================================================

PHONE_APPS = {
    "whatsapp": "com.whatsapp",
    "instagram": "com.instagram.android",
    "facebook": "com.facebook.katana",
    "chrome": "com.android.chrome",
    "youtube": "com.google.android.youtube",
    "maps": "com.google.android.apps.maps",
    "music": "com.google.android.apps.youtube.music",
}


# ============================================================
# OPEN PHONE APP
# ============================================================

def open_phone_app(package_name):
    result = adb_command([
        "shell",
        "cmd",
        "package",
        "resolve-activity",
        "--brief",
        package_name
    ])

    if "No wireless Android phone" in result:
        return result

    lines = result.strip().splitlines()

    if not lines:
        return "Could not find the phone app."

    activity = lines[-1].strip()

    if "/" not in activity:
        return "Could not find the phone app activity."

    result = adb_command([
        "shell",
        "am",
        "start",
        "-n",
        activity
    ])

    if "No wireless Android phone" in result:
        return result

    return "Phone app opened."
# ============================================================
# CLOSE PHONE APP
# ============================================================

def close_phone_app(package_name):
    result = adb_command([
        "shell",
        "am",
        "force-stop",
        package_name
    ])

    if "No wireless Android phone" in result:
        return result

    if "error" in result.lower():
        return result

    return "Phone app closed."


# ============================================================
# OPEN WHATSAPP
# ============================================================

def open_whatsapp_on_phone():
    return open_phone_app(PHONE_APPS["whatsapp"])


# ============================================================
# OPEN INSTAGRAM
# ============================================================

def open_instagram_on_phone():
    try:
        result = adb_command([
            "shell",
            "am",
            "start",
            "-n",
            "com.instagram.android/.activity.MainTabActivity"
        ])

        if result:
            return "Instagram opened on your phone."

        return "Could not open Instagram on your phone."

    except Exception as e:
        return f"Could not open Instagram on your phone: {e}"

# ============================================================
# CLOSE INSTAGRAM
# ============================================================

def close_instagram_on_phone():
    return close_phone_app(PHONE_APPS["instagram"])


# ============================================================
# OPEN FACEBOOK
# ============================================================

def open_facebook_on_phone():
    return open_phone_app(PHONE_APPS["facebook"])


# ============================================================
# CLOSE FACEBOOK
# ============================================================

def close_facebook_on_phone():
    return close_phone_app(PHONE_APPS["facebook"])


# ============================================================
# OPEN CHROME
# ============================================================

def open_chrome_on_phone():
    return open_phone_app(PHONE_APPS["chrome"])


# ============================================================
# OPEN YOUTUBE
# ============================================================

def open_youtube_on_phone():
    return open_phone_app(PHONE_APPS["youtube"])


# ============================================================
# OPEN GOOGLE MAPS
# ============================================================

def open_maps_on_phone():
    return open_phone_app(PHONE_APPS["maps"])


# ============================================================
# OPEN MUSIC
# ============================================================

def open_music_on_phone():
    return open_phone_app(PHONE_APPS["music"])


# ============================================================
# OPEN PHONE / DIALER
# ============================================================

def open_phone_on_phone():
    result = adb_command([
        "shell",
        "am",
        "start",
        "-a",
        "android.intent.action.DIAL"
    ])

    if "No wireless Android phone" in result:
        return result

    return "Phone dialer opened."


# ============================================================
# OPEN MESSAGES
# ============================================================

def open_messages_on_phone():
    result = adb_command([
        "shell",
        "am",
        "start",
        "-a",
        "android.intent.action.MAIN",
        "-n",
        "com.google.android.apps.messaging/.ui.ConversationListActivity"
    ])

    if "No wireless Android phone" in result:
        return result

    return "Messages opened on your phone."


# ============================================================
# OPEN CAMERA
# ============================================================

def open_camera_on_phone():
    result = adb_command([
        "shell",
        "am",
        "start",
        "-a",
        "android.media.action.IMAGE_CAPTURE"
    ])

    if "No wireless Android phone" in result:
        return result

    return "Camera opened on your phone."


# ============================================================
# YOUTUBE SHORTS
# ============================================================

def open_youtube_shorts_on_phone():
    """
    Open YouTube Shorts on the Android phone.
    """

    url = "https://www.youtube.com/shorts"

    result = adb_command([
        "shell",
        "am",
        "start",
        "-a",
        "android.intent.action.VIEW",
        "-d",
        url
    ])

    if "No wireless Android phone" in result:
        return result

    return "YouTube Shorts opened on your phone."


# ============================================================
# CLOSE YOUTUBE SHORTS
# ============================================================

def close_youtube_shorts_on_phone():
    """
    YouTube Shorts runs inside the YouTube application.

    Therefore closing Shorts means force-stopping the
    YouTube Android package.
    """

    return close_phone_app(
        "com.google.android.youtube"
    )


# ============================================================
# PHONE SCREEN SIZE
# ============================================================

def get_phone_screen_size():
    result = adb_command([
        "shell",
        "wm",
        "size"
    ])

    if "No wireless Android phone" in result:
        return None

    match = re.search(
        r"(\d+)x(\d+)",
        result
    )

    if not match:
        return None

    width = int(match.group(1))
    height = int(match.group(2))

    return width, height


# ============================================================
# PLAY / PAUSE YOUTUBE SHORTS
# ============================================================

def play_pause_youtube_shorts_on_phone():
    try:
        response = requests.get(
            PHONE_SERVER_URL + "/tap",
            timeout=5
        )

        if response.status_code == 200:
            return "YouTube Shorts play/pause toggled."

        return "Phone did not accept the tap command."

    except requests.exceptions.RequestException:
        return "Could not connect to the AI Assistant Phone app."
    """
    Toggle YouTube Shorts play/pause by tapping the
    center of the phone screen.
    """

    size = get_phone_screen_size()

    if size is None:
        return "Could not detect phone screen size."

    width, height = size

    result = adb_command([
        "shell",
        "input",
        "tap",
        str(width // 2),
        str(height // 2)
    ])

    if "No wireless Android phone" in result:
        return result

    return "YouTube Shorts play/pause toggled."


# ============================================================
# PHONE VOLUME
# ============================================================

def increase_phone_volume():
    result = adb_command([
        "shell",
        "input",
        "keyevent",
        "24"
    ])

    if "No wireless Android phone" in result:
        return result

    return "Phone volume increased."


def decrease_phone_volume():
    result = adb_command([
        "shell",
        "input",
        "keyevent",
        "25"
    ])

    if "No wireless Android phone" in result:
        return result

    return "Phone volume decreased."


def mute_phone_volume():
    result = adb_command([
        "shell",
        "input",
        "keyevent",
        "164"
    ])

    if "No wireless Android phone" in result:
        return result

    return "Phone mute command sent."


def unmute_phone_volume():
    result = adb_command([
        "shell",
        "input",
        "keyevent",
        "164"
    ])

    if "No wireless Android phone" in result:
        return result

    return "Phone unmute command sent."


# ============================================================
# PHONE MEDIA
# ============================================================

def play_pause_phone_media():
    result = adb_command([
        "shell",
        "input",
        "keyevent",
        "85"
    ])

    if "No wireless Android phone" in result:
        return result

    return "Phone media play/pause command sent."


# ============================================================
# OPEN WEBSITE ON PHONE
# ============================================================

def open_website_on_phone(website):
    website = website.strip()

    if not website:
        return "Please provide a website."

    if not website.startswith("http://") and not website.startswith("https://"):
        website = "https://" + website

    result = adb_command([
        "shell",
        "am",
        "start",
        "-a",
        "android.intent.action.VIEW",
        "-d",
        website
    ])

    if "No wireless Android phone" in result:
        return result

    return f"Opened {website} on your phone."


# ============================================================
# GOOGLE SEARCH ON PHONE
# ============================================================

def search_google_on_phone(query):
    query = query.strip()

    if not query:
        return "Please provide something to search."

    encoded = urllib.parse.quote_plus(query)

    url = f"https://www.google.com/search?q={encoded}"

    result = adb_command([
        "shell",
        "am",
        "start",
        "-a",
        "android.intent.action.VIEW",
        "-d",
        url
    ])

    if "No wireless Android phone" in result:
        return result

    return f"Searching Google for {query} on your phone."


# ============================================================
# YOUTUBE SEARCH ON PHONE
# ============================================================

def search_youtube_on_phone(query):
    query = query.strip()

    if not query:
        return "Please provide something to search."

    encoded = urllib.parse.quote_plus(query)

    url = (
        "https://www.youtube.com/results"
        f"?search_query={encoded}"
    )

    result = adb_command([
        "shell",
        "am",
        "start",
        "-a",
        "android.intent.action.VIEW",
        "-d",
        url
    ])

    if "No wireless Android phone" in result:
        return result

    return f"Searching YouTube for {query} on your phone."


# ============================================================
# YOUTUBE PLAYBACK
# ============================================================

def play_youtube_search_on_phone(query):
    """
    Search YouTube and open the first suitable video.
    """

    query = query.strip()

    if not query:
        return "Please provide a YouTube video or song name."

    try:
        import yt_dlp
    except ImportError:
        return "yt-dlp is not installed."

    try:
        search_query = f"ytsearch1:{query}"

        options = {
            "quiet": True,
            "skip_download": True,
            "extract_flat": True,
        }

        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(
                search_query,
                download=False
            )

        entries = info.get("entries", [])

        if not entries:
            return f"No YouTube video found for {query}."

        video = entries[0]

        video_id = video.get("id")

        if not video_id:
            return "Could not find the YouTube video."

        video_url = (
            f"https://www.youtube.com/watch?v={video_id}"
        )

        result = adb_command([
            "shell",
            "am",
            "start",
            "-a",
            "android.intent.action.VIEW",
            "-d",
            video_url
        ])

        if "No wireless Android phone" in result:
            return result

        return (
            f"Playing {query} on YouTube "
            f"on your phone."
        )

    except Exception as error:
        return f"YouTube error: {error}"


# ============================================================
# LAPTOP APPLICATIONS
# ============================================================

APP_COMMANDS = {
    "calculator": "calc.exe",
    "notepad": "notepad.exe",
    "paint": "mspaint.exe",
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "explorer": "explorer.exe",
}


# ============================================================
# OPEN LAPTOP APP
# ============================================================

def open_app(app_name):
    app_name = app_name.lower().strip()

    command = APP_COMMANDS.get(app_name)

    if command is None:
        return f"I don't know how to open {app_name}."

    try:
        subprocess.Popen(
            command,
            shell=True
        )

        return f"Opened {app_name}."

    except Exception as error:
        return f"Could not open {app_name}: {error}"


# ============================================================
# CLOSE LAPTOP APP
# ============================================================

def close_app(app_name):
    app_name = app_name.lower().strip()

    process_names = {
        "calculator": "CalculatorApp.exe",
        "notepad": "notepad.exe",
        "paint": "mspaint.exe",
        "chrome": "chrome.exe",
        "explorer": "explorer.exe",
    }

    process_name = process_names.get(app_name)

    if process_name is None:
        return f"I don't know how to close {app_name}."

    try:
        subprocess.run(
            [
                "taskkill",
                "/F",
                "/IM",
                process_name
            ],
            capture_output=True,
            text=True
        )

        return f"Closed {app_name}."

    except Exception as error:
        return f"Could not close {app_name}: {error}"


# ============================================================
# LAPTOP VOLUME
# ============================================================

def get_volume_interface():
    pythoncom.CoInitialize()

    devices = AudioUtilities.GetSpeakers()

    return devices.EndpointVolume

def increase_volume():
    try:
        volume = get_volume_interface()

        current = volume.GetMasterVolumeLevelScalar()

        new_volume = min(
            1.0,
            current + 0.10
        )

        volume.SetMasterVolumeLevelScalar(
            new_volume,
            None
        )

        return "Laptop volume increased."

    except Exception as error:
        return f"Volume error: {error}"


def decrease_volume():
    try:
        volume = get_volume_interface()

        current = volume.GetMasterVolumeLevelScalar()

        new_volume = max(
            0.0,
            current - 0.10
        )

        volume.SetMasterVolumeLevelScalar(
            new_volume,
            None
        )

        return "Laptop volume decreased."

    except Exception as error:
        return f"Volume error: {error}"


def mute_volume():
    try:
        volume = get_volume_interface()

        volume.SetMute(
            1,
            None
        )

        return "Laptop volume muted."

    except Exception as error:
        return f"Volume error: {error}"


def unmute_volume():
    try:
        volume = get_volume_interface()

        volume.SetMute(
            0,
            None
        )

        return "Laptop volume unmuted."

    except Exception as error:
        return f"Volume error: {error}"


# ============================================================
# LAPTOP MEDIA
# ============================================================

def play_pause_media():
    try:
        import ctypes

        VK_MEDIA_PLAY_PAUSE = 0xB3

        ctypes.windll.user32.keybd_event(
            VK_MEDIA_PLAY_PAUSE,
            0,
            0,
            0
        )

        ctypes.windll.user32.keybd_event(
            VK_MEDIA_PLAY_PAUSE,
            0,
            2,
            0
        )

        return "Laptop media play/pause command sent."

    except Exception as error:
        return f"Media error: {error}"


# ============================================================
# BRIGHTNESS
# ============================================================

def increase_brightness():
    try:
        current = int(
            subprocess.check_output(
                [
                    "powershell",
                    "-Command",
                    "(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightness).CurrentBrightness"
                ],
                text=True
            ).strip()
        )

        new_brightness = min(100, current + 10)

        subprocess.run(
            [
                "powershell",
                "-Command",
                f"(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,{new_brightness})"
            ],
            capture_output=True,
            text=True
        )

        return f"Laptop brightness increased to {new_brightness}%."

    except Exception as error:
        return f"Brightness error: {error}"
def decrease_brightness():
    try:
        current = int(
            subprocess.check_output(
                [
                    "powershell",
                    "-Command",
                    "(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightness).CurrentBrightness"
                ],
                text=True
            ).strip()
        )

        new_brightness = max(0, current - 10)

        subprocess.run(
            [
                "powershell",
                "-Command",
                f"$m=Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods; $m.WmiSetBrightness(1,{new_brightness})"
            ],
            capture_output=True,
            text=True
        )

        time.sleep(1)

        actual = int(
            subprocess.check_output(
                [
                    "powershell",
                    "-Command",
                    "(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightness).CurrentBrightness"
                ],
                text=True
            ).strip()
        )

        if actual == new_brightness:
            return f"Laptop brightness decreased to {actual}%."

        return f"Brightness command sent, but actual brightness is {actual}%."

    except Exception as error:
        return f"Brightness error: {error}"
#============================================================
# SCREENSHOT
# ============================================================

def take_screenshot():
    try:
        pictures = os.path.join(
            os.path.expanduser("~"),
            "Pictures",
            "AI Assistant"
        )

        os.makedirs(
            pictures,
            exist_ok=True
        )

        filename = time.strftime(
            "screenshot_%Y%m%d_%H%M%S.png"
        )

        path = os.path.join(
            pictures,
            filename
        )

        powershell_command = (
            "Add-Type -AssemblyName System.Windows.Forms; "
            "Add-Type -AssemblyName System.Drawing; "
            "$screen = "
            "[System.Windows.Forms.Screen]::PrimaryScreen; "
            "$bitmap = New-Object "
            "System.Drawing.Bitmap "
            "$screen.Bounds.Width, "
            "$screen.Bounds.Height; "
            "$graphics = "
            "[System.Drawing.Graphics]::FromImage($bitmap); "
            "$graphics.CopyFromScreen("
            "$screen.Bounds.Location, "
            "[System.Drawing.Point]::Empty, "
            "$screen.Bounds.Size); "
            f"$bitmap.Save('{path}'); "
            "$graphics.Dispose(); "
            "$bitmap.Dispose();"
        )

        result = subprocess.run(
            [
                "powershell",
                "-Command",
                powershell_command
            ],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            return f"Screenshot saved to {path}."

        return "Could not take screenshot."

    except Exception as error:
        return f"Screenshot error: {error}"


# ============================================================
# LAPTOP POWER
# ============================================================

def lock_laptop():
    try:
        subprocess.run(
            [
                "rundll32.exe",
                "user32.dll,LockWorkStation"
            ]
        )

        return "Laptop locked."

    except Exception as error:
        return f"Could not lock laptop: {error}"


def restart_laptop():
    try:
        subprocess.run(
            [
                "shutdown",
                "/r",
                "/t",
                "0"
            ]
        )

        return "Laptop restarting."

    except Exception as error:
        return f"Could not restart laptop: {error}"



# ============================================================
# WIFI
# ============================================================

def get_wifi_radio():
    try:
        import threading

        result = {}

        def worker():
            try:
                radios = Radio.get_radios_async().get()

                for radio in radios:
                    if radio.kind == RadioKind.WI_FI:
                        result["radio"] = radio
                        return

                result["radio"] = None

            except Exception as error:
                result["error"] = error

        thread = threading.Thread(target=worker)
        thread.start()
        thread.join()

        if "error" in result:
            raise result["error"]

        return result.get("radio")

    except Exception:
        return None
def get_wifi_status():
    try:
        radio = get_wifi_radio()

        if radio is None:
            return "Wi-Fi radio not found."

        if radio.state == RadioState.ON:
            return "Wi-Fi is on."

        return "Wi-Fi is off."

    except Exception as error:
        return f"Wi-Fi status error: {error}"


def turn_off_wifi():
    try:
        import threading

        result = {}

        def worker():
            try:
                radios = Radio.get_radios_async().get()

                wifi = next(
                    r for r in radios
                    if r.kind == RadioKind.WI_FI
                )

                wifi.set_state_async(RadioState.OFF).get()

                result["success"] = True

            except Exception as error:
                result["error"] = error

        thread = threading.Thread(target=worker)
        thread.start()
        thread.join()

        if "error" in result:
            return f"Wi-Fi error: {result['error']}"

        time.sleep(1)

        return get_wifi_status()

    except Exception as error:
        return f"Wi-Fi error: {error}"


def turn_on_wifi():
    try:
        import threading

        result = {}

        def worker():
            try:
                radios = Radio.get_radios_async().get()

                wifi = next(
                    r for r in radios
                    if r.kind == RadioKind.WI_FI
                )

                wifi.set_state_async(RadioState.ON).get()

                result["success"] = True

            except Exception as error:
                result["error"] = error

        thread = threading.Thread(target=worker)
        thread.start()
        thread.join()

        if "error" in result:
            return f"Wi-Fi error: {result['error']}"

        time.sleep(1)

        return get_wifi_status()

    except Exception as error:
        return f"Wi-Fi error: {error}"# ============================================================
# BLUETOOTH
# ============================================================

def turn_off_bluetooth():
    try:
        import concurrent.futures

        def get_radios():
            return Radio.get_radios_async().get()

        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            radios = executor.submit(get_radios).result()

            bluetooth = next(
                r for r in radios
                if r.kind == RadioKind.BLUETOOTH
            )

            executor.submit(
                lambda: bluetooth.set_state_async(
                    RadioState.OFF
                ).get()
            ).result()

        return "Bluetooth turned off."

    except Exception as error:
        return f"Bluetooth error: {error}"
def turn_on_bluetooth():
    try:
        import concurrent.futures

        def get_radios():
            return Radio.get_radios_async().get()

        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            radios = executor.submit(get_radios).result()

            bluetooth = next(
                r for r in radios
                if r.kind == RadioKind.BLUETOOTH
            )

            executor.submit(
                lambda: bluetooth.set_state_async(
                    RadioState.ON
                ).get()
            ).result()

        return "Bluetooth turned on."

    except Exception as error:
        return f"Bluetooth error: {error}"
def get_bluetooth_status():
    try:
        import concurrent.futures

        def get_radios():
            return Radio.get_radios_async().get()

        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            radios = executor.submit(get_radios).result()

            bluetooth = next(
                r for r in radios
                if r.kind == RadioKind.BLUETOOTH
            )

            if bluetooth.state == RadioState.ON:
                return "Bluetooth is on."

            return "Bluetooth is off."

    except Exception as error:
        return f"Bluetooth error: {error}"
# ============================================================
# BATTERY
# ============================================================

def get_battery_status():
    try:
        result = subprocess.check_output(
            [
                "powershell",
                "-Command",
                "(Get-CimInstance Win32_Battery).EstimatedChargeRemaining"
            ],
            text=True
        ).strip()

        if not result:
            return "Battery information is not available."

        battery = int(result)

        return f"Laptop battery is at {battery}%."

    except Exception as error:
        return f"Battery error: {error}"
# ============================================================
# SYSTEM INFORMATION
# ============================================================

def get_system_info():
    try:
        import platform
        import subprocess

        computer = platform.node()

        windows = subprocess.check_output(
            [
                "powershell",
                "-Command",
                "(Get-CimInstance Win32_OperatingSystem).Caption"
            ],
            text=True
        ).strip()

        processor = platform.processor()

        return (
            f"Computer name: {computer}. "
            f"Windows: {windows}. "
            f"Processor: {processor}."
        )

    except Exception as error:
        return f"System information error: {error}"
# ============================================================
# RAM
# ============================================================

def get_ram_status():
    try:
        import subprocess

        result = subprocess.check_output(
            [
                "powershell",
                "-Command",
                "[math]::Round((Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory / 1GB, 2)"
            ],
            text=True
        ).strip()

        return f"Laptop RAM is {result} GB."

    except Exception as error:
        return f"RAM error: {error}"
# ============================================================
# PROCESSOR
# ============================================================

def get_processor_info():
    try:
        import platform

        processor = platform.processor()

        return f"Processor: {processor}."

    except Exception as error:
        return f"Processor error: {error}"
# ============================================================
# STORAGE
# ============================================================

def get_storage_status():
    try:
        import shutil

        total, used, free = shutil.disk_usage("C:\\")

        total_gb = round(total / (1024 ** 3), 2)
        used_gb = round(used / (1024 ** 3), 2)
        free_gb = round(free / (1024 ** 3), 2)

        return (
            f"Laptop storage is {total_gb} GB total, "
            f"{used_gb} GB used, "
            f"and {free_gb} GB free."
        )

    except Exception as error:
        return f"Storage error: {error}"
# ============================================================
# GPU
# ============================================================

def get_gpu_info():
    try:
        import subprocess

        result = subprocess.check_output(
            [
                "powershell",
                "-Command",
                "(Get-CimInstance Win32_VideoController).Name"
            ],
            text=True
        ).strip()

        if not result:
            return "GPU information is not available."

        gpus = [line.strip() for line in result.splitlines() if line.strip()]

        return "Graphics card: " + ", ".join(gpus) + "."

    except Exception as error:
        return f"GPU error: {error}"
# ============================================================
# UPTIME
# ============================================================

def get_uptime():
    try:
        import subprocess

        result = subprocess.check_output(
            [
                "powershell",
                "-Command",
                "$boot=(Get-CimInstance Win32_OperatingSystem).LastBootUpTime; "
                "$uptime=(Get-Date)-$boot; "
                "[math]::Floor($uptime.TotalHours).ToString() + ' hours ' + "
                "$uptime.Minutes.ToString() + ' minutes'"
            ],
            text=True
        ).strip()

        return f"Laptop has been running for {result}."

    except Exception as error:
        return f"Uptime error: {error}"
# ============================================================
# INTERNET STATUS
# ============================================================

def get_internet_status():
    try:
        import requests

        response = requests.get(
            "https://www.google.com",
            timeout=5
        )

        if response.status_code == 200:
            return "Internet connection is working."

        return "Internet connection is available but the test failed."

    except Exception:
        return "Internet connection is not working."
# ============================================================
# WI-FI SIGNAL STRENGTH
# ============================================================

def get_wifi_signal_strength():
    try:
        import subprocess
        import re

        result = subprocess.check_output(
            [
                "powershell",
                "-Command",
                "(Get-NetAdapter -Physical | "
                "Where-Object {$_.Status -eq 'Up' -and "
                "$_.Name -match 'Wi-Fi|Wireless'}).Name"
            ],
            text=True,
            encoding="utf-8",
            errors="ignore"
        ).strip()

        if not result:
            return "Wi-Fi signal strength is not available."

        adapter = result.splitlines()[0].strip()

        signal = subprocess.check_output(
            [
                "powershell",
                "-Command",
                f"(Get-NetAdapterStatistics -Name '{adapter}').ReceivedBytes"
            ],
            text=True,
            encoding="utf-8",
            errors="ignore"
        ).strip()

        if not signal:
            return "Wi-Fi signal strength is not available."

        return "Wi-Fi adapter is connected."

    except Exception as error:
        return f"Wi-Fi signal error: {error}"
# ============================================================
# IP ADDRESS
# ============================================================

def get_ip_address():
    try:
        import socket

        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)

        return f"Laptop IP address is {ip_address}."

    except Exception as error:
        return f"IP address error: {error}"
# ============================================================
# MAC ADDRESS
# ============================================================

def get_mac_address():
    try:
        import subprocess
        import re

        result = subprocess.check_output(
            [
                "powershell",
                "-Command",
                "(Get-NetAdapter -Physical | "
                "Where-Object {$_.Status -eq 'Up'} | "
                "Select-Object -First 1 -ExpandProperty MacAddress)"
            ],
            text=True,
            encoding="utf-8",
            errors="ignore"
        ).strip()

        if not result:
            return "MAC address is not available."

        mac = re.sub(r"[^0-9A-Fa-f:-]", "", result)

        return f"Laptop MAC address is {mac}."

    except Exception as error:
        return f"MAC address error: {error}"
# ============================================================
# WINDOWS USERNAME
# ============================================================

def get_username():
    try:
        import getpass

        username = getpass.getuser()

        return f"Windows username is {username}."

    except Exception as error:
        return f"Username error: {error}"
# ============================================================
# WINDOWS VERSION
# ============================================================

def get_windows_version():
    try:
        import subprocess

        result = subprocess.check_output(
            [
                "powershell",
                "-Command",
                "(Get-CimInstance Win32_OperatingSystem).Caption"
            ],
            text=True
        ).strip()

        if not result:
            return "Windows version is not available."

        return f"Windows version is {result}."

    except Exception as error:
        return f"Windows version error: {error}"
# ============================================================
# WINDOWS BUILD
# ============================================================

def get_windows_build():
    try:
        import subprocess

        result = subprocess.check_output(
            [
                "powershell",
                "-Command",
                "(Get-CimInstance Win32_OperatingSystem).BuildNumber"
            ],
            text=True
        ).strip()

        if not result:
            return "Windows build number is not available."

        return f"Windows build number is {result}."

    except Exception as error:
        return f"Windows build error: {error}"
# ============================================================
# WINDOWS ARCHITECTURE
# ============================================================

def get_windows_architecture():
    try:
        import platform

        architecture = platform.architecture()[0]

        return f"Windows architecture is {architecture}."

    except Exception as error:
        return f"Architecture error: {error}"
# ============================================================
# SCREEN RESOLUTION
# ============================================================

def get_screen_resolution():
    try:
        import subprocess

        result = subprocess.check_output(
            [
                "powershell",
                "-Command",
                "$screen = Get-CimInstance Win32_VideoController | "
                "Where-Object {$_.CurrentHorizontalResolution -ne $null} | "
                "Select-Object -First 1; "
                "$screen.CurrentHorizontalResolution.ToString() + 'x' + "
                "$screen.CurrentVerticalResolution.ToString()"
            ],
            text=True
        ).strip()

        if not result:
            return "Screen resolution is not available."

        return f"Screen resolution is {result}."

    except Exception as error:
        return f"Screen resolution error: {error}"