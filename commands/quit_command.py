import sys

from apis.twitch import twitch_api
from command import Command

class QuitCommand(Command):
  def _send_response(self):
    if twitch_api.is_moderator(self.user):
      self.chatbot.send_chat_message('Disconnecting...')
      sys.exit()