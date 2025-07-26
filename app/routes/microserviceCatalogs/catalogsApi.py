from flask import Blueprint, jsonify, request
from app.logger import logger
from app.models.catalog import Catalog
from app.models.catalog_values import CatalogValue
from sqlalchemy.exc import SQLAlchemyError
from app import db


catalogs_api = Blueprint('catalogsApi', __name__)



@catalogs_api.route('v1/catalogs', methods=['GET'])
def get_catalogs():
    print("GET /catalogs endpoint reached")
    catalogs = get_all_catalogs()
    if catalogs:
        return jsonify({'catalogs': [catalog.to_dict() for catalog in catalogs]}), 200
    else:
        return jsonify({'message': 'Error getting catalogs'}), 400
@catalogs_api.route('v1/catalogs', methods=['POST'])
def add_catalog():
    print("POST /contract-add endpoint reached")
    data = request.get_json()
    if data:
        print(f"POST /contract-add endpoint reached {data}")
        logger.info(f"Contrato recibido: {data}")
        catalog_saved = create_new_catalog(data)
        logger.info(f"Contrato guardado: {catalog_saved}")
        if catalog_saved:
            return jsonify({
                "message": "Contrato agregado correctamente",
                "data": catalog_saved.to_dict()
            }), 201
        else:
            return jsonify({"message": "Error al agregar el contrato"}), 400
    else:
        return jsonify({"message": "No se recibió información válida"}), 400
    
@catalogs_api.route('v1/catalogs/<int:id>', methods=['PUT'])
def update_catalog(id):
    print("PUT /contract endpoint reached", id)
    data = request.get_json()
    catalog_updated = update_catalog_by_id(id, data)
    if catalog_updated:
        return jsonify({'message': 'Contract updated successfully'}), 200
    else:
        return jsonify({'message': 'Error updating contract'}), 400 


@catalogs_api.route('v1/catalogs/<int:id>', methods=['DELETE'])
def delete_catalog(id):
    print("DELETE /contract endpoint reached", id)
    catalog_deleted = delete_catalog_by_id(id)
    if catalog_deleted:
        return jsonify({'message': 'Contract deleted successfully'}), 200
    else:
        return jsonify({'message': 'Error deleting contract'}), 400

@catalogs_api.route('v1/catalogs/<int:id>', methods=['GET'])
def get_catalog_by_id(id):
    print("GET /contract endpoint reached", id)
    catalog = get_catalog_by_id(id)
    if catalog:
        return jsonify({'contract': catalog.to_dict()}), 200
    else:
        return jsonify({'message': 'Contract not found'}), 404        
    
def get_catalogs(self):
        try:
            return Catalog.query.all()
        except SQLAlchemyError as e:
            logger.error(f"Error al obtener catálogos: {str(e)}")
            return None

def get_catalog_by_id( id):
        try:
            return Catalog.query.filter_by(id=id).first()
        except SQLAlchemyError as e:
            logger.error(f"Error al obtener catálogo por ID: {str(e)}")
            return None

def create_new_catalog(data):
        try:
            if data:
                new_catalog = Catalog.create_new_catalog(data)
                return new_catalog
            return None
        except SQLAlchemyError as e:
            logger.error(f"Error al crear catálogo: {str(e)}")
            return None

def update_catalog_by_id( id, data):
        logger.info(f"Updating catalog with id: {id} and data: {data}")
        try:
            catalog = Catalog.query.filter_by(id=id).first()
            if not catalog:
                return None
            for key, value in data.items():
                if hasattr(catalog, key):
                    setattr(catalog, key, value)
            db.session.commit()
            return catalog
        except SQLAlchemyError as e:
            logger.error(f"Error al actualizar catálogo: {str(e)}")
            return None
        
def delete_catalog_by_id( id):
        try:
            catalog = Catalog.query.filter_by(id=id).first()
            if catalog:
                db.session.delete(catalog)
                db.session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            logger.error(f"Error al eliminar catálogo: {str(e)}")
            return False

def delete_all_catalogs(self):
        try:
            catalogs = Catalog.query.all()
            for catalog in catalogs:
                db.session.delete(catalog)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            logger.error(f"Error al eliminar todos los catálogos: {str(e)}")
            return False

def get_all_catalog_values(self):
        try:
            return CatalogValue.query.all()
        except SQLAlchemyError as e:
            logger.error(f"Error al obtener valores de catálogos: {str(e)}")
            return None

def get_catalog_value_by_id( id):
        try:
            return CatalogValue.query.filter_by(id=id).first()
        except SQLAlchemyError as e:
            logger.error(f"Error al obtener valor de catálogo por ID: {str(e)}")
            return None

def create_new_catalog_value( data):
        try:
            if data:
                new_catalog_value = CatalogValue.create_new_catalog_value(data)
                return new_catalog_value
            return None
        except SQLAlchemyError as e:
            logger.error(f"Error al crear valor de catálogo: {str(e)}")
            return None