"""
Database configuration and connection management using raw SQL.
Supports both SQLite (development) and PostgreSQL (Supabase production).
"""
import os
import json
import sqlite3
from typing import Optional, Dict, Any, List
from contextlib import contextmanager
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Try to import psycopg2 for PostgreSQL support
try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    PSYCOPG2_AVAILABLE = True
except ImportError:
    PSYCOPG2_AVAILABLE = False

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./burnout_detection.db")
IS_POSTGRES = DATABASE_URL.startswith("postgresql://") or DATABASE_URL.startswith("postgres://")


def get_connection():
    """
    Get database connection based on DATABASE_URL.
    Returns SQLite or PostgreSQL connection.
    """
    if IS_POSTGRES:
        if not PSYCOPG2_AVAILABLE:
            raise ImportError(
                "psycopg2 is required for PostgreSQL. Install with: pip install psycopg2-binary"
            )
        return psycopg2.connect(DATABASE_URL)
    else:
        # SQLite connection
        conn = sqlite3.connect(DATABASE_URL.replace("sqlite:///", ""), check_same_thread=False)
        conn.row_factory = sqlite3.Row  # Return rows as dict-like objects
        return conn


@contextmanager
def get_db():
    """
    Database connection context manager.
    Yields a connection and ensures it's closed.
    """
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def execute_query(query: str, params: tuple = None, fetch_one: bool = False, fetch_all: bool = False):
    """
    Execute a SQL query and return results.
    
    Args:
        query: SQL query string
        params: Query parameters tuple
        fetch_one: Return single row
        fetch_all: Return all rows
        
    Returns:
        Query results based on fetch flags
    """
    with get_db() as conn:
        cursor = conn.cursor()
        
        if IS_POSTGRES and PSYCOPG2_AVAILABLE:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute(query, params or ())
        
        if fetch_one:
            result = cursor.fetchone()
            if result and not IS_POSTGRES:
                # Convert SQLite Row to dict
                return dict(result)
            return result
        elif fetch_all:
            results = cursor.fetchall()
            if results and not IS_POSTGRES:
                # Convert SQLite Rows to dicts
                return [dict(row) for row in results]
            return results
        else:
            return cursor.rowcount


def init_db():
    """
    Initialize database by creating all tables.
    Reads SQL schema from schema.sql (SQLite) or schema_postgresql.sql (PostgreSQL).
    """
    # Choose schema file based on database type
    if IS_POSTGRES:
        schema_file = os.path.join(os.path.dirname(__file__), "schema_postgresql.sql")
    else:
        schema_file = os.path.join(os.path.dirname(__file__), "schema.sql")
    
    if not os.path.exists(schema_file):
        raise FileNotFoundError(f"Schema file not found: {schema_file}")
    
    with open(schema_file, "r", encoding="utf-8") as f:
        schema_sql = f.read()
    
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Split by semicolon and execute each statement
        # Filter out empty statements and comments-only statements
        statements = []
        for s in schema_sql.split(";"):
            s = s.strip()
            # Skip completely empty strings
            if not s:
                continue
            
            # Remove inline comments (everything after --)
            lines = []
            for line in s.split("\n"):
                # Find comment position
                comment_pos = line.find("--")
                if comment_pos >= 0:
                    line = line[:comment_pos]
                line = line.strip()
                if line:
                    lines.append(line)
            
            # Join lines and check if there's actual SQL content
            cleaned_statement = " ".join(lines).strip()
            
            # Only add if there's actual SQL content (not just whitespace/comments)
            if cleaned_statement and len(cleaned_statement) > 0:
                statements.append(cleaned_statement)
        
        # Execute each statement
        for statement in statements:
            # Double-check statement is not empty
            if not statement or len(statement.strip()) == 0:
                continue
                
            try:
                cursor.execute(statement)
            except Exception as e:
                # Ignore "table already exists" errors
                error_msg = str(e).lower()
                if ("already exists" in error_msg or 
                    "duplicate" in error_msg or
                    ("relation" in error_msg and "already exists" in error_msg)):
                    # Table/index already exists, skip silently
                    continue
                else:
                    # Re-raise other errors
                    raise
        
        conn.commit()


def dict_to_json(value: Any) -> str:
    """Convert dict/list to JSON string for database storage."""
    if isinstance(value, (dict, list)):
        return json.dumps(value)
    return value


def json_to_dict(value: Any) -> Any:
    """Convert JSON string from database to dict/list."""
    if isinstance(value, str):
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return value
    return value


def row_to_dict(row: Any, json_fields: List[str] = None) -> Dict[str, Any]:
    """
    Convert database row to dictionary.
    Handles both SQLite Row objects and PostgreSQL RealDictCursor rows.
    
    Args:
        row: Database row object
        json_fields: List of field names that contain JSON data
        
    Returns:
        Dictionary representation of row
    """
    if row is None:
        return None
    
    json_fields = json_fields or []
    
    if IS_POSTGRES and isinstance(row, dict):
        result = dict(row)
    elif hasattr(row, "keys"):  # SQLite Row object
        result = dict(row)
    else:
        # Fallback for tuple rows
        return None
    
    # Convert JSON fields
    for field in json_fields:
        if field in result:
            result[field] = json_to_dict(result[field])
    
    # Convert datetime strings to datetime objects if needed
    for key, value in result.items():
        if isinstance(value, str) and ("created_at" in key or "updated_at" in key or "timestamp" in key):
            try:
                result[key] = datetime.fromisoformat(value.replace("Z", "+00:00"))
            except (ValueError, AttributeError):
                pass
    
    return result
