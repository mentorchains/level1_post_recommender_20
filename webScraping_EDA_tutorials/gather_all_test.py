# Access the main link

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

BASE_URL = 'https://forum.flowster.app'

opts = Options()
opts.set_headless()
assert opts.headless # Operating in headless mode
browser = Firefox(options=opts)
browser.get(BASE_URL)

# Get the all the categories names (I believe we don't need this only the links?!) or perhaps it's okay to keep it?
categories = browser.find_elements_by_class_name('category-text-title')

# Get all the categories link 
categ_links = browser.find_elements_by_css_selector('.category > h3 > a')

# Store categories links and names in separate lists
categ_names = []
categ_urls = []
for categ, link in zip(categories, categ_links):
    categ_names.append(categ.text)
    categ_urls.append(link.get_attribute('href'))
    
# Access each category to get its topics etc
import requests
import time

SEC_URL = categ_urls[1]
#page = requests.get(SEC_URL)
browser.get(SEC_URL)
browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
time.sleep(3)

from bs4 import BeautifulSoup

soup = BeautifulSoup(browser.page_source, 'html.parser')

ps_topic_links = soup.find_all('a', class_='title raw-link raw-topic-link')

# Get all the topics inside the Product Sourcing category
ps_topic_urls = []
for topic_link in ps_topic_links:
    ps_topic_urls.append(BASE_URL + topic_link['href'])

# Access one of the topic URLS and get the comments and info about it from main post
PS_URL0 = ps_topic_urls[1]
browser.get(PS_URL0)
browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
time.sleep(3)

ps_soup = BeautifulSoup(browser.page_source, 'html.parser')
topic_title = ps_soup.find('a', class_='fancy-title').text.strip()

# DONE: A topic can not only have the category but also tags so redo this 
# BEFORE: topic_category = ps_soup.find('span', class_='category-name').text.strip()

# MERGE with topic title
browser.get('https://forum.flowster.app/t/fba-revenue-calculator-ship-to-amazon/911')# replace url with topic_url
browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
time.sleep(3)

fulfil_soup = BeautifulSoup(browser.page_source, 'html.parser')
topic_title = fulfil_soup.find_elements_by_class_name('a', class_='fancy-title').text.strip()

title_wraper = fulfil_soup.find('div', class_='title-wrapper')
topic_tags = title_wraper.find_all('span', class_='category-name')
topic_tags = [tag.text for tag in topic_tags]
topic_category = topic_tags[0]
topic_tags = topic_tags[1:]
return topic_category, topic_tags


# Get the actual comments
postsDivs = postStream.find_all('div', {'class': ['topic-post clearfix topic-owner regular', 'topic-post clearfix regular']})

comments = []
for i in range(len(postsDivs)):
    comment = postsDivs[i].find('div', class_='cooked').text
    #postsDivs[i].find('div', class_='cooked').text.replace('\n', ' ')
    comments.append(comment)

leading_comment = comments[0]
if len(comments) == 1:
    other_comments = []
else:
    other_comments = comments[1:]

# Get the other info like : likes, views, etc
created = postStream.find('li', class_="created-at")
created_at = created.find('span', class_='relative-date')['title']

last_reply = postStream.find('li', class_="last-reply")
last_reply = last_reply.find('span', class_='relative-date')['title']

replies = postStream.find('li', class_="replies")
nbr_replies = replies.find('span', class_='number').text

views = postStream.find('li', class_="secondary views")
nbr_views = views.find('span', class_='number').text

likes = postStream.find('li', class_="secondary likes")

# Some posts may not actually have likes or views or etc so we should handle it.
try:
    nbr_likes = likes.find('span', class_='number').text
    print(nbr_likes)
except:
    print(0)