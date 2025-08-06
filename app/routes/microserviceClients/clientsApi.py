from flask import Blueprint, jsonify, request
from app.logger import logger
from app.models.client import Client
import json

clients_api = Blueprint('clientsApi', __name__)
# http://127.0.0.1:5000/v1/clients/api/clients

# http://127.0.0.1:5000/v1/clients/get_all
@clients_api.route('/get_clients', methods=['GET'])
def get_all_clients():
        logger.info("clientsApi.py: Getting all clients")
        clientsList = get_all()
        if clientsList:
            return jsonify({
            "message": "Clientes encontrados",
            "data": [client.to_dict() for client in clientsList]
        }), 200
        else:
            return jsonify({"message": "No clients found"}), 404
        

@clients_api.route('/create_client', methods=['POST'])
def create_client():
        logger.info("clientsApi.py: Creating a new client")
        data = request.form
        if not data:
            return jsonify({"message": "No data provided"}), 400
        else:

            message,client = create_new_client(data)
            if client:
                return jsonify({
                "message": message,
                "data": client.to_dict()
            }), 201
            else:
                return jsonify({"message": "Client not created"}), 400
        

@clients_api.route('/api/clients/<int:id>', methods=['GET'])
def get_client_by_id(id):
        logger.info("clientsApi.py: Getting a client by id")
        client = find_by_id(id)
        if client:
            return jsonify(client.to_dict())
        else:
            return jsonify({"message": "Client not found"}), 404
        

@clients_api.route('/api/clients/<int:id>', methods=['PUT'])
def update_client(id):
        logger.info("clientsApi.py: Updating a client by id")
        data = request.get_json()
        if not data:
            return jsonify({"message": "No data provided"}), 400
        else:
            data = json.loads(data)
            client = update_by_id(id, data)
            if client:
                return jsonify(client.to_dict())
            else:
                return jsonify({"message": "Client not found"}), 404

@clients_api.route('/delete_client_by_id/<int:id>', methods=['DELETE'])
def delete_client(id):
        logger.info("clientsApi.py: Deleting a client by id")
        delete_client_by_id(id)
        return {"message": "Client deleted"},200

__all__ = ['client_api']

def create_new_client(data):        
    logger.info(f"Creating new client: {data}")
        #return self.client_repository.save(client)
        #validatinf input data
    saved_client = Client.create_new_client(data)
    if saved_client:
        return saved_client
    else:
        return None        
def get_all():
        logger.info("Getting all clients service")
        return Client.get_all()
def find_by_id(id):
        logger.info(f"Getting client by id: {id}")
        return Client.get_by_id(id)
def update_by_id(id,data):
        logger.info(f"Updating client by id: {id}")
        return Client.update_client(id,data)    
def delete_client_by_id(id):
        logger.info(f"Deleting client by id: {id}")
        return Client.delete_client(id)