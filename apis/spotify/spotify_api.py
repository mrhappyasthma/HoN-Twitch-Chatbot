import win32gui

SPOTIFY_WINDOW_NAME = 'SpotifyMainWindow'
NO_SONG_PLAYING = 'Spotify'  # If not song is playing, returns 'Spotify'.

def get_current_song_info():
  """Get the current Spotify now-playing song/artist info.

  Returns:
      Returns a string containing the Spotify now-playing song/artist,
      if it can be found. Otherwise, it returns an empty string.
  """
  window_id = win32gui.FindWindow(SPOTIFY_WINDOW_NAME, None)
  if window_id:
    song_info = win32gui.GetWindowText(window_id)
    if song_info and song_info != NO_SONG_PLAYING:
      return song_info
  return ''

def write_to_OBS_file():
  """Outputs the current song_info repeatedly into a text file for OBS.

  This text file can be used as a `Text Source` in OBS streaming software,
  to display the currently displaying Spotify song on stream.
  """
  last_song = ''
  while True:  # Loops forever. Should be ran inside a thread.
    song_info = get_current_song_info()
    if song_info and song_info != last_song:
      with open('now_playing.txt', 'w') as file:
        file.write(song_info)
        last_song = song_info
        print 'Updating song file: ' + song_info