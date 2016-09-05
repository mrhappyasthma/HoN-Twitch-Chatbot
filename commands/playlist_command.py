from command import Command

PLAYLIST_URL = ''  # Enter your playlist URL here.

class PlaylistCommand(Command):
  """Outputs a Playlist URL into Twitch chat."""
  def _send_response(self):
    if self.args[0] != '!playlist' or len(self.args) != 1:
      return
    self.chatbot.send_chat_message('Playlist: ' + PLAYLIST_URL)