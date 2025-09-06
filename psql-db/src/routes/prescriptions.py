import psycopg2
import json
import logging

from flask import request, jsonify
from db import db_connection
from auth import token_required

def register_routes(app):
    @app.route('/dbproj/prescriptions/<int:person_id>', methods=['GET'])
    @token_required
    def get_prescriptions(current_user=None, user_type=None, user_id=None, person_id=None):
        # Check if the user is authorized
        if user_type == 'patient' and user_id != person_id:
            return jsonify({"status": 403, "errors": "Patients can only view their own prescriptions."}), 403
        if user_type != 'patient':
            return jsonify({"status": 403, "errors": "Only patients can use this endpoint."}), 403

        try:
            conn = db_connection()
            cur = conn.cursor()

            cur.execute("SELECT * FROM get_prescriptions_for_patient(%s);", (person_id,))
            prescriptions = cur.fetchall()
            cur.close()
            conn.close()

            # Formatting the results as specified
            formatted_prescriptions = []
            for prescription in prescriptions:
                formatted_prescriptions.append({
                    "id": prescription[0],
                    "validity": prescription[1],
                    "posology": prescription[2]
                })

            return jsonify({"status": 200, "results": formatted_prescriptions}), 200
        except Exception as e:
            print(f"Error: {e}")
            return jsonify({"status": 500, "errors": str(e)}), 500
        

    @app.route('/dbproj/prescription/', methods=['POST'])
    @token_required
    def add_prescription(current_user=None, user_type=None, user_id=None):
        logging.info('POST /prescription')

        if user_type != 'doctor':
            return jsonify({'status': 400, 'errors': 'Only doctors can use this endpoint'}), 400

        payload = request.get_json()

        # Campos obrigatórios
        required_fields = ['type', 'event_id', 'validity', 'medicines']
        for field in required_fields:
            if field not in payload:
                return jsonify({'status': 400, 'errors': f'Missing field: {field}'}), 400

        prescription_type = payload['type']
        event_id = payload['event_id']
        validity = payload['validity']
        medicines = payload['medicines']

        if prescription_type not in ['hospitalization', 'appointment']:
            return jsonify({'status': 400, 'errors': 'Invalid prescription type'}), 400

        conn = db_connection()
        cur = conn.cursor()
        try:
            # Chamar a função PostgreSQL
            cur.execute("SELECT * FROM add_prescription(%s, %s, %s, %s::jsonb)", 
                        (prescription_type, event_id, validity, json.dumps(medicines)))
            result = cur.fetchone()

            if not result:
                return jsonify({'status': 500, 'errors': 'Failed to insert prescription'}), 500
            
            prescription_id = result[0]

            conn.commit()
            response = {'status': 200, 'results': {'prescription_id': prescription_id}}

        except (Exception, psycopg2.DatabaseError) as error:
            if conn:
                conn.rollback()
            logging.error(f'POST /prescription - error: {error}')
            response = {'status': 500, 'errors': str(error)}
        finally:
            if conn:
                conn.close()

        return jsonify(response)