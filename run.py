"""Run this script with |python run.py|."""

import imp
import os
import string
import sys
import threading
import Tkinter as tk

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


def terminate():
  print("Goodbye!")
  sys.exit()


def test_message(twitch_chat_bot):
  twitch_chat_bot.command_center.whisper("This is a test!")


def username_changed(twitch_chat_bot, var):
  twitch_chat_bot.command_center.hon_account = var.get()


def create_window(twitch_chat_bot):
  window = tk.Tk()
  window.title("HoN Twitch Chatbot")
  tk.Button(window, text="Exit", command=lambda: terminate())

  username_label = tk.Label(text="Username:")
  username_label.pack()

  username = tk.StringVar()
  try:
    username.trace_add("write", lambda *args: username_changed(twitch_chat_bot, username))
  except:  #python 2
    username.trace("w", lambda *args: username_changed(twitch_chat_bot, username))
  username_entry = tk.Entry(window, textvariable=username)
  username_entry.pack()

  test_button = tk.Button(text="Send test message", command=lambda: test_message(twitch_chat_bot))
  test_button.pack()

  window.mainloop()


def main():
  # Create the pyHoNBot and log in.
  configs = load_config()
  config = configs[0]
  if config:
    # Hack to allow pyHoNBot to use the correct home directory.
    bot.home = os.path.join(os.getcwd(), 'deps', 'pyHoNbot')
    hon_chat_bot = bot.Bot(config)
    print(config)

    twitch_chat_bot = ChatBot(hon_chat_bot)
    twitch_chat_bot.connect()

    # Spawn a new thread to handle the twitch bot chat commands.
    command_thread = threading.Thread(target=twitch_chat_bot.handle_commands)
    command_thread.start()

    # Spawn a new thread to output the text to file for OBS.
    obs_file_thread = threading.Thread(target=spotify_api.write_to_OBS_file)
    obs_file_thread.start()

    # Run the pyHoNBot which connects to the HoN chat channel.
    honbot_thread = threading.Thread(target=hon_chat_bot.run)
    honbot_thread.start()

    # Create the window to manage controls.
    create_window(twitch_chat_bot)


if __name__ == '__main__':
  main()
