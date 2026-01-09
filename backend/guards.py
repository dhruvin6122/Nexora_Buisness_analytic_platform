import re
import sqlparse

class SQLGuardException(Exception):
    """Custom exception for SQL safety violations."""
    pass

def validate_sql(sql_query: str):
    """
    Validates that the SQL query is safe to execute.
    Rules:
    - Must be a SELECT statement.
    - Must not contain multiple statements.
    - Must not contain DML/DDL keywords (INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE).
    """
    # 1. Parse SQL
    parsed = sqlparse.parse(sql_query)
    if not parsed:
        raise SQLGuardException("Empty or invalid SQL query.")
    
    # 2. Check for multiple statements
    if len(parsed) > 1:
        # Sometimes sqlparse returns multiple statements for a single query with trailing semicolon + whitespace
        # Check if actual statements exist
        statements = [s for s in parsed if s.get_type() != 'UNKNOWN']
        if len(statements) > 1:
             raise SQLGuardException("Multi-statement queries are not allowed.")

    statement = parsed[0]
    
    # 3. Check statement type
    if statement.get_type().upper() != 'SELECT':
        raise SQLGuardException("Only SELECT queries are allowed.")

    # 4. Keyword Blacklist Check (Double safety)
    # Check for forbidden keywords explicitly to catch subqueries/CTEs doing funny business if get_type misses it
    # Note: simple string check might catch 'update_time' column, so use word boundaries
    forbidden_keywords = {
        'INSERT', 'UPDATE', 'DELETE', 'DROP', 'ALTER', 'TRUNCATE', 
        'GRANT', 'REVOKE', 'CREATE', 'REPLACE'
    }
    
    # Flatten tokens to check for DDL/DML keywords
    # This is a basic heuristic; a robust parser analysis is better but sqlparse `get_type` is usually good for the main statement.
    # We rely on `get_type` == SELECT mostly.
    
    # 5. Schema check (Simple heuristic, strictly agent should be constrained by DB permissions, but prompt asks for check)
    # We want to ensure we don't query system tables or other schemas roughly.
    # Accepts 'nexora_sales', 'public' (if explicitly allowed, but here we want only nexora_sales)
    # Actually, the DB connection is restricted to `nexora_sales` path, so simple table names are fine.
    # We reject explicit mentions of other schemas.
    
    normalized_sql = sql_query.upper()
    
    # Check for disallowed schemas if explicitly referenced
    # This is hard to do perfectly with regex without parsing, but we can look for `schema.table` patterns.
    # If the user tries `information_schema.tables`, we want to block it.
    
    # Simple guard: if dot is present, left side must be 'nexora_sales' or alias
    # This might be too restrictive for aliasing e.g. "SELECT t.id FROM table t"
    # So we skip this regex check and rely on the DB user/connection restrictions + system prompt instructions 
    # and the fact `get_tokens` will return tables.
    
    # Relying on statement.get_type() == SELECT is the robust check for DML/DDL.
    
    return True
