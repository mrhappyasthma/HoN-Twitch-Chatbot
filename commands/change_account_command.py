from apis.twitch import twitch_api
from command import Command

class ChangeAccountCommand(Command):
  def __init__(self, user, args, chatbot):
    self.hon_account = None
    super(ChangeAccountCommand, self).__init__(user, args, chatbot)

  def _send_response(self):
    if self.args[0] != '!changeacc' or len(self.args) != 2:
      return
    if twitch_api.is_moderator(self.user):
      self.hon_account = self.args[1]
      if self.hon_account:
        self.chatbot.send_chat_message('Tracking HoN account: ' + self.hon_account)

  def get_new_account(self):
    return self.hon_account