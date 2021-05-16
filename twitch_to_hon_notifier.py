import json
import requests

import time # remove
import os
import sys
import twitch_settings

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'deps', 'pyHoNBot'))
from deps.pyHoNBot.hon import packets

class TwitchToHoNNotifier:
  """This class is responsible sending HoN whispers for Twitch notifications.

  It is responsible for polling the Twitch API for updates to things like
  followers, and forwarding appropriate messages into HoN.
  """

  def __init__(self, chatbot, honbot):
    self.chatbot = chatbot
    self.honbot = honbot
    self.recent_followers = []


  def initialize_followers(self):
    ids = []
    followers = self._get_last_10_followers()
    for follower in followers:
      user = follower.get('user', {})
      id = user.get('_id', 0)
      if id:
        ids.append(id)
    self.recent_followers = ids


  def _get_last_10_followers(self):
    """Query the Twitch API to get the last 10 followers.

    Returns:
      Returns a ptyhon dictionary containing the HTLM response content. If
      the response code is not 200, then an empty dictionary is returned.
    """
    twitch_followers_base_url = 'https://api.twitch.tv/kraken/channels/{0}/follows'
    url = twitch_followers_base_url.format(twitch_settings.CHANNEL)
    header = {'Client-ID': twitch_settings.CLIENT_ID}
    html_response = requests.get(url, headers=header)
    if html_response and html_response.content:
      response_content = json.loads(html_response.content)
      return response_content.get('follows', {}) if html_response.status_code == 200 else {}
    return {}


  def _alert_for_new_followers(self, followers):
    """Query the Twitch API to get the names/IDs of the last 10 followers."""
    ids = []
    for follower in followers:
      user = follower.get('user', {})
      display_name = user.get('display_name', 0)
      id = user.get('_id', 0)
      if display_name and id:
        ids.append(id)
        if not id in self.recent_followers:
          message_string = 'New Twitch follower: "' + display_name + '"!'
          print message_string
          hon_acc = self.chatbot.command_center.hon_account
          if hon_acc:
            self.honbot.write_packet(packets.ID.HON_SC_WHISPER, hon_acc, message_string)
    self.recent_followers = ids

  def poll(self):
    time.sleep(5) # this is super hacky... remove it in favor of waiting until pyHoNBot is connected.
    print 'Polling for Twitch notifications to foward to HoN...'
    while True: # Loops forever. Should be ran inside a thread.
      time.sleep(30)  # Only poll once per 30s, to avoid Twitch caching/slow update speeds.
      followers = self._get_last_10_followers()
      if followers:
        self._alert_for_new_followers(followers)