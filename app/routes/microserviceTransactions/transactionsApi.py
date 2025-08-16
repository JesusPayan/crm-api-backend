from flask import Blueprint, jsonify, request, current_app
# from app.logging import logging

from app.models.transaction import Transaction
from sqlalchemy.exc import SQLAlchemyError
from app import db
import logging
import os
from sqlalchemy import text
transaction_api = Blueprint('transactionsApi', __name__)

@transaction_api.route('/get_transactions', methods=['GET'])
def get_transactions_summary():
    logging.info("getting all Transactions")
    transaction_list = get_transactions()
    if transaction_list:
        return jsonify({
            "message": "Transactions found",
            "data": [trasaction.to_dict() for trasaction in transaction_list]
        }), 200
    else:
        return jsonify({'message': 'No transactions found'}), 404   
    
@transaction_api.route('/get_balance', methods=['GET'])
def get_balance_summary():
    logging.info("getting balance")
    balance = get_balance()
    if balance:
        return jsonify({
            "message": "Balance found",
            "data": balance
        }), 200
    else:
        return jsonify({'message': 'No balance found'}), 404
    
def get_transactions():
    logging.info("Service get all Transactions")
    transaction_list = Transaction.get_all_transactions()
    if transaction_list:
        return transaction_list
    else:
        return []
    
def get_balance():
    logging.info("Service get balance")
    balance = Transaction.get_balance_summary()
    if balance:
        return balance
    else:
        return