"""
User management routes using raw SQL.
"""
from fastapi import APIRouter, HTTPException
from app.database import get_db, execute_query, row_to_dict, IS_POSTGRES
from app import schemas, models
from datetime import datetime
import json

router = APIRouter(prefix="/api/users", tags=["users"])


@router.post("/", response_model=schemas.UserResponse, status_code=201)
def create_user(user: schemas.UserCreate):
    """
    Create a new user.
    """
    try:
        if IS_POSTGRES:
            query = """
                INSERT INTO users (name, age_range, occupation_type, created_at)
                VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
                RETURNING user_id, name, age_range, occupation_type, created_at
            """
            result = execute_query(
                query,
                params=(user.name, user.age_range, user.occupation_type),
                fetch_one=True
            )
            if not result:
                raise HTTPException(status_code=500, detail="Failed to create user")
            return row_to_dict(result)
        else:
            # SQLite
            query = """
                INSERT INTO users (name, age_range, occupation_type, created_at)
                VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            """
            execute_query(query, params=(user.name, user.age_range, user.occupation_type))
            
            # Get the inserted user
            get_query = "SELECT * FROM users WHERE user_id = (SELECT last_insert_rowid())"
            result = execute_query(get_query, fetch_one=True)
            if not result:
                raise HTTPException(status_code=500, detail="Failed to create user")
            return row_to_dict(result)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}")


@router.get("/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int):
    """
    Get user by ID.
    """
    if IS_POSTGRES:
        query = "SELECT * FROM users WHERE user_id = %s"
    else:
        query = "SELECT * FROM users WHERE user_id = ?"
    
    result = execute_query(query, params=(user_id,), fetch_one=True)
    
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    
    return row_to_dict(result)


@router.get("/", response_model=list[schemas.UserResponse])
def list_users(skip: int = 0, limit: int = 100):
    """
    List all users (for testing/admin purposes).
    """
    if IS_POSTGRES:
        query = "SELECT * FROM users ORDER BY user_id LIMIT %s OFFSET %s"
    else:
        query = "SELECT * FROM users ORDER BY user_id LIMIT ? OFFSET ?"
    
    results = execute_query(query, params=(limit, skip), fetch_all=True)
    return [row_to_dict(row) for row in results]
