from flask import Flask
from app import db
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Date, TIMESTAMP, DECIMAL
from sqlalchemy.orm import relationship
from app.logger import logger
from datetime import datetime, timedelta
from flask import jsonify
import numbers
import logging

class UserConfig(db.Model):
    __tablename__ = 'user_config'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user_name = Column(String(50), nullable=False)
    user_logo = Column(String(255), nullable=True)
    user_phone = Column(String(20), nullable=True)
    config_key = Column(String(50), nullable=False)
    config_value = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="configs")
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'config_key': self.config_key,
            'config_value': self.config_value,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f"<UserConfig(id={self.id}, user_id={self.user_id}, config_key='{self.config_key}', config_value='{self.config_value}')>"
    
    @staticmethod
    def get_by_user_and_key(user_id, config_key):
        return UserConfig.query.filter_by(user_id=user_id, config_key=config_key).first()
    
    @staticmethod
    def create_or_update(user_id, config_key, config_value):
        config = UserConfig.get_by_user_and_key(user_id, config_key)
        if config:
            config.config_value = config_value
            db.session.commit()
            logger.info(f"Updated UserConfig: {config}")
        else:
            new_config = UserConfig(user_id=user_id, config_key=config_key, config_value=config_value)
            db.session.add(new_config)
            db.session.commit()
            logger.info(f"Created UserConfig: {new_config}")
        return config or new_config