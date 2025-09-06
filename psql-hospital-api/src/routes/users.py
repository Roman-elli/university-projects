import logging
import psycopg2
import jwt, datetime

from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from db import db_connection
from config import Config
from services.users_service import validate_user

def register_routes(app):
    @app.route('/dbproj/register/<user_type>', methods=['POST'])
    def add_register(user_type):
        logging.info(f'POST /register/{user_type}')
        payload = request.get_json()

        valid_user_types = ['patient', 'assistant', 'nurse', 'doctor']
        if user_type not in valid_user_types:
            return jsonify({'status': Config.STATUS_CODES['api_error'], 'errors': 'Invalid user type'}), Config.STATUS_CODES['api_error']

        logging.debug(f'POST /register/{user_type} - payload: {payload}')

        is_valid, error_message = validate_user(user_type, payload)
        if not is_valid:
            return jsonify({'status': Config.STATUS_CODES['api_error'], 'errors': error_message}), Config.STATUS_CODES['api_error']

        conn = db_connection()
        cur = conn.cursor()

        try:
            hashed_password = generate_password_hash(payload.get('password'))
            if user_type == 'patient':
                cur.execute("SELECT insert_patient(%s, %s, %s, %s, %s)", 
                            (payload.get('name'), payload.get('email'), payload.get('phone'), payload.get('username'), hashed_password))
            elif user_type == 'assistant':
                cur.execute("SELECT insert_assistant(%s, %s, %s, %s, %s, %s, %s, %s)", 
                            (payload.get('start_date'), payload.get('due_date'), payload.get('salary'), payload.get('name'), payload.get('email'), payload.get('phone'), payload.get('username'), hashed_password))
            elif user_type == 'nurse':
                cur.execute("SELECT insert_nurse(%s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                            (payload.get('hierarchy'), payload.get('start_date'), payload.get('due_date'), payload.get('salary'), payload.get('name'), payload.get('email'), payload.get('phone'), payload.get('username'), hashed_password))
            elif user_type == 'doctor':
                cur.execute("SELECT insert_doctor(%s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                            (payload.get('license'), payload.get('start_date'), payload.get('due_date'), payload.get('salary'), payload.get('name'), payload.get('email'), payload.get('phone'), payload.get('username'), hashed_password))
            
            user_id = cur.fetchone()[0]
            conn.commit()
            response = {'status': Config.STATUS_CODES['success'], 'results': {'user_id': user_id}}

        except (Exception, psycopg2.DatabaseError) as error:
            logging.error(f'POST /register/{user_type} - error: {error}')
            if "Username already exists" in str(error):
                response = {'status': Config.STATUS_CODES['api_error'], 'errors': 'Username already exists'}
            else:
                response = {'status': Config.STATUS_CODES['internal_error'], 'errors': str(error)}
            conn.rollback()
        finally:
            if conn is not None:
                conn.close()

        return jsonify(response)

    @app.route('/dbproj/login', methods=['PUT'])
    def login():
        try:
            payload = request.get_json()
        except Exception as e:
            logging.error(f"Error parsing JSON: {e}")
            return jsonify({'status': Config.STATUS_CODES['api_error'], 'results': 'Invalid JSON format', 'error': str(e)}), Config.STATUS_CODES['api_error']

        if 'username' not in payload or 'password' not in payload:
            return jsonify({'status': Config.STATUS_CODES['api_error'], 'results': 'username and password are required'}), Config.STATUS_CODES['api_error']

        username = payload['username']
        password = payload['password']

        conn = db_connection()
        cur = conn.cursor()

        try:
            cur.execute("SELECT * FROM verify_login(%s, %s)", (username, password))
            user = cur.fetchone()

            logging.debug(f"User fetched from DB: {user}")

            if user and check_password_hash(user[3], password):
                token = jwt.encode({
                    'user_id': user[0],
                    'username': user[1],
                    'user_type': user[2],
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
                }, app.config['SECRET_KEY'], algorithm="HS256")
                response = {'status': Config.STATUS_CODES['success'], 'token': token, 'user_type': user[2]}
            else:
                response = {'status': Config.STATUS_CODES['api_error'], 'results': 'Invalid credentials'}

            conn.commit()

        except (Exception, psycopg2.DatabaseError) as error:
            logging.error(error)
            response = {'status': Config.STATUS_CODES['internal_error'], 'errors': str(error)}
            conn.rollback()
        finally:
            if conn is not None:
                conn.close()

        return jsonify(response)