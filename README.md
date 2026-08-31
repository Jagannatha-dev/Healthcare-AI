# Healthcare AI – Multi-Disease Prediction & Recommendation System

Healthcare AI is a web-based Artificial Intelligence and Machine Learning project designed to provide preliminary disease prediction and disease-specific healthcare information based on user-selected symptoms.

## 🚀 Project Overview

The system uses a trained Machine Learning model to analyze selected symptoms and predict a possible disease along with a confidence score. After prediction, the system retrieves additional disease-specific information from structured healthcare datasets.

The project combines **Machine Learning, Flask, Oracle Database, CSV datasets, and an AI Healthcare Chatbot** into a single healthcare support platform.

## ✨ Key Features

- 👤 User Registration and Login
- 🔐 Secure User Authentication
- 🩺 Symptom-Based Disease Prediction
- 🤖 Machine Learning Disease Classification
- 📊 Prediction Confidence Score
- 📋 Detailed Disease Information
- 🥗 Disease-Specific Diet Recommendations
- 🏃 Exercise Recommendations
- 💊 Medicine Information
- 🧪 Diagnosis and Laboratory Test Information
- ⚠️ Risk Factors and Complications
- 🛡️ Prevention and Precautions
- 🏥 Doctor/Specialist Information
- 🚑 Emergency Guidance
- ❤️ Health Tips
- 💬 AI Healthcare Chatbot
- 📚 Project-Related Chatbot Questions
- 📜 Prediction History
- 📄 Downloadable PDF Reports
- 👤 User Profile Management
- 🔑 Password Change
- 🛠️ Admin Panel
- 👥 User Management
- 📈 Prediction Management
- 📂 Healthcare Dataset Management

## 🧠 Machine Learning

The system uses a trained Machine Learning classification model to predict diseases from user-selected symptoms.

### Prediction Workflow

User Registration/Login  
↓  
Select Symptoms  
↓  
Machine Learning Model  
↓  
Predicted Disease + Confidence  
↓  
Recommendation Service  
↓  
Disease-Specific Information  
↓  
Result Page  
↓  
Prediction History / PDF Report / Chatbot

## 💬 AI Healthcare Chatbot

The chatbot provides disease-specific information by using disease mapping and structured healthcare datasets.

For example:

- "What are the symptoms of Typhoid?"
- "What diet is recommended for Dengue?"
- "What are the precautions for Asthma?"
- "What are the causes of Diabetes?"
- "Which specialist should I consult for a disease?"

The chatbot also supports project-related questions such as:

- What is the objective of the project?
- What technologies are used?
- How does the system work?
- Which Machine Learning algorithm is used?
- What database is used?
- What are the advantages?
- What are the limitations?
- What is the future scope?

## 📂 Healthcare Datasets

The system uses separate CSV datasets for different categories of healthcare information, including:

- `symptom_description.csv`
- `symptom_precaution.csv`
- `diet.csv`
- `exercise.csv`
- `medicine.csv`
- `doctor_specialist.csv`
- `health_tips.csv`
- `disease_causes.csv`
- `disease_diagnosis.csv`
- `disease_lab_tests.csv`
- `disease_risk_factors.csv`
- `disease_complications.csv`
- `disease_prevention.csv`
- `disease_treatment.csv`
- `disease_severity.csv`
- `emergency_level.csv`

This structure allows disease-specific information to be maintained and retrieved independently.

## 🛠️ Technologies Used

- **Python**
- **Flask**
- **Machine Learning**
- **scikit-learn**
- **Pandas**
- **Joblib**
- **Oracle Database**
- **HTML5**
- **CSS3**
- **JavaScript**
- **Bootstrap**
- **ReportLab**
- **CSV Datasets**

## 👨‍💼 Admin Panel

The Admin Panel provides administrative functionality for managing the application.

Main areas include:

- User Management
- Prediction Management
- Dataset Management
- Healthcare Data Management
- Viewing and managing system information

Dataset management allows authorized administrators to maintain healthcare information used by the Recommendation Service.

## 📜 Prediction History

Every completed prediction can be stored in the Oracle Database. Users can access their previous predictions and view details such as:

- Prediction ID
- Prediction Date
- Predicted Disease
- Confidence Score
- Symptoms Used

## 📄 PDF Reports

The system provides downloadable PDF reports containing prediction-related information and user details using the PDF generation module.

## 🗄️ Database

Oracle Database is used for persistent application data such as:

- User Accounts
- User Profiles
- Prediction History
- Prediction Records

Healthcare recommendation information is maintained separately through structured CSV datasets.

## 📁 Project Architecture

```text
Healthcare AI
│
├── app.py
├── db.py
│
├── models/
│   ├── disease_model.pkl
│   ├── label_encoder.pkl
│   └── symptoms.pkl
│
├── routes/
│   ├── auth.py
│   ├── prediction.py
│   ├── admin.py
│   ├── chatbot.py
│   ├── history.py
│   └── profile.py
│
├── services/
│   ├── chatbot_service.py
│   ├── recommendation_service.py
│   ├── history_service.py
│   ├── profile_service.py
│   └── pdf_service.py
│
├── dataset/
│   ├── diet.csv
│   ├── exercise.csv
│   ├── medicine.csv
│   ├── symptom_description.csv
│   ├── symptom_precaution.csv
│   ├── disease_causes.csv
│   ├── disease_diagnosis.csv
│   ├── disease_lab_tests.csv
│   ├── disease_risk_factors.csv
│   ├── disease_complications.csv
│   ├── disease_prevention.csv
│   ├── disease_treatment.csv
│   ├── disease_severity.csv
│   ├── doctor_specialist.csv
│   ├── health_tips.csv
│   └── emergency_level.csv
│
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── symptoms.html
│   ├── prediction_result.html
│   ├── history.html
│   ├── view_prediction.html
│   ├── chatbot.html
│   ├── profile.html
│   └── admin.html
│
└── static/
    ├── css/
    ├── js/
    └── images/
