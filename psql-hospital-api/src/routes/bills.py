import psycopg2
import logging

from flask import request, jsonify
from db import db_connection
from auth import token_required
from config import Config


def register_routes(app):
    @app.route('/dbproj/bills/<int:bill_id>', methods=['POST'])
    @token_required
    def execute_payment(bill_id, current_user=None, user_type=None, user_id=None):
        logging.info(f'POST /bills/{bill_id} by user {current_user} (type: {user_type}, id: {user_id})')

        if user_type != 'patient':
            return jsonify({'status': Config.STATUS_CODES['api_error'], 'errors': 'Only patients can pay their own bills'}), Config.STATUS_CODES['api_error']

        payload = request.get_json()

        required_fields = ['amount', 'payment_method']
        for field in required_fields:
            if field not in payload:
                return jsonify({'status': Config.STATUS_CODES['api_error'], 'errors': f'Missing field: {field}'}), Config.STATUS_CODES['api_error']

        amount = payload['amount']
        payment_method = payload['payment_method']

        conn = db_connection()
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM process_payment(%s, %s, %s, %s)", (bill_id, user_id, amount, payment_method))
            result = cur.fetchone()

            if result is None:
                return jsonify({'status': Config.STATUS_CODES['api_error'], 'errors': 'Failed to process the payment'}), Config.STATUS_CODES['api_error']

            remaining_value = result[0]

            conn.commit()

            response = {'status': Config.STATUS_CODES['success'], 'results': {'remaining_value': remaining_value}}

        except (Exception, psycopg2.DatabaseError) as error:
            if conn:
                conn.rollback()
            logging.error(f'POST /bills/{bill_id} - error: {error}')
            response = {'status': Config.STATUS_CODES['internal_error'], 'errors': str(error)}
        finally:
            if conn:
                conn.close()

        return jsonify(response)
