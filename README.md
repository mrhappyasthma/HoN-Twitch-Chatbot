# HoN-Twitch-Chatbot

As a HoN streamer, I wanted to bring everything used by my stream into one central location with lots of customization.
With that in mind, this bot is not exclusively HoN related. Some of the larger goals of the bot are: custom Twitch commands
(using the HoN stats API), Twitch chat -> HoN in-game chat, music controls (Spotify), etc.

## Requirements

You will need to download, install, and update the [Heroes of Newerth](https://www.heroesofnewerth.com/download/) windows client.

If you want to support the Spotify music library, then also install [Spotify](https://www.spotify.com/us/download/windows/).

You will also need to install the following tools: 
- [git](https://git-scm.com/download/win)
- [Python v2.7](https://www.python.org/downloads/windows/)

## Install

*Note: This bot is only designed to work on Windows.*

This section is likely to be complicated as I am still figuring out all my dependencies and constantly making changes...
Eventually I will try to automate these into a script.

1. Clone the code onto your machine using `git`, with the `--recursive` flag.

    ```
    git clone https://github.com/mrhappyasthma/HoN-Twitch-Chatbot.git --recursive
    ```
2.  Navigate to where your `python` version is installed and go to the `\Scripts` sub-directory. For example:

    ```
    cd C:\Python27\Scripts
    ```
3. Run the following commands:

    ```
    pip install requests
    pip install mock
    pip install pypiwin32
    ```
