from flask import Blueprint, jsonify, request
from app.logger import logger
from app.models.contract import Contract
from app.models.product import Product
from app.models.transaction import Transaction
from app.models.contract_summary import ContractSummary
from sqlalchemy.exc import SQLAlchemyError
from app import db
from datetime import datetime, timedelta

contracts_api = Blueprint('contractsApi', __name__)
print("contracts_api")
@contracts_api.route('/update_day_left', methods=['PUT'])
def update_day_left():
    print("PUT /contract endpoint reached")
    update_contracts_day_left()
    return jsonify({'message': 'Day left updated successfully'}), 200
@contracts_api.route('/create_contract', methods=['POST'])
def add_contract():
    print("POST /contract-add endpoint reached")
    data = request.form
    if data:
        print(f"POST /contract-add endpoint reached {data}")
        logger.info(f"Contrato recibido: {data}")
        contract_saved,message = create_new_contract(data)
        logger.info(f"Contrato guardado: {contract_saved}")
        if contract_saved:
            return jsonify({
                "message": "Contrato agregado correctamente",
                "data": contract_saved.to_dict()
            }), 201
        else:
            return jsonify({"message":  message}), 200
    else:
        return jsonify({"message": "No se recibió información válida"}), 400
@contracts_api.route('/renovate_contract/<int:id>', methods=['PUT'])
def renovate_contract(id):
        print("PUT /contract endpoint reached", id)
        data = request.form
        print("PUT /contract endpoint reached", data)
        contract_updated = renovate_contract_by_id(id, data)
        if contract_updated:
            return jsonify({'message': 'Contract updated successfully'}), 200
        else:
            return jsonify({'message': 'Error updating contract'}), 400     

@contracts_api.route('/delete_contract/<int:id>', methods=['DELETE'])
def delete_contract(id):
        print("DELETE /contract endpoint reached", id)
        contract_deleted = delete_contract_by_id(id)
        if contract_deleted:
            return jsonify({'message': 'Contract deleted successfully'}), 200
        else:
            return jsonify({'message': 'Error deleting contract'}), 400


@contracts_api.route('/get_contracts_summary', methods=['GET'])
def get_contracts():
    contracts_list, message = get_all_contracts()
    if contracts_list:
        # 
        return contracts_list
    else:
        return jsonify({'message': 'Error getting contracts'}), 400

@contracts_api.route('v1/contracts/<int:id>', methods=['GET'])
def get_contract_by_id(contract_id):
        print("GET /contract endpoint reached", contract_id)
        contract = get_contract_by_identifier(contract_id)
        if contract:
            return jsonify({'contract': contract.to_dict()}), 200
        else:
            return jsonify({'message': 'Contract not found'}), 404

def get_all_contracts():
        try:
            return ContractSummary.get_all(), "Contratos obtenidos exitosamente"
        
        except SQLAlchemyError as e:
            logger.error(f"Error al obtener contratos: {str(e)}")
            return None

def get_contract_by_identifier(id):
    try:
        return Contract.query.filter_by(id=id).first()
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener contrato por ID: {str(e)}")
        return None

def create_new_contract(data):
        client_id = None
        product_name = None
        contract_type = None
        created_by = None

        try:
            if data:
                logger.info(f"Creating new contract: {data}")
                if data['client_id'] is not None: client_id = data['client_id']
                if data['contract_type'] is not None: contract_type = data['contract_type']   
                if data['product_name'] is not None: product_name = data['product_name']
                if data['created_by'] is not None: created_by = data['created_by']
                if data['contract_duration'] is not None: duration = data['contract_duration']
                duration = calculate_duration(duration)
                if contract_type == 'Perfil':
                    contract_type = 1;
                elif contract_type == 'Completa' or contract_type == 'Cuenta completa':
                    contract_type = 2;
                else:
                    contract_type = 3;
                    
                new_contract,message = Contract.create_contract(client_id,product_name, contract_type, created_by,duration)
                #se agrega la logica para llevar el control de las transacciones $$
                if new_contract:
                    Transaction.add_transaction(1, new_contract.total_price, new_contract.client_id, new_contract.id)
                return new_contract,message 
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
def delete_contract_by_id(id):
    logger.info(f"Deleting contract with id: {id}")
    contract = Contract.query.filter_by(id=id).first()
    if contract:
        db.session.delete(contract)
        db.session.commit()
        return True
    else:
        return False
def renovate_contract_by_id(id, data):
    logger.info(f"Updating contract with id: {id} and data: {data}")
    try:
        contract = Contract.query.filter_by(id=id).first()
        if not contract:
            return None
        else:
            contract.start_date = datetime.now()
            contract.end_date = datetime.now() + timedelta(days=30)
            contract.days_left = 30
            contract.updated_at = datetime.now()
            contract.updated_by = data.get('renovate_by')
            contract.status = 1
            contract.status_desc = "Activo"
            db.session.commit()
            return contract, "Contrato renovado correctamente"
    except SQLAlchemyError as e:
        logger.error(f"Error al actualizar contrato: {str(e)}")
        return None
def update_contracts_day_left():
    
        contracts = Contract.query.filter(Contract.days_left>0).all()
            
        for contract in contracts:
            # print((contract.end_date - datetime.now().date()).days)
            contract.days_left = (contract.end_date - datetime.now().date()).days
            if contract.days_left <= 0:
                contract.status = 2
                contract.status_desc = "Vencido"
            elif contract.days_left <= 5:
                contract.status = 3
                contract.status_desc = "Proximo a vencer"
            db.session.commit()
            
            
def calculate_duration(duration):
    if duration.lower() == "semestral":
        return 180
    if duration.lower() == "semanal":
        return 7
    if duration.lower() == "trimestral":
        return 90
    if duration.lower() == "mensual":
        return 30
    elif duration.lower() == "anual":
        return 365