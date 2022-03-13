# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 12:25:47 2022

@author: nithi
"""

#Importing Necessary Libraries
import pickle
from re import S
import time
import logging
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import pandas as pd
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from selenium.webdriver.common.by import By
from tqdm import tqdm
import requests
import os

start_time = time.time()
person = []
date = []
stars = []
review = []
sentiment = []

browser = webdriver.Chrome(ChromeDriverManager().install())

#defining export_data funtion to export the data in variables
def export_data():
    if 'scrappedReviews.csv' in os.listdir(os.getcwd()):
        df1 = pd.read_csv('scrappedReviews.csv')
        '''Exporting data'''
        for i in range(0,len(df1["Person"])):
            if df1["Person"][i] not in person:
                person.append(df1["Person"][i])
                date.append(df1["Date"][i])
                stars.append(df1["Stars"][i])
                review.append(df1["Reviews"][i])
                sentiment.append(df1["Sentiment"][i])
        
        dataframe1 = pd.DataFrame()
        dataframe1["Person"] = person
        dataframe1["Date"] = date
        dataframe1["Stars"] = stars
        dataframe1["Reviews"] = review
        dataframe1["Sentiment"] = sentiment
        
        result = pd.concat([df1,dataframe1])
        result.to_csv('scrappedReviews.csv',index=False)
    else:
        '''Exporting data'''
        dataframe1 = pd.DataFrame()
        dataframe1["Person"] = person
        dataframe1["Date"] = date
        dataframe1["Stars"] = stars
        dataframe1["Reviews"] = review
        dataframe1["Sentiment"] = sentiment
        dataframe1.to_csv('scrappedReviews.csv',index=False)


#defining function for Checking the sentiment of any review
def check_review(reviewtext):
    '''
    Check the review is positive or negative'''
    file = open("pickle_model.pkl", 'rb')
    pickle_model = pickle.load(file)
    file_1 = open("feature.pkl", 'rb')
    vocab = pickle.load(file_1)
    #reviewText has to be vectorised, that vectorizer is not saved yet
    #load the vectorize and call transform and then pass that to model preidctor
    #load it later
    transformer = TfidfTransformer()
    loaded_vec = CountVectorizer(decode_error="replace",vocabulary=vocab)
    vectorised_review = transformer.fit_transform(loaded_vec.fit_transform([reviewtext]))
    # Add code to test the sentiment of using both the model
    # 0 == negative   1 == positive
    out = pickle_model.predict(vectorised_review)
    return out[0]


#Defining the Scraper File
def run_scraper(page,browser):
    global person,review
    print("Starting Chrome:")
    global step
    step = pd.DataFrame()
    
for page in range(1, 2):

        URL = f'https://www.etsy.com/in-en/c/jewelry/earrings/ear-jackets-and-climbers?ref=pagination&page={page}'
        
        try:
            #Count for every page of website
            URL = URL.format(page)
            browser.get(URL)
            print("Scraping Page:",page)
            
            
            #xpath of product table
            PATH_1 = "div[data-search-results]"
            
            #getting total items
            items = browser.find_element(By.CSS_SELECTOR, PATH_1)
            items = items.find_elements(By.TAG_NAME, 'li' )
            
            #available items in page
            end_product = len(items)
            
            #Count for every product of the page
            for product in range(0,end_product):
                print("Scarping reviews for product", product +1)
                
                #clicking on product
                try:
                    items[product].find_element(By.TAG_NAME, 'a').click()
                except:
                    print('Product link not found')

                #switch the focus of driver to new tab
                windows = browser.window_handles
                browser.switch_to.window(windows[1])
                
                try:
                   PATH_2 = "div[data-reviews]"
                   count = browser.find_element(By.CSS_SELECTOR, PATH_2)

                   #Number of review on any page
                   count = count.find_elements(By.CLASS_NAME, 'wt-grid__item-xs-12')
                   for r1 in range(1,len(count)+1):
                        dat1 = browser.find_element(By.XPATH ,'//*[@id="reviews"]/div[2]/div[2]/div[1]/div[1]/p'.format(r1)).text
                        if dat1[:dat1.find(',')-6] not in person:
                            try:
                                person.append(dat1[:dat1.find(',')-6])
                                date.append(dat1[dat1.find(',')-6:])
                            except Exception:
                                person.append("Not Found")
                                date.append("Not Found")
                            try:
                                stars.append(browser.find_element(By.XPATH ,
                                    '//*[@id="same-listing-reviews-panel"]/div/div[1]/div[2]/div[1]/div/div[1]'.format(
                                        r1)).text[0])
                            except Exception:
                                stars.append("No stars")
                            try:
                                review.append(browser.find_element(By.XPATH , 
                                    '//*[@id="same-listing-reviews-panel"]/div/div[1]/div[2]/div[1]/div/div[3]/div'.format(r1-1)).text)
                                sentiment.append(check_review(browser.find_element(By.XPATH ,
                                    '//*[@id="same-listing-reviews-panel"]/div/div[1]/div[2]/div[1]/div/div[3]/div'.format(r1-1)).text))
                            except Exception:
                                review.append("No Review")
                                sentiment.append(check_review("No Review"))
                except Exception:
                    try:
                        count = browser.find_element(By.XPATH, '//*[@id="same-listing-reviews-panel"]')
                        count = count.find_elements(By.CLASS_NAME, 'wt-pl-xs-0 wt-mb-xs-2 wt-mb-lg-6')
                        
                        for r2 in range(1,len(count)+1):
                            dat1 = browser.find_element(By.XPATH , 
                                        '//*[@id="reviews"]/div[2]/div[2]/div[1]/div[1]/p'.format(r2)).text
                            if dat1[:dat1.find(',')-6] not in person:
                                try:
                                    
                                    person.append(dat1[:dat1.find(',')-6])
                                    date.append(dat1[dat1.find(',')-6:])
                                except Exception:
                                    person.append("Not Found")
                                    date.append("Not Found")
                                try:
                                    stars.append(browser.find_element(By.XPATH,
                                        '//*[@id="same-listing-reviews-panel"]/div/div[1]/div[2]/div[1]/div/div[1]'.format(
                                            r2)).text[0])
                                except Exception:
                                    stars.append("No Stars")
                                try:
                                    review.append(browser.find_element(By.XPATH,
                                        '//*[@id="same-listing-reviews-panel"]/div/div[1]/div[2]/div[1]/div/div[3]/div'.format(
                                            r2-1)).text)
                                    sentiment.append(check_review(browser.find_element(By.XPATH,
                                        '//*[@id="same-listing-reviews-panel"]/div/div[1]/div[2]/div[1]/div/div[3]/div'.format(r2-1)).text))
                                except Exception:
                                    review.append("No Review")
                                    sentiment.append(check_review(
                                        "No Review"))                                        
                    except Exception:
                        try:
                            count = browser.find_element(By.XPATH, '//*[@id="same-listing-reviews-panel"]')
                            count = count.find_elements(By.CLASS_NAME, 'wt-pl-xs-0 wt-mb-xs-2 wt-mb-lg-6')
                            
                            for r3 in range(1,len(count)+1):
                                dat1 = browser.find_element(By.XPATH , 
                                            '//*[@id="reviews"]/div[2]/div[2]/div[1]/div[1]/p'.format(r3)).text
                                if dat1[:dat1.find(',')-6] not in person:
                                    try:
                                        person.append(dat1[:dat1.find(',')-6])
                                        date.append(dat1[dat1.find(',')-6:])
                                    except Exception:
                                        person.append("Not Found")
                                        date.append("Not Found")
                                    try:
                                        stars.append(browser.find_element(By.XPATH,
                                            '//*[@id="same-listing-reviews-panel"]/div/div[1]/div[2]/div[1]/div/div[1]'.format(r3)).text[0])
                                    except Exception:
                                        stars.append("No Stars")
                                    try:
                                        review.append(browser.find_element(By.XPATH,
                                            '//*[@id="review-preview-toggle-0"]'.format(r3-1)).text)
                                        sentiment.append(check_review(browser.find_element(By.XPATH,
                                            '//*[@id="review-preview-toggle-0"]'.format(r3-1)).text))
                                    except Exception:
                                        review.append("No Review")
                                        sentiment.append(check_review("No Review"))
                        except Exception:
                            print("Error")
                            continue
                    
                browser.close()
                export_data()
                #swtiching focus to main tab
                browser.switch_to.window(windows[0])
        except Exception as e_1:
            print(e_1)
            print("Program stoped:")
            browser.quit()
            
            

#defining the main function
def main():
       logging.basicConfig(filename='solution_etsy.log', level=logging.INFO)
       logging.info('Started')
if 'page.txt' in os.listdir(os.getcwd()):
        with open('page.txt','r') as file1:
            page = int(file1.read())
        for i in range(1, 2):
            run_scraper(i,browser)
else:
        for i in range(1, 2):
            with open('page.txt','w') as file:
                file.write(str(i,browser))
            run_scraper(i)
            
            export_data()
print("--- %s seconds ---" % (time.time() - start_time))
logging.info('Finished')

# Calling the main function 
if __name__ == '__main__':
    main()