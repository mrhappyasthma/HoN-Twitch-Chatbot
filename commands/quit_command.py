import os

from apis.twitch import twitch_api
from command import Command

class QuitCommand(Command):
  def _send_response(self):
    if self.args[0] != '!quit' or len(self.args) != 1:
      return
    if twitch_api.is_moderator(self.user):
      self.chatbot.send_chat_message('Disconnecting...')
      os._exit(1)  # Use this of sys.exit() to close all threads.