class Command(object):
  """An abstract class to be extended by each command.

  Upon initialization, commands should accept in a list of
  string arguments, the first of which should map to its
  command name.

  Commands should send text back to the server in response.
  """
  def __init__(self, user, args, chatbot):
    self.user = user
    self.args = args
    self.chatbot = chatbot
    self._send_response()

  def _send_response(self):
    """This should be overridden by subclasses to send a response to Twitch."""
    pass