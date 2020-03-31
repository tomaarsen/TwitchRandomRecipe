from TwitchWebsocket import TwitchWebsocket
import json, requests, random, logging, time, os, re

from Log import Log
Log(__file__)

from Settings import Settings

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

        # Fill previously initialised variables with data from the settings.txt file
        Settings(self)

        self.ws = TwitchWebsocket(host=self.host, 
                                  port=self.port,
                                  chan=self.chan,
                                  nick=self.nick,
                                  auth=self.auth,
                                  callback=self.message_handler,
                                  capability=[],
                                  live=True)
        self.ws.start_bot()
        
    def set_settings(self, host, port, chan, nick, auth, cooldown):
        self.host = host
        self.port = port
        self.chan = chan
        self.nick = nick
        self.auth = auth
        self.cooldown = cooldown

    def message_handler(self, m):
        try:
            if m.type == "366":
                logging.info(f"Successfully joined channel: #{m.channel}")
            
            elif m.type == "PRIVMSG":
                if m.message.startswith("!recipe"):
                    if time.time() > self.previous_time + self.cooldown:
                        # Generate a recipe
                        out = self.generate()
                        logging.info(out)
                        self.ws.send_message(out)
                        # Update the previous time for cooldown
                        self.previous_time = time.time()
                    
                    else:
                        out = f"Cooldown hit: {self.cooldown - (time.time() - self.previous_time):.2f} out of {self.cooldown}s remaining. You can't stop these whispers yet because I don't code THAT fast, jeez."
                        logging.info(out)
                        self.ws.send_whisper(m.user, out)

        except Exception as e:
            logging.exception(e)
    
    def read_corpus(self):
        # Path to the corpus directory
        corpus_dir = os.path.join(os.getcwd(), "corpus")
        # Fill the corpus such that each .txt file, eg "ingredients.txt"
        # has "ingredients" as key, and a list of nonempty strings from 
        # "ingredients.txt" as value for that key
        try:
            for filename in os.listdir(corpus_dir):
                if filename.endswith(".txt"):
                    with open(os.path.join(corpus_dir, filename)) as f:
                        self.corpus[filename.replace(".txt", "")] = [x for x in f.read().split("\n") if x]
        except FileNotFoundError:
            raise FileNotFoundError("This program relies on a \"formats.txt\" file within the \"corpus\" directory. See https://github.com/CubieDev/TwitchRandomRecipe for a default.")

        # Check whether the formats contain unknown tags, or the illegal tag {formats}
        if "formats" in self.corpus:
            for form in self.corpus["formats"]:
                tags = set(self.re_tag.findall(form)) - (self.corpus.keys() - set("formats"))
                if tags:
                    raise Exception(f"Unknown or illegal tag{'s' if len(tags) > 1 else ''} used: {', '.join('{' + tag + '}' for tag in tags)} in \"{form}\".")
        else:
            raise FileNotFoundError("This program relies on a \"formats.txt\" file within the \"corpus\" directory. See https://github.com/CubieDev/TwitchRandomRecipe for a default.")

    def generate(self):
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