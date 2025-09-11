from flask import Flask
from app import db
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Date, TIMESTAMP, DECIMAL
from sqlalchemy.orm import relationship
from app.logger import logger
from datetime import datetime, timedelta
from flask import jsonify
import numbers
import logging

class Ticket(db.Model):
    __tablename__ = 'tickets'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50))
    description = Column(String(255))
    status = Column(String(50))
    priority = Column(String(20), default='Low')
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    # assignedTo = Column(Integer, ForeignKey('user.id'), nullable=False)
    # client_id = Column(Integer, ForeignKey('user_config.id'), nullable=True)
    assignedTo = Column(Integer)
    client_id = Column(Integer)
    attachments = Column(String(255), nullable=True)
    
    @staticmethod
    def generate_new_ticket(title=title,description=description,status=status,priority=priority,assignedTo=assignedTo,client_id=client_id,attachments=attachments):
        
        
        new_ticket = Ticket(title=title,
                description=description,
                status=status,
                priority=priority,
                assignedTo= 2 if client_id else 2,
                client_id= 1 if client_id else 1,
                attachments=attachments)    
        try:
            db.session.add(new_ticket)
            db.session.commit()
            return new_ticket
        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}")
            return None
    def to_dict(self):
        return {            
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'priority': self.priority,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }