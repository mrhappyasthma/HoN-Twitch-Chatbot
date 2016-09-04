from command import Command

class AccountCommand(Command):
  def __init__(self, user, args, chatbot, hon_account):
    self.hon_account = hon_account
    super(AccountCommand, self).__init__(user, args, chatbot)

  def _send_response(self):
    if self.args[0] != '!acc' and self.args[0] != '!account':
      return
    if not self.hon_account:
      self.chatbot.send_chat_message('No HoN account has been set.')
    else:
      self.chatbot.send_chat_message('Current HoN account = "' + self.hon_account + '".')