import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))
from apis.hon.hon_hero_name_whitelist import hon_hero_name_whitelist
from command import Command
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'deps', 'pyHoNBot'))
from deps.pyHoNBot.hon import packets

class PickHeroCommand(Command):
  def __init__(self, user, args, chatbot, honbot, hon_account):
    self.honbot = honbot
    self.hon_account = hon_account
    super(PickHeroCommand, self).__init__(user, args, chatbot)

  def _send_response(self):
    if self.args[0] != '!pick' or len(self.args) != 2:
      return
    if not self.honbot or not self.hon_account:
      self.chatbot.send_chat_message('The HoN TwitchBot is currently down.')
    else:
      if self.args[1].lower() in map(str.lower, hon_hero_name_whitelist):
        hero_index = map(str.lower, hon_hero_name_whitelist).index(self.args[1].lower())
        message_string = 'Twitch user "' + self.user + '" wants to you to pick "' + hon_hero_name_whitelist[hero_index] + '"!'
        self.honbot.write_packet(packets.ID.HON_SC_WHISPER, self.hon_account, message_string)
        self.chatbot.send_chat_message('Hero request sent.')