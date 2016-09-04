import mock
import unittest

import hon_api


MOCK_MMR_RESPONSE = {'rnk_amm_team_rating': '1500.33'}


class MockResponse:
  def __init__(self, is_valid):
    if is_valid:
      self.status_code = 200
      self.content = '{"rnk_amm_team_rating": "1500.33"}'
    else:
      self.status_code = 404
      self.content = '{}'


def mock_requests_get(url):
  return MockResponse(url)


def mock_player_stats(username):
  return MOCK_MMR_RESPONSE if username == 'fake_username' else {}


class TestHonLib(unittest.TestCase):
  @mock.patch('requests.get')
  def test_get_player_stats(self, mock_request_gets):
    mock_request_gets.return_value = MockResponse(is_valid=True)
    response = hon_api._get_player_stats('fake_username')
    self.assertEqual(response, MOCK_MMR_RESPONSE)

    mock_request_gets.return_value = MockResponse(is_valid=False)
    response = hon_api._get_player_stats('invalid_username')
    self.assertEqual(response, {})

  @mock.patch('hon_api._get_player_stats', side_effect=mock_player_stats)
  def test_get_mmr(self, player_stats):
    mmr = hon_api.get_mmr('fake_username')
    self.assertEqual(mmr, '1500')

    mmr = hon_api.get_mmr('invalid_username')
    self.assertEqual(mmr, '')


if __name__ == '__main__':
  unittest.main()