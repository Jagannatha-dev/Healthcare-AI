# ==========================================
# Flask Configuration
# ==========================================

import os

SECRET_KEY = os.getenv("HEALTHCARE_AI_SECRET_KEY", "Healthcare_AI_2026")

# ==========================================
# Oracle Database Configuration
# ==========================================
# Values can be provided through environment variables.
# Local defaults keep the existing XEPDB1 setup working.

DB_USER = os.getenv("HEALTHCARE_AI_DB_USER", "healthcare_ai")
DB_PASSWORD = os.getenv("HEALTHCARE_AI_DB_PASSWORD", "Healthcare123")
DB_HOST = os.getenv("HEALTHCARE_AI_DB_HOST", "localhost")
DB_PORT = int(os.getenv("HEALTHCARE_AI_DB_PORT", "1521"))
DB_SERVICE = os.getenv("HEALTHCARE_AI_DB_SERVICE", "XEPDB1")

# ==========================================
# Upload Folder
# ==========================================

UPLOAD_FOLDER = "uploads"

# ==========================================
# Allowed Extensions
# ==========================================

ALLOWED_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg",
    "pdf"
}
