import mysql.connector
from mysql.connector import Error
import streamlit as st

# --- DATABASE CONFIGURATION ---
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "admin"  # <--- UPDATE THIS WITH YOUR MYSQL PASSWORD
DB_NAME = "streaming_db"

def get_connection():
    """Establish a connection to the MySQL database."""
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return connection
    except Error as e:
        # If database doesn't exist, connect without database to create it
        try:
            conn = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD
            )
            return conn
        except Error as err:
            st.error(f"Error connecting to MySQL: {err}")
            return None

def execute_query(query, params=None, fetch=False):
    """Execute a single query and return results if fetch is True."""
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, params or ())
            
            if fetch:
                result = cursor.fetchall()
                return result
            
            conn.commit()
            return True
        except Error as e:
            st.error(f"Query Error: {e}")
            return None
        finally:
            cursor.close()
            conn.close()
    return None

def init_db(ddl_path, dummy_data_path=None):
    """Initialize the database using the DDL file."""
    conn = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD)
    cursor = conn.cursor()
    
    try:
        # Read and execute DDL
        with open(ddl_path, 'r') as f:
            sql_commands = f.read().split(';')
            for command in sql_commands:
                if command.strip():
                    cursor.execute(command)
        
        # Optionally insert dummy data if tables are empty
        if dummy_data_path:
            cursor.execute("SELECT COUNT(*) FROM Users")
            if cursor.fetchone()[0] == 0:
                with open(dummy_data_path, 'r') as f:
                    sql_commands = f.read().split(';')
                    for command in sql_commands:
                        if command.strip():
                            cursor.execute(command)
        
        conn.commit()
        return True
    except Error as e:
        print(f"Init DB Error: {e}")
        return False
    finally:
        cursor.close()
        conn.close()
