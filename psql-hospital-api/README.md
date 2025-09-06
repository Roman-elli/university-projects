# 🏥 Hospital Management API  

This project was developed as part of a **university database project**. It is implemented in **Python** using **Flask** and connects to a **PostgreSQL** database to manage **patients, doctors, appointments, prescriptions, surgeries, and billing**.  

It provides a **REST API** with JWT-based authentication, allowing assistants, doctors, and patients to interact with the system securely.  

---

## 🚀 Features
- 🔑 **JWT Authentication** with role-based access (`patient`, `assistant`, `nurse`, `doctor`).  
- 🏥 **Patient management**: register, list appointments, and view prescriptions.  
- 🩺 **Doctor management**: schedule appointments, add prescriptions.  
- 📅 **Appointment and surgery scheduling** with automatic transaction handling.  
- 💰 **Billing and payments** for procedures and hospitalizations.  
- 📊 **Reports**: daily summary, monthly report, and top 3 patients by expenditure.  
- 🗄️ **Modular code structure**:
  - `src/routes/` → API endpoints, imported via `register_routes()`  
  - `src/services/` → business logic and helper functions  
  - `src/db/` → database connection  
  - `src/auth/` → JWT middleware  
  - `src/config.py` → configuration and constants  
  - `assets/src/table/` → SQL scripts to create tables  
  - `assets/src/functions/` → SQL stored procedures/functions  
  - `assets/src/triggers/` → SQL triggers  

- 📜 **Logging**: API logs are stored in `log_file.log` and also output to console
---

## ▶️ How to Run
1. Clone the repository

2. Install dependencies:

    pip install -r requirements.txt

3. Set up PostgreSQL database using the provided SQL scripts in assets/:

    - `table/createTable.sql`  
    - `functions/*.sql` (modularized by feature: auth, appointments, billing, reports, prescriptions)  
    - `triggers/*.sql` (modularized triggers for billing, appointments, username checks)  

4. Run the API:

    python src/main.py

5. Access the API at:

    http://127.0.0.1:8080/

📌 Notes

- API uses role-based access control, so endpoints are restricted by user type.
- JWT tokens expire in 1 hour by default.
- Example requests are provided in `docs/Project.postman_collections.json`.
- Database ER model is available in `docs/ERfinal.json`.
- This project is intended for academic purposes and demonstration of Python + Flask + PostgreSQL integration.