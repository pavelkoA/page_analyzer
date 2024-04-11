import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, render_template, request

from page_analyzer.validator import get_url, is_url


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL)


app = Flask(__name__)


@app.route("/")
def get_index():
    return render_template('index.html')


@app.post("/urls")
def create_url():
    site = request.form.get("url")
    if is_url(site): 
        return f'<h1>{get_url(site)}</h1>'
    return '<h1>AAAAAAAAAAAAA</h1>'