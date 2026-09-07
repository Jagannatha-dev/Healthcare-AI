# ==========================================
# Flask Configuration
# ==========================================

import os
import secrets

SECRET_KEY = os.getenv("HEALTHCARE_AI_SECRET_KEY", secrets.token_hex(32))

# ==========================================
# Oracle Database Configuration
# ==========================================
# Keep database credentials outside source control.
# The service defaults match the local Oracle XE/XEPDB1 setup.

DB_USER = os.getenv("HEALTHCARE_AI_DB_USER", "healthcare_ai")
DB_PASSWORD = os.getenv("HEALTHCARE_AI_DB_PASSWORD")
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
