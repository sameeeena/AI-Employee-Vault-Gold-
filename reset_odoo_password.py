"""
Reset Odoo Admin Password
Run this script to reset the admin password for odoo_db
"""
import psycopg2

# Connect to PostgreSQL
print("Connecting to PostgreSQL...")
try:
    conn = psycopg2.connect(
        host="localhost",
        database="odoo_db",
        user="openpg",
        password="openpgpwd"
    )
    conn.autocommit = True
    cur = conn.cursor()
    
    # Check if res_users table exists and has data
    print("Checking res_users table...")
    cur.execute("SELECT COUNT(*) FROM res_users;")
    count = cur.fetchone()[0]
    print(f"Total users in res_users: {count}")
    
    if count > 0:
        # List available users
        print("\nAvailable users:")
        cur.execute("SELECT id, login FROM res_users ORDER BY id LIMIT 10;")
        users = cur.fetchall()
        for user in users:
            print(f"  ID: {user[0]}, Login: {user[1]}")
        
        # Reset password for admin user (sameena02134@gmail.com)
        admin_login = "sameena02134@gmail.com"
        print(f"\nResetting password for user '{admin_login}' to 'admin'...")
        cur.execute(f"UPDATE res_users SET password='admin' WHERE login=%s;", (admin_login,))
        print(f"[OK] Password reset successful!")
        print(f"\nYou can now login with:")
        print(f"  Database: odoo_db")
        print(f"  Username: {admin_login}")
        print(f"  Password: admin")
    else:
        print("[ERROR] res_users table is empty!")
        print("The database might not have been initialized properly.")
        print("\nPlease:")
        print("  1. Go to http://localhost:8069")
        print("  2. Create a new database or reinitialize odoo_db")
        
    cur.close()
    conn.close()
    
except Exception as e:
    print(f"[ERROR] {e}")
    print("\nPossible issues:")
    print("  - PostgreSQL is not running")
    print("  - Database 'odoo_db' does not exist")
    print("  - Credentials in script are incorrect")
