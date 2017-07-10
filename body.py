from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import json
import random
import time
import keras.backend as K

capabilities = DesiredCapabilities.CHROME.copy()
capabilities['loggingPrefs'] = {'browser':'ALL'}
scientists = [
    'Newton', 'Einstein', 'Tesla', 'Heisenberg',
    'Euler', 'Gauss', 'Maxwell', 'Schrödinger',
    'Feynman', 'Curie', 'Noether', 'Boltzmann'
]


class SplixBot:
    def __init__(self, team_mode=False):
        self.driver = webdriver.Chrome(desired_capabilities=capabilities)
        self.wait = WebDriverWait(self.driver, float("inf"), poll_frequency=0.01)
        self.body = None
        self.team_mode = team_mode

    def join(self, name=None, url=None):
        assert not self.team_mode or url, 'Must have a url in team mode'

        url = url or 'http://splix.io/'
        name = name or random.choice(scientists)
        self.driver.get(url)

        self.body = self.wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body")))
        username = self.wait.until(EC.visibility_of_element_located((By.ID, "nameInput")))
        username.clear()
        username.send_keys(name)

        self.left  = lambda t=0: self.body.send_keys(Keys.ARROW_LEFT) or time.sleep(t)
        self.right = lambda t=0: self.body.send_keys(Keys.ARROW_RIGHT) or time.sleep(t)
        self.up    = lambda t=0: self.body.send_keys(Keys.ARROW_UP) or time.sleep(t)
        self.down  = lambda t=0: self.body.send_keys(Keys.ARROW_DOWN) or time.sleep(t)
        self.honk  = lambda t=0: self.body.send_keys(" ") or time.sleep(t)
        self.pause = lambda t=0: self.body.send_keys("p") or time.sleep(t)
        self.directions = {
            0: self.right,
            1: self.down,
            2: self.left,
            3: self.up,
            4: self.pause
        }

        if not self.team_mode:
            join_button = self.wait.until(EC.visibility_of_element_located((By.ID, "joinButton")))
            join_button.click()

            # pause at the start of the game
            for i in range(50):
                self.pause()


    def get_game_update(self):
        script = """
            console.clear();
            console.log(JSON.stringify({
                'players': players,
                'blocks': blocks,
                'score': realScoreStat
            }));
        """
        try:
            self.driver.execute_script(script)
            s = self.driver.get_log('browser')[-1]['message']
            return json.loads(s[1 + s.index('"'):-1].replace('\\"', '"'))
        except:
            return {}

    def play(self, brain, sleep=0):
        while True:
            try:
                start = time.time()
                action = brain.update(self.get_game_update())
                if action is not None:
                    self.directions[action]()
                end = time.time()
                print('Processing time: {:.5f} sec'.format(end - start))
                time.sleep(sleep)
            except KeyboardInterrupt:
                self.driver.close()
                import sys
                sys.exit()


def main():
    from brain import NeuralNetwork
    brain = NeuralNetwork()
    bot = SplixBot(team_mode=False)
    bot.join()
    bot.play(brain)

if __name__ == "__main__":
    main()
    K.clear_session()
