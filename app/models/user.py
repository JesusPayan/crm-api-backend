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

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=True)
    last_name = db.Column(db.String(255), nullable=True)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_subscription_start_date = db.Column(db.DateTime, nullable=True)  # Nuevo campo para fecha de inicio
    user_subscription_end_date = db.Column(db.DateTime, nullable=True)    # Nuevo campo para fecha de fin
    user_subscription_days_left = db.Column(db.Integer, default=0)  # Nuevo campo para días restantes
    subscription_status_id = db.Column(db.String(255), nullable=False)
    subscription_status_description = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "username": self.username,
            "email": self.email,
            "phone": self.phone,
            "is_active": self.is_active,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "subscription_status_id": self.subscription_status_id,
            "subscription_status_description": self.subscription_status_description
        }
    
    @staticmethod
    def get_by_id(user_id):
        return User.query.get(user_id)
    
    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()
    
    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username=username).first()
    
    @staticmethod
    def get_all_users():
        return User.query.all()
    @staticmethod
    def save_new_user(data):
        new_user = User(
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            username=data.get("username") or data.get("email"),
            email=data.get("email"),
            password=data.get("password"),  # Consider hashing the password
            phone=data.get("phone"),
            is_active=data.get("is_active", True),
            subscription_status_id=data.get("subscription_status_id", "1"),
            subscription_status_description=data.get("subscription_status_description", "Active")
        )
        try:
            db.session.add(new_user)
            db.session.commit()
            return new_user
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error saving new user: {str(e)}")
            return None
    