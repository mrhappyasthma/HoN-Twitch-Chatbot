import mock
import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), '..'))
import twitch_api


MOCK_TWITCH_RESPONSE = {'chatters': {'viewers': ['viewer1', 'viewer2'],
                                     'moderators': ['mod1', 'mod2']}}


class MockResponse:
  def __init__(self, is_valid):
    if is_valid:
      self.status_code = 200
      self.content = ('{"chatters": {"viewers": ["viewer1", "viewer2"],'
                      '"moderators": ["mod1", "mod2"]}}')
    else:
      self.status_code = 404
      self.content = '{}'


def mock_query_twitch():
  return MOCK_TWITCH_RESPONSE


def mock_get_chatters():
  return MOCK_TWITCH_RESPONSE['chatters']


def mock_get_moderators():
  return ['fake_mod']


class TestTwitchLib(unittest.TestCase):
  @mock.patch('requests.get')
  def test_query_twitch_viewer_api(self, mock_requests_get):
    mock_requests_get.return_value = MockResponse(is_valid=True)
    response = twitch_api._query_twitch_viewer_api()
    self.assertEqual(response, MOCK_TWITCH_RESPONSE)

    mock_requests_get.return_value = MockResponse(is_valid=False)
    response = twitch_api._query_twitch_viewer_api()
    self.assertEqual(response, {})

  @mock.patch('twitch_api._query_twitch_viewer_api', side_effect=mock_query_twitch)
  def test_get_chatters(self, mock_query):
    chatters = twitch_api._get_chatters()
    self.assertEquals(chatters, MOCK_TWITCH_RESPONSE['chatters'])

  @mock.patch('twitch_api._get_chatters', side_effect=mock_get_chatters)
  def test_get_all_viewers(self, mock_get_chats):
    all_viewers = twitch_api.get_all_viewers()
    self.assertEqual(set(all_viewers),
                     set(['viewer1', 'viewer2', 'mod1', 'mod2']))

  @mock.patch('twitch_api._get_chatters', side_effect=mock_get_chatters)
  def test_get_viewers(self, mock_get_chats):
    viewers = twitch_api.get_viewers()
    self.assertEqual(viewers, ['viewer1', 'viewer2'])

  @mock.patch('twitch_api._get_chatters', side_effect=mock_get_chatters)
  def test_get_moderators(self, mock_get_chats):
    mods = twitch_api.get_moderators()
    self.assertEqual(mods, ['mod1', 'mod2'])

  @mock.patch('twitch_api.get_moderators', side_effect=mock_get_moderators)
  def test_is_moderator(self, mock_get_mods):
    self.assertTrue(twitch_api.is_moderator('fake_mod'))
    self.assertFalse(twitch_api.is_moderator('invalid_user'))


if __name__ == '__main__':
  unittest.main()