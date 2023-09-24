import unittest
import requests
from unittest.mock import MagicMock
from view.lottie_animation import load_lottie_url


class TestLoadLottieURL(unittest.TestCase):

    def test_load_lottie_url_success(self):
        url = 'https://example.com/lottie_url'
        expected_result = {'key': 'value'}

        requests.get = MagicMock(return_value=MagicMock(status_code=200, json=MagicMock(return_value=expected_result)))

        result = load_lottie_url(url)

        self.assertEqual(result, expected_result)

    def test_load_lottie_url_failure(self):
        url = 'https://example.com/invalid_url'

        requests.get = MagicMock(return_value=MagicMock(status_code=404))

        result = load_lottie_url(url)

        self.assertIsNone(result)
