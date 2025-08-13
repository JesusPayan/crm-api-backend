from flask import Blueprint, jsonify, request, current_app
# from app.logging import logging
from app.models.product import Product
from app.models.product_summary import ProductSummary
from app.models.transaction import Transaction
from sqlalchemy.exc import SQLAlchemyError
from app import db
import logging
import os
from sqlalchemy import text
products_api = Blueprint('productsApi', __name__)

@products_api.route('/get_products_summary', methods=['GET'])
def get_products_summary():
    products_list = ProductSummary.get_all()
    if products_list:
        return products_list
@products_api.route('/update_product', methods=['PUT'])
def update_current_product():
    data = request.form
    id = data.get('id')
    print("PUT /product endpoint reached", id)
    product_updated, message = update_product_by_id(id, data)
    if product_updated:
        return jsonify({'message':message}), 200
    else:
        return jsonify({'message': 'Error updating product'}), 400
@products_api.route('/delete_all_products', methods=['DELETE'])
def delete_all_products():
    print("DELETE /products endpoint reached")
    products_deleted = delete_all()
    if products_deleted:
        return jsonify({'message': 'Products deleted successfully'}), 200
    else:
        return jsonify({'message': 'Error deleting products'}), 400
@products_api.route('/delete_product_by_id/<int:id>', methods=['DELETE'])
def delete_product(id):
    print("DELETE /product endpoint reached", id)
    product_deleted = delete_product_by_identifier(id)
    if product_deleted:
        return jsonify({'message': 'Product deleted successfully'}), 200
    else:
        return jsonify({'message': 'Error deleting product'}), 400
@products_api.route('/delete_product_by_name/<string:name>', methods=['DELETE'])
def delete_product_by_description(name):
    print("DELETE /product endpoint reached", name)
    product_deleted = delete_product(name)
    if product_deleted:
        return jsonify({"message": "Producto eliminado correctamente"}), 200
    else:
        return jsonify({"message": "Error al eliminar el producto"}), 400
@products_api.route('/get_product_by_status/<string:status>', methods=['GET'])
def get_product_by_status(status):
    print("GET /product_by_status endpoint reached for status:", status) 
    products_list = find_product_by_status(status)
    if products_list:
        # Asume que cada producto tiene un método to_dict()
        return jsonify({
            "message": "Productos encontrados",
            "data": [product.to_dict() for product in products_list]
        }), 200
    else:    
        return jsonify({"message": "Productos no encontrados"}), 404
@products_api.route('/get_products', methods=['GET'])
def get_products():
    print("GET /products endpoint reached")
    products_list = get_all_products()
    if products_list:
        # Asume que cada producto tiene un método to_dict()
        return jsonify({
            "message": "Productos encontrados",
            "data": [product.to_dict() for product in products_list]
        }), 200
    else:    
        return jsonify({"message": "Productos no encontrados"}), 404
@products_api.route('/get_product/<string:name>', methods=['GET'])
def get_product(name):
    print("GET /product endpoint reached")
    product = get_product_by_name(name)
    if product:
        return jsonify({
            "message": "Producto encontrado",
            "data": product.to_dict()
        }), 200
    else:    
        return jsonify({"message": "Producto no encontrado"}), 404
@products_api.route('/get_product_by_id/<int:id>', methods=['GET'])
def get_product_by_id(id):
    print("GET /product endpoint reached")
    product = get_by_id(id)
    if product:
        return jsonify({
            "message": "Producto encontrado",  
            "data": product.to_dict()
        }), 200
    else:    
        return jsonify({
            "message": "Producto no encontrado"
            }), 404
@products_api.route('/create_product', methods=['POST'])
def add_product():
    if 'image' not in request.files:
        return jsonify({"message": "No se ha seleccionado ninguna imagen"}), 400

    image = request.files['image']
    if image.filename == "":
        return jsonify({"message": "Nombre de archivo vacío"}), 400
    image_path = r'C:\dev\Sistemas\CRM\crm-frontend-app\src\assets\images\products'
    UPLOAD_FOLDER = os.path.join(os.getcwd(), image_path)
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    current_app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    image_path = os.path.join(UPLOAD_FOLDER, image.filename)
    image.save(image_path)

    data = request.form
    
    if data:
        logging.info(f"POST /product-add endpoint reached input:{data}")
        message, product_saved = create_new_product(data, image_path)
        logging.info(f"Producto guardado: {product_saved}")
        if product_saved:
            return jsonify({
                "message": message,
                "data": product_saved.to_dict()
            }), 201
        else:
            return jsonify({"message": message}), 400
    else:
        return jsonify({"message": "No se recibió información válida"}), 400
def delete_product_by_identifier(id):
        try:
            product = Product.query.filter_by(id=id).first()
            if product:
                db.session.execute(text('DELETE FROM product WHERE id =:id'), dict(id=f'{id}'))
                db.session.commit()
                return True
            else:
                return False
        except SQLAlchemyError as e:
            logging.error(f"Error al eliminar producto por ID: {e.with_traceback()}")
            return False
        
def delete_all():
        try:
            products = Product.query.all()
            for product in products:
                db.session.delete(product)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            logging.error(f"Error al eliminar todos los productos: {str(e)}")
            return False                

def get_all_products():
        try:
            return Product.query.all()
        except SQLAlchemyError as e:
            logging.error(f"Error al obtener productos: {str(e)}")
            return None

def  get_by_id(id):
        try:
            return Product.query.filter_by(id=id).first()
        except SQLAlchemyError as e:
            logging.error(f"Error al obtener producto por ID: {str(e)}")
            return None 
def create_new_product(data,image_path):
        try:
            if data:
                current_balance,message = Transaction.get_current_balance()     
                if current_balance:   
                    new_product,message = Product.create_new_product(data,image_path)
                    if new_product:
                        Transaction.add_transaction(2, new_product.investment, 0,0)
                    return message,new_product
                else:
                    return message,None
            return None
        except SQLAlchemyError as e:
            logging.error(f"Error al crear producto: {str(e)}")
            return None

def delete_product_by_id(id):
        try:
            product = Product.query.filter_by(id=id).first()
            if product:
                db.session.delete(product)
                db.session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            logging.error(f"Error al eliminar producto: {str(e)}")
            return False

def update_product_by_id(id, data):
    logging.info(f"Updating product with name: {id} and data: {data}")
    try:
        product = Product.update_product(id, data)
        if not product:
            return None
        else:    
            return product, "Product updated successfully"
    except SQLAlchemyError as e:
            logging.error(f"Error al actualizar producto: {str(e)}")
            return None 

# def delete_product_by_name(name):
#         try:
#             product = Product.query.filter_by(description=name).first()
#             if product:
#                 db.session.delete(product)
#                 db.session.commit()
#                 return True
#             return False
#         except SQLAlchemyError as e:
#             logging.error(f"Error al eliminar producto por nombre: {str(e)}")
#             return False
# def find_product_by_status(status):
#         return Product.query.filter_by(status_desc=status).all()

# def get_product_by_name(name):
#         try:
#             return Product.query.filter_by(description=name).first()
#         except SQLAlchemyError as e:
#             logging.error(f"Error al obtener producto por nombre: {str(e)}")
#             return None