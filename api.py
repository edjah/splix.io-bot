import re
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time


capabilities = DesiredCapabilities.CHROME.copy()
capabilities['loggingPrefs'] = {'browser':'ALL'}
driver = webdriver.Chrome(desired_capabilities=capabilities)
wait = WebDriverWait(driver, float("inf"), poll_frequency=0.1)

def go_to_site():
    driver.get("http://splix.io/")

def join(name="testest"):
    username = wait.until(EC.visibility_of_element_located((By.ID, "nameInput")))
    username.clear()
    username.send_keys(name)
    join_button = wait.until(EC.visibility_of_element_located((By.ID, "joinButton")))
    join_button.click()

def left(body):
    body.send_keys(Keys.ARROW_LEFT)

def right(body):
    body.send_keys(Keys.ARROW_RIGHT)

def up(body):
    body.send_keys(Keys.ARROW_UP)

def down(body):
    body.send_keys(Keys.ARROW_DOWN)

def pause(body):
    body.send_keys("p")

def honk(body):
    body.send_keys(" ")


def get_game_update():
    driver.execute_script('console.log(JSON.stringify(players))')
    s = driver.get_log('browser')[-1]['message']
    s = s[1 + s.index('"'):-1]


# close the browser window
def quit():
    driver.close()

# main method
if __name__ == "__main__":
    go_to_site()
    join()

    body = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body")))
    print('body located')
    for command in [up, left, down, right, pause, honk]:
        command(body)
        time.sleep(1)

    quit()
