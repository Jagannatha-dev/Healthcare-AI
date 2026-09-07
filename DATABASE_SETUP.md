# Healthcare AI - Database Setup

## Oracle XE / XEPDB1

The application is configured for Oracle Database service `XEPDB1` on port `1521` by default.

## Environment variables

Create a local `.env` file or set these variables in the operating system. Do not commit `.env`.

```text
HEALTHCARE_AI_SECRET_KEY=<long-random-secret>
HEALTHCARE_AI_DB_USER=healthcare_ai
HEALTHCARE_AI_DB_PASSWORD=<your-oracle-password>
HEALTHCARE_AI_DB_HOST=localhost
HEALTHCARE_AI_DB_PORT=1521
HEALTHCARE_AI_DB_SERVICE=XEPDB1
```

The repository includes `.env.example` as a template.

## Test the connection

From the project virtual environment:

```powershell
& ".\venv\Scripts\python.exe" ".\test_db.py"
```

Expected result:

```text
Oracle connection test PASSED
Service: XEPDB1
```

## Manual Oracle check

```text
C:\Temp\sqlplus.exe system@localhost:1521/XEPDB1
```

Then:

```sql
SELECT table_name FROM user_tables ORDER BY table_name;
SELECT COUNT(*) FROM USERS;
SELECT COUNT(*) FROM PREDICTION_HISTORY;
```

## Important security note

If database credentials have ever been committed to a public repository, rotate the Oracle database password and use a new secret. Environment variables prevent the new password from being stored in source code, but they do not revoke an already exposed password.
