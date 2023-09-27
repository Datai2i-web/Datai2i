from flask import Flask ,request, render_template 
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from gridfs import GridFS
import os
from werkzeug.utils import secure_filename

# uri = "mongodb+srv://chandrakarthik42:Karthik421@cluster0.rtwqhrx.mongodb.net/?retryWrites=true&w=majority"
uri = "mongodb+srv://datai2i-admin:EGwhDoTMIFAHqwoX@datai2i.efqtgwz.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

db=client.data.Products


app = Flask(__name__)

@app.route('/')
def index():
    data = list(db.find({}))
    return render_template('index.html',data=data)

@app.route('/render')
def render():
    data = list(db.find({}))
    for i in data:
        print(i)
    return render_template('render.html',data=data)

# Define a route for the form page
@app.route('/upload_data', methods=['GET'])
def show_form():
    return render_template('form.html')  # Replace 'your_template.html' with the actual template name

def save_uploaded_file(file, upload_folder):
    filename = secure_filename(file.filename)
    file_path = os.path.join(upload_folder, filename)
    file.save(file_path)
    return file_path

# Define a route for handling form submission
@app.route('/upload', methods=['POST'])
def upload_post():
    # Access form data using request.form
    title = request.form['title']
    sub_title = request.form['sub_title']
    product_desc = request.form['product_desc']
    
    # Access uploaded file using request.files
    product_logo = request.files['product_logo']
    print(product_logo)
    
    # Save the product logo file
    upload_folder = './media/'
    product_logo_filename = save_uploaded_file(product_logo, upload_folder)
    
    # Initialize lists to store features and product_features data
    features = []
    product_features = []
    print(request.form)
    feature_counter = 1
    while True:
        feature_text = request.form.get(f'features[feature_{feature_counter}][text]')
        feature_image = request.files.get(f'features[feature_{feature_counter}][image]')

        if not feature_text:
            break

        # Create a dictionary to store feature data
        feature_data = {'text': feature_text}

        if feature_image:
            # Handle the feature image and description here
            feature_image_filename = save_uploaded_file(feature_image, upload_folder)
            feature_data['image'] = feature_image_filename

        features.append(feature_data)
        feature_counter += 1

    # Process the form data for product features
    product_feature_counter = 1
    while True:
        product_feature_text = request.form.get(f'product_features[feature_{product_feature_counter}][text]')
        product_feature_image = request.files.get(f'product_features[feature_{product_feature_counter}][image]')

        if not product_feature_text:
            break

        # Create a dictionary to store product feature data
        product_feature_data = {'text': product_feature_text}

        if product_feature_image:
            # Handle the product feature image and description here
            product_feature_image_filename = save_uploaded_file(product_feature_image, upload_folder)
            product_feature_data['image'] = product_feature_image_filename

        product_features.append(product_feature_data)
        product_feature_counter += 1



    # Process the form data for product features


    # Create a document to insert into MongoDB
    product_data = {
        'title': title,
        'sub_title': sub_title,
        'product_desc': product_desc,
        'product_logo': product_logo_filename,
        'features': features,
        'product_features': product_features
    }
    print(product_data)
    # Insert the document into the MongoDB collection
    db.insert_one(product_data)

    # Redirect or render a response (you can customize this)
    return "Product uploaded successfully!"

if __name__ == '__main__':
    app.run(debug=True)

