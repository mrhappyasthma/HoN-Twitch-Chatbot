import json
import requests

import hon_settings


HON_API_URL = 'http://api.heroesofnewerth.com/'


def _get_player_stats(username):
  """Queries the HoN Stats API for a user's stats.

  Args:
      username: A string containing the HoN username to query the
          stats for.

  Returns:
      Returns a python dictionary containing the HTML response content. If
      the response code is not 200, then an empty dictionary is returned.
  """
  stats_tmpl = 'player_statistics/ranked/nickname/{0}/?token={1}'
  url = HON_API_URL + stats_tmpl.format(username, hon_settings.HON_TOKEN)
  html_response = requests.get(url)
  response_content = json.loads(html_response.content)
  return response_content if html_response.status_code == 200 else {}


def get_mmr(username):
  """Returns a string containing a user's M stat.

  Args:
      username: A string containing the HoN username to query the
          stats for.

  Returns:
    Returns a string containing the user's mmr. If it cannot be queried
    successfully, then an empty string is returned.
  """
  mmr_key = 'rnk_amm_team_rating'
  stats_dict = _get_player_stats(username)
  mmr_string = stats_dict.get(mmr_key, '-1');
  mmr = int(round(float(mmr_string)))  # Round the mmr float string to int.
  return str(mmr) if mmr is not -1 else ''