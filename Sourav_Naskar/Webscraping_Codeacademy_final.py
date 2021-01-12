from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import time
from datetime import datetime
import os
import pandas as pd


class CodeacademyWebscraper:
    driver = None                   # Selenium webdriver object
    topicDict = {}                  # Dictionary of all topics and their attributes
    topicDataframe = \
        pd.DataFrame(columns=[      # Pandas dataframe of all topic attributes
        'Topic Title', 
        'Category', 
        'Tags', 
        'Leading Comment', 
        'Other Comments',
        'Likes',
        'Views'])


    def __init__(self, webdriverPath):
        # Set up webdriver
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')     # Ignore security certificates
        options.add_argument('--incognito')                     # Use Chrome in Incognito mode
        options.add_argument('--headless')                      # Run in background
        self.driver = webdriver.Chrome( \
            executable_path = webdriverPath, \
            options = options)

    def get_title(self, topicSoup):
        topicName = topicSoup.find('a', class_='fancy-title').text

        # Remove leading and trailing spaces and newlines
        topicName = topicName.replace('\n', '').strip()
        return topicName

    def get_category_and_tags(self, topicSoup):    
        topicCategoryDiv = topicSoup.find('div', class_='topic-category ember-view')
        tagAnchors = topicCategoryDiv.find_all('span', class_='category-name')

        tagList = []
        for anchor in tagAnchors:
            tagList.append(anchor.text)
        
        if (len(tagList) == 1):
            category = tagList[0]
            tags = []
            return category, tags
        else:
            category = tagList[0]
            tags = tagList[1:]
            return category, tags

    
    def get_comments(self, topicSoup):
        # Get all the posts HTML
        comment = topicSoup.find_all('div', class_='cooked')
        comments = []
        temp = ''
        for ele in comment:
            temp += ele.get_text()
            comments.append(temp)
        try:
            leading_comment = comments[0]
            if len(comments) == 1:
                other_comments = []
            else:
                other_comments = comments[1:]
        except:
            leading_comment, other_comments = [], []

        return leading_comment, other_comments


    def get_views(self, topicSoup):
        views = topicSoup.find('li', class_='secondary views')
        if views == None:
            return str(0)
        return views.span.text
        

    def get_likes(self, topicSoup):
        likes = topicSoup.find('li', class_='secondary likes')
        if likes == None:
            return str(0)
        return likes.span.text
    

    def runApplication(self, baseURL):
        # Open Chrome web client using Selenium and retrieve page source
        self.driver.get(baseURL)
        # Get all the categories link 
        categ_links = self.driver.find_elements_by_css_selector('.category > h3 > a')
        categ_urls = []
        for link in categ_links:
            categ_urls.append(link.get_attribute('href'))
        
        # Go over each category url
        for categ_url in categ_urls:
            # Access category webpage
            self.driver.get(categ_url)
            
            # Load the entire webage by scrolling to the bottom
            lastHeight = self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            while (True):
                # Scroll to bottom of page
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                # Wait for new page segment to load
                time.sleep(0.5)

                # Calculate new scroll height and compare with last scroll height
                newHeight = self.driver.execute_script("return document.body.scrollHeight")
                if newHeight == lastHeight:
                    break
                lastHeight = newHeight

            # Generate category soup object
            categoryHTML = self.driver.page_source
            categorySoup = BeautifulSoup(categoryHTML, 'html.parser')

            # Find all anchor objects that contain topic information
            topicAnchors = categorySoup.find_all('a', class_='title raw-link raw-topic-link')

            # Get hyperlink references and append it to the base URL to get the topic page URLs
            topicPageURLs = []
            for i in range(len(topicAnchors)):
                href = topicAnchors[i]['href']
                topicPageURLs.append(baseURL + href)


            # 2nd for loop to loop through all topics in a category
            for topicURL in topicPageURLs:
                # Get topic HTML text and generate topic soup object
                self.driver.get(topicURL)
                topicHTML = self.driver.page_source
                topicSoup = BeautifulSoup(topicHTML, 'html.parser')

                # Scape all topic attributes of interest
                topicTitle = self.get_title(topicSoup)
                category, tags = self.get_category_and_tags(topicSoup)
                
                leadingComment, otherComments = self.get_comments(topicSoup)
                numLikes = self.get_likes(topicSoup)
                numViews = self.get_views(topicSoup)

                # Create attribute dictionary for topic
                attributeDict = {
                    'Topic Title'       :   topicTitle,
                    'Category'          :   category,
                    'Tags'              :   tags,
                    'Leading Comment'   :   leadingComment,
                    'Other Comments'    :   otherComments,
                    'Likes'             :   numLikes,
                    'Views'             :   numViews}
                
                # Add the new entry to the topic dictionary and Pandas dataframe
                self.topicDict[topicTitle] = attributeDict
                self.topicDataframe = self.topicDataframe.append(attributeDict, ignore_index=True)

                
                print('Topic Title:')
                print(topicTitle)
                print('Category:')
                print(category)
                print('Tags:')
                print(tags)
                
                print('Leading Comment:')
                print(leadingComment)
                
                print('Other Comments:')
                print(otherComments)
                print('Likes:')
                print(numLikes)
                print('Views:')
                print(numViews)
                
        
        # Get unique timestamp of the webscraping
        timeStamp = datetime.now().strftime('%Y%m%d%H%M%S')

        # Save data in CSV file and store in the save folder as this program
        
        csvFilename = 'Codeacademy_Webscrapper_' + timeStamp + '.csv'

        
        csvFileFullPath = os.path.join(os.path.dirname(os.path.abspath("__file__")), csvFilename)

       

        self.topicDataframe.to_csv(csvFileFullPath)



if __name__=='__main__':
    # Local path to webdriver
    webdriverPath = 'C:\Program Files (x86)\chromedriver.exe'

    # Codeacademy forum base URL
    baseURL = 'https://discuss.codecademy.com/'
    

    # Create Codeacademy forum webscraping object
    codeacademyWebscraper = CodeacademyWebscraper(webdriverPath)

    # Run webscraping and save data
    codeacademyWebscraper.runApplication(baseURL)