import psycopg2
import logging

from flask import request, jsonify
from db import db_connection
from auth import token_required
from config import Config

def register_routes(app):
    @app.route('/dbproj/appointments/<int:patient_user_id>', methods=['GET'])
    @token_required
    def get_appointments(current_user, user_type, user_id, patient_user_id):
        if user_type != 'assistant' and user_type != 'patient':
            return jsonify({'status': Config.STATUS_CODES['api_error'], 'errors': 'Only assistants and patients can access this endpoint'}), Config.STATUS_CODES['api_error']

        if user_type == 'patient' and user_id != patient_user_id:
            return jsonify({'status': Config.STATUS_CODES['api_error'], 'errors': 'Patients can only see their own appointments'}), Config.STATUS_CODES['api_error']

        logging.info(f'GET /appointments/{patient_user_id}')

        conn = db_connection()
        cur = conn.cursor()

        try:
            cur.execute("SELECT * FROM get_patient_appointments(%s)", (patient_user_id,))
            rows = cur.fetchall()

            results = []
            for row in rows:
                results.append({
                    'appointment_id': row[0],
                    'doctor_id': row[1],
                    'date': row[2],
                    'doctor_name': row[3]
                })

            response = {'status': Config.STATUS_CODES['success'], 'results': results}

        except (Exception, psycopg2.DatabaseError) as error:
            logging.error(f'GET /appointments/{patient_user_id} - error: {error}')
            response = {'status': Config.STATUS_CODES['internal_error'], 'errors': str(error)}

        finally:
            if conn is not None:
                conn.close()

        return jsonify(response)
    
    @app.route('/dbproj/appointment', methods=['POST'])
    @token_required
    def create_appointment(current_user=None, user_type=None, user_id=None):
        if user_type != 'patient':
            return jsonify({"status": 403, "errors": "Unauthorized access"}), 403

        try:
            data = request.get_json()
            doctor_id = data['doctor_id']
            date = data['date']
            duration = data['duration']
            cost = data['cost']

            conn = db_connection()
            cur = conn.cursor()
            cur.execute("SELECT create_appointment(%s, %s, %s, %s, %s);", (user_id, doctor_id, date, duration, cost))
            appointment_id = cur.fetchone()[0]
            conn.commit()
            cur.close()
            conn.close()

            return jsonify({"status": 200, "results": appointment_id}), 200
        except Exception as e:
            print(f"Error: {e}")
            return jsonify({"status": 500, "errors": str(e)}), 500

