from Log import Log
Log(__file__)

from TwitchWebsocket import TwitchWebsocket
import random, logging, time, os, re
from typing import Union

from Settings import Settings
from Database import Database

logger = logging.getLogger(__name__)

class TwitchRandomRecipe:
    def __init__(self):
        self.host = None
        self.port = None
        self.chan = None
        self.nick = None
        self.auth = None

        # Regular expression for detecting a tag
        self.re_tag = re.compile(r"(?:{(.*?)})")
        # Get default, empty corpus using all .txt files in the corpus directory
        # Each file is expected to have the format "{tag}.txt" where "{tag}" is what
        # will be used in the formats. Eg "ingredient.txt" has "ingredient" as tag.
        # And hence a random ingredient replaces a "... {ingredient} ..." in formats.txt
        self.corpus = {}
        # Fill the corpus
        self.read_corpus()
        # Used for cooldowns
        self.previous_time = 0

        # Database for storing who should not be whispered cooldowns
        self.db = Database()

        # Fill previously initialised variables with data from the settings.txt file
        Settings(self)

        self.ws = TwitchWebsocket(host=self.host, 
                                  port=self.port,
                                  chan=self.chan,
                                  nick=self.nick,
                                  auth=self.auth,
                                  callback=self.message_handler,
                                  capability=["commands"],
                                  live=True)
        self.ws.start_bot()
        
    def set_settings(self, host: str, port: int, chan: str, nick: str, auth: str, cooldown: Union[int, float]):
        self.host = host
        self.port = int(port)
        self.chan = chan
        self.nick = nick
        self.auth = auth
        self.cooldown = float(cooldown)

    def message_handler(self, m: "TwitchWebsocket.Message"):
        try:
            if m.type == "366":
                logger.info(f"Successfully joined channel: #{m.channel}")
            
            if m.type == "PRIVMSG":
                if m.message.startswith("!recipe"):
                    if time.time() > self.previous_time + self.cooldown:
                        # Generate a recipe
                        out = self.generate()
                        logger.info(out)
                        self.ws.send_message(out)
                        # Update the previous time for cooldown
                        self.previous_time = time.time()
                    
                    else:
                        out = f"Cooldown hit: {self.cooldown - (time.time() - self.previous_time):.2f} out of {self.cooldown}s remaining. !nopm to stop these cooldown pm's."
                        logger.info(out)
                        if not self.db.check_whisper_ignore(m.user):
                            self.ws.send_whisper(m.user, out)
            
            elif m.type == "WHISPER":
                # Allow people to whisper the bot to disable or enable whispers.
                if m.message == "!nopm":
                    logger.debug(f"Adding {m.user} to Do Not Whisper.")
                    self.db.add_whisper_ignore(m.user)
                    self.ws.send_whisper(m.user, "You will no longer be sent whispers. Type !yespm to reenable.")

                elif m.message == "!yespm":
                    logger.debug(f"Removing {m.user} from Do Not Whisper.")
                    self.db.remove_whisper_ignore(m.user)
                    self.ws.send_whisper(m.user, "You will again be sent whispers. Type !nopm to disable again.")

        except Exception as e:
            logger.exception(e)
    
    def read_corpus(self) -> None:
        # Path to the corpus directory
        corpus_dir = os.path.join(os.getcwd(), "corpus")
        # Fill the corpus such that each .txt file, eg "ingredients.txt"
        # has "ingredients" as key, and a list of nonempty strings from 
        # "ingredients.txt" as value for that key
        try:
            for filename in os.listdir(corpus_dir):
                if filename.endswith(".txt"):
                    with open(os.path.join(corpus_dir, filename)) as f:
                        self.corpus[filename.replace(".txt", "")] = [x for x in f.read().split("\n") if x and not x.startswith(("#", "//"))]
        except FileNotFoundError:
            raise FileNotFoundError("This program relies on a \"formats.txt\" file within the \"corpus\" directory. See https://github.com/CubieDev/TwitchRandomRecipe for a default.")

        # Check whether the formats file exists
        if "formats" in self.corpus:
            # Check whether the formats file is not empty
            if not self.corpus["formats"]:
                raise Exception("Please fill \"formats.txt\" with some formats. See https://github.com/CubieDev/TwitchRandomRecipe for more information.")

            # Check whether the formats contain unknown tags, or the illegal tag {formats}
            for form in self.corpus["formats"]:
                unknown_tags = set(self.re_tag.findall(form)) - (self.corpus.keys() - set("formats"))
                if unknown_tags:
                    raise Exception(f"Unknown or illegal tag{'s' if len(unknown_tags) > 1 else ''} used: {', '.join('{' + tag + '}' for tag in unknown_tags)} in \"{form}\".")
        else:
            raise FileNotFoundError("This program relies on a \"formats.txt\" file within the \"corpus\" directory. See https://github.com/CubieDev/TwitchRandomRecipe for a default.")

    def generate(self) -> str:
        # Randomly pick a format
        form = random.choice(self.corpus["formats"])
        
        # Look for a tag
        match = self.re_tag.search(form)
        while match:
            # Replace the tag with a corresponding corpus element
            form = form.replace(match.group(), random.choice(self.corpus[match.group(1)]), 1)
            # And look for a new tag
            match = self.re_tag.search(form)
        
        return form

if __name__ == "__main__":
    TwitchRandomRecipe()