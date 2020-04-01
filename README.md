# TwitchRandomRecipe
 Allow chat to generate some horrible recipes

---

# Explanation
When the bot has started, it will start listening to chat messages in the channel listed in the `settings.json` file. Whenever such a chat message starts with `!recipe`, the bot will randomly pick a message format like `Boil {amount} {measurement} of {ingredient} together with {amount} {measurement} of {vegetable}, with some fried {vegetable}` and replace all sections wrapped in curly braces with some randomly picked phrase of that type.

A possible output is:
<pre>
<b>Boil 5/8 jars of dr pepper together with 13 fluid ounces of watermelon, with some fried radish.</b>
</pre>
Doesn't that sound just delicious?

---

## How it works
Alongside the `TwitchRandomRecipe.py` that controls it all, is a `corpus` directory, containing all text to be generated. The file `formats.txt` must always exist within this `corpus` directory. This file contains all text formats to be filled in.<br>
Some examples are:
<pre>
Try {amount} {measurement} of {ingredient} with {amount} {measurement} of {vegetable}, topped with {herb} and {herb}.
How about {amount} {measurement} of {ingredient}, together with {amount} {measurement} of {ingredient}, and seasoned with some {herb}.
Mix some {vegetable} with {amount} {measurement} of {ingredient}, served ontop of {ingredient}.
</pre>
As you can see, these formats contain words within curly brackets, also known as *tags*. When generating a recipe using one of these formats, a tag `{amount}` will be replaced with a random item in `corpus/amount.txt`.<br>
Similarly, the tag `{measurement}` will be replaced with a random item from `corpus/measurement.txt`, and so on.

This means that if you wanted to add or change some formats to include fruits, you can make the file `fruit.txt` in the `corpus` directory, and add the `{fruit}` tag to your formats.<br>
This file `fruit.txt` might look like:
<pre>
apple
apricot
avocado
banana
bell pepper
bilberry
lackberry
blackcurrant
blood orange
blueberry
...
</pre>
The majority of the existing files within `corpus.txt` are from [schollz](https://github.com/schollz)'s [ingredients](https://github.com/schollz/ingredients/tree/master/corpus) repository. I thank him for providing an open sourced list of ingredients, vegetables, fruits and more.

Because of the flexibility of this system, it is even possible to make formats with tags and corresponding text files that are completely unrelated to recipes. You could make formats about games:<br>
<pre>Did you see that {streamer} beat {proplayer} in {game} last night?</pre>
or art inspiration:<br>
<pre>You should {artform} a {jobtitle} riding a {creature}.</pre>
or even sport predictions:<br>
<pre>{nhlteam} will beat {nhlteam} {score} to {score}.</pre>

---
### Cooldown

To prevent spam, a cooldown between `!recipe` uses is implemented. To further reduce spam, whenever a user hits such a cooldown, they are whispered the time until the cooldown expires, rather than being told so in chat. Users can whisper the bot `!nopm` to disable these cooldown whispers, and `!yespm` to (re)enable the cooldown private messages.

The length of this cooldown in seconds can be modified in the `settings.json` file. For more information, see the [Settings](#settings) section below.

---

# Settings
This bot is controlled by a settings.txt file, which looks like:
```json
{
    "Host": "irc.chat.twitch.tv",
    "Port": 6667,
    "Channel": "#<channel>",
    "Nickname": "<name>",
    "Authentication": "oauth:<auth>",
    "Cooldown": 20,
}
```

| **Parameter**        | **Meaning** | **Example** |
| -------------------- | ----------- | ----------- |
| Host                 | The URL that will be used. Do not change.                         | "irc.chat.twitch.tv" |
| Port                 | The Port that will be used. Do not change.                        | 6667 |
| Channel              | The Channel that will be connected to.                            | "#CubieDev" |
| Nickname             | The Username of the bot account.                                  | "CubieB0T" |
| Authentication       | The OAuth token for the bot account.                              | "oauth:pivogip8ybletucqdz4pkhag6itbax" |
| Cooldown | A cooldown in seconds between generations. | 20 |

*Note that the example OAuth token is not an actual token, but merely a generated string to give an indication what it might look like.*

I got my real OAuth token from https://twitchapps.com/tmi/.

---

# Requirements
* [Python 3.6+](https://www.python.org/downloads/)
* [Module requirements](requirements.txt)<br>
Install these modules using `pip install -r requirements.txt` in the commandline.

Among these modules is my own [TwitchWebsocket](https://github.com/CubieDev/TwitchWebsocket) wrapper, which makes making a Twitch chat bot a lot easier.
This repository can be seen as an implementation using this wrapper.

---

# Other Twitch Bots

* [TwitchMarkovChain](https://github.com/CubieDev/TwitchMarkovChain)
* [TwitchGoogleTranslate](https://github.com/CubieDev/TwitchGoogleTranslate)
* [TwitchRhymeBot](https://github.com/CubieDev/TwitchRhymeBot)
* [TwitchCubieBotGUI](https://github.com/CubieDev/TwitchCubieBotGUI)
* [TwitchCubieBot](https://github.com/CubieDev/TwitchCubieBot)
* [TwitchUrbanDictionary](https://github.com/CubieDev/TwitchUrbanDictionary)
* [TwitchWeather](https://github.com/CubieDev/TwitchWeather)
* [TwitchDeathCounter](https://github.com/CubieDev/TwitchDeathCounter)
* [TwitchSuggestDinner](https://github.com/CubieDev/TwitchSuggestDinner)
* [TwitchPickUser](https://github.com/CubieDev/TwitchPickUser)
* [TwitchSaveMessages](https://github.com/CubieDev/TwitchSaveMessages)
* [TwitchMMLevelPickerGUI](https://github.com/CubieDev/TwitchMMLevelPickerGUI) (Mario Maker 2 specific bot)
* [TwitchMMLevelQueueGUI](https://github.com/CubieDev/TwitchMMLevelQueueGUI) (Mario Maker 2 specific bot)
* [TwitchPackCounter](https://github.com/CubieDev/TwitchPackCounter) (Streamer specific bot)
* [TwitchDialCheck](https://github.com/CubieDev/TwitchDialCheck) (Streamer specific bot)
* [TwitchSendMessage](https://github.com/CubieDev/TwitchSendMessage) (Not designed for non-programmers)
