from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

def web_scrape(link):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)
    url = link
    driver.get(url)

    try:
        WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'songs-list svelte-1vyb47z songs-list--header-is-visible songs-list--playlist')))
    except Exception:
        pass

    page = driver.page_source
    soup = BeautifulSoup(page, 'html.parser')

    name = soup.find('span',{'dir':'auto'}).get_text()

    songs = {}
    for i, song in enumerate(soup.find_all('div', {'class':'songs-list-row__song-name svelte-1th7508'}), start=1):  
        songs[i] = [(song.get_text())]

    i = 1
    for artist in soup.find_all('span', {'class':'svelte-1th7508'}):
        if artist.get_text():
            songs[i].append(artist.get_text())
            i += 1

    return songs, name

