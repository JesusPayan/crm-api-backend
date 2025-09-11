from flask import Blueprint, jsonify, request, current_app
from app.models.ticket import Ticket
from app.models.ticket_detail import ticket_detail
from sqlalchemy.exc import SQLAlchemyError
from app import db
import logging
import os
from sqlalchemy import text


tickets_api = Blueprint('ticketsApi', __name__)

@tickets_api.route('/get_tickets', methods=['GET'])
def get_tickets():  
    try:
        tickets = Ticket.query.all()
        print(ticket.to_dict() for ticket in tickets)
        tickets_list = [ticket.to_dict() for ticket in tickets]
        return jsonify({"message":"Tickets retrieved successfully",
                      "data":tickets_list,
                      "code":200})
    except SQLAlchemyError as e:
        logging.error(f"Database error: {str(e)}")
        return jsonify({"error": "Database error occurred"}), 500
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500

@tickets_api.route('/create_ticket', methods=['POST'])
def create_ticket():
    code = 200
    message = ""
    if request.form:
        data = request.form
        ticket, code = generate_new_ticket(data)
        if ticket:
            message = "Ticket created successfully" 
            code = 201
        else:
            message = "Failed to create ticket"
            code = 400
    else:
        message = "No form data provided"
        code = 400

    return jsonify({"message": message}), code
    
def generate_new_ticket(data):
    
        title = data.get('title')
        description = data.get('description')
        status = data.get('status', 'Open')
        priority = data.get('priority', 'Low')                      
        assignedTo = data.get('assignedTo')
        client_id = request.args.get('client_id')
        attachments = request.args.get('attachments')

        if not title or not description or not assignedTo:
            return "Missing required fields: title, description, assignedTo", 400
        else:
            new_ticket = Ticket.generate_new_ticket(title, description, status, priority, assignedTo, client_id, attachments)
            if new_ticket:
                return new_ticket.to_dict(), 201
            else:
                return None, 500
