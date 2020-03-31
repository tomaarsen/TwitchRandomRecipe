
import logging, json, os
logger = logging.getLogger(__name__)

class Settings:
    """ Loads data from settings.json into the bot """

    PATH = os.path.join(os.getcwd(), "settings.json")

    def __init__(self, bot):
        logger.debug("Loading settings.json file...")
        try:
            # Try to load the file using json.
            # And pass the data to the Bot class instance if this succeeds.
            with open(Settings.PATH, "r") as f:
                settings = f.read()
                data = json.loads(settings)
                bot.set_settings(data['Host'],
                                data['Port'],
                                data['Channel'],
                                data['Nickname'],
                                data['Authentication'],
                                data['Cooldown'])
                logger.debug("Settings loaded into Bot.")

        except ValueError:
            logger.error("Error in settings file.")
            raise ValueError("Error in settings file.")

        except FileNotFoundError:
            # If the file is missing, create a standardised settings.json file
            # With all parameters required.
            logger.error("Please fix your settings.json file that was just generated.")
            Settings.write_default_settings_file()
            raise ValueError("Please fix your settings.json file that was just generated.")

    @staticmethod
    def write_default_settings_file():
        # If the file is missing, create a standardised settings.json file
        # With all parameters required.
        with open(Settings.PATH, "w") as f:
            standard_dict = {
                                "Host": "irc.chat.twitch.tv",
                                "Port": 6667,
                                "Channel": "#<channel>",
                                "Nickname": "<name>",
                                "Authentication": "oauth:<auth>",
                                "Cooldown": 30,
                            }
            f.write(json.dumps(standard_dict, indent=4, separators=(",", ": ")))