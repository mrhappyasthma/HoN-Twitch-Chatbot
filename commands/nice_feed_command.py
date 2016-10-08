import os
import sys

from command import Command
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'deps', 'pyHoNBot'))
from deps.pyHoNBot.hon import packets

class NiceFeedCommand(Command):
  def __init__(self, user, args, chatbot, honbot, hon_account):
    self.honbot = honbot
    self.hon_account = hon_account
    super(NiceFeedCommand, self).__init__(user, args, chatbot)

  def _send_response(self):
    if self.args[0] != '!nicefeed' or len(self.args) != 1:
      return
    if not self.honbot or not self.hon_account:
      self.chatbot.send_chat_message('The HoN TwitchBot is currently down.')
    else:
      message_string = 'Nice feed you fking noob!'
      self.honbot.write_packet(packets.ID.HON_SC_WHISPER, self.hon_account, message_string)
      self.chatbot.send_chat_message('Nice feed message sent to: ' + self.hon_account)