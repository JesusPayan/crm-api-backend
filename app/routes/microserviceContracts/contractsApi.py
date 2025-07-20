from flask import Blueprint, jsonify, request
from app.logger import logger
from app.models import Contract
from sqlalchemy.exc import SQLAlchemyError
from app import db
contracts_api = Blueprint('contractsApi', __name__)


print("✅ contractsApi cargado correctamente")

@contracts_api.route('/add_contract', methods=['POST'])
def add_contract():
    print("POST /contract-add endpoint reached")
    data = request.get_json()
    if data:
        print(f"POST /contract-add endpoint reached {data}")
        logger.info(f"Contrato recibido: {data}")
        contract_saved = create_new_contract(data)
        logger.info(f"Contrato guardado: {contract_saved}")
        if contract_saved:
            return jsonify({
                "message": "Contrato agregado correctamente",
                "data": contract_saved.to_dict()
            }), 201
        else:
            return jsonify({"message": "Error al agregar el contrato"}), 400
    else:
        return jsonify({"message": "No se recibió información válida"}), 400
@contracts_api.route('v1/contracts/<int:id>', methods=['PUT'])
def update_contract(contract_id):
        print("PUT /contract endpoint reached", contract_id)
        data = request.get_json()
        contract_updated = update_contract_by_id(contract_id, data)
        if contract_updated:
            return jsonify({'message': 'Contract updated successfully'}), 200
        else:
            return jsonify({'message': 'Error updating contract'}), 400     

@contracts_api.route('v1/contracts/<int:id>', methods=['DELETE'])
def delete_contract(contract_id):
        print("DELETE /contract endpoint reached", contract_id)
        contract_deleted = delete_contract_by_id(contract_id)
        if contract_deleted:
            return jsonify({'message': 'Contract deleted successfully'}), 200
        else:
            return jsonify({'message': 'Error deleting contract'}), 400

@contracts_api.route('v1/contracts', methods=['GET'])
def get_contracts():
        print("GET /contracts endpoint reached")
        contracts = get_all_contracts()
        if contracts:
            return jsonify({'contracts': [contract.to_dict() for contract in contracts]}), 200
        else:
            return jsonify({'message': 'Error getting contracts'}), 400

@contracts_api.route('v1/contracts/<int:id>', methods=['GET'])
def get_contract_by_id(contract_id):
        print("GET /contract endpoint reached", contract_id)
        contract = get_contract_by_id(contract_id)
        if contract:
            return jsonify({'contract': contract.to_dict()}), 200
        else:
            return jsonify({'message': 'Contract not found'}), 404

def get_all_contracts(self):
        try:
            return Contract.query.all()
        except SQLAlchemyError as e:
            logger.error(f"Error al obtener contratos: {str(e)}")
            return None

def get_contract_by_id(self, id):
    try:
        return Contract.query.filter_by(id=id).first()
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener contrato por ID: {str(e)}")
        return None

def create_new_contract(data):
        try:
            if data:
                new_contract = Contract.create_new_contract(data)
                return new_contract
            return None
        except SQLAlchemyError as e:
            logger.error(f"Error al crear contrato: {str(e)}")
            return None
def update_contract_by_id(self, id, data):
        logger.info(f"Updating contract with id: {id} and data: {data}")
        try:
            contract = Contract.query.filter_by(id=id).first()
            if not contract:
                return None
            for key, value in data.items():
                if hasattr(contract, key):
                    setattr(contract, key, value)
            db.session.commit()
            return contract
        except SQLAlchemyError as e:
            logger.error(f"Error al actualizar contrato: {str(e)}")
            return None
def delete_contract_by_id(self, id):
    logger.info(f"Deleting contract with id: {id}")
    contract = Contract.query.filter_by(id=id).first()
    if contract:
        db.session.delete(contract)
        db.session.commit()
        return True
    else:
        return False
    