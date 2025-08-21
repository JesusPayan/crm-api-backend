from flask import Blueprint, jsonify, request
from app.logger import logger
from app.models.client_summary import ClientSummary
from app.models.client import Client
import json
import pandas as pd

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
        
@clients_api.route('/import_clients', methods=['POST'])
def import_clienst():
        logger.info("Import Api.py: Importing clients")
        file = request.files['file']
        if not file:
            return jsonify({"message": "No se envio ningun archivo"}), 400
        else:
            #se envio un archivo para su procesamiento 
            existing_clients,message,imported_clients = import_new_clients(file)
            if imported_clients and existing_clients:
                return jsonify({
                    "message": f"Se importaron {len(imported_clients)} clientes exitosamente ya existian {len(existing_clients)} clientes",
                }),200
            elif imported_clients:
                return jsonify({
                    "message": f"Se importaron {len(imported_clients)} clientes exitosamente",
                }),200
            elif existing_clients:
                return jsonify({
                    "message": f"Ya existian {len(existing_clients)} clientes",
                }),200
            else:
                return jsonify({
                    f"message": "No se importaron clientes",
                }),400
@clients_api.route('/create_client', methods=['POST'])
def create_client():
        logger.info("clientsApi.py: Creating a new client")
        data = request.form
        if not data:
            return jsonify({"message": "No data provided"}), 400
        else:

            client,message = create_new_client(data)
            if client:
                return jsonify({
                "message": message,
                "data": client.to_dict()
            }), 201
            else:
                return jsonify({"message": "Client not created"}), 400
        
@clients_api.route('/get_clients_summary', methods=['GET'])
def get_contracts_summary():
    logger.info("clientsApi.py: Getting  clients summary")
    clientsSummaryList = get_all_summary()
    if clientsSummaryList:
        # return jsonify({
        #     "message": "Clientes encontrados",
        #     "data": [client.to_dict() for client in clientsSummaryList]
        # }), 200
        return clientsSummaryList
    else:
        return jsonify({"message": "No clients found"}), 404
    

@clients_api.route('/api/clients/<int:id>', methods=['GET'])
def get_client_by_id(id):
        logger.info("clientsApi.py: Getting a client by id")
        client = find_by_id(id)
        if client:
            return jsonify(client.to_dict())
        else:
            return jsonify({"message": "Client not found"}), 404
        

@clients_api.route('/update_client', methods=['PUT'])
def update_client():
        data = request.form
        logger.info("ClientsApi.py: Updating a client...")
        if not data:
            return jsonify({"message": "No data provided"}), 400
        else:
            # data = json.loads(data)
            id = data.get('id')
            client, message = update_by_id(id, data)
            if client:
                return jsonify("message", message), 200
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
    saved_client, message = Client.create_new_client(data)
    if saved_client:
        return saved_client, message
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
    
def get_all_summary():
        logger.info("Getting all clients summary")
        return ClientSummary.get_all()
def import_new_clients(file):
    logger.info(f"Importing new clients: {file}")
    try:
        # leer el archivo CSV con pandas
        df = pd.read_csv(file)

        # validar que tenga las columnas necesarias
        required_columns = ["name", "mother_lastname", "father_lastname", "telephone1", "email1", "created_by"]
        for col in required_columns:
            if col not in df.columns:
                return None, f"El CSV no contiene la columna requerida: {col}"

        # convertir a lista de registros
        records = df[required_columns].values.tolist()

        imported_clients = []
        existing_clients = []
        for record in records:
            existing_client, message = Client.existing_client(record)
            if  existing_client:
                logger.info(f"Client already exists: {existing_clients}")
                existing_clients.append(existing_clients)
                continue
            else:
                logger.info(f"Client does not exist: {existing_client}")
                saved_client,message = Client.create_new_clients(record)
                if saved_client:
                    logger.info(f"Client created: {saved_client}")
                    imported_clients.append(saved_client)
                else:
                    logger.error(f"Error creating client: {saved_client}")

        return existing_clients,message,imported_clients
    
    except Exception as e:
        logger.error(f"Error importing new clients: {str(e)}")
        return None, f"Error al importar clientes: {str(e)}"
    
    
    
    