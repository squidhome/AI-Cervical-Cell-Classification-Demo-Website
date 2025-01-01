import streamlit as st
import sqlite3
from database import init_db, get_wib_timestamp, get_doctor_statistics, get_patient_ids, get_diagnosis_count, save_additional_information, get_wib_timestamp
from model import load_model, predict_image
from authentication import login, signup, profile, forgot_password, logout
from PIL import Image
import os
import pandas as pd
import time
from datetime import date
from io import BytesIO
import uuid
from streamlit_option_menu import option_menu # pip install streamlit-option-menu 
from streamlit_card import card # pip install streamlit-card

# Initialize demo mode
DEMO = True

# Initialize database
init_db()

# # Load model
# @st.cache_resource
# def get_model():
#     return load_model()

def info():
    st.title("Pap Smear Information")
    st.write("""
            ### What is a Pap Smear?
            A Pap smear, also called a Pap test, is a procedure to test for cervical cancer in women. 
            The test involves collecting cells from your cervix and examining them under a microscope to check for abnormalities.
            
            ### Why is it important?
            Early detection of cervical cancer or precancerous conditions can save lives. 
            Regular screening can help prevent cervical cancer by identifying changes in cervical cells early, 
            allowing for timely treatment and intervention.
            
            ### When should you get a Pap smear?
            - Starting at age 21, women should get a Pap smear every 3 years.
            - Women aged 30 and above can consider combining Pap testing with HPV testing every 5 years.
            
            Consult your healthcare provider for personalized recommendations.
    """)    

def about_us():
    st.title("About us")
    st.write("""
        Welcome to AI-Powered Cervical Cancer Screening, where technology meets expertise 
        to make cervical cancer detection faster and more accessible. Our advanced AI 
        analyzes Pap Smear images with precision, offering quick insights into the health of your cervix. 
        But we don't rely solely on automation—we understand that expert medical judgment is irreplaceable. 
        That’s why our platform combines the power of AI with thorough evaluation by experienced doctors, 
        ensuring both accuracy and personalized care.
    """) 
    st.write("""
        Our mission is to empower healthcare professionals and patients by providing reliable, 
        accessible tools for early detection. With our innovative approach, we help you 
        take proactive steps toward better health, offering you trusted results and expert advice every step of the way.
    """)  

def help():
    st.title("Help")
    # Menambahkan CSS custom untuk padding
    st.markdown("""
        <style>
            .custom-text {
                margin: -10px 0px;  /* Menambahkan padding di semua sisi */
                line-height: 1.5;  /* Jarak antar baris teks */
            }
        </style>
    """, unsafe_allow_html=True)

    # Menambahkan teks dengan CSS kustom
    st.markdown("""
        <div class="custom-text">
            If you <strong>encounter any technical issues</strong> while using our website, 
            please <strong>contact our technical support team</strong> for assistance.<br><br>     
        </div>
                
        <div class="custom-text">
            You can reach us through the following contact:<br>
            Email: <strong>PapSmearAI_technical_support@example.com</strong><br>
            Phone: <strong>+021-123-456-7890</strong><br><br>   
        </div class="custom-text">
            Our technical support team is available to help resolve any issues you may encounter promptly. Thank you for your understanding and cooperation.
        <div>
                
        </div>
    """, unsafe_allow_html=True)

# def classify():
#     st.title("Classify Pap Smear Image with AI")

#     # Fetch patient list
#     conn = sqlite3.connect("database.db")
#     cursor = conn.cursor()
#     cursor.execute("SELECT id, username, email FROM users WHERE role = 'patient'")
#     patients = cursor.fetchall()
#     conn.close()

#     # # Define authorized access (for survey purposes)
#     # authorized_users = {
#     #     "D2": ["P3", "P4"]  # User D2 can only access P3 & P4 data (those dummy accounts used for survey purposes)
#     # }

#     # # Get current user from session state (example implementation)
#     # current_user = st.session_state.get("user_id")  # Ambil user_id dari sesi login

#     # if current_user in authorized_users:
#     #     allowed_id = authorized_users[current_user]
#     #     patients = [patient for patient in patients if patient[0] in allowed_id]  # Filter user yang diizinkan

#     if len(patients) == 0:
#         st.warning("No patients available.")
#     else:
#         # Dropdown for patient selection
#         patient_selection = st.selectbox(
#             "Select Patient",
#             options=[f"{patient[1]} ({patient[2]})" for patient in patients],
#             key="selected_patient"
#         )
#         selected_patient_id = [patient[0] for patient in patients if f"{patient[1]} ({patient[2]})" == patient_selection][0]

#         # Upload and classify image
#         uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

#         # # Set default result in session_state if not already set
#         # if 'result' not in st.session_state:
#         #     st.session_state.result = {}

#         if uploaded_file is not None:
#             image = Image.open(uploaded_file)
#             # st.image(image, caption="Uploaded Image", use_column_width=True)
#             if st.button("Classify"):
#                 model = load_model()
#                 probabilities, predicted_class = predict_image(image, model)
#                 class_labels = ["HSIL", "Kelompok Endoserviks", "LSIL", "Limfosit", "Netrofil", "SCC", 
#                                 "Sel Intermediate", "Sel Parabasal", "Sel Superficial"]
#                 prediction = class_labels[predicted_class]
#                 confidence = probabilities[0][predicted_class].item() * 100

#                 st.session_state.result = {
#                     'patient_id': selected_patient_id,
#                     'image_path': uploaded_file,
#                     "classification": prediction,
#                     "confidence": confidence
#                 }        
#                 st.success("Classification successful!")
#                 st.write(f"**Prediction:** {st.session_state.result['classification']}")
#                 st.write(f"**Confidence:** {st.session_state.result['confidence']:.2f}%")

#                 st.session_state.classified = True

#         # Additional Information Form
#         if "classified" in st.session_state:
#             st.subheader("Additional Evaluation")
#             cancer_stadium = st.selectbox("Cancer Stadium", ["1", "2", "3", "4", "None"])
#             cell_percentage = st.number_input("Cell Percentage", min_value=0.0, max_value=100.0)
#             diagnosis = st.text_area("Diagnosis")
#             conclusion = st.text_area("Conclusion")
#             treatment_options = st.multiselect(
#                 "Treatment",
#                 ["Chemotherapy", "Radiotherapy", "Targeted Therapy", "Surgery", "Medicine", "Other", "None"]
#             )
#             suggestions = st.text_area("Suggestions")
#             referral_letter = st.file_uploader("Upload Referral Letter (PDF)", type=["pdf"])

