from apis.spotify import spotify_api
from command import Command

class SongCommand(Command):
  """Outputs the current song into Twitch chat."""
  def _send_response(self):
    if self.args[0] != '!song' or len(self.args) != 1:
      return
    song_info = spotify_api.get_current_song_info()
    if song_info:
      self.chatbot.send_chat_message('Now playing: ' + song_info)
    else:
      self.chatbot.send_chat_message('No song currently playing.')