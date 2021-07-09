import requests
import pytest
import json


class TestHomeWork4:
    agents = [
        ({'User-Agent': 'Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
          'platform': 'Mobile', 'browser': 'No', 'device': 'Android'}),
        ({'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1',
         'platform': 'Mobile', 'browser': 'Chrome', 'device': 'iOS'}),
        ({'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
            'platform': 'Googlebot', 'browser': 'Unknown', 'device': 'Unknown'}),
        ({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0',
            'platform': 'Web', 'browser': 'Chrome', 'device': 'No'}),
        ({'User-Agent': 'Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
          'platform': 'Mobile', 'browser': 'No', 'device': 'iPhone'})
    ]

    @pytest.mark.parametrize('agents', agents)
    def test_user_agent(self, agents):
        response = requests.get("https://playground.learnqa.ru/ajax/api/user_agent_check", headers={"User-Agent": agents['User-Agent']})

        response_text = json.loads(response.text)

        assert response_text['platform'] == agents['platform'], "The platform not equal to expected."
        assert response_text['browser'] == agents['browser'], "The browser not equal to expected."
        assert response_text['device'] == agents['device'], "The device not equal to expected."