#             if st.button("Submit"):
#                 save_additional_information(
#                     # st.session_state.patient_id, st.session_state.image_path, 
#                     st.session_state.result, st.session_state.user_id, cancer_stadium, cell_percentage, 
#                     diagnosis, conclusion, treatment_options, suggestions, referral_letter
#                 )
#                 st.success("Additional information saved successfully!")    

#                 # Reset flag untuk form
#                 del st.session_state.classified

# st.session_state.classification_id = 0
def classify():
    st.title("Classify Pap Smear Image with AI")

    # Initialize session state if not already initialized
    if "patient_id" not in st.session_state:
        st.session_state.patient_id = []
        st.session_state.image_bytes = []
        st.session_state.image_name = []
        st.session_state.classification = []
        st.session_state.confidence = []
    if "classified" not in st.session_state:
        st.session_state.classified = False
    if "results" not in st.session_state:
        st.session_state.results = []
    
    # Fetch patient list
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, email FROM users WHERE role = 'patient'")
    patients = cursor.fetchall()
    conn.close()

    if len(patients) == 0:
        st.warning("No patients available.")
    else:
        # Dropdown for patient selection
        patient_selection = st.selectbox(
            "Select Patient",
            options=[f"{patient[1]} ({patient[2]})" for patient in patients],
            key="selected_patient"
        )
        selected_patient_id = [patient[0] for patient in patients if f"{patient[1]} ({patient[2]})" == patient_selection][0]

        # Upload and classify image
        uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            if st.button("Classify"):
                model = load_model()
                probabilities, predicted_class = predict_image(image, model)
                class_labels = ["HSIL", "Kelompok Endoserviks", "LSIL", "Limfosit", "Netrofil", "SCC", 
                                "Sel Intermediate", "Sel Parabasal", "Sel Superficial"]
                prediction = class_labels[predicted_class]
                confidence = probabilities[0][predicted_class].item() * 100

                # Convert image to bytes
                buffer = BytesIO()
                image.save(buffer, format="PNG")
                image_bytes = buffer.getvalue()

                # Store classification result in session state, tied to selected patient ID
                st.session_state.patient_id = selected_patient_id
                st.session_state.image_bytes = image_bytes
                st.session_state.image_name = uploaded_file.name
                st.session_state.classification = prediction
                st.session_state.confidence = confidence

                st.success("Classification successful!")
                st.write(f"**Prediction:** {prediction}")
                st.write(f"**Confidence:** {confidence:.2f}%")

                st.session_state.classified = True

        # Additional Information Form
        if st.session_state.classified == True:
            st.subheader("Additional Evaluation")
            cancer_stadium = st.selectbox("Cancer Stadium", ["1", "2", "3", "4", "None"])
            cell_percentage = st.number_input("Cell Percentage", min_value=0.0, max_value=100.0)
            diagnosis = st.text_area("Diagnosis")
            conclusion = st.text_area("Conclusion")
            treatment_options = st.multiselect(
                "Treatment",
                ["Chemotherapy", "Radiotherapy", "Targeted Therapy", "Surgery", "Medicine", "Other", "None"]
            )
            suggestions = st.text_area("Suggestions")
            referral_letter = st.file_uploader("Upload Referral Letter (PDF)", type=["pdf"])

            if st.button("Submit"):
                # Generate a unique ID for the classification
                classification_id = str(uuid.uuid4())

                st.session_state.results.append({
                    'id': classification_id,
                    'patient_id': st.session_state.patient_id,
                    'image_bytes': st.session_state.image_bytes,
                    'image_name': st.session_state.image_name,
                    'classification': st.session_state.classification,
                    "confidence": st.session_state.confidence,
                    'cancer_stadium': cancer_stadium,
                    'cell_percentage': cell_percentage,
                    'diagnosis': diagnosis,
                    'conclusion': conclusion,
                    'treatment': treatment_options,
                    'suggestions': suggestions,
                    'referral_letter_bytes': referral_letter.read() if referral_letter else None,
                    'referral_letter_name': referral_letter.name if referral_letter else None,
                    'timestamp': get_wib_timestamp()
                })
                st.success("Additional information saved successfully!")   
                # st.session_state.classification_id += 1

                # Reset flag untuk form
                del st.session_state.classified
                del st.session_state.patient_id
                del st.session_state.image_bytes
                del st.session_state.image_name
                del st.session_state.classification
                del st.session_state.confidence

# def view_diagnosis():
#     st.title("View Diagnosis")

#     conn = sqlite3.connect("database.db")
#     cursor = conn.cursor()
#     cursor.execute("""
#         SELECT 
#             classification_results.*, 
#             users.name AS doctor_name
#         FROM classification_results
#         JOIN users 
#         ON classification_results.doctor_id = users.id
#         WHERE classification_results.user_id = ? 
#         ORDER BY classification_results.timestamp DESC
#     """, (st.session_state.user_id,))
#     results = cursor.fetchall()
#     conn.close()

#     if len(results) == 0:
#         st.warning("No diagnosis found.")
#     else:
#         for result in results:
#             st.write(f"**Created:** {result[13]}")
#             st.write(f"**Checked by Doctor:** {result[14]}")
#             st.write(f"**Pap Smear Image**:")

#             file_name = os.path.basename(result[3])

#             # Display the image
#             st.image(result[3], caption=file_name, width=350)

#             # Create a download button
#             with open(result[3], "rb") as file:
#                 st.download_button(
#                     label="Download Image",
#                     data=file,
#                     file_name=file_name,
#                     mime="image/png"
#                 )

#             st.write(f"**Classification:** {result[4]}")
#             st.write(f"**Confidence:** {result[5]:.2f}%")
#             st.write(f"**Cancer Stadium:** {result[6]}")
#             st.write(f"**Cell Percentage:** {result[7]:.2f}%")
#             st.write(f"**Diagnosis:** {result[8]}")
#             st.write(f"**Conclusion:** {result[9]}")
#             st.write(f"**Treatment:** {result[10]}")
#             st.write(f"**Suggestions:** {result[11]}")
            
#             if result[12]:  # Check if referral letter exists
#                 st.write("Existing Referral Letter: " + (os.path.basename(result[12])))
#                 referral_letter_path = result[12]  # result[12] contains the full file path like 'path/namafile.pdf'

#                 if os.path.exists(referral_letter_path):  # Check if the file exists at the given path
#                     # Create a unique key for each download button
#                     download_button_key = f"download_referral__{result[0]}_{os.path.basename(referral_letter_path)}"

