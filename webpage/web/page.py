from flask import Flask, jsonify, render_template, request
from pymongo import MongoClient
from bson import json_util

app = Flask(__name__)

# MongoDB connection URI
uri = "mongodb+srv://kacper:test@baza1.flvotty.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri)

# MongoDB database and collection
db = client.products
products_collection = db.ecommerce

@app.route('/products', methods=['GET'])
def get_products():
    query_params = request.args.to_dict()

    query = {}

    if 'name' in query_params:
        query['name'] = {"$regex": query_params['name'], "$options": "i"}

    sort_field = query_params.get('sort', None)
    if sort_field:
        sort_order = int(query_params.get('order', 1))  
        sort_criteria = [(sort_field, sort_order)]
    else:
        sort_criteria = None

    products = list(products_collection.find(query, sort=sort_criteria))

    return render_template('products.html', products=products, query_params=query_params)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
