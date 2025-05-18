from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
import time
import pickle



# Put tournament links here in this EXACT format
tournament_urls = [
    "https://www.start.gg/tournament/freaks-denton-166/event/smash-ultimate-singles",
    "https://www.start.gg/tournament/freaks-richardson-191-ft-100-in-pot-bonuses/event/singles-1v1-50-pot-bonus",
    "https://www.start.gg/tournament/freaks-denton-167-50-pot-bonus-sponsored-by-final-form/event/singles-1v1-50-pot-bonus",
    "https://www.start.gg/tournament/freaks-richardson-192/event/singles-1v1",
    "https://www.start.gg/tournament/don-t-get-tilted-236/event/dgt-smash-singles",
    "https://www.start.gg/tournament/don-t-get-tilted-237/event/dgt-smash-singles",
    "https://www.start.gg/tournament/don-t-get-tilted-238/event/dgt-smash-singles",
    "https://www.start.gg/tournament/ssbu-open-at-cecc-may-madness-2025/event/ultimate-singles",
    "https://www.start.gg/tournament/zouffle-smash-texas-8/event/smash-ultimate-singles"



]



options = Options()
service = Service(GeckoDriverManager().install())
driver = webdriver.Firefox(service=service, options=options)

# Set up a cookies file in braacket
driver.get("https://braacket.com/")
time.sleep(2)

# Load the cookies file with login info
with open("braacket_cookies.pkl", "rb") as f:
    cookies = pickle.load(f)
    for cookie in cookies:
        driver.add_cookie(cookie)


# Get info from url for input as metadata in braacket
def get_tournament(url):
    start = url.find("tournament/") + len("tournament/")
    end = url.find("/event", start)
    return url[start:end] if start > -1 and end > -1 else None

def get_event(url):
    start = url.find("event/") + len("event/")
    return url[start:] if start > -1 else None


# Main function to create a tournament in braacket
def add_tourney(tournament, event):
    time.sleep(2)
    driver.get("https://braacket.com/tournament/import/smashgg?league=DFWSMASH2")
    time.sleep(2)

    ID_input = driver.find_element(By.NAME, "tournament")
    ID_input.send_keys(tournament)

    event_input = driver.find_element(By.NAME, "event")
    event_input.send_keys(event)


    exclude_dq = driver.find_element(By.NAME, "exclude_dq")
    driver.execute_script("arguments[0].scrollIntoView(true);", exclude_dq)
    time.sleep(0.5)  # Give time for scroll animation
    exclude_dq.click()


    admin_league_inherit = driver.find_element(By.NAME, "admin_league_inherit")
    driver.execute_script("arguments[0].scrollIntoView(true);", admin_league_inherit)
    time.sleep(0.5)  # Give time for scroll animation
    admin_league_inherit.click()

    add_tourney = driver.find_element(By.CSS_SELECTOR, ".my-btn-group-responsive > div:nth-child(1) > button:nth-child(1)")
    driver.execute_script("arguments[0].scrollIntoView(true);", admin_league_inherit)
    time.sleep(0.5)  # Give time for scroll animation
    add_tourney.click()
    time.sleep(13)


minutes = str((len(tournament_urls)*20)/60)
print("\nShould take " + minutes + " minutes\n\n")
print("--------------------------------------------------")


for url in tournament_urls:
        tournament = get_tournament(url)
        event = get_event(url)
        add_tourney(tournament, event)

        print("Added:  " + tournament)


print("--------------------------------------------------\nFinished!")