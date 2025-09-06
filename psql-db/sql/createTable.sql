
CREATE TABLE patient (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(512) NOT NULL,
    email TEXT,
    phone BIGINT,
    username VARCHAR(512) NOT NULL,
    password VARCHAR(512) NOT NULL,
    UNIQUE (username)
);

CREATE TABLE doctor (
    id BIGSERIAL PRIMARY KEY,
    license TEXT NOT NULL,
    start_date DATE NOT NULL,
    due_date DATE NOT NULL,
    salary INTEGER NOT NULL,
    name VARCHAR(512) NOT NULL,
    email TEXT,
    phone BIGINT,
    username VARCHAR(512) NOT NULL,
    password VARCHAR(512) NOT NULL,
    UNIQUE (license, username)
);

CREATE TABLE nurse (
    id BIGSERIAL PRIMARY KEY,
    hierarchy INTEGER,
    start_date DATE NOT NULL,
    due_date DATE NOT NULL,
    salary INTEGER NOT NULL,
    name VARCHAR(512) NOT NULL,
    email TEXT,
    phone BIGINT,
    username VARCHAR(512) NOT NULL,
    password VARCHAR(512) NOT NULL,
    UNIQUE (username)
);

CREATE TABLE assistant (
    id BIGSERIAL PRIMARY KEY,
    start_date DATE NOT NULL,
    due_date DATE NOT NULL,
    salary INTEGER NOT NULL,
    name VARCHAR(512) NOT NULL,
    email TEXT,
    phone BIGINT,
    username VARCHAR(512) NOT NULL,
    password VARCHAR(512) NOT NULL,
    UNIQUE (username)
);

CREATE TABLE appointment (
    id BIGSERIAL PRIMARY KEY,
    cost FLOAT(8),
    duration BIGINT NOT NULL,
    clinical_date TIMESTAMP NOT NULL,
    bill_id BIGINT NOT NULL,
    patient_id BIGINT NOT NULL,
    doctor_id BIGINT NOT NULL
);

CREATE TABLE hospitalization (
    id BIGSERIAL PRIMARY KEY,
    duration BIGINT,
    start_date TIMESTAMP NOT NULL,
    bill_id BIGINT,
    patient_id BIGINT NOT NULL,
    nurse_id BIGINT NOT NULL
);

CREATE TABLE surgery (
    id BIGSERIAL PRIMARY KEY,
    hospitalization_id BIGINT NOT NULL,
    cost FLOAT(8),
    duration BIGINT NOT NULL,
    clinical_date TIMESTAMP NOT NULL,
    bill_id BIGINT NOT NULL,
    patient_id BIGINT NOT NULL,
    doctor_id BIGINT NOT NULL
);

CREATE TABLE prescription (
    id BIGSERIAL PRIMARY KEY,
    validity DATE NOT NULL
);

CREATE TABLE medicine (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(512),
    composition TEXT
);

CREATE TABLE dosage (
    period INTEGER,
    amount TEXT,
    medicine_id BIGINT,
    prescription_id BIGINT,
    PRIMARY KEY(medicine_id, prescription_id)
);

CREATE TABLE probsev (
    probability INTEGER,
    severity INTEGER,
    side_effect_id BIGINT,
    medicine_id BIGINT,
    PRIMARY KEY(side_effect_id, medicine_id)
);

CREATE TABLE side_effect (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(512),
    details TEXT
);

CREATE TABLE medical_field (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(512)
);

CREATE TABLE bill (
    id BIGSERIAL PRIMARY KEY,
    total_cost BIGINT,
    type BOOL NOT NULL,
    patient_id BIGINT NOT NULL,
    UNIQUE (id, patient_id)
);

CREATE TABLE payment (
    amount INTEGER,
    payment_time DATE,
    patient_id BIGINT,
    bill_id BIGINT,
    method VARCHAR(512),
    PRIMARY KEY(patient_id, bill_id)
);


CREATE TABLE functionalities (
    functionality VARCHAR(512) NOT NULL,
    surgery_id BIGINT,
    nurse_id BIGINT,
    PRIMARY KEY(surgery_id, nurse_id)
);

CREATE TABLE medical_field_association (
    field_id BIGINT,
    related_field_id BIGINT NOT NULL,
    PRIMARY KEY(field_id)
);

CREATE TABLE doctor_medical_field (
    doctor_id BIGINT,
    field_id BIGINT,
    PRIMARY KEY(doctor_id, field_id)
);

