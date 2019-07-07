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
    selected_feature = ""
    top_review_1 = ""
    top_review_2 = ""
    bottom_review_1 = ""
    bottom_review_2 = ""
    product_img=""
    topic_rating = ""

    topic_list = ['car fit','child fit','comfort','ease of install','ease of use','easy to clean', 
                  'ease of use','material','price','safety','shipping','travel']

    if request.method == 'POST':
        product_id = request.form.get('productId')
        selected_feature = request.form.get('selectFeature').replace(' ','_') 
        print(selected_feature) 
        product_row = df_rating.loc[df_rating['product_id'] == product_id].reset_index()
        if len(product_row) == 0: 
            product_name = "not found"
            return render_template("notfound.html",product_id=product_id)
        else: 
            product_name = df_product_id_name[df_product_id_name['product_id'].str.match(product_id)]["product_name"].tolist()[0]
      
        product_img = 'britax' 
        if 'graco' in product_name: 
            product_img = 'graco'
        if 'britax' in product_name: 
            product_img = 'britax'
        if 'diono' in product_name: 
            product_img = 'diono'
        if 'safety' in product_name: 
            product_img = 'safety'
        if 'cosco' in product_name: 
            product_img = 'cosco' 
        if 'evenflo' in product_name: 
            product_img = 'evenflo'
        if 'disney' in product_name: 
            product_img = 'disney'
        if 'chicco' in product_name: 
            product_img = 'chicco'
       
        topic = selected_feature.replace("_"," ")
        if len(product_row) > 0 and topic in product_row: 
                # lookup compound score for topic 
                rating = float(product_row.iloc[0][topic])
                # if rating is not available, then use empty string, otherwise map to 1-5 
                if math.isnan(rating): 
                    topic_rating  = ""
                else: 
                    topic_rating  = round(((rating + 1) * 2) + 1,1)

        if topic not in product_row: 
            return render_template("topicnotfound.html", topic=topic)
        if topic_rating == "": 
            return render_template("notfound.html", product_id=product_id, selected_feature=selected_feature) 
   
        # convert star rating number
        if topic_rating >= 0 and topic_rating <= 1: 
            star_rating = "onestar"
        if topic_rating > 1.0 and topic_rating <= 2: 
            star_rating = "twostar" 
        if topic_rating > 2 and topic_rating <= 2.5: 
            star_rating = "twohalfstar" 
        if topic_rating > 2.5 and topic_rating <= 3.0: 
            star_rating = "threestar" 
        if topic_rating > 3.0 and topic_rating <= 3.5: 
            star_rating = "threehalfstar" 
        if topic_rating > 3.5 and topic_rating <= 4.0: 
            star_rating = "fourstar" 
        if topic_rating > 4.0: 
            star_rating = "fivestar"

        # lookup reviews for each topic 
        review_rows = df_review.loc[df_review['product_id'] == product_id]
        print(review_rows) 
        topic=selected_feature.replace('_',' ') 
        
        try: 
            top_review_1 = review_rows[review_rows["topic_tags4"] == topic].iloc[0]['review_body']
            top_review_2 = review_rows[review_rows["topic_tags4"] == topic].iloc[1]['review_body']
            bottom_review_1 = review_rows[review_rows["topic_tags4"] == topic].iloc[-1]['review_body']
            bottom_review_2 = review_rows[review_rows["topic_tags4"] == topic].iloc[-2]['review_body']
        except: 
            print("exception") 

        import re 
        top_review_1 = re.sub(r'\bbr\b', ',', top_review_1)
        top_review_2 = re.sub(r'\bbr\b', ',', top_review_2)
        bottom_review_1 = re.sub(r'\bbr\b', ',', bottom_review_1)
        bottom_review_2 = re.sub(r'\bbr\b', ',', bottom_review_2)
        print(top_review_1) 
        print(bottom_review_1)
        print(product_img)
       #  for topic in topic_list:  
       #      clean_topic = topic.replace(" ","_")
       #      try:
       #          top_sentence = review_rows[review_rows["topic_tags4"] == topic].iloc[0]['review_body']
       #          top_sentiment = review_rows[review_rows["topic_tags4"] == topic].iloc[0]['sentiment'] 
       #          if top_sentiment == 'Positive': 
       #              positive_reviews[clean_topic] = top_sentence  
       #          bottom_sentence = review_rows[review_rows["topic_tags4"] == topic].iloc[-1]['review_body']
       #          bottom_sentiment = review_rows[review_rows["topic_tags4"] == topic].iloc[-1]['sentiment'] 
       #          if bottom_sentiment == 'Negative': 
       #              negative_reviews[clean_topic] = bottom_sentence 
       #      except: 
       #          print("caught exception")
        return render_template("output.html", product_id=product_id,
                                              product_name=product_name,
                                              product_img=product_img,
                                              selected_feature=selected_feature.replace('_', ' '),
                                              topic_sentiment=topic_rating,
                                              star_rating=star_rating,
                                              top_review_1=top_review_1,
                                              bottom_review_1=bottom_review_1,
                                              top_review_2=top_review_2,
                                              bottom_review_2=bottom_review_2) 

    # pass all model value to the HTML page 
    else: 
        return render_template("home.html", product_id=product_id,product_name=product_name)

if __name__ == '__main__':
    app.run(debug=True)
