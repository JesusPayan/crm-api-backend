from flask import Flask
from app import db
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Date, TIMESTAMP, DECIMAL
from sqlalchemy.orm import relationship
from app.logger import logger
from datetime import datetime, timedelta
from flask import jsonify
import numbers



class Transaction(db.Model):
    __tablename__ = 'accounting'

    id = Column(Integer, primary_key=True, autoincrement=True)
    Transaction_type_id = Column(String(50))
    Transaction_type_desc = Column(String(100))
    # client_id = Column(Integer, ForeignKey('client.id'), nullable=False)
    # contract_id = Column(Integer, ForeignKey('contracts.id'), nullable=False)
    client_id = Column(Integer, ForeignKey('client.id'), nullable=True)
    contract_id = Column(Integer, ForeignKey('contracts.id'), nullable=True)
    Transaction_date = Column(Date)
    Transaction_amount = Column(DECIMAL(10, 2))
    Transaction_description = Column(String(100))
    Transaction_reference = Column(String(100))
    Transaction_status = Column(Integer)
    Transaction_status_desc = Column(String(100))
    
    contract = relationship('Contract', backref='accounting', lazy=True)
    client = relationship('Client', backref='accounting', lazy=True)
    @staticmethod
    def get_all_transactions():
        transactions = db.session.query(Transaction).all()
        return transactions
    def to_dict(self):
        return {
                "id":self.id,
                "Transaction_type_id":self.Transaction_type_id,
                "Transaction_type_desc":self.Transaction_type_desc,
                "Transaction_date":self.Transaction_date,
                "Transaction_amount":self.Transaction_amount,
                "Transaction_description":self.Transaction_description,
                "Transaction_reference":self.Transaction_reference,
                "Transaction_status":self.Transaction_status,
                "Transaction_status_desc":self.Transaction_status_desc
        }
    @staticmethod
    def get_by_id(id):
        transaction = db.session.query(Transaction).filter_by(id=id).first()
        return transaction
    def update_transaction(self, id, data):
        transaction = db.session.query(Transaction).filter_by(id=id).update(data)
        if not transaction:
            return None
        else:
            db.session.commit()
            return transaction
    def delete_transaction(self, id):
        transaction = db.session.query(Transaction).filter_by(id=id).delete()
        db.session.commit()
        return transaction
    def add_transaction(type, amount, client_id, contract_id):
        logger.info(f"Adding transaction with type: {type}, amount: {amount}, client_id: {client_id}, contract_id: {contract_id}")
        
        if amount:
            amount = float(amount)
        if client_id:
            client_id = int(client_id)
        if contract_id:
            contract_id = int(contract_id)
        if type == 1:
            type_desc = "Venta"
            new_transaction = Transaction(
                Transaction_type_id=type,
                Transaction_type_desc=type_desc,
                contract_id=contract_id,  # ← CORRECTO
                client_id=client_id,
                Transaction_date=datetime.now().date(),
                Transaction_amount=amount,
                Transaction_description="Complete"
            )
        elif type == 2:
            type_desc = "Compra"
            new_transaction = Transaction(
            Transaction_type_id=type,
            Transaction_type_desc=type_desc,
            Transaction_date=datetime.now().date(),
            Transaction_amount=amount,
            Transaction_description="Complete"
        )
        
        try:
            db.session.add(new_transaction)
            db.session.flush()
            db.session.commit()
            return new_transaction, "Transacción creada con exito"
        except Exception as e:
            logger.error(f"Error al crear la transacción: {str(e.with_traceback())}")
            return None, "Error al crear la transacción"
        
    
    