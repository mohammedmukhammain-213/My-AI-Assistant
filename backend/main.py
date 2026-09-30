import re
import requests
import webbrowser

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from laptop.control import (
    # Laptop
    open_app,
    close_app,
    turn_on_wifi,
    turn_off_wifi,
    get_wifi_status,
    turn_on_bluetooth,
    turn_off_bluetooth,
    get_bluetooth_status,
    increase_volume,
    decrease_volume,
    mute_volume,
    unmute_volume,
    take_screenshot,
    play_pause_media,
    increase_brightness,
    decrease_brightness,
    lock_laptop,
    restart_laptop,
    get_battery_status,
    get_system_info,
    get_ram_status,
    get_processor_info,
    get_storage_status,
    get_gpu_info,
    get_uptime,
    get_internet_status,
    get_wifi_signal_strength,
    get_ip_address,
    get_mac_address,
    get_username,
    get_windows_version,
    get_windows_build,
    get_windows_architecture,
    get_screen_resolution,
    # Phone / ADB
    get_adb_devices,
    open_camera_on_phone,
    open_phone_on_phone,
    open_messages_on_phone,
    open_chrome_on_phone,
    open_music_on_phone,
    open_youtube_on_phone,
    open_youtube_shorts_on_phone,
    open_whatsapp_on_phone,
    open_maps_on_phone,
    open_instagram_on_phone,
    close_instagram_on_phone,
    open_facebook_on_phone,
    close_facebook_on_phone,
    close_phone_app,
    open_website_on_phone,
    search_google_on_phone,
    search_youtube_on_phone,
    play_youtube_search_on_phone,

    # Phone volume / media
    play_pause_phone_media,
    increase_phone_volume,
    decrease_phone_volume,
    mute_phone_volume,
    unmute_phone_volume,

    # YouTube Shorts
    play_pause_youtube_shorts_on_phone,
)


# ============================================================
# FASTAPI APP
# ============================================================

