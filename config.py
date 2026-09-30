# ==========================================
# Flask Configuration
# ==========================================
# All sensitive values are now read from environment
# variables (loaded from a local .env file).
#
# Setup:
#   1. Copy .env.example to .env
#   2. Fill in your actual credentials in .env
#   3. Never commit .env to version control
#
# Generate a strong SECRET_KEY with:
#   python -c "import secrets; print(secrets.token_hex(32))"

import os

from dotenv import load_dotenv

load_dotenv()

# Flask secret key (used for session signing)
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-change-me")

# ==========================================
# Oracle Database Configuration
# ==========================================

DB_USER = os.environ.get("DB_USER", "healthcare_ai")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "")
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT", "1521")
DB_SERVICE = os.environ.get("DB_SERVICE", "XEPDB1")

# ==========================================
# Upload Folder
# ==========================================

UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER", "uploads")

# ==========================================
# Allowed Extensions
# ==========================================

ALLOWED_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg",
    "pdf"
}
