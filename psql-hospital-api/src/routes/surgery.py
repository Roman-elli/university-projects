from flask import request, jsonify
from db import db_connection
from auth import token_required
from config import Config


def register_routes(app):
    @app.route('/dbproj/surgery', methods=['POST'])
    @app.route('/dbproj/surgery/<int:hospitalization_id>', methods=['POST'])
    @token_required
    def schedule_surgery(hospitalization_id=None, current_user=None, user_type=None, user_id=None):
        if user_type != 'assistant':
            return jsonify({'status': Config.STATUS_CODES['api_error'], 'errors': 'Only assistants can use this endpoint'}), Config.STATUS_CODES['api_error']
        data = request.json
        patient_id = data.get('patient_id')
        doctor_id = data.get('doctor_id')
        nurses = data.get('nurses', [])
        date = data.get('date')
        duration = data.get('duration')
        cost = data.get('cost')

        # Extract nurse IDs and roles from the nested list
        nurse_ids = [nurse[0] for nurse in nurses]
        roles = [nurse[1] for nurse in nurses]

        conn = db_connection()
        cur = conn.cursor()

        try:
            # Iniciar transação
            conn.autocommit = False

            # Chamar a função PostgreSQL
            cur.execute("""
                SELECT * FROM schedule_surgery_fn(%s, %s, %s, %s, %s, %s, %s, %s)
            """, (patient_id, doctor_id, nurse_ids, roles, date, duration, cost, hospitalization_id))

            result = cur.fetchone()
            if result is None:
                raise Exception("Failed to create surgery or hospitalization")

            hospitalization_id, surgery_id, bill_id = result
            print(f"Surgery ID: {surgery_id}, Bill ID: {bill_id}, Hospitalization ID: {hospitalization_id}")  # Debug

            # Confirmar transação
            conn.commit()
            return jsonify({
                "status": "success",
                "errors": None,
                "results": {
                    "hospitalization_id": hospitalization_id,
                    "surgery_id": surgery_id,
                    "bill_id": bill_id,
                    "patient_id": patient_id,
                    "doctor_id": doctor_id,
                    "date": date
                }
            }), 201

        except Exception as e:
            # Reverter transação em caso de erro
            conn.rollback()
            print(f"Error: {str(e)}")  # Debug
            return jsonify({"status": "error", "errors": str(e)}), 400

        finally:
            cur.close()
            conn.close()

