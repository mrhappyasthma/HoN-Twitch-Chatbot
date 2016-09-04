"""Run this script with |python run.py|."""

import string

from chatbot import ChatBot


def main():
  bot = ChatBot()
  bot.connect()
  bot.handle_commands()


if __name__ == '__main__':
  main()
