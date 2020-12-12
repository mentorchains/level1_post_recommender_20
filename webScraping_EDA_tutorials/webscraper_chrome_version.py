'''
@file       FlowsterWebscraper.py
@date       2020/06/09
@brief      Class to scrape attributes of interest from all topics on the Flowster Discourse forum
'''

import time
from datetime import datetime
import os

from bs4 import BeautifulSoup
from selenium import webdriver

import pandas as pd
import json


'''
@brief  Webscraper that scrapes attributes of interest from all topics on the Flowster Discourse forum
'''
class FlowsterWebscraper:
    driver = None                   # Selenium webdriver object
    topicDict = {}                  # Dictionary of all topics and their attributes
    topicDataframe = \
        pd.DataFrame(columns=[      # Pandas dataframe of all topic attributes
        'Topic Title', 
        'Category', 
        'Tags', 
        'Author', 
        'Commenters',
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


    '''
    @brief      Retrieves a topic title
    @param      topicSoup   BeautifulSoup object that contains the topic page HTML
    @return     topicName   Topic name
    '''
    def get_title(self, topicSoup):
        topicName = topicSoup.find('a', class_='fancy-title').text

        # Remove leading and trailing spaces and newlines
        topicName = topicName.replace('\n', '').strip()
        return topicName


    '''
    @brief      Retrieves a topic's category and tags
    @param      topicSoup   BeautifulSoup object that contains the topic page HTML
    @return     category    Category that the topic belongs to
    @return     tags        List of topic tags
    '''
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

    
    '''
    @brief      Retrieves a topic's author and commenters
    @param      topicSoup   BeautifulSoup object that contains the topic page HTML
    @return     author      Author username
    @return     commenters  List of unique commenter usernames
    '''
    def get_author_and_commenters(self, topicSoup):
        names = topicSoup.find_all("div", class_="names trigger-user-card")
        authorList = []
        for name in names:
            author = name.span.a.text
            authorList.append(author)
        
        # Remove redundant names
        authorList = list(set(authorList))

        if (len(authorList) == 1):
            author = authorList[0]
            commenters = []
            return author, commenters
        else:
            author = authorList[0]
            commenters = authorList[1:]
            return author, commenters


    '''
    @brief      Retrieves a topic's comments
    @param      topicSoup       BeautifulSoup object that contains the topic page HTML
    @return     leadingComment  Leading comment (by the author)
    @return     otherComments   List of other comments
    '''
    def get_comments(self, topicSoup):
        postStream = topicSoup.find('div', class_='post-stream')
        postDivs = postStream.find_all('div', \
            {'class':['topic-post clearfix regular','topic-post clearfix topic-owner regular']})

        comments = []
        for i in range(len(postDivs)):
            comment = postDivs[i].find('div', class_='cooked').text
            comments.append(comment)
        
        if (len(comments) == 1):
            leadingComment = comments[0]
            otherComments = []
            return leadingComment, otherComments
        else:
            leadingComment = comments[0]
            otherComments = comments[1:]
            return leadingComment, otherComments


    '''
    @brief      Retrieves a topic's number of views
    @param      topicSoup           BeautifulSoup object that contains the topic page HTML
    @return     views.span.text     Number of views as a string
    '''
    def get_views(self, topicSoup):
        views = topicSoup.find('li', class_='secondary views')
        if views == None:
            return str(0)
        return views.span.text
        

    '''
    @brief      Retrieves a topic's number of likes
    @param      topicSoup           BeautifulSoup object that contains the topic page HTML
    @return     likes.span.text     Number of likes as a string
    '''
    def get_likes(self, topicSoup):
        likes = topicSoup.find('li', class_='secondary likes')
        if likes == None:
            return str(0)
        return likes.span.text
    

    '''
    @brief      Runs the webscraper application and saves the data in both JSON and CSV files
    @param      baseURL     Link to the Flowster forum home page
    @return     None
    '''
    def runApplication(self, baseURL):
        # Open Chrome web client using Selenium and retrieve page source
        self.driver.get(baseURL)
        baseHTML = self.driver.page_source

        # Get base HTML text and generate soup object
        baseSoup = BeautifulSoup(baseHTML, 'html.parser')

        # Find all anchor objects that contain category information
        categoryAnchors = baseSoup.find_all('a', class_='category-title-link')

        # Get hyperlink references and append it to the base URL to get the category page URLs
        categoryPageURLs = []
        for i in range(len(categoryAnchors)):
            href = categoryAnchors[i]['href']
            categoryPageURLs.append(baseURL + href)

        # 1st for loop to loop through all categories
        for categoryURL in categoryPageURLs:
            # Access category webpage
            self.driver.get(categoryURL)

            # Load the entire webage by scrolling to the bottom
            lastHeight = self.driver.execute_script("return document.body.scrollHeight")
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
                author, commenters = self.get_author_and_commenters(topicSoup)
                leadingComment, otherComments = self.get_comments(topicSoup)
                numLikes = self.get_likes(topicSoup)
                numViews = self.get_views(topicSoup)

                # Create attribute dictionary for topic
                attributeDict = {
                    'Topic Title'       :   topicTitle,
                    'Category'          :   category,
                    'Tags'              :   tags,
                    'Author'            :   author,
                    'Commenters'        :   commenters,
                    'Leading Comment'   :   leadingComment,
                    'Other Comments'    :   otherComments,
                    'Likes'             :   numLikes,
                    'Views'             :   numViews}
                
                # Add the new entry to the topic dictionary and Pandas dataframe
                self.topicDict[topicTitle] = attributeDict
                self.topicDataframe = self.topicDataframe.append(attributeDict, ignore_index=True)

                '''
                print('Topic Title:')
                print(topicTitle)

                print('Category:')
                print(category)

                print('Tags:')
                print(tags)

                print('Author:')
                print(author)

                print('Commenters:')
                print(commenters)

                print('Leading Comment:')
                print(leadingComment)
                
                print('Other Comments:')
                print(otherComments)

                print('Likes:')
                print(numLikes)

                print('Views:')
                print(numViews)
                '''
        
        # Get unique timestamp of the webscraping
        timeStamp = datetime.now().strftime('%Y%m%d%H%M%S')

        # Save data in JSON and CSV files and store in the save folder as this program
        jsonFilename = 'Flowster_Topic_Attributes_' + timeStamp + '.json'
        csvFilename = 'Flowster_Topic_Attributes_' + timeStamp + '.csv'

        jsonFileFullPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), jsonFilename)
        csvFileFullPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), csvFilename)

        with open(jsonFileFullPath, 'w') as f:
            json.dump(self.topicDict, f)

        self.topicDataframe.to_csv(csvFileFullPath)



if __name__=='__main__':
    # Local path to webdriver
    webdriverPath = r'C:\Users\kevin\Desktop\chromedriver_win32\chromedriver.exe'

    # Flowster forum base URL
    baseURL = 'https://forum.flowster.app'
    baseURL = 'https://sellercentral.amazon.com/forums/'

    # Create FLowster webscraping object
    flowsterWebscraper = FlowsterWebscraper(webdriverPath)

    # Run webscraping and save data
    flowsterWebscraper.runApplication(baseURL)


    
    
    
