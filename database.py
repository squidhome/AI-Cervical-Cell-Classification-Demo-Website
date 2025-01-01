import sqlite3
import hashlib
import os
import sqlite3
from datetime import datetime
import pytz

# Function to initialize the database and create tables
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Create Users table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id TEXT PRIMARY KEY, -- ID seperti D1, P1, A1
                        username TEXT NOT NULL,
                        name TEXT NOT NULL,
                        email TEXT NOT NULL UNIQUE,
                        password TEXT NOT NULL,
                        birthdate DATE NOT NULL,
                        role TEXT NOT NULL -- 'doctor', 'patient', 'admin'
                    )''')

    # Create Classification Results table
    cursor.execute('''CREATE TABLE IF NOT EXISTS classification_results (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id TEXT NOT NULL, -- ID pasien (format: P1, P2, etc.)
                        doctor_id TEXT NOT NULL, -- ID dokter (format: D1, D2, etc.)
                        image_path TEXT NOT NULL,
                        classification TEXT NOT NULL,
                        confidence REAL NOT NULL,
                        cancer_stadium TEXT NOT NULL,  -- TEXT type to store values like '1', '2', '3', '4', or 'None'
                        cell_percentage REAL NOT NULL,  -- Float value for cell percentage
                        diagnosis TEXT NOT NULL,
                        conclusion TEXT NOT NULL,
                        treatment TEXT NOT NULL,
                        suggestions TEXT NOT NULL,
                        referral_letter TEXT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL, -- Waktu diagnosis dilakukan (default: waktu saat ini)
                        FOREIGN KEY(user_id) REFERENCES users(id)
                    )''')

    conn.commit()
    conn.close()

# Hash password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Generate User ID (Doctor -> D1, Patient -> P1, Admin -> A1)
def generate_user_id(role):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Hitung jumlah pengguna dengan role tertentu
    cursor.execute("SELECT COUNT(*) FROM users WHERE role = ?", (role,))
    count = cursor.fetchone()[0]

    # Tetapkan prefix ID berdasarkan role
    prefix_map = {"doctor": "D", "patient": "P", "admin": "A"}
    prefix = prefix_map.get(role, "U")  # Default 'U' for unknown role

    # Generate new ID (e.g., D1, P1, A1)
    user_id = f"{prefix}{count + 1}"

    conn.close()
    return user_id

# Add user
def add_user(user_id, name, username, email, password, birth_date, role):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (id, username, name, email, password, birthdate, role) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (user_id, username, name, email, hash_password(password), birth_date, role))
    conn.commit()
    conn.close()

# Validate user login
def validate_user(email, password):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", 
                   (email, hash_password(password)))
    user = cursor.fetchone()
    conn.close()
    return user

# Fungsi untuk memperbarui password di database
def update_forget_password(email, new_password):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE users 
        SET password = ? 
        WHERE email = ?
    """, (hash_password(new_password), email))
    conn.commit()
    conn.close()

# Fungsi untuk memeriksa password lama
def verify_old_password(user_id, old_password):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE id = ?", (user_id,))
    stored_password = cursor.fetchone()
    conn.close()
    
    if stored_password and stored_password[0] == hash_password(old_password):
        return True
    return False

# Fungsi untuk mengganti password
def update_password_profile(user_id, new_password):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET password = ? WHERE id = ?", (hash_password(new_password), user_id))
    conn.commit()
    conn.close()

# Fungsi untuk mendapatkan timestamp dalam WIB
def get_wib_timestamp():
    utc_now = datetime.now(pytz.utc)  # Ambil waktu saat ini dalam UTC
    wib = pytz.timezone("Asia/Jakarta")  # Zona waktu WIB
    wib_now = utc_now.astimezone(wib)  # Konversi ke WIB
    return wib_now.strftime("%Y-%m-%d %H:%M:%S")  # Format sesuai kebutuhan

def save_additional_information(result, doctor_id, cancer_stadium, cell_percentage, diagnosis, conclusion, treatment, suggestions, referral_letter):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    image_filename = save_image(result['image_path'])

    # Save referral letter if uploaded
    if referral_letter is not None:
        referral_filename = save_referral_letter(referral_letter)

    timestamp = '2024-06-09'

    cursor.execute('''INSERT INTO classification_results (
                        user_id, doctor_id, image_path, classification, confidence, cancer_stadium, cell_percentage, diagnosis, 
                        conclusion, treatment, suggestions, referral_letter, timestamp
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
                        result['patient_id'], doctor_id, image_filename, result['classification'], result['confidence'],
                        cancer_stadium, cell_percentage, diagnosis, conclusion, ', '.join(treatment), suggestions, 
                        referral_filename if referral_letter else None, timestamp
                    ))

    conn.commit()
    conn.close()

def save_image(image):
    if not os.path.exists("uploads/images"):
        os.makedirs("uploads/images")
    
    # Save PDF file to disk
    image_filename = f"uploads/images/{image.name}"
    with open(image_filename, "wb") as f:
        f.write(image.getbuffer())
    
    return image_filename
 
# Function to save referral letter (PDF)
def save_referral_letter(referral_letter):
    if not os.path.exists("uploads/referral_letters"):
        os.makedirs("uploads/referral_letters")
    
    # Save PDF file to disk
    referral_filename = f"uploads/referral_letters/{referral_letter.name}"
    with open(referral_filename, "wb") as f:
        f.write(referral_letter.getbuffer())
    
    return referral_filename

# Statistik dokter
def get_doctor_statistics():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    query = """
    SELECT 
        c.doctor_id,
        u.username AS doctor_username,
        u.name AS doctor_name,
        u.birthdate AS doctor_birthdate,
        COUNT(DISTINCT c.user_id) AS total_patients,
        SUM(CASE WHEN c.user_id IS NOT NULL THEN 1 ELSE 0 END) AS diagnosed_patients
    FROM 
        classification_results c
    JOIN 
        users u ON c.doctor_id = u.id
    WHERE 
        u.role = 'doctor'
    GROUP BY 
        c.doctor_id;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Fungsi untuk mendapatkan daftar pasien dari database
def get_patient_ids():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    query = "SELECT id, username, name, birthdate FROM users WHERE role = 'patient'"
    cursor.execute(query)
    patients = cursor.fetchall()  # Mengembalikan [(id1, name1), (id2, name2), ...]
    conn.close()
    return patients

# Fungsi untuk menghitung jumlah hasil diagnosis pasien
def get_diagnosis_count(patient_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    query = "SELECT COUNT(*) FROM classification_results WHERE user_id = ?"
    cursor.execute(query, (patient_id,))
    count = cursor.fetchone()[0]  # Ambil jumlah diagnosis
    conn.close()
    return count

