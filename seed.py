"""
seed.py — Run once to create the default admin user
Usage: python seed.py
"""
import psycopg2
from werkzeug.security import generate_password_hash
import os

DATABASE_URL = os.environ.get(
    'DATABASE_URL',
    'postgresql://postgres.lmpelkcqwvximzvnobsr:nCg2UVPDxkZ3SvZJ@aws-1-ap-northeast-1.pooler.supabase.com:6543/postgres?sslmode=require'
)

def seed():
    conn = psycopg2.connect(DATABASE_URL)
    cur  = conn.cursor()

    # Admin user
    hashed = generate_password_hash('admin123')
    cur.execute('''
        INSERT INTO users (username, email, full_name, password_hash)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (username) DO UPDATE SET password_hash = EXCLUDED.password_hash
    ''', ('admin', 'admin@vcacs.edu', 'System Administrator', hashed))

    # Sample classes
    classes = [
        ('FY BSc CS', '2024'), ('SY BSc CS', '2024'),
        ('TY BSc CS', '2024'), ('FY BCA', '2024'),
        ('SY BCA', '2024'),    ('TY BCA', '2024'),
    ]
    for cn, yr in classes:
        cur.execute('INSERT INTO classes (class_name, year) VALUES (%s,%s) ON CONFLICT DO NOTHING', (cn, yr))

    # Sample departments / courses
    courses = [
        ('Data Structures',    'CS101', 4, 'Core CS subject'),
        ('Database Management','CS201', 4, 'DBMS fundamentals'),
        ('Web Technology',     'CS301', 3, 'HTML/CSS/JS/Flask'),
        ('Operating Systems',  'CS401', 4, 'OS concepts'),
        ('Python Programming', 'CS105', 3, 'Python language'),
    ]
    for row in courses:
        cur.execute('''
            INSERT INTO courses (course_name, course_code, credit_hours, description)
            VALUES (%s,%s,%s,%s) ON CONFLICT (course_code) DO NOTHING
        ''', row)

    conn.commit()
    cur.close()
    conn.close()
    print("✅ Database seeded successfully!")
    print("   Admin login → username: admin | password: admin123")

if __name__ == '__main__':
    seed()
