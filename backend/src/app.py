from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from flask_cors import CORS

from bson import ObjectId

# Instantiation
app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb+srv://Aruanova1:Aruanova1337@pythonreact.vxvz6kz.mongodb.net/pythonreact?retryWrites=true&w=majority'
mongo = PyMongo(app)

# Settings
CORS(app)

# Database
db = mongo.db.pythonreact
products = db.products  # Assuming "products" is your collection

# Routes
@app.route('/products', methods=['POST'])
def createProduct():
  print(request.json)
  result = products.insert_one({
    'product_name': request.json['product_name'],
    'category': request.json['category'],
    'price': request.json['price'],
    'description': request.json['description'],
    'image_url': request.json['image_url']
  })
  return jsonify(str(ObjectId(result.inserted_id)))


@app.route('/products', methods=['GET'])
def getProducts():
    products_list = []
    for doc in products.find():
        products_list.append({
            '_id': str(ObjectId(doc['_id'])),
            'product_name': doc['product_name'],
            'category': doc['category'],
            'price': doc['price'],
            'description': doc['description'],
            'image_url': doc['image_url']
        })
    return jsonify(products_list)

@app.route('/products/<id>', methods=['GET'])
def getProduct(id):
  product = products.find_one({'_id': ObjectId(id)})
  print(product)
  return jsonify({
      '_id': str(ObjectId(product['_id'])),
      'product_name': product['product_name'],
      'category': product['category'],
      'price': product['price'],
      'description': product['description'],
      'image_url': product['image_url']
  })

@app.route('/products/<id>', methods=['DELETE'])
def deleteProduct(id):
  products.delete_one({'_id': ObjectId(id)})
  return jsonify({'message': 'Product Deleted'})

@app.route('/products/<id>', methods=['PUT'])
def updateProduct(id):
  print(request.json)
  products.update_one({'_id': ObjectId(id)}, {"$set": {
    'product_name': request.json['product_name'],
    'category': request.json['category'],
    'price': request.json['price'],
    'description': request.json['description'],
    'image_url': request.json['image_url']
  }})
  return jsonify({'message': 'Product Updated'})

if __name__ == "__main__":
    app.run(debug=True)
