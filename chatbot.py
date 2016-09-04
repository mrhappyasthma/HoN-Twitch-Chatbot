import socket
import StringIO

import twitch_settings


class ChatBot():
  """A bot that can connect to a Twitch channel and interact with the chat.

  To use this bot, first configure your settings in `/twitch_settings.py`.

  Then you can use the ChatBot like so:
      bot = ChatBot()
      bot.connect()
      bot.send_chat_message('Hello World')
  """
  def __init__(self, host='irc.twitch.tv', port=6667):
    self.host = host
    self.port = port
    self.socket = None
    self._load_twitch_settings()

  def _load_twitch_settings(self):
    """Sets the corresponding twitch settings."""
    self.password = twitch_settings.OAUTH
    self.username = twitch_settings.BOT_USERNAME
    self.channel = twitch_settings.CHANNEL

  def _send(self, text):
    """Sends the provided text over a socket.

    Implicitly adds '\r\n' to the end of the text.

    Args:
        text: A string of text to be send over the socket.
    """
    if self.socket:
      self.socket.send(text + '\r\n')
    else:
      print 'ERROR: Cannot send message "' + text + '" because you have not connected yet.'

  def _login(self):
    """Logs in to an account using a username and oauth as a password.

    Note: If the connection has not been opened, nothing happens.
    """
    if self.socket:
      self._send('PASS ' + self.password)
      self._send('NICK ' + self.username)
    else:
      print 'ERROR: Cannot login channel because you have not connected yet.'

  def _read_lines(self, incomplete_data):
    buffer = StringIO.StringIO(100000)
    if incomplete_data:
      buffer.write(incomplete_data)
    data = self.socket.recv(1024)
    buffer.write(data)
    return buffer.getvalue().splitlines()

  def _wait_until_successful_channel_join(self):
    incomplete_data = ""
    while True:
      lines = self._read_lines(incomplete_data)
      incomplete_data = lines[-1]

      for line in lines:
        print line
        if 'End of /NAMES list' in line:
          return

  def join_channel(self, channel):
    """Sends the command over the socket to join a given channel.

    Note: If the connection has not been opened, nothing happens.

    Args:
        channel: The string name of the channel to join.
    """
    if self.socket:
      self.channel = channel
      self._send('JOIN #' + self.channel)
      self._wait_until_successful_channel_join()
      self.send_chat_message('Successfully joined chat!')
    else:
      print 'ERROR: Cannot join channel #' + channel + ' because you have not connected yet.'

  def connect(self):
    """Connects with Twitch by logging-in and joining a channel.

    Note: Calling this method twice will have no effect.
    """
    if not self.socket:
      self.socket = socket.socket()
      self.socket.connect((self.host, self.port))
      self._login()
      self.join_channel(self.channel)
    else:
      print 'WARNING: You cannot connect twice.'

  def send_chat_message(self, message):
    """Sends a message over the socket to the current Twitch chat channel.

    Note: If the connection has not been opened, nothing happens.

    Args:
        message: The string that the bot will send over the socket and print
        into the twitch chat channel.
    """
    if self.socket:
      message = 'PRIVMSG #' + self.channel + ' :' + message
      self._send(message)
    else:
      print 'ERROR: Cannot send message "' + message + '" because you have not connected yet.'