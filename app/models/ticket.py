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
    __tablename__ = 'ticket'

    id = Column(Integer, primary_key=True)
    title = Column(String(50))
    description = Column(String(255))
    status = Column(String(50))
    priority = Column(String(20), default='Low')
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    assignedTo = Column(Integer, ForeignKey('user.id'), nullable=False)
    client_id = Column(Integer, ForeignKey('user_config.id'), nullable=True)
    attachments = Column(String(255), nullable=True)