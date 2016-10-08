"""Run this script with |python run.py|."""

import imp
import os
import string
import sys
import threading

from chatbot import ChatBot
from apis.spotify import spotify_api
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'deps', 'pyHoNBot'))
from deps.pyHoNBot import bot
honbot = imp.load_source('honbot', 'deps/pyHoNBot/honbot')


def load_config():
  '''Copied from main() in pyHoNBot/honbot.'''
  config_modules = []
  for config_name in honbot.config_names('default'):
    name = os.path.basename(config_name).split('.')[0] + '_config'
    module = imp.load_source(name, config_name)
    module.filename = config_name

    if not hasattr(module, 'prefix'):
       module.prefix = r'\.'

    config_modules.append(module)
  return config_modules


def main():
  # Create the pyHoNBot and log in.
  configs = load_config()
  config = configs[0]
  if config:
    # Hack to allow pyHoNBot to use the correct home directory.
    bot.home = os.path.join(os.getcwd(), 'deps', 'pyHoNbot')
    hon_chat_bot = bot.Bot(config)

    twitch_chat_bot = ChatBot(hon_chat_bot)
    twitch_chat_bot.connect()

    # Spawn a new thread to handle the twitch bot chat commands.
    command_thread = threading.Thread(target=twitch_chat_bot.handle_commands)
    command_thread.start()

    # Spawn a new thread to output the text to file for OBS.
    obs_file_thread = threading.Thread(target=spotify_api.write_to_OBS_file)
    obs_file_thread.start()

    # Run the pyHoNBot.
    hon_chat_bot.run()


if __name__ == '__main__':
  main()
