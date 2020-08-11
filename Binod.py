from selenium import webdriver
from selenium.common import exceptions
import time

data = {}

def scrape(url):

    driver = webdriver.Chrome('E:\\Downloads\\chromedriver')

    driver.get(url)
    driver.maximize_window()
    time.sleep(5)

    try:
        title = driver.find_element_by_xpath('//*[@id="container"]/h1/yt-formatted-string').text
        comment_section = driver.find_element_by_xpath('//*[@id="comments"]')
    except exceptions.NoSuchElementException:
        print('Error: Double check selector or element may not be loaded while executing find operation!')

    driver.execute_script('arguments[0].scrollIntoView();', comment_section)
    time.sleep(7)

    last_height = driver.execute_script('return document.documentElement.scrollHeight')

    while True:
        driver.execute_script('window.scrollTo(0,document.documentElement.scrollHeight);')
        time.sleep(2)

        new_height = driver.execute_script('return document.documentElement.scrollHeight')

        if new_height == last_height:
            break
        last_height = new_height

    driver.execute_script('window.scrollTo(0,document.documentElement.scrollHeight);')

    try:
        username_elems = driver.find_elements_by_xpath('//*[@id="author-text"]')
        comment_elems = driver.find_elements_by_xpath('//*[@id="content-text"]')
    except exceptions.NoSuchElementException:
        print('Error: Double check selector or element may not be loaded while executing find operation!')

    print(f'\n> VIDEO TITLE: {title}\n')
    print(f'> COMMENTS HAVING BINOD IN IT:\n')

    for username, comment in zip(username_elems, comment_elems):
        data[username.text] = comment.text
        # print(f'{username.text}:\n')
        # print(f'{comment.text}')

    for key in data.keys():
        if 'binod' in data[key].lower() or 'b i n o d' in data[key].lower():
            print(f'\'{key}\' has commented \'{data[key]}\' on your video which has \'Binod\' in it!')

    print()
    driver.close()

if __name__ == "__main__":
    url = input('Enter the URL of the video: https://')
    scrape(f'https://{url}')
