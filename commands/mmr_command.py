from apis.hon import hon_api
from command import Command

class MmrCommand(Command):
  def __init__(self, user, args, chatbot, hon_account):
    self.hon_account = hon_account
    super(MmrCommand, self).__init__(user, args, chatbot)

  def _send_response(self):
    if self.args[0] != '!mmr' or not self.hon_account:
      return
    mmr = hon_api.get_mmr(self.hon_account)
    self.chatbot.send_chat_message(mmr)