#                     # Create a download button for the referral letter with a unique key
#                     with open(referral_letter_path, "rb") as file:
#                         st.download_button(
#                             label="Download Referral Letter",
#                             data=file,
#                             file_name=os.path.basename(referral_letter_path),  # Extract the filename from the full path
#                             mime="application/pdf",  # Assuming it's a PDF
#                             key=download_button_key  # Unique key for the download button
#                     )
#             else:
#                 st.write('No referral letter available.')
#             st.write("---")

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

def view_diagnosis():
    st.title("View Diagnosis")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Mengambil semua tahun unik dari timestamp
    cursor.execute("""
        SELECT DISTINCT strftime('%Y', timestamp) AS year
        FROM classification_results
        WHERE user_id = ?
        ORDER BY year DESC
    """, (st.session_state.user_id,))
    years = [row[0] for row in cursor.fetchall()]

    # Menambahkan opsi "All" untuk menampilkan semua tahun
    years.insert(0, "All")
    
    # Dropdown untuk memilih tahun
    selected_year = st.selectbox("Filter by Year", years)

    # Query untuk mengambil data sesuai tahun yang dipilih
    if selected_year == "All":
        query = """
            SELECT 
                classification_results.*, 
                users.name AS doctor_name
            FROM classification_results
            JOIN users 
            ON classification_results.doctor_id = users.id
            WHERE classification_results.user_id = ? 
            ORDER BY classification_results.timestamp DESC
        """
        cursor.execute(query, (st.session_state.user_id,))
    else:
        query = """
            SELECT 
                classification_results.*, 
                users.name AS doctor_name
            FROM classification_results
            JOIN users 
            ON classification_results.doctor_id = users.id
            WHERE classification_results.user_id = ? 
            AND strftime('%Y', classification_results.timestamp) = ? 
            ORDER BY classification_results.timestamp DESC
        """
        cursor.execute(query, (st.session_state.user_id, selected_year))

    results = cursor.fetchall()
    conn.close()

    if len(results) == 0:
        st.warning("No diagnosis found.")
    else:
        for result in results:
            # Menyisipkan CSS
            st.markdown(get_card_style(), unsafe_allow_html=True)

            # Custom CSS for different classification
            if result[4] in ["HSIL", "LSIL", "SCC"]:
                st.markdown(
                    """
                    <h4 style="color: #FF0000; margin-top: -20px; font-size: 24px;">Alert: Potential Dangerous Cells Detected by AI!</h4>
                    """, unsafe_allow_html=True
                )
            else:
                st.markdown(
                    """
                    <h4 style="color: #009500; margin-top: -20px; font-size: 24px;">AI Analysis: No Dangerous Cells Detected</h4>
                    """, unsafe_allow_html=True
                )

            # Menampilkan diagnosis dalam card
            st.markdown(
                f"""
                <div class="custom-card">
                    <h3>AI Diagnosis Summary</h3>
                    <p><strong>Created At:</strong> {result[13]}</p>
                    <p><strong>AI Classification:</strong> {result[4]}</p>
                    <p><strong>AI Confidence Score:</strong> {result[5]:.2f}%</p>
                    <h3>Doctor's Evaluation</h3>
                    <p><strong>Diagnosed by Doctor:</strong> {result[14]}</p>
                    <p><strong>Cancer Stage:</strong> {result[6]}</p>
                    <p><strong>Cell Percentage:</strong> {result[7]:.2f}%</p>
                    <p><strong>Diagnosis:</strong> {result[8]}</p>
                    <p><strong>Conclusion:</strong> {result[9]}</p>
                    <p><strong>Recommended Treatment:</strong> {result[10]}</p>
                    <p><strong>Suggestions:</strong> {result[11]}</p>
                </div>
                """, unsafe_allow_html=True
            )

            # Menampilkan gambar dengan st.image()
            st.image(result[3], caption=os.path.basename(result[3]), width=350)

            # Menampilkan download button untuk gambar
            with open(result[3], "rb") as file:
                st.download_button(
                    label="Download Pap Smear Image",
                    data=file,
                    file_name=os.path.basename(result[3]),
                    mime="image/png"
                )

            # Menampilkan referral letter jika ada
            if result[12]:  # Check if referral letter exists
                st.write("Existing Referral Letter: " + (os.path.basename(result[12])))
                referral_letter_path = result[12]  # result[12] contains the full file path like 'path/namafile.pdf'
                
                # Menampilkan tombol download untuk referral letter
                with open(referral_letter_path, "rb") as file:
                    st.download_button(
                        label="Download Referral Letter",
                        data=file,
                        file_name=os.path.basename(referral_letter_path),  # Extract the filename from the full path
                        mime="application/pdf"  # Assuming it's a PDF
                    )
            else:
                st.write('No referral letter available.')

            st.write("---")

def user_dashboard():
    st.title("Admin Dashboard")
    st.write("Manage Users and Classification Results")

    st.subheader("User Management")
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Dropdown untuk filter berdasarkan role
    role_filter = st.selectbox("Filter Users by Role", ["All", "Doctor", "Patient", "Admin"])

    # Query untuk mengambil data sesuai filter
    if role_filter == "All":
        query = "SELECT id, username, name, email, birthdate, role FROM users"
        cursor.execute(query)
    else:
        query = "SELECT id, username, name, email, birthdate, role FROM users WHERE role = ?"
        cursor.execute(query, (role_filter.lower(),))

    users = cursor.fetchall()
    conn.close()

    # Tampilkan data berdasarkan filter
    if users:
        for user in users:
            # Menyisipkan CSS
            st.markdown(get_card_style(), unsafe_allow_html=True)

            # Menampilkan diagnosis dalam card
            st.markdown(
                f"""
                <div class="custom-card">
                    <p><strong>ID:</strong> {user[0]}</p>
                    <p><strong>Username:</strong> {user[1]}</p>
                    <p><strong>Name:</strong> {user[2]}</p>
                    <p><strong>Email:</strong> {user[3]}</p>
                    <p><strong>Birth Date:</strong> {user[4]}</p>
                    <p><strong>Role:</strong> {user[5]}</p>
                </div>
                """, unsafe_allow_html=True
            )

            # # Update User
            # if st.button(f"Update {user[1]}"):
            #     # Set session state when the button is clicked to show the form
            #     st.session_state.update_form = user[1]

            # Menampilkan form jika tombol update ditekan
            with st.expander(f"Update Profile {user[1]}"):
                with st.form(f"update_user_{user[0]}"):
                    # Set session state for the inputs to ensure data is updated
                    username = st.text_input("Username", user[1])
                    email = st.text_input("Email", user[3])
                    name = st.text_input("Name", user[2])
                    birth_date = st.date_input("Birth Date", user[4], min_value=date(1900, 1, 1), max_value=date.today())
                    role = st.selectbox("Role", ["doctor", "patient", "admin"], index=["doctor", "patient", "admin"].index(user[5]))

                    submit_button = st.form_submit_button("Save")

                    if submit_button:
                        # Update to the database
                        conn = sqlite3.connect("database.db")
                        cursor = conn.cursor()
                        cursor.execute("UPDATE users SET username = ?, name = ?, email = ?, birthdate = ?, role = ? WHERE id = ?",
                                        (username, name, email, birth_date, role, user[0]))
                        conn.commit()
                        conn.close()

                        st.success("User updated successfully!")
                        st.session_state.update_form = None
                        
                        st.write("Please refresh to see the latest result.")
                        # # Delay before rerun
                        # time.sleep(2)
                        # # Rerun the page after delay
                        # st.rerun()
            # Delete User
            if st.button(f"Delete {user[1]}"):
                conn = sqlite3.connect("database.db")
                cursor = conn.cursor()
                cursor.execute("DELETE FROM users WHERE id = ?", (user[0],))
                conn.commit()
                conn.close()
                st.warning("User deleted successfully!")

            st.write("---")
    else:
        st.warning(f"No users found for role: {role_filter}")


    # # Add New User
    # st.subheader("Add New User")
    # with st.form("add_user_form"):
    #     username = st.text_input("Username")
    #     email = st.text_input("Email")
    #     password = st.text_input("Password", type="password")
    #     role = st.selectbox("Role", ["doctor", "patient", "admin"])
    #     submit = st.form_submit_button("Add User")
    #     if submit:
    #         try:
    #             add_user(username, email, password, role)
    #             st.success("User added successfully!")
    #         except:
    #             st.error("Error: Email already exists.")

