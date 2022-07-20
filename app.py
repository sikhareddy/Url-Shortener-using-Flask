import os 
import string
from flask import Flask, render_template, request,redirect,abort
import random
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import column_property
from datetime import datetime 



app= Flask(__name__)

application_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(application_dir,'db1.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

data ={}



table= SQLAlchemy(app)

@app.route('/')

def home_get():
    return render_template('index1.html')

class link(table.Model):
    __tablename__ = 'link'
    id= table.Column(table.Integer, primary_key=True)
    original_url = table.Column(table.String(500))
    shorten_url= table.Column(table.String(5), unique=True)
    date= table.Column(table.DateTime,default=datetime.now)
   
    def __init__(self,shorten_url,original_url):
        self.shorten_url = shorten_url
        self.original_url = original_url
    
    def __repr__(self):
        return '{} => {}'.format(self.original_url,self.shorten_url)

@app.route('/', methods=['POST'])
def home_post():
    
    original_url = request.form.get('in_1')
    if 'http' not in original_url:
      original_url = f'http://{original_url}'
    if original_url is None:
     return "<h2 style='color:red'> Invalid URL </h2>"
    shorten_url = random.randint(1000, 9999)
    data[shorten_url] = original_url
    DATA = link(shorten_url,original_url)
    table.session.add(DATA)
    table.session.commit()
    return render_template('index1.html', short=shorten_url) 

    


@app.route('/history')

def history_get():
    DATA = link.query.all()
    return render_template('history1.html', DATA=DATA)

   

@app.route('/<shorten_url>')
def redirect_to_url(shorten_url):
    Link = link.query.filter_by(shorten_url=shorten_url).first_or_404()

    Link.id = Link.id + 1
    table.session.commit()

    return redirect(Link.original_url) 



if __name__ == "__main__":
    table.create_all()
    app.run(debug=True)