CREATE TABLE hospitalization_prescription (
    hospitalization_id BIGINT,
    prescription_id BIGINT NOT NULL,
    PRIMARY KEY(hospitalization_id)
);

CREATE TABLE appointment_prescription (
    appointment_id BIGINT,
    prescription_id BIGINT NOT NULL,
    PRIMARY KEY(appointment_id)
);

-- Manter a estrutura dos ALTER TABLEs
ALTER TABLE appointment ADD UNIQUE (bill_id, patient_id);
ALTER TABLE appointment ADD CONSTRAINT appointment_fk1 FOREIGN KEY (bill_id, patient_id) REFERENCES bill(id, patient_id);
ALTER TABLE appointment ADD CONSTRAINT appointment_fk2 FOREIGN KEY (doctor_id) REFERENCES doctor(id);
ALTER TABLE hospitalization ADD CONSTRAINT hospitalization_fk2 FOREIGN KEY (nurse_id) REFERENCES nurse(id);
ALTER TABLE surgery ADD UNIQUE (bill_id, patient_id);
ALTER TABLE surgery ADD CONSTRAINT surgery_fk1 FOREIGN KEY (hospitalization_id) REFERENCES hospitalization(id);
ALTER TABLE surgery ADD CONSTRAINT surgery_fk3 FOREIGN KEY (doctor_id) REFERENCES doctor(id);
ALTER TABLE dosage ADD CONSTRAINT dosage_fk1 FOREIGN KEY (medicine_id) REFERENCES medicine(id);
ALTER TABLE dosage ADD CONSTRAINT dosage_fk2 FOREIGN KEY (prescription_id) REFERENCES prescription(id);
ALTER TABLE probsev ADD CONSTRAINT probsev_fk1 FOREIGN KEY (side_effect_id) REFERENCES side_effect(id);
ALTER TABLE probsev ADD CONSTRAINT probsev_fk2 FOREIGN KEY (medicine_id) REFERENCES medicine(id);
ALTER TABLE bill ADD CONSTRAINT bill_fk1 FOREIGN KEY (patient_id) REFERENCES patient(id);
ALTER TABLE payment ADD CONSTRAINT payment_fk1 FOREIGN KEY (patient_id) REFERENCES patient(id);
ALTER TABLE payment ADD CONSTRAINT payment_fk2 FOREIGN KEY (bill_id, patient_id) REFERENCES bill(id, patient_id);
ALTER TABLE functionalities ADD CONSTRAINT functionalities_fk1 FOREIGN KEY (surgery_id) REFERENCES surgery(id);
ALTER TABLE functionalities ADD CONSTRAINT funcionalidades_fk2 FOREIGN KEY (nurse_id) REFERENCES nurse(id);
ALTER TABLE medical_field_association ADD CONSTRAINT medical_field_association_fk1 FOREIGN KEY (field_id) REFERENCES medical_field(id);
ALTER TABLE medical_field_association ADD CONSTRAINT medical_field_association_fk2 FOREIGN KEY (related_field_id) REFERENCES medical_field(id);
ALTER TABLE doctor_medical_field ADD CONSTRAINT doctor_medical_field_fk1 FOREIGN KEY (doctor_id) REFERENCES doctor(id);
ALTER TABLE doctor_medical_field ADD CONSTRAINT doctor_medical_field_fk2 FOREIGN KEY (field_id) REFERENCES medical_field(id);
ALTER TABLE hospitalization_prescription ADD UNIQUE (prescription_id);
ALTER TABLE hospitalization_prescription ADD CONSTRAINT hospitalization_prescription_fk1 FOREIGN KEY (hospitalization_id) REFERENCES hospitalization(id);
ALTER TABLE hospitalization_prescription ADD CONSTRAINT hospitalization_prescription_fk2 FOREIGN KEY (prescription_id) REFERENCES prescription(id);
ALTER TABLE appointment_prescription ADD UNIQUE (prescription_id);
ALTER TABLE appointment_prescription ADD CONSTRAINT appointment_prescription_fk1 FOREIGN KEY (appointment_id) REFERENCES appointment(id);
ALTER TABLE appointment_prescription ADD CONSTRAINT appointment_prescription_fk2 FOREIGN KEY (prescription_id) REFERENCES prescription(id);
ALTER TABLE medicine ADD CONSTRAINT unique_medicine_name UNIQUE (name);