# def update_delete_diagnosis():
#     st.subheader("Classification Results Per User")

#     # Database connection
#     conn = sqlite3.connect("database.db")
#     cursor = conn.cursor()

#     # Fetch user list with classification results
#     cursor.execute("""
#         SELECT DISTINCT users.id, users.username, users.email 
#         FROM classification_results 
#         JOIN users 
#         ON classification_results.user_id = users.id
#     """)
#     users = cursor.fetchall()

#     # # Define authorized access (for survey purposes)
#     # authorized_users = {
#     #     "D2": ["P3", "P4"]  # User D2 can only access P3 & P4 data (those dummy accounts used for survey purposes)
#     # }

#     # # Get current user from session state (example implementation)
#     # current_user = st.session_state.get("user_id")  # Ambil user_id dari sesi login

#     # if current_user in authorized_users:
#     #     allowed_id = authorized_users[current_user]
#     #     users = [user for user in users if user[0] in allowed_id]  # Filter user yang diizinkan

#     if users:
#         # User selection dropdown
#         selected_user = st.selectbox(
#             "Select User",
#             options=[f"{user[1]} ({user[2]})" for user in users],
#             key="selected_user"
#         )

#         # Get the selected user's ID
#         selected_user_id = [user[0] for user in users if f"{user[1]} ({user[2]})" == selected_user][0]

#         # Fetch classification results for the selected user
#         cursor.execute("""
#             SELECT 
#                 classification_results.*, 
#                 patient_users.username AS patient_username, 
#                 patient_users.email AS patient_email,
#                 doctor_users.name AS doctor_name
#             FROM classification_results 
#             JOIN users AS patient_users 
#             ON classification_results.user_id = patient_users.id
#             JOIN users AS doctor_users 
#             ON classification_results.doctor_id = doctor_users.id
#             WHERE classification_results.user_id = ?
#             ORDER BY classification_results.timestamp DESC
#         """, (selected_user_id,))
#         results = cursor.fetchall()
#         conn.close()

#         if results:
#             st.write(f"### Results for {selected_user}")
#             for result in results:
#                 # Menyisipkan CSS
#                 st.markdown(get_card_style(), unsafe_allow_html=True)

#                 if result[4] in ["HSIL", "LSIL", "SCC"]:
#                     st.markdown(
#                         """
#                         <h4 style="color: #FF0000; margin-top: -20px; font-size: 24px;">Alert: Potential Dangerous Cells Detected by AI!</h4>
#                         """, unsafe_allow_html=True
#                     )
#                 else:
#                     st.markdown(
#                         """
#                         <h4 style="color: #009500; margin-top: -20px; font-size: 24px;">AI Analysis: No Dangerous Cells Detected</h4>
#                         """, unsafe_allow_html=True
#                     )

#                 # Menampilkan diagnosis dalam card
#                 st.markdown(
#                     f"""
#                     <div class="custom-card">
#                         <h3>AI Diagnosis Summary</h3>
#                         <p><strong>Created At:</strong> {result[13]}</p>
#                         <p><strong>AI Classification:</strong> {result[4]}</p>
#                         <p><strong>AI Confidence Score:</strong> {result[5]:.2f}%</p>
#                         <h3>Doctor's Evaluation</h3>
#                         <p><strong>Diagnosed by Doctor:</strong> {result[14]}</p>
#                         <p><strong>Cancer Stage:</strong> {result[6]}</p>
#                         <p><strong>Cell Percentage:</strong> {result[7]:.2f}%</p>
#                         <p><strong>Diagnosis:</strong> {result[8]}</p>
#                         <p><strong>Conclusion:</strong> {result[9]}</p>
#                         <p><strong>Recommended Treatment:</strong> {result[10]}</p>
#                         <p><strong>Suggestions:</strong> {result[11]}</p>
#                     </div>
#                     """, unsafe_allow_html=True
#                 )

#                 # Menampilkan gambar dengan st.image()
#                 st.write("### Pap Smear Image")
#                 st.image(result[3], caption=os.path.basename(result[3]), width=350)

#                 # Menampilkan download button untuk gambar
#                 with open(result[3], "rb") as file:
#                     st.download_button(
#                         label="Download Pap Smear Image",
#                         data=file,
#                         file_name=os.path.basename(result[3]),
#                         mime="image/png",
#                         key = f"download_image__{result[0]}_{os.path.basename(result[3])}"
#                     )

#                 # Menampilkan referral letter jika ada
#                 if result[12]:  # Check if referral letter exists
#                     st.write("Existing Referral Letter: " + (os.path.basename(result[12])))
#                     referral_letter_path = result[12]  # result[12] contains the full file path like 'path/namafile.pdf'

