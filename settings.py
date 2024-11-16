import logging
from importlib.resources import files
from shutil import which
import json

_DEFAULT_SETTINGS = {
    "savePath": "./downloaded_content",
    "ffmpegPath": "ffmpeg",
    "colors": {
        "border": "3c3f41",
        "background": "2b2b2b",
        "defaultText": "a9b7c6",
        "titleText": "b0b0b0",
        "url": "287bde",
        "greenButton": "30593d",
        "redButton": "a02f020"
    },
    "font": "Roboto",
    "fontSizes": {
        "tiny": "8",
        "small": "10",
        "normal": "12",
        "large": "20",
        "huge": "30"
    }
}


def get_settings(reset: bool = False) -> dict:
    def load_defaults():
        defaults = _DEFAULT_SETTINGS.copy()
        with open('./settings.json', mode='w') as fp:
            json.dump(defaults, fp, indent=2)
        logging.info("Default settings loaded")
        return defaults
    
    if reset:
        settings = load_defaults()
        return settings

    try:
        with open('./settings.json', mode='r') as fp:
            settings = json.load(fp)
            logging.info("User settings loaded")
    except FileNotFoundError as e:
        logging.error(f'FileNotFoundError: {e.filename}')
        settings = None
    except json.JSONDecodeError as e:
        logging.error(f'JSONDecodeError: {e.msg}')
        settings = None

    if not settings:
        load_defaults()
    return settings


# TODO: Check for FFmpeg on user's system - issue notification if not found
# TODO: Recheck if a path is entered, or the user installs FFmpeg and requests a recheck
def check_ffmpeg(path) -> None:
    if not which(path):
        logging.warning("FFmpeg not found")
        # TODO: pop-up window
        print("FFmpeg not found on your system.\n"
              "Please install FFmpeg.\nhttps://www.ffmpeg.org\n"
              "or specify the path.")
        # TODO: return an error for display on main window
    else:
        logging.info("FFmpeg found")


if __name__ == "__main__":
    get_settings()
    check_ffmpeg("ffmpeg")
