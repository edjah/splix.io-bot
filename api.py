import re
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import json
import time


capabilities = DesiredCapabilities.CHROME.copy()
capabilities['loggingPrefs'] = {'browser':'ALL'}
body = None
driver = webdriver.Chrome(desired_capabilities=capabilities)
wait = WebDriverWait(driver, float("inf"), poll_frequency=0.1)

# visit the website
def go_to_site():
    global body
    driver.get("http://splix.io/")
    body = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body")))

# join a game with a given username
def join(name="testest"):
    username = wait.until(EC.visibility_of_element_located((By.ID, "nameInput")))
    username.clear()
    username.send_keys(name)
    join_button = wait.until(EC.visibility_of_element_located((By.ID, "joinButton")))
    join_button.click()

    # pause at the start of the game
    for i in range(50):
        pause()

def join_team(name="testest"):
    global body
    body = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body")))
    team_url = input("Enter lobby url: ")

    driver.get(team_url)
    username = wait.until(EC.visibility_of_element_located((By.ID, "nameInput")))
    username.clear()
    username.send_keys(name)

# retrieve information about the game state
def get_game_update():
    script = """
        console.clear();
        console.log(JSON.stringify(players));
    """
    driver.execute_script(script)
    s = driver.get_log('browser')[-1]['message']
    return json.loads(s[1 + s.index('"'):-1].replace('\\"', '"'))


# helper functions for game controls
left  = lambda t=0: body.send_keys(Keys.ARROW_LEFT) or time.sleep(t)
right = lambda t=0: body.send_keys(Keys.ARROW_RIGHT) or time.sleep(t)
up    = lambda t=0: body.send_keys(Keys.ARROW_UP) or time.sleep(t)
down  = lambda t=0: body.send_keys(Keys.ARROW_DOWN) or time.sleep(t)
honk  = lambda t=0: body.send_keys(" ") or time.sleep(t)
pause = lambda t=0: body.send_keys("p") or time.sleep(t)


if __name__ == "__main__":
    # try:
    #     go_to_site()
    #     join_team()
    #     for command in [right, up] * 10:
    #         command(0.1)
    #     left(1)
    #     for command in [down, left] * 10:
    #         command(0.1)
    #     pause()
    # except Exception as e:
    #     print(e)

    # time.sleep(1)
    # try:
    #     driver.close()
    # except:
    #     pass
    join_team()