#                     # Menampilkan tombol download untuk referral letter
#                     with open(referral_letter_path, "rb") as file:
#                         st.download_button(
#                             label="Download Referral Letter",
#                             data=file,
#                             file_name=os.path.basename(referral_letter_path),  # Extract the filename from the full path
#                             mime="application/pdf",  # Assuming it's a PDF
#                             key = f"download_letter__{result[0]}_{os.path.basename(referral_letter_path)}"
#                         )
#                 else:
#                     st.write('No referral letter available.')

#                 # Update Result
#                 with st.expander(f"Update Result {result[0]}"):
#                     with st.form(f"update_form_{result[0]}"):
#                         # classification = st.text_input("Classification", value=result[3])
#                         # confidence = st.number_input("Confidence", value=result[4])
#                         cancer_stadium = st.selectbox("Cancer Stadium", ["1", "2", "3", "4", "None"], index=["1", "2", "3", "4", "None"].index(result[6]))
#                         cell_percentage = st.number_input("Cell Percentage", value=result[7], min_value=0.0, max_value=100.0)
#                         diagnosis = st.text_area("Diagnosis", value=result[8])
#                         conclusion = st.text_area("Conclusion", value=result[9])
#                         treatment = st.multiselect(
#                             "Treatment",
#                             ["Chemotherapy", "Radiotherapy", "Targeted Therapy", "Surgery", "Medicine", "Other", "None"],
#                             default=result[10].split(", ") if result[10] else []  # Mengonversi string menjadi list
#                         )
#                         suggestions = st.text_area("Suggestions", value=result[11])

#                         # File uploader for the referral letter
#                         new_referral_letter = st.file_uploader("Upload new Referral Letter (PDF)", type=["pdf"])

#                         submit_button = st.form_submit_button(label="Submit Changes")
#                         if submit_button:
#                             if new_referral_letter is not None:
#                                 # Path file lama
#                                 old_referral_letter_path = result[12]  # result[12] menyimpan path file lama dari database
                                
#                                 # Jika file lama ada dan bukan None, hapus file lama
#                                 if old_referral_letter_path and os.path.exists(old_referral_letter_path):
#                                     os.remove(old_referral_letter_path)

#                                 # Save new referral letter and update the path in the database
#                                 referral_letter_path = f"uploads/referral_letters/{new_referral_letter.name}"
#                                 with open(referral_letter_path, "wb") as f:
#                                     f.write(new_referral_letter.getbuffer())
                            
#                             # Update classification result in database
#                             conn = sqlite3.connect("database.db")
#                             cursor = conn.cursor()
#                             cursor.execute("""
#                                 UPDATE classification_results 
#                                 SET 
#                                     cancer_stadium = ?, 
#                                     cell_percentage = ?, 
#                                     diagnosis = ?, 
#                                     conclusion = ?, 
#                                     treatment = ?, 
#                                     suggestions = ?, 
#                                     referral_letter = ?
#                                 WHERE id = ?
#                             """, (
#                                 cancer_stadium, cell_percentage, diagnosis, conclusion, ", ".join(treatment), 
#                                 suggestions, referral_letter_path if new_referral_letter else result[12], result[0]
#                             ))
#                             conn.commit()
#                             conn.close()
#                             st.success("Result updated successfully!")

#                             st.write("Page will be refreshed on 2 seconds.")
#                             # Delay before rerun
#                             time.sleep(2)
#                             # Rerun the page after delay
#                             st.rerun()

#                 # Delete Result
#                 delete_button = st.button(f"Delete Result {result[0]}")
#                 if delete_button:
#                     conn = sqlite3.connect("database.db")
#                     cursor = conn.cursor()
#                     cursor.execute("DELETE FROM classification_results WHERE id = ?", (result[0],))
#                     conn.commit()
#                     conn.close()
#                     st.warning("Result deleted successfully!")

#                     st.write("Page will be refreshed on 2 seconds.")
#                     # Delay before rerun
#                     time.sleep(2)
#                     # Rerun the page after delay
#                     st.rerun()
                
#                 st.write("---")
#         else:
#             st.warning("No classification results found for the selected user.")
#     else:
        # st.warning("No patients with classification results found.")

