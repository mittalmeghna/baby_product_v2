from flask import Flask, render_template, request, url_for, flash, redirect
import pickle
import sklearn
import pandas as pd
import math

app = Flask(__name__)
rating_file = open('data/df_rating.pickle', 'rb')
review_file = open('data/df_sorted_comments.pickle', 'rb')
df_review = pickle.load(review_file, encoding='latin1')
df_rating = pickle.load(rating_file, encoding='latin1') 
df_product_id_name = pd.read_csv("data/product_id_product_name_mapping.csv",index_col=False) 

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])

def home():
    product_id = ''
    product_name = ''
    # dictionary mapping topic to its compound for a given product_id 
    topic_sentiment = {}
    # dict mapping topic to its top positive review 
    positive_reviews = {}
    # dict mapping topic to its top negative review 
    negative_reviews = {}
    rating = ""
    topic_list = ['car fit','child fit','comfort','ease of install','ease of use','easy to clean', 
                  'ease of use','material','price','safety','shipping','travel']

    if request.method == 'POST':
        product_id = request.form.get('productId')
        product_row = df_rating.loc[df_rating['product_id'] == product_id].reset_index()
        if len(product_row) == 0: 
            product_name = "not found"
        else: 
            product_name = df_product_id_name[df_product_id_name['product_id'].str.match(product_id)]["product_name"].tolist()[0]
       
        if len(product_row) > 0: 
            for topic in topic_list: 
                # dict keys are with underscore, while topic names are without underscore
                clean_topic = topic.replace(" ","_")
                # lookup compound score for topic 
                rating = float(product_row.iloc[0][topic])
                # if rating is not available, then use empty string, otherwise map to 1-5 
                if math.isnan(rating): 
                    topic_sentiment[clean_topic] = ""
                else: 
                    topic_sentiment[clean_topic] = round(((rating + 1) * 2) + 1,1)
    
        # lookup reviews for each topic 
        review_rows = df_review.loc[df_review['product_id'] == product_id]
        print(review_rows) 

        for topic in topic_list:  
            clean_topic = topic.replace(" ","_")
            try:
                top_sentence = review_rows[review_rows["topic_tags4"] == topic].iloc[0]['review_body']
                top_sentiment = review_rows[review_rows["topic_tags4"] == topic].iloc[0]['sentiment'] 
                if top_sentiment == 'Positive': 
                    positive_reviews[clean_topic] = top_sentence  
                bottom_sentence = review_rows[review_rows["topic_tags4"] == topic].iloc[-1]['review_body']
                bottom_sentiment = review_rows[review_rows["topic_tags4"] == topic].iloc[-1]['sentiment'] 
                if bottom_sentiment == 'Negative': 
                    negative_reviews[clean_topic] = bottom_sentence 
            except: 
                print("caught exception")
    # pass all model value to the HTML page 
    return render_template("home.html", product_id=product_id,product_name=product_name,topic_sentiment=topic_sentiment, positive_reviews=positive_reviews,negative_reviews=negative_reviews)

if __name__ == '__main__':
    app.run(debug=True)
