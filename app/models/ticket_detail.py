from flask import Flask
from app import db
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Date, TIMESTAMP, DECIMAL
from sqlalchemy.orm import relationship
from app.logger import logger
from datetime import datetime, timedelta
from flask import jsonify
import numbers
import logging

class ticket_detail(db.Model):
    __tablename__ = 'ticket_detail'

    id = Column(Integer, primary_key=True)
    ticket_id = Column(Integer, ForeignKey('ticket.id'), nullable=False)
    comments = Column(String(255))
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    ticket = relationship('Ticket', backref='details', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'ticket_id': self.ticket_id,
            'detail_description': self.detail_description,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'user_id': self.user_id
        }
    
    def __repr__(self):
        return f"<TicketDetail(id={self.id}, ticket_id={self.ticket_id}, detail_description='{self.detail_description}')>"