def update_delete_diagnosis():
    st.subheader("Classification Results Per User")

    # Database connection
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Fetch patient list with classification results
    cursor.execute("""
        SELECT DISTINCT users.id, users.username, users.email 
        FROM classification_results 
        JOIN users 
        ON classification_results.user_id = users.id
    """)
    users = cursor.fetchall()

    if users:
        # User selection dropdown
        selected_user = st.selectbox(
            "Select User",
            options=[f"{user[1]} ({user[2]})" for user in users],
            key="selected_user"
        )

        st.write(f"### Results for {selected_user}")

        # Get the selected user's ID
        selected_user_id = [user[0] for user in users if f"{user[1]} ({user[2]})" == selected_user][0]
        
        if "results" in st.session_state and st.session_state.results is not None:
            # Filter results for selected patient
            results = [res for res in st.session_state.results if res['patient_id'] == selected_user_id]

            id = 0
            for result in results:
                id += 1
                # Insert CSS styling
                st.markdown(get_card_style(), unsafe_allow_html=True)

                if result['classification'] in ["HSIL", "LSIL", "SCC"]:
                    st.markdown(
                        "<h4 style='color: #FF0000; margin-top: -20px; font-size: 24px;'>Alert: Potential Dangerous Cells Detected by AI!</h4>", 
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        "<h4 style='color: #009500; margin-top: -20px; font-size: 24px;'>AI Analysis: No Dangerous Cells Detected</h4>", 
                        unsafe_allow_html=True
                    )

                # Display diagnosis in card
                st.markdown(
                    f"""
                    <div class="custom-card">
                        <h3>AI Diagnosis Summary</h3>
                        <p><strong>Created At:</strong> {result['timestamp']}</p>
                        <p><strong>AI Classification:</strong> {result['classification']}</p>
                        <p><strong>AI Confidence Score:</strong> {result['confidence']:.2f}%</p>
                        <h3>Doctor's Evaluation</h3>
                        <p><strong>Cancer Stage:</strong> {result['cancer_stadium']}</p>
                        <p><strong>Cell Percentage:</strong> {result['cell_percentage']:.2f}%</p>
                        <p><strong>Diagnosis:</strong> {result['diagnosis']}</p>
                        <p><strong>Conclusion:</strong> {result['conclusion']}</p>
                        <p><strong>Recommended Treatment:</strong> {', '.join(result['treatment'])}</p>
                        <p><strong>Suggestions:</strong> {result['suggestions']}</p>
                    </div>
                    """, unsafe_allow_html=True
                )

                image_file = BytesIO(result['image_bytes'])
                # Display image with st.image()
                st.write("### Pap Smear Image")
                st.image(image_file, caption=result['image_name'], width=350)

                # Display download button for image
                st.download_button(
                    label="Download Pap Smear Image",
                    data=image_file,
                    file_name=result['image_name'],
                    mime="image/png",
                    key = f"download_image_{id}_{os.path.basename(result['image_name'])}"
                )

                referral_letter = result['referral_letter_bytes']
                # Display referral letter if available
                if referral_letter:
                    st.download_button(
                        label="Download Referral Letter",
                        data=referral_letter,
                        file_name=result['referral_letter_name'],
                        mime="application/pdf",
                        key = f"download_letter_{id}_{os.path.basename(referral_letter)}"
                    )
                else:
                    st.write('No referral letter available.')

                # # Update Result
                # with st.expander(f"Update Result"):
                #     with st.form(f"update_form_{result['patient_id']}_{{result['id']}}"):
                #         cancer_stadium = st.selectbox("Cancer Stadium", ["1", "2", "3", "4", "None"], index=["1", "2", "3", "4", "None"].index(result['cancer_stadium']))
                #         cell_percentage = st.number_input("Cell Percentage", value=result['cell_percentage'], min_value=0.0, max_value=100.0)
                #         diagnosis = st.text_area("Diagnosis", value=result['diagnosis'])
                #         conclusion = st.text_area("Conclusion", value=result['conclusion'])
                #         treatment = st.multiselect(
                #             "Treatment",
                #             ["Chemotherapy", "Radiotherapy", "Targeted Therapy", "Surgery", "Medicine", "Other", "None"],
                #             default=result['treatment'] if result['treatment'] else []
                #         )
                #         suggestions = st.text_area("Suggestions", value=result['suggestions'])

                #         # File uploader for the referral letter
                #         new_referral_letter = st.file_uploader("Upload new Referral Letter (PDF)", type=["pdf"])

                #         submit_button = st.form_submit_button(label="Update")
                #         if submit_button:
                #             # Update in session 
                #             for res in st.session_state.results:
                #                 if res['id'] == result['id']:
                #                     res.update({
                #                         'cancer_stadium': cancer_stadium,
                #                         'cell_percentage': cell_percentage,
                #                         'diagnosis': diagnosis,
                #                         'conclusion': conclusion,
                #                         'treatment': treatment,
                #                         'suggestions': suggestions,
                #                         'referral_letter_bytes': new_referral_letter.read() if new_referral_letter else None,
                #                         'referral_letter_name': new_referral_letter.name if new_referral_letter else None,
                #                     })
                #                     st.success("Results updated successfully!")
                #                     st.write("Please refresh to see the latest results.")
                #                     # # Delay before rerun
                #                     # time.sleep(2)
                #                     # # Rerun the page after delay
                #                     # st.rerun()
                #                     break
        
        # Fetch classification results for the selected user
        cursor.execute("""
            SELECT 
                classification_results.*, 
                patient_users.username AS patient_username, 
                patient_users.email AS patient_email,
                doctor_users.name AS doctor_name
            FROM classification_results 
            JOIN users AS patient_users 
            ON classification_results.user_id = patient_users.id
            JOIN users AS doctor_users 
            ON classification_results.doctor_id = doctor_users.id
            WHERE classification_results.user_id = ?
            ORDER BY classification_results.timestamp DESC
        """, (selected_user_id,))
        results = cursor.fetchall()
        conn.close()

        if results:
            for result in results:
                # Menyisipkan CSS
                st.markdown(get_card_style(), unsafe_allow_html=True)

                if result[4] in ["HSIL", "LSIL", "SCC"]:
                    st.markdown(
                        """
                        <h4 style="color: #FF0000; margin-top: -20px; font-size: 24px;">Alert: Potential Dangerous Cells Detected by AI!</h4>
                        """, unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        """
                        <h4 style="color: #009500; margin-top: -20px; font-size: 24px;">AI Analysis: No Dangerous Cells Detected</h4>
                        """, unsafe_allow_html=True
                    )

                # Menampilkan diagnosis dalam card
                st.markdown(
                    f"""
                    <div class="custom-card">
                        <h3>AI Diagnosis Summary</h3>
                        <p><strong>Created At:</strong> {result[13]}</p>
                        <p><strong>AI Classification:</strong> {result[4]}</p>
                        <p><strong>AI Confidence Score:</strong> {result[5]:.2f}%</p>
                        <h3>Doctor's Evaluation</h3>
                        <p><strong>Diagnosed by Doctor:</strong> {result[14]}</p>
                        <p><strong>Cancer Stage:</strong> {result[6]}</p>
                        <p><strong>Cell Percentage:</strong> {result[7]:.2f}%</p>
                        <p><strong>Diagnosis:</strong> {result[8]}</p>
                        <p><strong>Conclusion:</strong> {result[9]}</p>
                        <p><strong>Recommended Treatment:</strong> {result[10]}</p>
                        <p><strong>Suggestions:</strong> {result[11]}</p>
                    </div>
                    """, unsafe_allow_html=True
                )

                # Menampilkan gambar dengan st.image()
                st.write("### Pap Smear Image")
                st.image(result[3], caption=os.path.basename(result[3]), width=350)

                # Menampilkan download button untuk gambar
                with open(result[3], "rb") as file:
                    st.download_button(
                        label="Download Pap Smear Image",
                        data=file,
                        file_name=os.path.basename(result[3]),
                        mime="image/png",
                        key = f"download_image__{result[0]}_{os.path.basename(result[3])}"
                    )

                # Menampilkan referral letter jika ada
                if result[12]:  # Check if referral letter exists
                    st.write("Existing Referral Letter: " + (os.path.basename(result[12])))
                    referral_letter_path = result[12]  # result[12] contains the full file path like 'path/namafile.pdf'

                    # Menampilkan tombol download untuk referral letter
                    with open(referral_letter_path, "rb") as file:
                        st.download_button(
                            label="Download Referral Letter",
                            data=file,
                            file_name=os.path.basename(referral_letter_path),  # Extract the filename from the full path
                            mime="application/pdf",  # Assuming it's a PDF
                            key = f"download_letter__{result[0]}_{os.path.basename(referral_letter_path)}"
                        )
                else:
                    st.write('No referral letter available.')

                # # Update Result
                # with st.expander(f"Update Result"):
                #     with st.form(f"update_form_{result[0]}"):
                #         # classification = st.text_input("Classification", value=result[3])
                #         # confidence = st.number_input("Confidence", value=result[4])
                #         cancer_stadium = st.selectbox("Cancer Stadium", ["1", "2", "3", "4", "None"], index=["1", "2", "3", "4", "None"].index(result[6]))
                #         cell_percentage = st.number_input("Cell Percentage", value=result[7], min_value=0.0, max_value=100.0)
                #         diagnosis = st.text_area("Diagnosis", value=result[8])
                #         conclusion = st.text_area("Conclusion", value=result[9])
                #         treatment = st.multiselect(
                #             "Treatment",
                #             ["Chemotherapy", "Radiotherapy", "Targeted Therapy", "Surgery", "Medicine", "Other", "None"],
                #             default=result[10].split(", ") if result[10] else []  # Mengonversi string menjadi list
                #         )
                #         suggestions = st.text_area("Suggestions", value=result[11])

                #         # File uploader for the referral letter
                #         new_referral_letter = st.file_uploader("Upload new Referral Letter (PDF)", type=["pdf"])

                #         submit_button = st.form_submit_button(label="Submit Changes")
                #         if submit_button:
                #             if new_referral_letter is not None:
                #                 # Path file lama
                #                 old_referral_letter_path = result[12]  # result[12] menyimpan path file lama dari database
                                
                #                 # Jika file lama ada dan bukan None, hapus file lama
                #                 if old_referral_letter_path and os.path.exists(old_referral_letter_path):
                #                     os.remove(old_referral_letter_path)

                #                 # Save new referral letter and update the path in the database
                #                 referral_letter_path = f"uploads/referral_letters/{new_referral_letter.name}"
                #                 with open(referral_letter_path, "wb") as f:
                #                     f.write(new_referral_letter.getbuffer())

        conn.close()