app = FastAPI(
    title="My AI Assistant",
    version="1.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# OLLAMA
# ============================================================

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2"


# ============================================================
# DATABASE
# ============================================================

from database.memory import (
    init_database,
    save_message,
    get_messages,
    save_fact,
    get_facts,
    delete_fact,
    delete_all_facts,
)


# ============================================================
# INITIALIZE DATABASE
# ============================================================

init_database()


# ============================================================
# MEMORY COMMANDS
# ============================================================

def handle_memory_commands(command):
    lower = command.lower().strip()
    
    # --------------------------------------------------------
    # SHOW MEMORY
    # --------------------------------------------------------

    if (
        "show my memory" in lower
        or "show memory" in lower
        or "what do you remember" in lower
        or "what do you know about me" in lower
    ):
        facts = get_facts()

        if not facts:
            return "I don't have any saved memories."

        lines = ["Here is what I remember about you:"]

        if isinstance(facts, dict):
            for key, value in facts.items():
                lines.append(f"- {key}: {value}")

        elif isinstance(facts, list):
            for item in facts:
                if isinstance(item, (list, tuple)) and len(item) >= 2:
                    lines.append(f"- {item[0]}: {item[1]}")

                elif isinstance(item, dict):
                    key = item.get("key", item.get("name", "memory"))
                    value = item.get("value", "")
                    lines.append(f"- {key}: {value}")

                else:
                    lines.append(f"- {item}")

        else:
            lines.append(f"- {facts}")

        return "\n".join(lines)
    # --------------------------------------------------------
    # REMEMBERED NAME
    # --------------------------------------------------------

    if (
        "what is my name" in lower
        or "what's my name" in lower
        or "who am i" in lower
    ):
        facts = dict(get_facts())
        name = facts.get("name")

        if name:
            return f"Your name is {name}."

        return "I don't know your name yet."
    if (
        "what is my favorite color" in lower
        or "what's my favorite color" in lower
    ):
        facts = dict(get_facts())
        color = facts.get("favorite color")

        if color:
            return f"Your favorite color is {color}."

        return "I don't know your favorite color yet."
    if (
        "what is my favorite food" in lower
        or "what's my favorite food" in lower
    ):
        facts = dict(get_facts())
        food = facts.get("favorite food")

        if food:
            return f"Your favorite food is {food}."

        return "I don't know your favorite food yet."
    if (
        "what is my favorite movie" in lower
        or "what's my favorite movie" in lower
    ):
        facts = dict(get_facts())
        movie = facts.get("favorite movie")

        if movie:
            return f"Your favorite movie is {movie}."

        return "I don't know your favorite movie yet."
    if (
        "what is my favorite sport" in lower
        or "what's my favorite sport" in lower
    ):
        facts = dict(get_facts())
        sport = facts.get("favorite sport")

        if sport:
            return f"Your favorite sport is {sport}."

        return "I don't know your favorite sport yet."
    if (
        "what is my favorite animal" in lower
        or "what's my favorite animal" in lower
    ):
        facts = dict(get_facts())
        animal = facts.get("favorite animal")

        if animal:
            return f"Your favorite animal is {animal}."

        return "I don't know your favorite animal yet."
    if (
        "what laptop do i have" in lower
        or "what is my laptop" in lower
        or "what's my laptop" in lower
    ):
        facts = dict(get_facts())
        laptop = facts.get("laptop")

        if laptop:
            return f"Your laptop is {laptop}."

        return "I don't know your laptop yet."
    if (
        "what phone do i have" in lower
        or "what is my phone" in lower
        or "what's my phone" in lower
    ):
        facts = dict(get_facts())
        phone = facts.get("phone")

        if phone:
            return f"Your phone is {phone}."

        return "I don't know your phone yet."
    if (
        "where do i live" in lower
        or "what is my location" in lower
        or "what's my location" in lower
        or "where am i from" in lower
    ):
        facts = dict(get_facts())
        location = facts.get("location")

        if location:
            return f"You live in {location}."

        return "I don't know your location yet."
    if (
        "what do i study" in lower
        or "what am i studying" in lower
        or "what is my study" in lower
        or "what's my study" in lower
    ):
        facts = dict(get_facts())
        study = facts.get("study")

        if study:
            return f"You study {study}."

        return "I don't know what you study yet."

    if (
        "what is my hobby" in lower
        or "what is my hobby" in lower
    ):
        facts = dict(get_facts())
        hobby = facts.get("hobby")

        if hobby:
            return f"Your hobby is {hobby}."

        return "I don't know your hobby yet."
    if (
        "what do i like" in lower
        or "what are my likes" in lower
        or "what things do i like" in lower
    ):
        facts = dict(get_facts())
        likes = facts.get("likes")

        if likes:
            return f"You like {likes}."

        return "I don't know what you like yet."
    # --------------------------------------------------------
    # FORGET ONE MEMORY
    # --------------------------------------------------------

    if "forget my favorite food" in lower:
        delete_fact("favorite food")
        return "I forgot your favorite food."

    if "forget my favorite movie" in lower:
        delete_fact("favorite movie")
        return "I forgot your favorite movie."

    if "forget my favorite sport" in lower:
        delete_fact("favorite sport")
        return "I forgot your favorite sport."

    if "forget my favorite animal" in lower:
        delete_fact("favorite animal")
        return "I forgot your favorite animal."

    if "forget my favorite color" in lower:
        delete_fact("favorite color")
        return "I forgot your favorite color."

    if "forget my laptop" in lower:
        delete_fact("laptop")
        return "I forgot your laptop."

    if "forget my phone" in lower:
        delete_fact("phone")
        return "I forgot your phone."

    if "forget my location" in lower:
        delete_fact("location")
        return "I forgot your location."

    if "forget what i study" in lower:
        delete_fact("study")
        return "I forgot what you study."

    if "forget my hobby" in lower:
        delete_fact("hobby")
        return "I forgot your hobby."

    if "forget what i like" in lower:
        delete_fact("likes")
        return "I forgot what you like."

    if "forget my name" in lower:
        delete_fact("name")
        return "I forgot your name."
    # --------------------------------------------------------
    # FORGET EVERYTHING
    # --------------------------------------------------------

    if (
        "forget everything" in lower
        or "forget all my memories" in lower
        or "delete all memories" in lower
        or "clear all memory" in lower
        or "clear my memory" in lower
    ):
        delete_all_facts()
        return "All saved memories have been deleted."

    # --------------------------------------------------------
    # NAME
    # --------------------------------------------------------

    match = re.search(
        r"(?:my name is|call me|i am)\s+(.+)",
        command,
        re.IGNORECASE
    )

    if match:
        name = match.group(1).strip()
        name = re.sub(
            r"\s+remember that$",
            "",
            name,
            flags=re.IGNORECASE
        ).strip()

        save_fact("name", name)
        return f"I'll remember that your name is {name}."

    # --------------------------------------------------------
    # FAVORITE COLOR
    # --------------------------------------------------------

    match = re.search(
        r"my favorite color is\s+(.+)",
        command,
        re.IGNORECASE
    )

    if match:
        value = match.group(1).strip()
        save_fact("favorite color", value)
        return f"I'll remember that your favorite color is {value}."

    # --------------------------------------------------------
    # FAVORITE SPORT
    # --------------------------------------------------------

    match = re.search(
        r"my favorite sport is\s+(.+)",
        command,
        re.IGNORECASE
    )

    if match:
        value = match.group(1).strip()
        save_fact("favorite sport", value)
        return f"I'll remember that your favorite sport is {value}."

    # --------------------------------------------------------
    # FAVORITE ANIMAL
    # --------------------------------------------------------

    match = re.search(
        r"my favorite animal is\s+(.+)",
        command,
        re.IGNORECASE
    )

    if match:
        value = match.group(1).strip()
        save_fact("favorite animal", value)
        return f"I'll remember that your favorite animal is {value}."

    # --------------------------------------------------------
    # FAVORITE FOOD
    # --------------------------------------------------------

    match = re.search(
        r"my favorite food is\s+(.+)",
        command,
        re.IGNORECASE
    )

    if match:
        value = match.group(1).strip()
        save_fact("favorite food", value)
        return f"I'll remember that your favorite food is {value}."

    # --------------------------------------------------------
    # FAVORITE MOVIE
    # --------------------------------------------------------

    match = re.search(
        r"my favorite movie is\s+(.+)",
        command,
        re.IGNORECASE
    )

    if match:
        value = match.group(1).strip()
        save_fact("favorite movie", value)
        return f"I'll remember that your favorite movie is {value}."

    # --------------------------------------------------------
    # LAPTOP
    # --------------------------------------------------------

    match = re.search(
        r"my laptop is\s+(.+)",
        command,
        re.IGNORECASE
    )

    if match:
        value = match.group(1).strip()
        save_fact("laptop", value)
        return f"I'll remember that your laptop is {value}."
    

    # --------------------------------------------------------
    # PHONE
    # --------------------------------------------------------

    match = re.search(
        r"my phone is\s+(.+)",
        command,
        re.IGNORECASE
    )

    if match:
        value = match.group(1).strip()
        save_fact("phone", value)
        return f"I'll remember that your phone is {value}."

    # --------------------------------------------------------
    # LOCATION
    # --------------------------------------------------------

    match = re.search(
        r"(?:i live in|my location is|i am from)\s+(.+)",
        command,
        re.IGNORECASE
    )

    if match:
        value = match.group(1).strip()
        save_fact("location", value)
        return f"I'll remember that you are from {value}."

    # --------------------------------------------------------
    # STUDY
    # --------------------------------------------------------

    match = re.search(
        r"(?:i study|i am studying)\s+(.+)",
        command,
        re.IGNORECASE
    )

    if match:
        value = match.group(1).strip()
        save_fact("study", value)
        return f"I'll remember that you study {value}."

    # --------------------------------------------------------
    # HOBBY
    # --------------------------------------------------------

    match = re.search(
        r"my hobby is\s+(.+)",
        command,
        re.IGNORECASE
    )

    if match:
        value = match.group(1).strip()
        save_fact("hobby", value)
        return f"I'll remember that your hobby is {value}."

    # --------------------------------------------------------
    # LIKES
    # --------------------------------------------------------

    match = re.search(
        r"i like\s+(.+)",
        command,
        re.IGNORECASE
    )

    if match:
        value = match.group(1).strip()
        save_fact("likes", value)
        return f"I'll remember that you like {value}."

    return None


# ============================================================
# PHONE COMMANDS
# ============================================================

def handle_phone_commands(command):
    lower = command.lower().strip()

    # ========================================================
    # PHONE ADB STATUS
    # ========================================================

    if (
        "phone status" in lower
        or "check phone connection" in lower
        or "is my phone connected" in lower
        or "check adb" in lower
    ):
        return get_adb_devices()

    # ========================================================
    # PHONE UNMUTE
    # ========================================================

    if (
        "unmute my phone" in lower
        or "unmute phone" in lower
        or "turn on phone sound" in lower
    ):
        return unmute_phone_volume()

    # ========================================================
    # PHONE MUTE
    # ========================================================

    if (
        "mute my phone" in lower
        or "mute phone" in lower
        or "turn off phone sound" in lower
    ):
        return mute_phone_volume()

    # ========================================================
    # PHONE VOLUME UP
    # ========================================================

    if (
    "increase phone volume" in lower
    or "increase my phone volume" in lower
    or "increase volume on my phone" in lower
        or "phone volume up" in lower
        or "turn up phone volume" in lower
        or "make my phone louder" in lower
    ):
        return increase_phone_volume()

    # ========================================================
    # PHONE VOLUME DOWN
    # ========================================================
    if (
    "decrease phone volume" in lower
        or "decrease my phone volume" in lower
        or "decrease volume on my phone" in lower
        or "phone volume down" in lower
        or "turn down phone volume" in lower
        or "make my phone quieter" in lower
    ):
        return decrease_phone_volume()

    # ========================================================
    # OPEN YOUTUBE SHORTS
    # ========================================================

    if (
        "open youtube shorts on my phone" in lower
        or "open youtube shorts on phone" in lower
        or "open shorts on my phone" in lower
        or "open shorts on phone" in lower
    ):
        return open_youtube_shorts_on_phone()

    # ========================================================
    # CLOSE YOUTUBE SHORTS
    # ========================================================

    if (
        "close youtube shorts on my phone" in lower
        or "close youtube shorts on phone" in lower
        or "close shorts on my phone" in lower
        or "close shorts on phone" in lower
    ):
        return close_phone_app("com.google.android.youtube")

    # ========================================================
    # PLAY / PAUSE YOUTUBE SHORTS
    # ========================================================

    if (
        "pause youtube shorts on my phone" in lower
        or "play youtube shorts on my phone" in lower
        or "pause youtube shorts on phone" in lower
        or "play youtube shorts on phone" in lower
        or "pause shorts on my phone" in lower
        or "play shorts on my phone" in lower
    ):
        return play_pause_youtube_shorts_on_phone()

    # ========================================================
    # PHONE MEDIA PLAY / PAUSE
    # ========================================================

    if (
        "pause media on my phone" in lower
        or "play media on my phone" in lower
        or "pause music on my phone" in lower
        or "play music on my phone" in lower
        or "pause phone media" in lower
        or "play phone media" in lower
    ):
        return play_pause_phone_media()
    # ========================================================
    # YOUTUBE PLAY / PAUSE ON PHONE
    # ========================================================

    if (
        "pause youtube on my phone" in lower
        or "pause youtube on phone" in lower
    ):
        return play_pause_phone_media()

    if (
        "play youtube on my phone" in lower
        or "play youtube on phone" in lower
    ):
        open_youtube_on_phone()
        return play_pause_phone_media()
    # ========================================================
    # OPEN PHONE CAMERA
    # ========================================================

    if (
        "open camera on my phone" in lower
        or "open camera on phone" in lower
        or "open phone camera" in lower
    ):
        return open_camera_on_phone()

    # ========================================================
    # OPEN PHONE DIALER
    # ========================================================

    if (
        "open dialer on my phone" in lower
        or "open phone dialer" in lower
        or "open phone on my phone" in lower
    ):
        return open_phone_on_phone()

    # ========================================================
    # OPEN PHONE MESSAGES
    # ========================================================

    if (
        "open messages on my phone" in lower
        or "open messages on phone" in lower
        or "open phone messages" in lower
    ):
        return open_messages_on_phone()

    # ========================================================
    # OPEN CHROME ON PHONE
    # ========================================================

    if (
        "open chrome on my phone" in lower
        or "open chrome on phone" in lower
    ):
        return open_chrome_on_phone()

    # ========================================================
    # OPEN MUSIC ON PHONE
    # ========================================================

    if (
        "open music on my phone" in lower
        or "open music on phone" in lower
        or "open youtube music on my phone" in lower
    ):
        return open_music_on_phone()
    # ========================================================
    # CLOSE YOUTUBE MUSIC ON PHONE
    # ========================================================

    if (
        "close youtube music on my phone" in lower
        or "close youtube music on phone" in lower
        or "close music on my phone" in lower
        or "close music on phone" in lower
    ):
        return close_phone_app("com.google.android.apps.youtube.music")

    # ========================================================
    # OPEN YOUTUBE ON PHONE
    # ========================================================

    if (
        "open youtube on my phone" in lower
        or "open youtube on phone" in lower
    ):
        return open_youtube_on_phone()

    # ========================================================
    # OPEN WHATSAPP ON PHONE
    # ========================================================

    if (
        "open whatsapp on my phone" in lower
        or "open whatsapp on phone" in lower
    ):
        return open_whatsapp_on_phone()

    # ========================================================
    # OPEN GOOGLE MAPS ON PHONE
    # ========================================================

    if (
        "open maps on my phone" in lower
        or "open maps on phone" in lower
        or "open google maps on my phone" in lower
    ):
        return open_maps_on_phone()
    # ========================================================
    # CLOSE GOOGLE MAPS ON PHONE
    # ========================================================

    if (
        "close maps on my phone" in lower
         or "close maps on phone" in lower
        or "close google maps on my phone" in lower
        or "close google maps on phone" in lower
    ):
        return close_phone_app("com.google.android.apps.maps")

    # ========================================================
    # OPEN INSTAGRAM ON PHONE
    # ========================================================

    if (
        "open instagram on my phone" in lower
        or "open instagram on phone" in lower
    ):
        return open_instagram_on_phone()

    # ========================================================
    # CLOSE INSTAGRAM ON PHONE
    # ========================================================

    if (
        "close instagram on my phone" in lower
        or "close instagram on phone" in lower
    ):
        return close_instagram_on_phone()

    # ========================================================
    # OPEN FACEBOOK ON PHONE
    # ========================================================

    if (
        "open facebook on my phone" in lower
        or "open facebook on phone" in lower
    ):
        return open_facebook_on_phone()

    # ========================================================
    # CLOSE FACEBOOK ON PHONE
    # ========================================================

    if (
        "close facebook on my phone" in lower
        or "close facebook on phone" in lower
    ):
        return close_facebook_on_phone()

    # ========================================================
    # CLOSE WHATSAPP ON PHONE
    # ========================================================

    if (
        "close whatsapp on my phone" in lower
        or "close whatsapp on phone" in lower
    ):
        return close_phone_app("com.whatsapp")

    # ========================================================
    # CLOSE CHROME ON PHONE
    # ========================================================

    if (
        "close chrome on my phone" in lower
        or "close chrome on phone" in lower
    ):
        return close_phone_app("com.android.chrome")

    # ========================================================
    # CLOSE YOUTUBE ON PHONE
    # ========================================================

    if (
        "close youtube on my phone" in lower
        or "close youtube on phone" in lower
    ):
        return close_phone_app("com.google.android.youtube")
    # ========================================================
    # OPEN GOOGLE ON PHONE
    # ========================================================

    if (
        "open google on my phone" in lower
        or "open google on phone" in lower
    ):
        return open_website_on_phone("https://www.google.com")

    
    # ========================================================
    # OPEN WEBSITE ON PHONE
    # ========================================================

    website_match = re.search(
        r"(?:open|go to|visit)\s+(.+?)\s+on my phone$",
        command,
        re.IGNORECASE
    )

    if website_match:
        website = website_match.group(1).strip()

        if "." in website:
            return open_website_on_phone(website)

    # ========================================================
    # GOOGLE SEARCH ON PHONE
    # ========================================================

    google_match = re.search(
        r"(?:search google for|google search for|search for)\s+(.+?)\s+on my phone$",
        command,
        re.IGNORECASE
    )

    if google_match:
        query = google_match.group(1).strip()
        return search_google_on_phone(query)

    # ========================================================
    # YOUTUBE SEARCH ON PHONE
    # ========================================================

    youtube_match = re.search(
        r"(?:search youtube for|youtube search for)\s+(.+?)\s+on my phone$",
        command,
        re.IGNORECASE
    )

    if youtube_match:
        query = youtube_match.group(1).strip()
        return search_youtube_on_phone(query)

    # ========================================================
    # PLAY YOUTUBE VIDEO ON PHONE
    # ========================================================

    play_match = re.search(
        r"(?:play|watch)\s+(.+?)\s+(?:on youtube|on my phone)$",
        command,
        re.IGNORECASE
    )

    if play_match:
        query = play_match.group(1).strip()

        if query:
            return play_youtube_search_on_phone(query)

    return None


# ============================================================
# LAPTOP COMMANDS
# ============================================================

def handle_laptop_commands(command):
    lower = command.lower().strip()

    # ========================================================
    # WIFI
    # ========================================================
    if (
        "turn on wifi" in lower
        or "turn on wi-fi" in lower
        or "enable wifi" in lower
        or "enable wi-fi" in lower
        or "turn wifi on" in lower
        or "turn wi-fi on" in lower
    ):
        return turn_on_wifi()

    if (
        "turn off wifi" in lower
        or "turn off wi-fi" in lower
        or "turn wifi off" in lower
        or "turn wi-fi off" in lower
        or "disable wifi" in lower
        or "disable wi-fi" in lower
    ):
        return turn_off_wifi()

    if (
        "wifi status" in lower
        or "wi-fi status" in lower
        or "is wifi on" in lower
        or "is wi-fi on" in lower
    ):
        return get_wifi_status()

    # ========================================================
    # BLUETOOTH
    # ========================================================

    if (
        "turn on bluetooth" in lower
        or "enable bluetooth" in lower
    ):
        return turn_on_bluetooth()

    if (
        "turn off bluetooth" in lower
        or "disable bluetooth" in lower
    ):
        return turn_off_bluetooth()

    if (
        "bluetooth status" in lower
        or "is bluetooth on" in lower
    ):
        return get_bluetooth_status()

    # ========================================================
    # SCREENSHOT
    # ========================================================

    if (
        "take screenshot" in lower
        or "take a screenshot" in lower
        or lower == "screenshot"
    ):
        return take_screenshot()

    # ========================================================
    # MEDIA
    # ========================================================

    if (
        "play media" in lower
        or "pause media" in lower
        or "play music" in lower
        or "pause music" in lower
        or "play or pause media" in lower
    ):
        return play_pause_media()

    # ========================================================
    # LAPTOP VOLUME
    # ========================================================
    if (
        "increase volume" in lower
        or "increase laptop volume" in lower
        or "volume up" in lower
        or "laptop volume up" in lower
        or "turn up volume" in lower
        or "make it louder" in lower
    ):
        return increase_volume()

    if (
        "decrease volume" in lower
        or "volume down" in lower
        or "turn down volume" in lower
        or "make it quieter" in lower
    ):
        return decrease_volume()

        # LAPTOP MUTE / UNMUTE

    if (
        "unmute laptop" in lower
        or "unmute computer" in lower
        or "unmute volume" in lower
    ):
        return unmute_volume()

    if (
        "mute laptop" in lower
        or "mute computer" in lower
        or "mute volume" in lower
    ):
        return mute_volume()

    # ========================================================
    # BRIGHTNESS
    # ========================================================
    if (
        "increase brightness" in lower
        or "increase laptop brightness" in lower
        or "brightness up" in lower
        or "laptop brightness up" in lower
        or "make screen brighter" in lower
    ):
        return increase_brightness()
    if (
        "decrease brightness" in lower
        or "decrease laptop brightness" in lower
        or "brightness down" in lower
        or "laptop brightness down" in lower
        or "make screen darker" in lower
    ):
        return decrease_brightness()

    # ========================================================
    # LOCK
    # ========================================================

    if (
        "lock laptop" in lower
        or "lock computer" in lower
        or "lock my laptop" in lower
    ):
        return lock_laptop()

    # ========================================================
    # RESTART
    # ========================================================

    if (
        "restart laptop" in lower
        or "restart computer" in lower
        or "restart my laptop" in lower
    ):
        return restart_laptop()

    # ========================================================
    # LAPTOP APPS
    # ========================================================

    laptop_apps = {
        "calculator": "calculator",
        "notepad": "notepad",
        "paint": "paint",
        "chrome": "chrome",
        "explorer": "explorer",
    }

    for name, app_name in laptop_apps.items():

        if f"open {name}" in lower:
            return open_app(app_name)

        if f"close {name}" in lower:
            return close_app(app_name)

    return None


# ============================================================
# OLLAMA AI
# ============================================================

def ask_ollama(command):
    facts = get_facts()
    messages = get_messages()

    memory_text = ""

    if facts:

        if isinstance(facts, dict):
            memory_text = "\n".join(
                f"{key}: {value}"
                for key, value in facts.items()
            )

        elif isinstance(facts, list):
            memory_lines = []

            for item in facts:

                if isinstance(item, (list, tuple)) and len(item) >= 2:
                    memory_lines.append(
                        f"{item[0]}: {item[1]}"
                    )

                elif isinstance(item, dict):
                    key = item.get(
                        "key",
                        item.get("name", "memory")
                    )
                    value = item.get("value", "")
                    memory_lines.append(
                        f"{key}: {value}"
                    )

                else:
                    memory_lines.append(str(item))

            memory_text = "\n".join(memory_lines)

        else:
            memory_text = str(facts)

    recent_messages = ""

    if messages:
        for message in messages[-10:]:

            if isinstance(message, (list, tuple)) and len(message) >= 2:
                recent_messages += (
                    f"{message[0]}: {message[1]}\n"
                )

            elif isinstance(message, dict):
                role = message.get("role", "user")
                content = message.get(
                    "content",
                    message.get("message", "")
                )

                recent_messages += (
                    f"{role}: {content}\n"
                )

            else:
                recent_messages += f"{message}\n"

    prompt = f"""
You are My AI Assistant.

Give short, clear and useful answers.

Saved memory:
{memory_text}

Recent conversation:
{recent_messages}

User:
{command}

Assistant:
"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False,
                "keep_alive": -1,
                "options": {
                    "num_predict": 50
                }
            },
            timeout=120
        )

        response.raise_for_status()

        data = response.json()

        answer = data.get("response", "").strip()

        if not answer:
            return "I could not generate a response."

        return answer

    except requests.exceptions.ConnectionError:
        return (
            "Ollama is not running. "
            "Please start Ollama and try again."
        )

    except requests.exceptions.Timeout:
        return "Ollama took too long to respond."

    except Exception as error:
        return f"AI error: {error}"


# ============================================================
# MAIN COMMAND HANDLER
# ============================================================

def process_command(command):
    command = command.strip()
    lower = command.lower()

    if not command:
        return "Please enter a command."

    if (
        "battery" in lower
        or "battery status" in lower
        or "how much battery" in lower
    ):
        return get_battery_status()
    if (
        "how is my laptop" in lower
        or "laptop status" in lower
        or "system status" in lower
    ):
        battery = get_battery_status()
        wifi = get_wifi_status()
        bluetooth = get_bluetooth_status()
        ram = get_ram_status()
        storage = get_storage_status()

        return f"{battery} {wifi} {bluetooth} {ram} {storage}"
        
    if "what time is it" in lower or "current time" in lower:
        from datetime import datetime
        return datetime.now().strftime("The current time is %I:%M %p.")

    if (
        "what is today's date" in lower
        or "what is todays date" in lower
        or "current date" in lower
        or "today's date" in lower
    ):
        from datetime import datetime
        return datetime.now().strftime("Today's date is %d %B %Y.")
    if (
        "tell me about my laptop" in lower
        or "system information" in lower
        or "system info" in lower
    ):
        return get_system_info()
    if (
        "how much ram" in lower
        or "ram status" in lower
        or "ram" in lower
    ):
        return get_ram_status()
    if (
        "what processor" in lower
        or "which processor" in lower
        or "cpu information" in lower
    ):
        return get_processor_info()
    if (
        "how much storage" in lower
        or "storage status" in lower
        or "disk space" in lower
    ):
        return get_storage_status()
    if (
        "what graphics card" in lower
        or "which graphics card" in lower
        or "gpu information" in lower
        or "gpu" in lower
    ):
        return get_gpu_info()
    if (
        "how long has my laptop been running" in lower
        or "laptop uptime" in lower
        or "last boot time" in lower
    ):
        return get_uptime()
    if (
        "is my internet working" in lower
        or "internet status" in lower
        or "check my internet" in lower
    ):
        return get_internet_status()
    if (
        "wifi signal" in lower
        or "wi-fi signal" in lower
        or "wifi strength" in lower
        or "wi-fi strength" in lower
    ):
        return get_wifi_signal_strength()
    if (
        "what is my ip address" in lower
        or "what is my ip" in lower
        or "my ip address" in lower
    ):
        return get_ip_address()
    if (
        "what is my mac address" in lower
        or "what is my mac" in lower
        or "my mac address" in lower
    ):
        return get_mac_address()
    if (
        "what is my username" in lower
        or "what is my windows username" in lower
        or "my username" in lower
    ):
        return get_username()
    if (
        "what version of windows" in lower
        or "windows version" in lower
        or "which windows" in lower
    ):
        return get_windows_version()
    if (
        "what is my windows build" in lower
        or "windows build number" in lower
        or "windows build" in lower
    ):
        return get_windows_build()
    if (
        "windows architecture" in lower
        or "32 bit or 64 bit" in lower
        or "32-bit or 64-bit" in lower
        or "is my laptop 64 bit" in lower
    ):
        return get_windows_architecture()
    if (
        "screen resolution" in lower
        or "display resolution" in lower
        or "what is my screen size" in lower
    ):
        return get_screen_resolution()
    # --------------------------------------------------------
    # Save user message
    # --------------------------------------------------------

    try:
        save_message("user", command)
    except Exception:
        pass

    # --------------------------------------------------------
    # Memory commands
    # --------------------------------------------------------

    result = handle_memory_commands(command)

    if result is not None:
        try:
            save_message("assistant", result)
        except Exception:
            pass

        return result

    # --------------------------------------------------------
    # Phone commands
    # --------------------------------------------------------

    result = handle_phone_commands(command)

    if result is not None:
        try:
            save_message("assistant", result)
        except Exception:
            pass

        return result

    # --------------------------------------------------------
    # Laptop commands
    # --------------------------------------------------------

    result = handle_laptop_commands(command)

    if result is not None:
        try:
            save_message("assistant", result)
        except Exception:
            pass

        return result

    # --------------------------------------------------------
    # Ollama AI
    # --------------------------------------------------------

    result = ask_ollama(command)

    try:
        save_message("assistant", result)
    except Exception:
        pass

    return result


# ============================================================
# API: ROOT
# ============================================================

@app.get("/")
def root():
    return {
        "status": "online",
        "assistant": "My AI Assistant",
        "ai": "Ollama - Llama 3.2"
    }


# ============================================================
# API: ASK
# ============================================================

@app.post("/ask")
def ask(data: dict):
    command = data.get("command", "")

    if not command:
        return {
            "response": "Please enter a command."
        }

    response = process_command(command)

    return {
        "response": response
    }


# ============================================================
# API: HISTORY
# ============================================================

@app.get("/history")
def history():
    try:
        messages = get_messages()

        return {
            "messages": messages
        }

    except Exception as error:
        return {
            "messages": [],
            "error": str(error)
        }


# ============================================================
# STARTUP
# ============================================================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )