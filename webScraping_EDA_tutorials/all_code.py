from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import requests
import time

BASE_URL = 'https://forum.flowster.app'
browser = None

opts = Options()
opts.set_headless()
assert opts.headless # Operating in headless mode
browser = Firefox(options=opts)

# We didn't get this 
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

# TODO: loop over each category url from categ_urls and get categ_url 
def get_topics_urls(categ_url):
    """
    Get topic URLS for each category
    """
    browser.get(categ_url)
                 browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(3)
    
    categ_topic_soup = BeautifulSoup(browser.page_source, 'html.parser')
    
    categ_topic_links = categ_topic_soup.find_all('a', class_='title raw-link raw-topic-link')
    
    # Get all the topics inside the Product Sourcing category
    categ_topic_urls = []
    
    for topicb_link in categ_topic_links:
        categ_topic_urls.append(BASE_URL + topic_link['href'])
    
    return categ_topic_urls

# TODO: Loop over each categ_topic_urls to get topic_url
def get_topic_soup(topic_url):
    """
    Get current topic_soup
    """
    browser.get(topic_url)
    browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(3)
    topic_soup = BeautifulSoup(browser.page_source, 'html.parser')
    return topic_soup

topic_soup = get_topic_soup(topic_url)

def get_topic_title_tags(topic_soup):
    """
    Get topic title
    """
    topic_title = topic_soup.find('a', class_='fancy-title').text.strip()
    
    title_wraper = topic_soup.find('div', class_='title-wrapper')
    
    topic_tags = title_wraper.find_all('span', class_='category-name')
    topic_tags = [tag.text for tag in topic_tags]
    topic_tags = topic_tags[1:]
    
    topic_category = topic_tags[0]
    
    return topic_title, topic_category, topic_tags
    
def get_topic_comments(topic_soup):
    """
    Get topic leading post and its replies.
    """
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
    
    return leading_comment, other_comments

def get_topic_created_at(topic_soup):
    """
    Get the topic creation date
    """
    created = topic_soup.find('li', class_="created-at")
    created_at = created.find('span', class_='relative-date')['title']
    if created_at == None:
        return str(0)
    return created_at


def get_topic_replies_nbr(topic_soup):
    """
    Get the topic's nbr of replies
    """    
    replies = topic_soup.find('li', class_="replies")
    nbr_replies = replies.find('span', class_='number').text
    if nbr_replies == None:
        return str(0)
    return nbr_replies

def get_topic_views_nbr(topic_soup):
    """
    Get the topic's nbr of views
    """ 
    views = topic_soup.find('li', class_="secondary views")
    nbr_views = views.find('span', class_='number').text
    if nbr_views == None:
        return str(0)
    return nbr_views

def get_topic_likes_nbr(topic_soup):
    """
    Get the topic's nbr of likes
    """ 
    likes = topic_soup.find('li', class_="secondary likes")
    nbr_likes = likes.find('span', class_='number').text
    if nbr_likes == None:
        return str(0)
    return nbr_likes