def admin_statistics():    
    # Statistik dokter
    doctor_stats = get_doctor_statistics()

    if doctor_stats:
        st.write("### Doctor Statistics")
        
        st.markdown(get_card_style(), unsafe_allow_html=True)
        
        # Dropdown untuk memilih dokter
        doctor_names = [f"{stat[0]} | {stat[2]} | {stat[3]}" for stat in doctor_stats]  # Menampilkan ID dokter dan nama
        selected_doctor = st.selectbox("Select Doctor", doctor_names)
        
        # Mendapatkan data dokter yang dipilih
        selected_doctor_id = selected_doctor.split(" ")[0]  # Mengambil ID dokter (misal D1, D2, dll)
        
        # Menampilkan statistik dokter yang dipilih
        for stat in doctor_stats:
            if stat[0] == selected_doctor_id:
                # Menampilkan statistik dalam card
                st.markdown(
                    f"""
                    <div class="custom-card">
                        <h4>{stat[2]}</h4>
                        <p><strong>Doctor ID:</strong> {stat[0]}</p>
                        <p><strong>Username:</strong> {stat[1]}</p>
                        <p><strong>Name:</strong> {stat[2]}</p>
                        <p><strong>Birth Date:</strong> {stat[3]}</p>
                        <p><strong>Total Patients: {stat[4]}</strong></p>
                        <p><strong>Total Diagnoses: {stat[5]}</strong></p>
                    </div>
                    """, unsafe_allow_html=True
                )
                st.write("---")
    else:
        st.warning("No statistics available for doctors.")

    # Ambil daftar pasien
    st.write("### Check Patient Diagnosis Count")
    patients = get_patient_ids()
    if patients:
        # Dropdown untuk memilih pasien
        selected_patient = st.selectbox(
            "Select Patient:",
            options=[f"{patient[0]} | {patient[2]} | {patient[3]}" for patient in patients]
        )

        # Ambil ID pasien yang dipilih
        selected_patient_id = selected_patient.split(" ")[0]

        # Hitung jumlah hasil diagnosis
        diagnosis_count = get_diagnosis_count(selected_patient_id)

        for patient in patients:
            if patient[0] == selected_patient_id:
                # Menampilkan statistik dalam card
                st.markdown(
                    f"""
                    <div class="custom-card">
                        <h4>{patient[2]}</h4>
                        <p><strong>Patient ID:</strong> {selected_patient_id}</p>
                        <p><strong>Username:</strong> {patient[1]}</p>
                        <p><strong>Name:</strong> {patient[2]}</p>
                        <p><strong>Birth Date:</strong> {patient[3]}</p>
                        <p><strong>Total Diagnoses: {diagnosis_count}</strong></p>
                    </div>
                    """, unsafe_allow_html=True
                )

                # # Tampilkan hasil
                # st.write(f"**Patient ID:** {selected_patient_id}")
                # st.write(f"**Total Diagnoses:** {diagnosis_count}")
    else:
        st.warning("No patients found in the database.")

