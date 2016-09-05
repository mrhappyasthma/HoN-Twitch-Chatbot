"""Run this script with |python run.py|."""

import string
import threading

from chatbot import ChatBot
from apis.spotify import spotify_api

def main():
  bot = ChatBot()
  bot.connect()

  # Spawn a new thread to handle bot chat commands.
  command_thread = threading.Thread(target=bot.handle_commands)
  command_thread.start()

  # Spawn a new thread to output the text to file for OBS.
  obs_file_thread = threading.Thread(target=spotify_api.write_to_OBS_file)
  obs_file_thread.start()



if __name__ == '__main__':
  main()
