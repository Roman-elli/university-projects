
import logging
import psycopg2

from flask import jsonify
from db import db_connection
from auth import token_required
from config import Config

def register_routes(app):
    
    @app.route('/dbproj/daily/<string:date>', methods=['GET'])
    @token_required
    def daily_summary(date, current_user=None, user_type=None, user_id=None):
        logging.info(f'GET /daily/{date}')

        if user_type != 'assistant':
            return jsonify({'status': Config.STATUS_CODES['api_error'], 'errors': 'Only assistants can use this endpoint'}), Config.STATUS_CODES['api_error']

        conn = db_connection()
        cur = conn.cursor()

        try:
            cur.execute("SELECT * FROM get_daily_summary(%s)", (date,))
            result = cur.fetchone()

            response = {
                'status': Config.STATUS_CODES['success'],
                'results': {
                    'total_hospitalizations': result[0],
                    'total_surgeries': result[1],
                    'total_prescriptions': result[2],
                    'total_amount_spent': result[3]
                }
            }

        except (Exception, psycopg2.DatabaseError) as error:
            logging.error(f'GET /daily/{date} - error: {error}')
            response = {'status': Config.STATUS_CODES['internal_error'], 'errors': str(error)}
        finally:
            if conn is not None:
                conn.close()

        return jsonify(response)
    
    
    @app.route('/dbproj/report', methods=['GET'])
    @token_required
    def generate_monthly_report(current_user=None, user_type=None, user_id=None):
        if user_type != 'assistant':
            return jsonify({'status': Config.STATUS_CODES['api_error'], 'errors': 'Only assistants can generate this report'}), Config.STATUS_CODES['api_error']

        conn = db_connection()
        cur = conn.cursor()

        try:
            cur.execute("SELECT * FROM get_monthly_report()")
            results = cur.fetchall()

            report = []
            for row in results:
                report.append({
                    "month": row[0],
                    "doctor": row[1],
                    "surgeries": row[2]
                })

            response = {'status': Config.STATUS_CODES['success'], 'results': report}

        except (Exception, psycopg2.DatabaseError) as error:
            logging.error(f'GET /report - error: {error}')
            response = {'status': Config.STATUS_CODES['internal_error'], 'errors': str(error)}
            conn.rollback()
        finally:
            if conn is not None:
                conn.close()

        return jsonify(response)
    
    @app.route('/dbproj/top3', methods=['GET'])
    @token_required
    def get_top3_patients(current_user=None, user_type=None, user_id=None):
        logging.info('GET /top3')

        if user_type != 'assistant':
            return jsonify({'status': 400, 'errors': 'Only assistants can use this endpoint'}), 400

        conn = db_connection()
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM top3()")
            results = cur.fetchall()

            if not results:
                return jsonify({'status': 404, 'errors': 'No data found'}), 404

            top3_patients = []
            for row in results:
                patient_name, amount_spent, procedure_id, doctor_id, procedure_date, cost, procedure_type = row
                patient_info = next((p for p in top3_patients if p['patient_name'] == patient_name), None)
                if not patient_info:
                    patient_info = {
                        'patient_name': patient_name,
                        'amount_spent': amount_spent,
                        'procedures': []
                    }
                    top3_patients.append(patient_info)
                patient_info['procedures'].append({
                    'id': procedure_id,
                    'doctor_id': doctor_id,
                    'date': procedure_date,
                    'cost': cost,
                    'type': procedure_type
                })

            response = {'status': 200, 'results': top3_patients}

        except (Exception, psycopg2.DatabaseError) as error:
            if conn:
                conn.rollback()
            logging.error(f'GET /top3 - error: {error}')
            response = {'status': 500, 'errors': str(error)}
        finally:
            if conn:
                conn.close()

        return jsonify(response)


