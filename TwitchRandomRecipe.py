from TwitchWebsocket import TwitchWebsocket
import json, requests, random, logging, time

from Log import Log
Log(__file__)

from Settings import Settings

class TwitchDinner:
    def __init__(self):
        self.host = None
        self.port = None
        self.chan = None
        self.nick = None
        self.auth = None

        self.formats = [
            "Try some {} with {}, topped with {} and {}.", 
            "How about {}, together with {}, and seasoned with some {}.",
            "Mix some {} with {}, served ontop of {}.",
            "Boil {} together with {}, with some fried {}.",
            "Fry some {} with {} at high temperatures, served as a base for {}.",
            "Deep-fry {} as a side for {}.",
            "Blend {} with {} to make a delicious smoothie.",
            "The {} with {} is just to die for!",
            "{} and {}, the secret to a succesful {}.",
            "Dice some {}, fry it in a pan together with {}, garnish with some {} and serve.",
            "Take this {}, throw it in a pot, add some {}, a {}. Baby, you got a stew going.",
            "You should know, {} with {} is heaven on Earth.",
            "Whatever you do, never, EVER mix {} with {}",

            "Were you really going to just eat some raw {}? Come on beb, have some respect.",
        ]
        self.previous_time = 0
        
        with open("ingredients.txt") as f:
            self.ingredients = f.read().split("\n")

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
                        # Randomly pick a format
                        form = random.choice(self.formats)
                        # Get the amount of ingredients in the format
                        n = form.count("{}")
                        # Fetch ingredients from the list by https://github.com/schollz/ingredients
                        ingredients = random.choices(self.ingredients, k=n)
                        # Apply ingredients to format
                        output = form.format(*ingredients)
                        logging.info(output)
                        self.ws.send_message(output)
                        # Update the previous time for cooldown
                        self.previous_time = time.time()
                    
                    else:
                        out = f"Cooldown hit: {self.cooldown - (time.time() - self.previous_time):.2f} out of {self.cooldown}s remaining. You can't stop these whispers yet because I don't code THAT fast, jeez."
                        logging.info(out)
                        self.ws.send_whisper(m.user, out)

        except Exception as e:
            logging.exception(e)
    
if __name__ == "__main__":
    TwitchDinner()