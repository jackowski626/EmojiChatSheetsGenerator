# Emoji Unicode sheets generator for EmojiChat (Forge) for 1.7.10

## What is this?
This is a tool allowing you to create unicode sheets (and directly resource packs) with Twemoji emojis for Minecraft (only tested on 1.7.10, for now).

## How?
It replaces a subset of Chinese characters with emojis.

## Usage:
* Clone/Download this repo
* For now just run `python main.py` and install any dependencies if yelled at. (Probably `pillow` (it's not pillow you'll have to google the package name, there are multiple forks or something))
* If you want custom emotes, a new folder `custom_emojis` will be created in the `assets` folder. Drop them there and rerun `python main.py`.
You can download emotes from a server you're in using this tool: https://github.com/ThaTiemsz/Discord-Emoji-Downloader
* The resource pack is generated in the `production` folder. If you don't use custom emojis you can probably use it out of the box with either of these projects installed on your server: https://github.com/jackowski626/EmojiChatForge ; https://github.com/RadBuilder/EmojiChat. Otherwise you'll need to manually fill the file with emoji IDs and put it in the correct config folder of `EmojiChatForge`. The sussy baka plugin won't work with custom emojis

## Planned features:
* Adding a simple discord bot written in python that can generate the id list automatically
* Adding support for other mc versions (updating the emojichat mod tbh)

## You are welcome to contribute or send suggestions/complaints to Boys Gregified HQ