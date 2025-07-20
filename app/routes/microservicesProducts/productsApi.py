from flask import Blueprint, jsonify, request
from app.logger import logger
from app.models import Product
from sqlalchemy.exc import SQLAlchemyError
from app import db

products_api = Blueprint('productsApi', __name__)

@products_api.route('/update_product_by_id/<int:id>', methods=['PUT'])
def update_current_product(id):
    print("PUT /product endpoint reached", id)
    data = request.get_json()
    product_updated = update_product_by_id(id, data)
    if product_updated:
        return jsonify({'message': 'Product updated successfully'}), 200
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
    product_deleted = delete_product_by_id(id)
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
    products_list = get_product_by_status(status)
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
    data = request.get_json()
    if data:
        print(f"POST /product-add endpoint reached {data}")
        logger.info(f"POST /product-add endpoint reached input:{data}")
        product_saved = create_new_product(data)
        logger.info(f"Producto guardado: {product_saved}")
        if product_saved:
            return jsonify({
                "message": "Producto agregado correctamente",
                "data": product_saved.to_dict()
            }), 201
        else:
            return jsonify({"message": "Error al agregar el producto"}), 400
    else:
        return jsonify({"message": "No se recibió información válida"}), 400
    
    
def delete_product_by_id(id):
        try:
            product = Product.query.filter_by(id=id).first()
            if product:
                db.session.execute("DELETE FROM product WHERE id = :id", {"id": id})
                db.session.commit()
                return True
            else:
                return False
        except SQLAlchemyError as e:
            logger.error(f"Error al eliminar producto por ID: {str(e)}")
            return False
        
def delete_product_by_name(name):
        try:
            product = Product.query.filter_by(description=name).first()
            if product:
                db.session.delete(product)
                db.session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            logger.error(f"Error al eliminar producto por nombre: {str(e)}")
            return False
def delete_all():
        try:
            products = Product.query.all()
            for product in products:
                db.session.delete(product)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            logger.error(f"Error al eliminar todos los productos: {str(e)}")
            return False                

def get_all_products():
        try:
            return Product.query.all()
        except SQLAlchemyError as e:
            logger.error(f"Error al obtener productos: {str(e)}")
            return None

def get_product_by_name(name):
        try:
            return Product.query.filter_by(description=name).first()
        except SQLAlchemyError as e:
            logger.error(f"Error al obtener producto por nombre: {str(e)}")
            return None
def  get_by_id(id):
        try:
            return Product.query.filter_by(id=id).first()
        except SQLAlchemyError as e:
            logger.error(f"Error al obtener producto por ID: {str(e)}")
            return None 
def create_new_product(data):
        try:
            if data:
                new_product = Product.create_new_product(data)
                return new_product
            return None
        except SQLAlchemyError as e:
            logger.error(f"Error al crear producto: {str(e)}")
            return None
def update_product(id, data):
        try:
            product = Product.query.filter_by(des).first()
            if not product:
                return None
            for key, value in data.items():
                if hasattr(product, key):
                    setattr(product, key, value)
            db.session.commit()
            return product
        except SQLAlchemyError as e:
            logger.error(f"Error al actualizar producto: {str(e)}")
            return None
def delete_product(id):
        try:
            product = Product.query.filter_by(id=id).first()
            if product:
                db.session.delete(product)
                db.session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            logger.error(f"Error al eliminar producto: {str(e)}")
            return False

    # Otros filtros según atributos específicos:

def get_product_by_status(status):
        return Product.query.filter_by(status_desc=status).all()
    
def update_product_by_id(id, data):
    logger.info(f"Updating product with name: {id} and data: {data}")
    try:
        product = Product.query.filter_by(id=id).first()
        if not product:
            return None
        for key, value in data.items():
            if hasattr(product, key):
                    setattr(product, key, value)
            db.session.commit()
            return product
    except SQLAlchemyError as e:
            logger.error(f"Error al actualizar producto: {str(e)}")
            return None 
