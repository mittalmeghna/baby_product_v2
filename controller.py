# kiankai
from flask import Flask, render_template, request, url_for, flash, redirect
import pickle
import sklearn
import pandas

app = Flask(__name__)
score_file = open('data/model_scores.pickle', 'rb')
review_file = open('data/model_reviews.pickle', 'rb')
df_scores = pickle.load(score_file, encoding='latin1')
df_review = pickle.load(review_file, encoding='latin1')

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    product_id = ''
    product_name = ''
    topic_sentiment = {} 
    positive_reviews = {}
    negative_reviews = {}
    
    if request.method == 'POST':
        positive_reviews = {}
        product_id = request.form.get('productId')
        score_row = df_scores.loc[df_scores['product_id'] == product_id]
        if len(score_row) == 0: 
            product_name = "not found"
        else: 
            product_name = score_row['product_title'].tolist()[0]  

        for topic in score_row["topic_tags"].tolist(): 
            clean_topic = topic.replace(" ","_")
            topic_sentiment[clean_topic] = score_row.loc[df_scores["topic_tags"] == topic,"sentiment"].tolist()[0]

        review_rows = df_review.loc[df_review['product_id'] == product_id]

        for topic in score_row["topic_tags"].tolist(): 
            clean_topic = topic.replace(" ","_")
            try: 
                positive_reviews[clean_topic] = review_rows[review_rows["topic_tags"] == topic].loc[review_rows["sentiment"] == 1, "review_body"][0]
                negative_reviews[clean_topic] = review_rows[review_rows["topic_tags"] == topic].loc[review_rows["sentiment"] == 0, "review_body"].tolist()[0]
            except: 
                print("caught exception")
    return render_template("home.html", product_id=product_id,product_name=product_name,topic_sentiment=topic_sentiment, positive_reviews=positive_reviews,negative_reviews=negative_reviews)

if __name__ == '__main__':
    app.run(debug=True)