# Main app
def main():
    st.set_page_config(page_title="Cervical Cell Classification", layout="wide")

    # Session state for user authentication
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.role = None
        st.session_state.username = None

    # Default menu
    menu = ["Home", "Logout"]
    icons = ["house", "box-arrow-right"]
    styles = {
                "container": {"padding": "5px"},
                "nav-link": {"font-size": "15px", "text-align": "left", "margin": "0px"},
                "nav-link-selected": {"background-color": "#24869E", "color": "white", "font-weight": "800"}
            }
    
    # Navigation bar
    if st.session_state.authenticated:
        with st.sidebar:
            if st.session_state.role == "doctor":
                menu = ["Home", "Profile", "Pap Smear Information", "Classify Image", "Patient Diagnosis", "Logout"]  
                icons = ["house", "person", "info-circle", "image", "journal-medical", "box-arrow-right"]
            elif st.session_state.role == "patient":
                menu = ["Home", "Profile", "Pap Smear Information", "View Diagnosis", "Logout"]  
                icons = ["house", "person", "info-circle", "file-medical", "box-arrow-right"]
            elif st.session_state.role == "admin":
                menu = ["Home", "Profile", "User Dashboard", "Patient Diagnosis", "Statistical Report", "Logout"]
                icons = ["house", "person", "gear", "journal-medical", "bar-chart", "box-arrow-right"]

            option = option_menu(
                menu_title="Navigation",
                menu_icon="menu-up",  # Icon for navigation
                options=menu,
                icons=icons,  # Icons for each menu
                styles=styles
            )
        
    else:
        if DEMO:
            menu = ["Home", "Login", "Pap Smear Information"]
            icons = ["house", "key", "info-circle"]
        else:
            menu = ["Home", "Login", "Sign Up", "Forgot Password", "Pap Smear Information"]
            icons = ["house", "key", "person-plus", "lock", "info-circle"]

        with st.sidebar:
            option = option_menu(
                menu_title="Navigation",
                menu_icon="menu-up",  # Icon for navigation
                options=menu,
                icons=icons,  # Icons for each menu
                styles=styles
            )
    
    # option = st.sidebar.radio("Navigation", menu)

    # Tutorial langsung di sidebar
    st.sidebar.markdown("<h2 style='font-size: 24px; font-weight: 700;'>Website Tutorial</h2>", unsafe_allow_html=True)

     # Custom CSS for card design
    card_style = """
        <style>
        .custom-card {
            background-color: #f9f9f9;
            padding: 15px;
            margin-bottom: 15px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .custom-card h4 {
            margin-top: 0;
            font-size: 18px;
            font-weight: bold;
        }
        .custom-card p {
            font-size: 15.5px;
            text-align: justify;
        }
        </style>
    """

    st.markdown(card_style, unsafe_allow_html=True)
    
    # Display the tutorial in cards
    if st.session_state.role == 'patient':
        st.sidebar.markdown("""
            <div class="custom-card">
                <h4>How to Use the Website</h4>
                <p><strong>1. Home Page:</strong> After logging in, you'll be directed to the Home page, which provides information about the features available to you, as well as details about the app in the About Us section and contact information for technical support in the Help section.</p>
                <p><strong>2. Profile:</strong> You can access the Profile page to update or view your personal information.</p>
                <p><strong>3. Pap Smear Information:</strong> Select the Pap Smear Information option to learn more about what a Pap Smear is, why it’s important, and when to get one.</p>
                <p><strong>4. View Diagnosis:</strong> Select View Diagnosis to check your Pap Smear diagnosis results that have been previously classified by AI & further evaluated by a doctor.</p>
                <p><strong>5. Logout:</strong> Click Logout to exit your account and return to the login page.</p>
            </div>
        """, unsafe_allow_html=True)

    elif st.session_state.role == 'doctor':
        st.sidebar.markdown("""
            <div class="custom-card">
                <h4>How to Use the Website</h4>
                <p><strong>1. Home Page:</strong> After logging in, you'll be directed to the Home page, which provides information about the app. The main feature for you is Classify Image, which allows you to classify Pap Smear images for diagnosis.</p>
                <p><strong>2. Profile:</strong> You can access the Profile page to view and update your account information.</p>
                <p><strong>3. Pap Smear Information:</strong> Select the Pap Smear Information option to learn more about what a Pap Smear is, why it’s important, and when to get one.</p>
                <p><strong>4. Classify Image:</strong> Select Classify Image to upload a Pap Smear image you wish to classify. After the AI classification, you can add Additional Evaluation to help evaluate the AI's classification.</p>
                <p><strong>5. Patient Diagnosis:</strong> Select Patient Diagnosis to update or delete patient diagnoses, if necessary.</p>
                <p><strong>6. Logout:</strong> Click Logout to exit your account and return to the login page.</p>
            </div>
        """, unsafe_allow_html=True)

    elif st.session_state.role == 'admin':
        st.sidebar.markdown("""
            <div class="custom-card">
                <h4>How to Use the Website</h4>
                <p><strong>1. Home Page:</strong> After logging in, you will be directed to the Home page, which outlines the features available to admins, such as managing users and viewing statistical reports.</p>
                <p><strong>2. Profile:</strong> You can also access the Profile page to update your account information.</p>
                <p><strong>3. User Dashboard:</strong> Select User Dashboard to manage user data, such as updating or deleting user accounts.</p>
                <p><strong>4. Patient Diagnosis:</strong> Select Patient Diagnosis to update or delete patient diagnoses, if necessary.</p>
                <p><strong>5. Statistical Report:</strong> Select Statistical Report to view statistics related to doctor diagnoses and patient diagnosis counts.</p>
                <p><strong>6. Logout:</strong> Click Logout to exit your account and return to the login page.</p>
            </div>
        """, unsafe_allow_html=True)

    else:
        st.sidebar.markdown("""
            <div class="custom-card">
                <h4>How to Use the Website</h4>
                <p><strong>1. Home Page:</strong> When you first enter the app, you'll see a welcome message suggesting that you log in to access other features.</p>
                <p><strong>2. Login:</strong> Click on the Login option in the navigation menu. Enter your email and password to access your account.</p>
                <p><strong>3. Sign Up:</strong> If you don’t have an account, click on Sign Up to create a new account.</p>
                <p><strong>4. Forgot Password:</strong> If you've forgotten your password, click Forgot Password and follow the instructions to reset it.</p>
                <p><strong>5. Pap Smear Information:</strong> Select the Pap Smear Information option to learn more about what a Pap Smear is, why it’s important, and when to get one.</p>
            </div>
        """, unsafe_allow_html=True)

    title = 'Welcome to AI-Powered Cervical Cancer Screening'

    # Home Page
    if option == "Home" and st.session_state.role == 'doctor':
        st.title(title)
        st.write("This app allows you to classify Pap Smear images.")
        about_us()
        help()

    elif option == "Home" and st.session_state.role == 'patient':
        st.title(title)
        st.write("This app allows you to view your pap smear diagnoses.")
        about_us()
        help()

    elif option == "Home" and st.session_state.role == 'admin':
        st.title(title)
        st.write("This app allows you to manage user, diagnose result, and doctor & patient statistical.")
        about_us()
        help()
    
    elif option == "Home" and st.session_state.authenticated == False:
        st.title(title)
        st.write("Please login to access the features.")
        about_us()
        help()

    # Profile Page
    elif option == "Profile":
        profile(st.session_state.user_id)

    # Login Page
    elif option == "Login":
        login()

    # Sign-Up Page
    elif option == "Sign Up":
        signup()

    elif option == "Forgot Password":
        forgot_password()

    elif option == "Pap Smear Information":
        info()

    # Doctor: Classify Image Page
    elif option == "Classify Image" and st.session_state.role == "doctor":
        classify()

    # Patient: View Diagnosis
    elif option == "View Diagnosis" and st.session_state.role == "patient":
        view_diagnosis()
    
    elif option == "Patient Diagnosis" and (st.session_state.role in ['doctor', 'admin']):
        update_delete_diagnosis()

    elif option == "User Dashboard" and st.session_state.role == 'admin':
        user_dashboard()

    elif option == "Statistical Report" and st.session_state.role == 'admin':
        admin_statistics()

    # Logout
    elif option == "Logout":
        logout()

if __name__ == "__main__":
    main()

# Untuk menjalankan Streamlit, gunakan perintah berikut di terminal:
# python -m streamlit run app.py