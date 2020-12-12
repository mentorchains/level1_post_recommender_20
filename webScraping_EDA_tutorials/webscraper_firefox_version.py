from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import requests
import time
from datetime import datetime
import os
import pandas as pd
import json

class WebScraper:
    browser = None # Selenium webriver object
    topic_dict = {} # Dictionary of all topics and their attributes
    topic_df = pd.DataFrame(columns=[
        'Topic Title',
        'Category',
        'Tags',
        'Leading Post',
        'Post Replies',
        'Created_at',
        'Likes',
        'Views',
        'Replies',
    ])
    
    def __init__(self, webdriverPath):
        # Set up the webdriver
        opts = Options()
        opts.set_headless()
        assert opts.headless # Operating in headless mode
        self.browser = Firefox(options=opts, executable_path=webdriverPath)
        
    def get_topic_title_details(self, topic_soup):
        """
        Get topic title, category and tags
        """
        topic_title = topic_soup.find('a', class_='fancy-title').text.strip()

        title_wraper = topic_soup.find('div', class_='title-wrapper')

        topic_tags = title_wraper.find_all('span', class_='category-name')
        topic_tags = [tag.text for tag in topic_tags]
        
        try: 
            topic_category = topic_tags[0]
        
            if len(topic_tags) == 1:
                topic_tags = []
            else:
                topic_tags = topic_tags[1:]
        except:
            topic_category = ''
            topic_tags = ''
            
        return topic_title, topic_category, topic_tags
        
    def get_topic_comments(self, topic_soup):
        """
        Get topic leading post and its replies.
        """
        postStream = topic_soup.find('div', class_='post-stream')
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
    
    def get_topic_created_at(self, topic_soup):
        """
        Get the topic creation date
        """
        created = topic_soup.find('li', class_="created-at")
        
        if created is None:
            created_at = str(0)
        else:
            created_at = created.find('span', class_='relative-date')['title']
    
        return created_at

    def get_topic_replies_nbr(self, topic_soup):
        """
        Get the topic's nbr of replies
        """    
        replies = topic_soup.find('li', class_="replies")
        
        if replies == None:
            nbr_replies = str(0)
        else:
            nbr_replies = replies.find('span', class_='number').text
        
        return nbr_replies

    def get_topic_views_nbr(self, topic_soup):
        """
        Get the topic's nbr of views
        """ 
        views = topic_soup.find('li', class_="secondary views")
        
        if views is None:
            nbr_views = str(0)
        else:
            nbr_views = views.find('span', class_='number').text
        
        return nbr_views

    def get_topic_likes_nbr(self, topic_soup):
        """
        Get the topic's nbr of likes
        """ 
        likes = topic_soup.find('li', class_="secondary likes")
        
        if likes is None:
            nbr_likes = str(0)
        else:
            nbr_likes = likes.find('span', class_='number').text
        
        return nbr_likes
    
    def runApp(self, BASE_URL, SITE_NAME):
        """
        Run the scraping process
        """
        # Open Firefox web client using Selenium and retrieve page source
        self.browser.get(BASE_URL)
        
        # Get all the categories link 
        categ_links = self.browser.find_elements_by_css_selector('.category > h3 > a')
        categ_urls = []
        for link in categ_links:
            categ_urls.append(link.get_attribute('href'))
        
        # Go over each category url
        for categ_url in categ_urls:
            # Access category webpage
            self.browser.get(categ_url)
            
            # Load the entire webage by scrolling to the bottom
            lastHeight = self.browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            
            while (True):
                # Scroll to bottom of page
                self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                # Wait for new page segment to load
                time.sleep(0.5)

                # Calculate new scroll height and compare with last scroll height
                newHeight = self.browser.execute_script("return document.body.scrollHeight")
                if newHeight == lastHeight:
                    break
                    
                lastHeight = newHeight
            
            # Generate category soup
            categoryHTML = self.browser.page_source
            categ_topic_soup = BeautifulSoup(categoryHTML, 'html.parser')
    
            categ_topic_links = categ_topic_soup.find_all('a', class_='title raw-link raw-topic-link')
    
            # Get all the topic urls inside the current category
            categ_topic_urls = []
            for topic_link in categ_topic_links:
                categ_topic_urls.append(BASE_URL + topic_link['href'])
            
            # Loop through all the topics in the current category
            for categ_topic_url in categ_topic_urls:
                # Get current topic_soup
                self.browser.get(categ_topic_url)
                topicHTML = self.browser.page_source
                topic_soup = BeautifulSoup(topicHTML, 'html.parser')
                
                # Scrape all topic attributes of interest
                topic_title, topic_category, topic_tags = self.get_topic_title_details(topic_soup)
                leading_comment, other_comments = self.get_topic_comments(topic_soup)
                created_at = self.get_topic_created_at(topic_soup)
                nbr_replies = self.get_topic_replies_nbr(topic_soup)
                nbr_views = self.get_topic_views_nbr(topic_soup)
                nbr_likes = self.get_topic_likes_nbr(topic_soup)
                
                # Attribute dictionary for each topic in a category
                attribute_dict = {
                            'Topic Title': topic_title,
                            'Category': topic_category,
                            'Tags': topic_tags,
                            'Leading Post': leading_comment,
                            'Post Replies': other_comments,
                            'Created_at': created_at,
                            'Likes': nbr_likes,
                            'Views': nbr_views,
                            'Replies': nbr_replies}
                
                self.topic_dict[topic_title] = attribute_dict
                self.topic_df = self.topic_df.append(attribute_dict, ignore_index=True)
                
                # TEST
                print('Title :', topic_title)
                
        # Get unique timestamp of the webscraping
        timeStamp = datetime.now().strftime('%Y%m%d%H%M%S')
        
        # Save data in JSON and CSV files and store in the save folder as this program
        jsonFilename = SITE_NAME + '_SCRAPED_DATA' + timeStamp + '.json'
        csvFilename = SITE_NAME + '_SCRAPED_DATA' + timeStamp + '.csv'
        
        jsonFileFullPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), jsonFilename)
        csvFileFullPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), csvFilename)
        
        # Save scraped data  into json file
        with open(jsonFileFullPath, 'w') as f:
            json.dump(self.topic_dict, f)
        
        # Save dataframe into csv file
        self.topic_df.to_csv(csvFileFullPath)
        
if __name__=='__main__':
    # Local path to webdriver
    webdriverPath = r'/usr/local/bin/geckodriver'
    
    # Forum to scrape URL    
    BASE_URL = 'https://forum.flowster.app'
    
    # Name of the forum
    SITE_NAME = 'FLOWSTER'
        
    # WebScraping object
    webScraper = WebScraper(webdriverPath)
    
    # Run the webscraper and save scraped data
    webScraper.runApp(BASE_URL, SITE_NAME)
        