import json
import requests

import twitch_settings


def _query_twitch_viewer_api():
  """Query the Twitch API to get the viewer data for the current channel.

  Returns:
      Returns a python dictionary containing the HTML response content. If
      the response code is not 200, then an empty dictionary is returned.
  """
  twitch_chatters_base_url = 'http://tmi.twitch.tv/group/user/{0}/chatters'
  url = twitch_chatters_base_url.format(twitch_settings.CHANNEL)
  html_response = requests.get(url)
  response_content = json.loads(html_response.content)
  return response_content if html_response.status_code == 200 else {}


def _get_chatters():
  """Get a dictionary containing the various lists of chatters in the channel.

  The dictionary contains a few lists based on the undocumented twitch API:
      - 'viewers': A list of all regular, non-upgraded viewers.
      - 'moderators': A list of all elected moderators.
      - 'staff': A list of all Twitch staff in the chat.
      - 'admins': Not sure what this is.
      - 'global_mods': Not sure what this is.

  Returns:
      Returns a dictionary containing all the various lists of viewer types in
      the current channel.
  """
  api_response = _query_twitch_viewer_api()
  return api_response.get('chatters', {}) if api_response else {}


def get_all_viewers():
  """Get a list of all the viewers in the channel.

  This returns a combined list of all regular users and moderators.

  Returns:
      Returns a list of strings containing all the usernames of all the
      viewers.
  """
  viewers = get_viewers()
  moderators = get_moderators()
  all_viewers = viewers + moderators
  return list(set(all_viewers))


def get_viewers():
  """Get a list of all the regular viewers in the channel.

  If a user is a moderator, admin, etc. then they are excluded from this list.

  Returns:
      Returns a list of strings containing all the usernames of the
      regular viewers.
  """
  chatters = _get_chatters()
  return chatters.get('viewers', []) if chatters else []


def get_moderators():
  """Get a list of the moderators in the current channel.

  Returns:
      Returns a list of strings containing all the usernames of the
      moderators for the current channel.
  """
  chatters = _get_chatters()
  return chatters.get('moderators', []) if chatters else []


def is_moderator(viewer):
  """Returns whether or not the viewer is a moderator in the current channel.

  Args:
      viewer: A string representing the viewer's twitch username.

  Return:
      Returns a boolean indicating if the viewer is a moderator in the
      current channel.
  """
  return True if viewer in get_moderators() else False