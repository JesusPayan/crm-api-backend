from flask import Flask
from app import db
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Date, TIMESTAMP, DECIMAL
from sqlalchemy.orm import relationship
from app.logger import logger
from datetime import datetime, timedelta
from flask import jsonify
from app.models.product import Product
import numbers



# Tabla: contracts
class Contract(db.Model):
    __tablename__ = 'contracts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey('client.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    contract_type = Column(Integer)
    contract_type_desc = Column(String(100))
    start_date = Column(Date)
    end_date = Column(Date)
    days_left = Column(Integer)
    status = Column(Integer)
    status_desc = Column(String(100))
    created_at = Column(TIMESTAMP)
    created_by = Column(String(100))
    updated_at = Column(TIMESTAMP)
    updated_by = Column(String(100))
    total_price = Column(DECIMAL(10, 2))
    

    client = relationship("Client", back_populates="contracts")
    product = relationship("Product", back_populates="contracts")
    @staticmethod
    def get_all_contracts():
        contracts = db.session.query(Contract).all()
        return contracts
    @staticmethod
    def get_by_id(id):
        contract = db.session.query(Contract).filter_by(id=id).first()
        return contract

    @staticmethod
    def delete_contract(id):
        contract = db.session.query(Contract).filter_by(id=id).delete()
        db.session.commit()
        return contract
    @staticmethod
    def create_contract(client_id,product_name, contract_type, created_by,duration):
        print("contract_type",contract_type)
        logger.info(f"Models: Creating contract with client_id: {client_id}, product_name: {product_name}, contract_type: {contract_type}, created_by: {created_by}")   
        #Tipos de contratos 1: Completa, 2: Perfil, 3 renovacion perfil
        #Si el tipo de contrato es 1 significa que el cliente va a adquirir un perfil
        if contract_type == 1:
        #validamos que haya disponibilidad de perfiles, para el producto seleccionado
            product = db.session.query(Product).filter(Product.description == product_name)\
                                            .filter(Product.status == 1)\
                                            .filter(Product.available_profiles > 0)\
                                            .first()
            
            #si no hay perfiles disponibles se debe regresar el mensaje sin perfiles disponibles
            if not product:
                return False,"Sin perfiles disponibles para el producto seleccionado"
            else:
                current_price = product.client_profile_price
                logger.info(f"Product with description:{product.description} perfiles disponibles = {product.available_profiles}")  
        if contract_type == 2:
            #validamos que haya disponibilidad de cuentas completas
            product = product = db.session.query(Product).filter(Product.description == product_name)\
                                            .filter(Product.status == 1)\
                                            .filter(Product.available_profiles >= Product.total_profiles).first()
            if not product:
                return False,"No hay cuentas disponibles para el producto seleccionado"
            else:
                current_price = product.client_complete_price
                logger.info(f"Product with description:{product.description} perfiles disponibles = {product.available_profiles}")
                                                     
        if product:
            logger.info(f"Product with description:{product.description} perfiles disponibles = {product.available_profiles}")
            contract = Contract(
                client_id=client_id,
                product_id=product.id,
                start_date=datetime.now(),
                contract_type=contract_type,
                #Se asumira que la contratacion es de 30 dias
                end_date=datetime.now() + timedelta(days=duration),
                days_left=duration,
                status=1,
                status_desc="Activo",
                created_at=datetime.now(),
                created_by=created_by,
                updated_at=datetime.now(),
                updated_by=created_by,
                total_price=current_price,
                contract_type_desc= "Perfil" if contract_type == 1 else "Completa"
            )
            try:
                db.session.add(contract)
                db.session.flush()
                db.session.commit()
            except Exception as e:
                logger.error(f"Error creating new contract: {str(e.with_traceback())}")
                return None
            #actualizamos el total de perfiles disponibles
            if contract_type == 1:
                product.available_profiles -= 1
            if contract_type == 2:    
                product.available_profiles -= product.total_profiles
            db.session.commit()
            
            if contract:
                return contract,"Contrato creado exitosamente"
            else:
                return None

    def to_dict(self):
        return {
            "id": self.id,
            "client_id": self.client_id,
            "product_id": self.product_id,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "status": self.status,
            "status_desc": self.status_desc,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "created_by": self.created_by,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "updated_by": self.updated_by
        }
        