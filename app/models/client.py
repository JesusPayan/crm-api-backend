from flask import Flask
from app import db
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Date, TIMESTAMP, DECIMAL
from sqlalchemy.orm import relationship
from app.logger import logger
from datetime import datetime, timedelta
from flask import jsonify
from app.models.transaction import Transaction
from app.models.contract import Contract
import numbers
import logging



# Tabla: client
class Client(db.Model):
    __tablename__ = 'client'

    id = Column(Integer, primary_key=True, autoincrement=True)
    cve_internal = Column(String(50))
    name = Column(String(100))
    mother_lastname = Column(String(100))
    father_lastname = Column(String(100))
    telephone1 = Column(String(20))
    telephone2 = Column(String(20))  # <-- corregido
    email1 = Column(String(100))
    email2 = Column(String(100))
    status = Column(Integer)
    status_desc = Column(String(100))
    created_at = Column(TIMESTAMP)
    created_by = Column(String(100))
    updated_at = Column(TIMESTAMP)
    updated_by = Column(String(100))

    contracts = relationship("Contract", back_populates="client", lazy=True)

    @staticmethod
    def delete_client(id):
        deleted_client = False
        logging.info(f"model Client: Deleting client by id: {id}")
        client = db.session.query(Client).filter_by(id=id)
        client_id = client.first().id
        logging.info(f"model Client: Deleting client by id: {client_id}")
        try:
            #borramos actualizamos la tabla account y luego borramos el cliente
            
            db.session.query(Contract).filter(Contract.client_id == client_id).delete()
            db.session.query(Transaction).filter(Transaction.client_id == client_id).delete()
            client.delete()
            db.session.commit()
            deleted_client = True
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error deleting client: {str(e)}")
            deleted_client = False
        return client

    @staticmethod
    def get_all():
        logger.info("models.py: Getting all clients")
        clients = Client.query.all()
        if not clients:
            return None
        return clients
        

    @staticmethod
    def get_by_id(id):
        return db.session.query(Client).filter_by(id=id).first()

    @staticmethod
    def update_client(id, data):
        
        client = db.session.query(Client).filter_by(id=id).update(data)
        db.session.commit()
        if client:
            return client, "Cliente actualizado exitosamente"
        else:
            return None
    @staticmethod
    def existing_client(data):
        existingClient = Client.query.filter_by(name=data[0], father_lastname=data[1], mother_lastname=data[2], telephone1=data[3], email1=data[4]).first()
        if existingClient:
            logger.info(f"Client already exists: {existingClient}")
            return existingClient, "El cliente ya existe"
        else:
            logger.info(f"Client does not exist:")
            return None, "El cliente no existe"
    @staticmethod
    def create_new_clients(data):
        logger.info(f"Creating new client input received: {data}")
        importedClient = None



        new_client = Client(
                    name=data[0],
                    father_lastname=data[1],
                    mother_lastname=data[2],
                    status=1,
                    status_desc="Activo",
                    telephone1=data[3],
                    # telephone2=data['telephone2'] or data['telephone1'],
                    email1=data[4],
                    created_by=data[5],
                    created_at=datetime.now()
        )
        try:
            db.session.add(new_client)
            db.session.flush()
            db.session.commit()
            return new_client, "Cliente creado exitosamente"
        except Exception as e:
                    logger.error(f"Error creating new client: {str(e)}")
                    return None, "Error al crear el cliente"

    @staticmethod
    def create_new_client(data):
        logger.info(f"Creating new client input received: {data}")
        
        new_client = Client(
            name=data.get('name'),
            father_lastname=data.get('father_lastname'),
            mother_lastname=data.get('mother_lastname'),
            status=1,
            status_desc="Activo",
            telephone1=data.get('telephone1'),
            telephone2=data.get('telephone2') or data.get('telephone1'),
            email1=data.get('email1'),
            email2=data.get('email2') or data.get('email1'),
            created_by=data.get('created_by'),
            created_at=datetime.now()
        )
        try:
            db.session.add(new_client)
            db.session.flush()
            db.session.commit()
            return new_client, "Cliente creado exitosamente"
        except Exception as e:
            logger.error(f"Error creating new client: {str(e)}")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "father_lastname": self.father_lastname,
            "mother_lastname": self.mother_lastname,
            "telephone1": self.telephone1,
            "telephone2": self.telephone2,
            "email1": self.email1,
            "email2": self.email2,
            "status": self.status,
            "status_desc": self.status_desc,
            "created_at": self.created_at,
            "created_by": self.created_by,
            "updated_at": self.updated_at,
            "updated_by": self.updated_by
        }