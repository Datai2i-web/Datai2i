from flask import Flask , render_template 
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


uri = "mongodb+srv://datai2i-admin:EGwhDoTMIFAHqwoX@datai2i.efqtgwz.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri, server_api=ServerApi('1'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', data = db)


if __name__ == "__main__":
    app.run( debug = True )