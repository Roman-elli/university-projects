import flask
import logging
import psycopg2
import json
import jwt
import datetime
from flask import request, jsonify
from flask_cors import CORS
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

app = flask.Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'your_secret_key'

StatusCodes = {
    'success': 200,
    'api_error': 400,
    'internal_error': 500
}

##########################################################
## DATABASE ACCESS
##########################################################

def db_connection():
    return psycopg2.connect(
        user='dbproject',
        password='dbproject',
        host='localhost',
        port='5432',
        database='dbproject'
    )

##########################################################
## JWT Middleware
##########################################################

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        try:
            token = token.split(" ")[1]  # Assuming the token is sent as "Bearer <token>"
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            kwargs['current_user'] = data['username']
            kwargs['user_type'] = data['user_type']
            kwargs['user_id'] = data['user_id']
        except Exception as e:
            return jsonify({'message': 'Token is invalid!'}), 403
        return f(*args, **kwargs)
    return decorated_function

##########################################################
## ENDPOINTS
##########################################################

@app.route('/')
def landing_page():
    return """
    Hello Teacher (Python Native)!  <br/>
    <br/>
    Main page of the Project!<br/>
    <br/>
    BD 2023-2024 Team<br/>
    <br/>
    """

@app.route('/dbproj/login', methods=['PUT'])
def login():
    try:
        payload = request.get_json()
    except Exception as e:
        logging.error(f"Error parsing JSON: {e}")
        return jsonify({'status': StatusCodes['api_error'], 'results': 'Invalid JSON format', 'error': str(e)}), StatusCodes['api_error']

    if 'username' not in payload or 'password' not in payload:
        return jsonify({'status': StatusCodes['api_error'], 'results': 'username and password are required'}), StatusCodes['api_error']

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
            response = {'status': StatusCodes['success'], 'token': token, 'user_type': user[2]}
        else:
            response = {'status': StatusCodes['api_error'], 'results': 'Invalid credentials'}

        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
        response = {'status': StatusCodes['internal_error'], 'errors': str(error)}
        conn.rollback()
    finally:
        if conn is not None:
            conn.close()

    return jsonify(response)


@app.route('/dbproj/register/<user_type>', methods=['POST'])
def add_register(user_type):
    logging.info(f'POST /register/{user_type}')
    payload = request.get_json()

    valid_user_types = ['patient', 'assistant', 'nurse', 'doctor']
    if user_type not in valid_user_types:
        return jsonify({'status': StatusCodes['api_error'], 'errors': 'Invalid user type'}), StatusCodes['api_error']

    logging.debug(f'POST /register/{user_type} - payload: {payload}')

    is_valid, error_message = validate_user(user_type, payload)
    if not is_valid:
        return jsonify({'status': StatusCodes['api_error'], 'errors': error_message}), StatusCodes['api_error']

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
        response = {'status': StatusCodes['success'], 'results': {'user_id': user_id}}

    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(f'POST /register/{user_type} - error: {error}')
        if "Username already exists" in str(error):
            response = {'status': StatusCodes['api_error'], 'errors': 'Username already exists'}
        else:
            response = {'status': StatusCodes['internal_error'], 'errors': str(error)}
        conn.rollback()
    finally:
        if conn is not None:
            conn.close()

    return jsonify(response)

def validate_user(user_type, payload):
    fields_required = {
        'doctor': ['license', 'start_date', 'due_date', 'salary', 'name', 'email', 'phone', 'username', 'password'],
        'nurse': ['hierarchy', 'start_date', 'due_date', 'salary', 'name', 'email', 'phone', 'username', 'password'],
        'patient': ['name', 'email', 'phone', 'username', 'password'],
        'assistant': ['start_date', 'due_date', 'salary', 'name', 'email', 'phone', 'username', 'password']
    }
    missing_fields = [field for field in fields_required[user_type] if field not in payload]
    if missing_fields:
        return False, f'Missing fields: {", ".join(missing_fields)}'
    return True, None



@app.route('/dbproj/appointments/<int:patient_user_id>', methods=['GET'])
@token_required
def get_appointments(current_user, user_type, user_id, patient_user_id):
    if user_type != 'assistant' and user_type != 'patient':
        return jsonify({'status': StatusCodes['api_error'], 'errors': 'Only assistants and patients can access this endpoint'}), StatusCodes['api_error']

    if user_type == 'patient' and user_id != patient_user_id:
        return jsonify({'status': StatusCodes['api_error'], 'errors': 'Patients can only see their own appointments'}), StatusCodes['api_error']

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

        response = {'status': StatusCodes['success'], 'results': results}

    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(f'GET /appointments/{patient_user_id} - error: {error}')
        response = {'status': StatusCodes['internal_error'], 'errors': str(error)}

    finally:
        if conn is not None:
            conn.close()

    return jsonify(response)


