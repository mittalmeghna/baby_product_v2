# kiankai
from flask import Flask, render_template, request, url_for, flash, redirect
import pickle
import sklearn
import pandas

app = Flask(__name__)
infile = open('model.pickle', 'rb')
df = pickle.load(infile, encoding='latin1')

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    product_id = ''
    product_name = ''
    safety = 0 
    comfort = 0 
    price = 0 
    ease_of_install = 0 
    review = ''
    if request.method == 'POST':
        product_id = request.form.get('AsinNumber')
        row = df.loc[df['product_id'] == product_id]
        product_name = row['name'].tolist()[0]
        safety = safety + row['safety'].tolist()[0]
        comfort = comfort + row['comfort'].tolist()[0]
        ease_of_install = ease_of_install + row['ease_of_install'].tolist()[0]
    return render_template("home.html", product_id=product_id,safety=safety,comfort=comfort,price=price,ease_of_install=ease_of_install,product_name=product_name)

if __name__ == '__main__':
    app.run(debug=True)
