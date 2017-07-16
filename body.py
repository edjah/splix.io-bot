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

    def join(self, name=None, url=None, pause_at_start=True):
        assert not self.team_mode or url, 'Must have a url in team mode'

        url = url or 'http://splix.io/'
        name = name or random.choice(scientists)
        self.driver.get(url)

        self.body = self.wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body")))
        username = self.wait.until(EC.visibility_of_element_located((By.ID, "nameInput")))
        username.clear()
        username.send_keys(name)

        self.left  = lambda t=0: self.body.send_keys(Keys.ARROW_LEFT) or t and time.sleep(t)
        self.right = lambda t=0: self.body.send_keys(Keys.ARROW_RIGHT) or t and time.sleep(t)
        self.up    = lambda t=0: self.body.send_keys(Keys.ARROW_UP) or t and time.sleep(t)
        self.down  = lambda t=0: self.body.send_keys(Keys.ARROW_DOWN) or t and time.sleep(t)
        self.honk  = lambda t=0: self.body.send_keys(" ") or t and time.sleep(t)
        self.pause = lambda t=0: self.body.send_keys("p") or t and time.sleep(t)
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
            if pause_at_start:
                for i in range(50):
                    self.pause(0.02)


    def get_game_update(self):
        script = """
            console.clear();
            console.log(JSON.stringify({
                'players': players,
                'blocks': blocks,
                'score': Math.round(realScoreStat),
                'dead': myPlayer && myPlayer.isDead && myPlayer.deathWasCertain,
                'suicide': lastStatKiller === 'yourself'

            }));
        """
        self.driver.execute_script(script)
        s = self.driver.get_log('browser')[-1]['message']
        if '{\\"' in s:
            return json.loads(s[1 + s.index('"'):-1].replace('\\"', '"'))
        else:
            return {}
    def play(self, brain, sleep=0):
        while True:
            try:
                start = time.time()
                dead, update = False, self.get_game_update()
                if update and update['dead']:
                    time.sleep(1)
                    score, suicide = update['score'], update['suicide']
                    print('You died\nScore: {} | Suicide: {}'.format(score, suicide))
                    return update
                else:
                    action = brain.update(update)
                    if action is not None:
                        self.directions[action]()
                    end = time.time()
                    print('Action: {} | Update time: {:.5f} sec'.format(action, end - start))
                    time.sleep(sleep)
            except KeyboardInterrupt:
                self.driver.quit()
                return update


def main():
    from brain import NeuralNetwork
    brain = NeuralNetwork(init_method='load', json='model.json', h5='model.h5')
    bot = SplixBot(team_mode=False)
    bot.join()
    bot.play(brain)

if __name__ == "__main__":
    main()
    K.clear_session()
