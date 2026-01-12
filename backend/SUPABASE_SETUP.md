# Supabase Setup Guide

This guide explains how to migrate from SQLite to Supabase (PostgreSQL) for production deployment.

## Prerequisites

- Supabase account ([sign up here](https://supabase.com))
- Python with `psycopg2-binary` installed

## Step 1: Create Supabase Project

1. Go to [supabase.com](https://supabase.com) and sign in
2. Click "New Project"
3. Fill in project details:
   - Name: Your project name
   - Database Password: Choose a strong password (save this!)
   - Region: Choose closest to your users
4. Wait for project to be created (2-3 minutes)

## Step 2: Get Database Connection String

1. In Supabase dashboard, go to **Project Settings** → **Database**
2. Find **Connection string** section
3. Copy the **URI** format connection string
   - Format: `postgresql://postgres:[YOUR-PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres`
   - Replace `[YOUR-PASSWORD]` with your database password

## Step 3: Update Environment Variables

Update your `backend/.env` file:

```env
# Change DATABASE_URL to Supabase connection string
DATABASE_URL=postgresql://postgres:your_password@db.xxxxx.supabase.co:5432/postgres

# Keep other settings
GOOGLE_GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL_NAME=gemini-pro
```

## Step 4: Install PostgreSQL Driver

```bash
cd backend
pip install psycopg2-binary
```

## Step 5: Create Database Schema

### Option 1: Using Supabase SQL Editor (Recommended)

1. Go to Supabase dashboard → **SQL Editor**
2. Click **New Query**
3. Copy contents of `backend/app/schema_postgresql.sql`
4. Paste into SQL Editor
5. Click **Run** (or press Ctrl+Enter)

### Option 2: Using psql Command Line

```bash
# Install psql if not available
# macOS: brew install postgresql
# Ubuntu: sudo apt-get install postgresql-client

# Run schema
psql $DATABASE_URL -f app/schema_postgresql.sql
```

### Option 3: Using Python Script

```bash
cd backend
python -c "
from app.database import get_connection
import os

# Read PostgreSQL schema
schema_file = os.path.join('app', 'schema_postgresql.sql')
with open(schema_file, 'r') as f:
    schema = f.read()

# Execute schema
conn = get_connection()
cursor = conn.cursor()

# Split by semicolon and execute each statement
statements = [s.strip() for s in schema.split(';') if s.strip()]
for statement in statements:
    if statement:
        cursor.execute(statement)

conn.commit()
conn.close()
print('Schema created successfully!')
"
```

## Step 6: Verify Connection

Test the connection:

```bash
cd backend
python -c "
from app.database import execute_query, row_to_dict

# Test query
result = execute_query('SELECT version()', fetch_one=True)
print('Connected to:', result)
"
```

## Step 7: Run Application

Start the backend server:

```bash
cd backend
uvicorn app.main:app --reload
```

The application will automatically use PostgreSQL when it detects a `postgresql://` connection string.

## Migration from SQLite to Supabase

If you have existing SQLite data:

1. **Export data from SQLite:**
   ```bash
   sqlite3 burnout_detection.db .dump > data_dump.sql
   ```

2. **Convert SQLite dump to PostgreSQL format:**
   - Remove SQLite-specific syntax
   - Convert `INTEGER PRIMARY KEY AUTOINCREMENT` to `SERIAL PRIMARY KEY`
   - Convert `TEXT` JSON fields to `JSONB`
   - Update timestamp formats

3. **Import to Supabase:**
   - Use Supabase SQL Editor or psql
   - Or write a migration script

## Troubleshooting

### Connection Errors

**Error: "psycopg2 not installed"**
```bash
pip install psycopg2-binary
```

**Error: "Connection refused"**
- Check your DATABASE_URL is correct
- Verify Supabase project is active
- Check firewall/network settings

**Error: "Authentication failed"**
- Verify database password in connection string
- Reset password in Supabase dashboard if needed

### Schema Errors

**Error: "relation already exists"**
- Tables already created, safe to ignore
- Or drop existing tables first (be careful!)

**Error: "syntax error"**
- Ensure you're using `schema_postgresql.sql` (not `schema.sql`)
- Check for SQLite-specific syntax

### Performance Tips

- Supabase automatically creates indexes
- Use connection pooling for production
- Monitor query performance in Supabase dashboard
- Consider enabling Row Level Security (RLS) for multi-tenant scenarios

## Security Best Practices

1. **Never commit connection strings to git**
   - Use `.env` file (already in `.gitignore`)
   - Use environment variables in production

2. **Use Supabase Row Level Security (RLS)**
   - Enable RLS in Supabase dashboard
   - Create policies to restrict data access

3. **Rotate database passwords regularly**
   - Update in Supabase dashboard
   - Update DATABASE_URL in environment

4. **Use Supabase API keys for client-side access**
   - Not needed for this backend-only setup
   - Consider for future frontend direct access

## Next Steps

- Set up database backups in Supabase
- Configure connection pooling
- Monitor database usage and performance
- Set up alerts for database issues

## Support

- [Supabase Documentation](https://supabase.com/docs)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [psycopg2 Documentation](https://www.psycopg.org/docs/)
