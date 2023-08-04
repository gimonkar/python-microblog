from flask import Flask,render_template,request
import datetime
from pymongo import MongoClient
import certifi
import os
from dotenv import load_dotenv
load_dotenv()
def create_app():

    app = Flask(__name__)
    # con_string="mongodb+srv://root1:root1@microblog-app.zzn5eva.mongodb.net/"
    # , tlsCAFile=certifi.where()
    client = MongoClient(os.getenv("MONGODB_URI"), tlsCAFile=certifi.where())
    app.db = client.microblog

    @app.route('/',methods=['GET','POST'])
    def home():
        if request.method=="POST":
            formated_date=datetime.datetime.today().strftime("%Y-%m-%d")
            entry_content= request.form.get("content")
            app.db.oneentry.insert_one({"content":entry_content,"date":formated_date})
        entries_with_date = [
            (entry["content"],
            entry["date"],
            datetime.datetime.strptime(entry["date"],"%Y-%m-%d").strftime("%b %d")
            )
            for entry in app.db.oneentry.find( {} )
        ]

        return render_template("index.html",entries=entries_with_date)
    return app


create_app()