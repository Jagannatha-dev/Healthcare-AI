# Local Configuration and Secret Safety

The application reads Flask and Oracle settings from environment variables. Keep real credentials in a local `.env` file or your operating-system environment, and never commit that file.

Required variables:

- `HEALTHCARE_AI_SECRET_KEY`
- `HEALTHCARE_AI_DB_USER`
- `HEALTHCARE_AI_DB_PASSWORD`
- `HEALTHCARE_AI_DB_HOST`
- `HEALTHCARE_AI_DB_PORT`
- `HEALTHCARE_AI_DB_SERVICE`

The repository may contain older commits with credentials. If a real database password was previously committed, rotate that password in Oracle and then use the new value locally.
