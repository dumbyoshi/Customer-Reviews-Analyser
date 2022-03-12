import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv(r"C:\Users\nithi\OneDrive\Documents\Sentiment Analysis NLP\scrappedReviews.csv" , low_memory=(False))
df.Sentiment
review_value = df.Sentiment
len(df.Sentiment)

Negative = 0
for i in range(len(review_value)):
    print("Trying_Index",i)
    if review_value[i] == '0':
        Negative = Negative + 1
        print("Negative- ",Negative)
        

Positive = len(review_value) - Negative

Positive
Negative

x = list()
x.append(Positive)
x.append(Negative)
y = list()
y.append('Positive_Outcome') 
y.append('Negative_Outcome')

print(x)
print(y)

plt.pie(x,labels=y,autopct='%.2f%%')

       
        