@app.route('/dbproj/prescription/', methods=['POST'])
@token_required
def add_prescription(current_user=None, user_type=None, user_id=None):
    logger.info('POST /prescription')

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
        logger.error(f'POST /prescription - error: {error}')
        response = {'status': 500, 'errors': str(error)}
    finally:
        if conn:
            conn.close()

    return jsonify(response)



@app.route('/dbproj/daily/<string:date>', methods=['GET'])
@token_required
def daily_summary(date, current_user=None, user_type=None, user_id=None):
    logging.info(f'GET /daily/{date}')

    if user_type != 'assistant':
        return jsonify({'status': StatusCodes['api_error'], 'errors': 'Only assistants can use this endpoint'}), StatusCodes['api_error']

    conn = db_connection()
    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM get_daily_summary(%s)", (date,))
        result = cur.fetchone()

        response = {
            'status': StatusCodes['success'],
            'results': {
                'total_hospitalizations': result[0],
                'total_surgeries': result[1],
                'total_prescriptions': result[2],
                'total_amount_spent': result[3]
            }
        }

    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(f'GET /daily/{date} - error: {error}')
        response = {'status': StatusCodes['internal_error'], 'errors': str(error)}
    finally:
        if conn is not None:
            conn.close()

    return jsonify(response)


@app.route('/dbproj/surgery', methods=['POST'])
@app.route('/dbproj/surgery/<int:hospitalization_id>', methods=['POST'])
@token_required
def schedule_surgery(hospitalization_id=None, current_user=None, user_type=None, user_id=None):
    if user_type != 'assistant':
        return jsonify({'status': StatusCodes['api_error'], 'errors': 'Only assistants can use this endpoint'}), StatusCodes['api_error']
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


@app.route('/dbproj/report', methods=['GET'])
@token_required
def generate_monthly_report(current_user=None, user_type=None, user_id=None):
    if user_type != 'assistant':
        return jsonify({'status': StatusCodes['api_error'], 'errors': 'Only assistants can generate this report'}), StatusCodes['api_error']

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

        response = {'status': StatusCodes['success'], 'results': report}

    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(f'GET /report - error: {error}')
        response = {'status': StatusCodes['internal_error'], 'errors': str(error)}
        conn.rollback()
    finally:
        if conn is not None:
            conn.close()

    return jsonify(response)



@app.route('/dbproj/bills/<int:bill_id>', methods=['POST'])
@token_required
def execute_payment(bill_id, current_user=None, user_type=None, user_id=None):
    logger.info(f'POST /bills/{bill_id} by user {current_user} (type: {user_type}, id: {user_id})')

    if user_type != 'patient':
        return jsonify({'status': StatusCodes['api_error'], 'errors': 'Only patients can pay their own bills'}), StatusCodes['api_error']

    payload = request.get_json()

    required_fields = ['amount', 'payment_method']
    for field in required_fields:
        if field not in payload:
            return jsonify({'status': StatusCodes['api_error'], 'errors': f'Missing field: {field}'}), StatusCodes['api_error']

    amount = payload['amount']
    payment_method = payload['payment_method']

    conn = db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM process_payment(%s, %s, %s, %s)", (bill_id, user_id, amount, payment_method))
        result = cur.fetchone()

        if result is None:
            return jsonify({'status': StatusCodes['api_error'], 'errors': 'Failed to process the payment'}), StatusCodes['api_error']

        remaining_value = result[0]

        conn.commit()

        response = {'status': StatusCodes['success'], 'results': {'remaining_value': remaining_value}}

    except (Exception, psycopg2.DatabaseError) as error:
        if conn:
            conn.rollback()
        logger.error(f'POST /bills/{bill_id} - error: {error}')
        response = {'status': StatusCodes['internal_error'], 'errors': str(error)}
    finally:
        if conn:
            conn.close()

    return jsonify(response)


@app.route('/dbproj/top3', methods=['GET'])
@token_required
def get_top3_patients(current_user=None, user_type=None, user_id=None):
    logger.info('GET /top3')

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
        logger.error(f'GET /top3 - error: {error}')
        response = {'status': 500, 'errors': str(error)}
    finally:
        if conn:
            conn.close()

    return jsonify(response)

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


if __name__ == '__main__':
    logging.basicConfig(filename='log_file.log', level=logging.DEBUG)
    logger = logging.getLogger('logger')
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s [%(levelname)s]:  %(message)s', '%H:%M:%S')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    host = '127.0.0.1'
    port = 8080
    app.run(host=host, debug=True, threaded=True, port=port)
    logger.info(f'API v1.0 online: http://{host}:{port}')
