import streamlit as st
import sqlite3
import os
import smtplib
import random
import string
from dotenv import load_dotenv
from pathlib import Path
from datetime import date
import time
from database import generate_user_id, validate_user, add_user, verify_old_password, update_password_profile, update_forget_password

DEMO = True

def login():
    st.title("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = validate_user(email, password)
        if user:
            st.session_state.authenticated = True
            st.session_state.user_id = user[0]
            st.session_state.username = user[1]
            st.session_state.role = user[6]
            st.success(f"Welcome back, {user[1]}!")
            st.write("The page will be refreshed in 1 minute.")
            # Delay before rerun
            time.sleep(1)
            # Rerun the page after delay
            st.rerun()
        else:
            st.error("Invalid email or password.")

def signup():
    st.title("Sign Up")
    username = st.text_input("Username")
    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    birth_date = st.date_input("Birth Date", min_value = date(1900, 1, 1), max_value = date.today())
    role = st.selectbox("Role", ["doctor", "patient", "admin"])
    if st.button("Sign Up"):
        if username and email and password and birth_date:
            user_id = generate_user_id(role)

            try:
                add_user(user_id, name, username, email, password, birth_date, role)
                st.success("Account created successfully! Please log in.")
            except sqlite3.IntegrityError:
                st.error("Email already exists. Please use a different email.")
        else:
            st.error("Please fill out all fields!")

# Fungsi untuk mengirim password baru (menggunakan Mailtrap untuk testing)
def send_new_password_email(receiver_email, new_password):
    load_dotenv(Path('.gitignore/.env'))
    mailtrap_host = os.getenv('MAILTRAP_HOST')
    mailtrap_port = os.getenv('MAILTRAP_PORT')
    mailtrap_username = os.getenv('MAILTRAP_USERNAME')
    mailtrap_password = os.getenv('MAILTRAP_PASSWORD')

    print(f"Mailtrap Host: {mailtrap_host}")
    print(f"Mailtrap Port: {mailtrap_port}")
    print(f"Mailtrap Username: {mailtrap_username}")
    print(f"Mailtrap Password: {mailtrap_password}")

    
    sender = "Private Person <noreply@example.com>"  # Dummy sender email address
    receiver = f"Private Person <{receiver_email}>" # Dummy receiver email address
    message = f"""\
        Subject: Your New Password
        To: {receiver}
        From: {sender}

        Your new temporary password is: {new_password}\n
        Please login using this password and change it immediately."""
    
    try:
        with smtplib.SMTP(mailtrap_host, mailtrap_port) as server:
            server.set_debuglevel(1)  # Aktifkan debugging log
            # print("Connected to SMTP server")
            server.starttls()
            # print("Started TLS encryption")
            server.login(mailtrap_username, mailtrap_password)
            # print("Logged in successfully")
            server.sendmail(sender, receiver, message)
            # print("Email sent successfully")
        st.success(f"A new password has been sent to {receiver_email}.")
        return True
    except Exception as e:
        st.error(f"Error: {e}")
        return False

# Fungsi untuk menghasilkan password random
def generate_random_password(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# Halaman untuk reset password
def forgot_password():
    st.title("Forget Password")

    # Meminta email pengguna
    email = st.text_input("Enter your registered email address:")
    if st.button("Reset Password"):
        # Periksa apakah email ada dalam database
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            # Hasilkan password baru
            new_password = generate_random_password()
            
            # Perbarui password di database
            update_forget_password(email, new_password)
            
            # Kirim password baru ke email pengguna
            if send_new_password_email(email, new_password):
                st.success("A temporary password has been sent to your email. Please log in and change your password.")
        else:
            st.error("Email not found in our records.")

# Fungsi untuk menentukan style card berdasarkan diagnosis
def get_card_style():
    return """
    <style>
    .custom-card {
        background-color: rgba(255, 255, 255, 0.9);
        border: 2px solid grey;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        margin: 5px 0px 30px 0;
    }
    .custom-card h3 {
        color: black;
    }
    .custom-card p {
        color: black;
    }
    </style>
    """

def profile(user_id):
    st.title("Profile")

    # Koneksi ke database
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Ambil data user berdasarkan ID
    query = "SELECT id, username, name, email, birthdate, role FROM users WHERE id = ?"
    cursor.execute(query, (user_id,))
    user = cursor.fetchone()

    if not user:
        st.error("User not found!")
        return

    # Menyisipkan CSS
    st.markdown(get_card_style(), unsafe_allow_html=True)

    # Checkbox untuk toggle show/hide password
    show_profile = st.checkbox("Show Profile", value=False)

    # Menampilkan diagnosis dalam card
    st.markdown(
        f"""
        <div class="custom-card">
            <p><strong>ID:</strong> {"*" * len(user[0]) if not show_profile and user[0] else user[0]}</p>
            <p><strong>Username:</strong> {"*" * len(user[1]) if not show_profile and user[1] else user[1]}</p>
            <p><strong>Name:</strong> {"*" * len(user[2]) if not show_profile and user[2] else user[2]}</p>
            <p><strong>Email:</strong> {"*" * len(user[3]) if not show_profile and user[3] else user[3]}</p>
            <p><strong>Birth Date:</strong> {"*" * len(user[4]) if not show_profile and user[4] else user[4]}</p>
            <p><strong>Role:</strong> {"*" * len(user[5]) if not show_profile and user[5] else user[5]}</p>
        </div>
        """, unsafe_allow_html=True
    )

    if not DEMO:
        # Form untuk mengubah profil
        with st.expander("Edit Your Profile"):
            with st.form("change_profile_form", clear_on_submit=False):
                new_username = st.text_input("Username", user[1])
                new_name = st.text_input("Name", user[2])
                new_email = st.text_input("Email", user[3])

                submit_button = st.form_submit_button("Save Changes")

                if submit_button:
                    # Validasi input
                    if not new_username or not new_name or not new_email:
                        st.warning("Username, name, and email cannot be empty.")
                    else:
                        # Update query
                        update_query = "UPDATE users SET username = ?, name = ?, email = ? WHERE id = ?"
                        update_data = (new_username, new_name, new_email, user_id)

                        # Eksekusi query
                        try:
                            cursor.execute(update_query, update_data)
                            conn.commit()
                            conn.close()
                            st.success("Profile updated successfully!")
                            st.write("Page will be refreshed on 2 seconds.")
                            # Delay before rerun
                            time.sleep(2)
                            # Rerun the page after delay
                            st.rerun()
                        except Exception as e:
                            st.error(f"An error occurred: {e}")

        with st.expander("Change Your Password"):
            with st.form("change_password_form", clear_on_submit=False):
                # Input password lama dan baru
                old_password = st.text_input("Old Password", type="password", placeholder="Leave blank if unchanged")
                new_password = st.text_input("New Password", type="password", placeholder="Leave blank if unchanged")
                confirm_password = st.text_input("Confirm New Password", type="password", placeholder="Leave blank if unchanged")

                # new_password = st.text_input("Password", type="password", placeholder="Leave blank if unchanged")
                change_password = st.form_submit_button("Change Password")

                if change_password:
                    if not old_password or not new_password or not confirm_password:
                        st.error("Please fill in all fields.")
                    elif not verify_old_password(user_id, old_password):
                        st.error("Old password is incorrect.")
                    elif new_password != confirm_password:
                        st.error("New password and confirmation do not match.")
                    else:
                        update_password_profile(user_id, new_password)
                        st.success("Password successfully changed!")
                        st.write("Page will be refreshed on 2 seconds.")
                        # Delay before rerun
                        time.sleep(2)
                        # Rerun the page after delay
                        st.rerun()

        # Tutup koneksi database
        conn.close()

def logout():
    st.session_state.authenticated = False
    st.session_state.user_id = None
    st.session_state.role = None
    st.session_state.username = None
    # del st.session_state.classification_results
    # del st.session_state.classified
    # del st.session_state.results
    st.info("You have been logged out.")
    st.write("Page will be refreshed on 2 seconds.")
    # # Delay before rerun
    # time.sleep(2)
    # # Rerun the page after delay
    # st.rerun()
