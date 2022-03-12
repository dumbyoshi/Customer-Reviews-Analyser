# Sentiment-Analysis-NLP-project
This a intermediate ML project using Regression algorithm which detect whether the reviews are positive or negative
This Repo is based on Machine Learning and Deep Learning , It is a NLP project.
This Project is used to analyze the customer's reviews of different products from a E-commerce Website 
called Etsy whether it is a Positive or Negative review.
------------------------------------------------------------------------------------------------------------------
So the first step is to collect a json file from the amazon website which contains numerous number of reviews which can be used to train,
the model .
The Model used here is Logistic Regression which is a machine learning algorithm ,after trained it is converted to a pickle file which used 
in creating the GUI.
Now the web scraping part in which etsy_scrap_final code scraps the customer reviews, names,ratings which is used in testing part.
This project GUI part has a Pie Chart and a word cloud in which it displays the maximum words used in the reviews , next a dropdown box which has
100 review which we have been scraped.There is a space to type our own Reviews and check it whether it is positive or negative,this is identified 
by training the model previously
The JSON file is not attached due to the size limit.
