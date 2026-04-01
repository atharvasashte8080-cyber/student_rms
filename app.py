"""
Student Record Management System
Flask Backend Application
Author: Shruti V. Bhosale (Mini Project)
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from functools import wraps
import psycopg2
import psycopg2.extras
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'srms_secret_key_2024_vcacs')

# ─── DATABASE CONFIG ───────────────────────────────────────────────────────────
# Replace with your Supabase PostgreSQL connection string
DATABASE_URL = os.environ.get(
    'DATABASE_URL',
    'postgresql://postgres.lmpelkcqwvximzvnobsr:nCg2UVPDxkZ3SvZJ@aws-1-ap-northeast-1.pooler.supabase.com:6543/postgres'
)

def get_db():
    """Get a database connection."""
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = False
    return conn

def query_db(sql, args=(), one=False, commit=False):
    """Helper to run queries safely."""
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        cur.execute(sql, args)
        if commit:
            conn.commit()
            return cur.rowcount
        rv = cur.fetchone() if one else cur.fetchall()
        return rv
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()

# ─── AUTH DECORATOR ────────────────────────────────────────────────────────────
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

# ─── AUTH ROUTES ───────────────────────────────────────────────────────────────
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        if not username or not password:
            flash('Username and password are required.', 'error')
            return render_template('login.html')

        try:
            user = query_db(
                'SELECT * FROM users WHERE username = %s',
                (username,), one=True
            )
            if user and check_password_hash(user['password_hash'], password):
                session['user_id'] = user['id']
                session['username'] = user['username']
                session['full_name'] = user.get('full_name', username)
                flash(f'Welcome back, {session["full_name"]}!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid username or password.', 'error')
        except Exception as e:
            flash('Database connection error. Check your config.', 'error')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('login'))


# ─── DASHBOARD ─────────────────────────────────────────────────────────────────
@app.route('/dashboard')
@login_required
def dashboard():
    try:
        total_students = query_db('SELECT COUNT(*) as cnt FROM students', one=True)['cnt']
        total_courses  = query_db('SELECT COUNT(*) as cnt FROM courses', one=True)['cnt']
        total_teachers = query_db('SELECT COUNT(*) as cnt FROM teachers', one=True)['cnt']
        total_classes  = query_db('SELECT COUNT(*) as cnt FROM classes', one=True)['cnt']

        recent_students = query_db(
            'SELECT * FROM students ORDER BY created_at DESC LIMIT 5'
        )
        dept_stats = query_db(
            'SELECT department, COUNT(*) as cnt FROM students GROUP BY department ORDER BY cnt DESC'
        )
    except Exception as e:
        flash('Could not load dashboard data. ' + str(e), 'error')
        total_students = total_courses = total_teachers = total_classes = 0
        recent_students = []
        dept_stats = []

    return render_template('dashboard.html',
        total_students=total_students,
        total_courses=total_courses,
        total_teachers=total_teachers,
        total_classes=total_classes,
        recent_students=recent_students,
        dept_stats=dept_stats
    )


# ─── STUDENTS ──────────────────────────────────────────────────────────────────
@app.route('/students')
@login_required
def view_students():
    search = request.args.get('search', '').strip()
    dept   = request.args.get('dept', '').strip()
    cls    = request.args.get('class', '').strip()

    sql  = 'SELECT * FROM students WHERE 1=1'
    args = []

    if search:
        sql  += ' AND (first_name ILIKE %s OR last_name ILIKE %s OR roll_no ILIKE %s)'
        like  = f'%{search}%'
        args += [like, like, like]
    if dept:
        sql  += ' AND department = %s'
        args.append(dept)
    if cls:
        sql  += ' AND class_id = %s'
        args.append(cls)

    sql += ' ORDER BY created_at DESC'

    try:
        students    = query_db(sql, args)
        departments = query_db('SELECT DISTINCT department FROM students ORDER BY department')
        classes     = query_db('SELECT * FROM classes ORDER BY class_name')
    except Exception as e:
        flash('Error loading students: ' + str(e), 'error')
        students = departments = classes = []

    return render_template('students.html',
        students=students,
        departments=departments,
        classes=classes,
        search=search,
        selected_dept=dept,
        selected_class=cls
    )


@app.route('/students/add', methods=['GET', 'POST'])
@login_required
def add_student():
    if request.method == 'POST':
        data = {
            'first_name':   request.form.get('first_name', '').strip(),
            'last_name':    request.form.get('last_name', '').strip(),
            'roll_no':      request.form.get('roll_no', '').strip(),
            'gender':       request.form.get('gender', '').strip(),
            'dob':          request.form.get('dob') or None,
            'email':        request.form.get('email', '').strip(),
            'phone_no':     request.form.get('phone_no', '').strip(),
            'address':      request.form.get('address', '').strip(),
            'guardian_name':request.form.get('guardian_name', '').strip(),
            'guardian_contact': request.form.get('guardian_contact', '').strip(),
            'department':   request.form.get('department', '').strip(),
            'class_id':     request.form.get('class_id') or None,
            'admission_date': request.form.get('admission_date') or None,
        }

        # Basic validation
        if not data['first_name'] or not data['roll_no'] or not data['department']:
            flash('First name, roll number, and department are required.', 'error')
        else:
            try:
                query_db('''
                    INSERT INTO students
                        (first_name, last_name, roll_no, gender, dob, email,
                         phone_no, address, guardian_name, guardian_contact,
                         department, class_id, admission_date)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ''', list(data.values()), commit=True)
                flash('Student added successfully!', 'success')
                return redirect(url_for('view_students'))
            except psycopg2.errors.UniqueViolation:
                flash('Roll number already exists. Use a unique roll number.', 'error')
            except Exception as e:
                flash('Error adding student: ' + str(e), 'error')

    try:
        classes = query_db('SELECT * FROM classes ORDER BY class_name')
    except:
        classes = []

    return render_template('add_student.html', classes=classes)


@app.route('/students/edit/<int:sid>', methods=['GET', 'POST'])
@login_required
def edit_student(sid):
    try:
        student = query_db('SELECT * FROM students WHERE id = %s', (sid,), one=True)
    except Exception as e:
        flash('Student not found.', 'error')
        return redirect(url_for('view_students'))

    if not student:
        flash('Student not found.', 'error')
        return redirect(url_for('view_students'))

    if request.method == 'POST':
        data = {
            'first_name':   request.form.get('first_name', '').strip(),
            'last_name':    request.form.get('last_name', '').strip(),
            'roll_no':      request.form.get('roll_no', '').strip(),
            'gender':       request.form.get('gender', '').strip(),
            'dob':          request.form.get('dob') or None,
            'email':        request.form.get('email', '').strip(),
            'phone_no':     request.form.get('phone_no', '').strip(),
            'address':      request.form.get('address', '').strip(),
            'guardian_name': request.form.get('guardian_name', '').strip(),
            'guardian_contact': request.form.get('guardian_contact', '').strip(),
            'department':   request.form.get('department', '').strip(),
            'class_id':     request.form.get('class_id') or None,
            'admission_date': request.form.get('admission_date') or None,
            'id': sid
        }

        if not data['first_name'] or not data['roll_no']:
            flash('First name and roll number are required.', 'error')
        else:
            try:
                query_db('''
                    UPDATE students SET
                        first_name=%s, last_name=%s, roll_no=%s, gender=%s,
                        dob=%s, email=%s, phone_no=%s, address=%s,
                        guardian_name=%s, guardian_contact=%s,
                        department=%s, class_id=%s, admission_date=%s
                    WHERE id=%s
                ''', list(data.values()), commit=True)
                flash('Student updated successfully!', 'success')
                return redirect(url_for('view_students'))
            except Exception as e:
                flash('Error updating student: ' + str(e), 'error')

    try:
        classes = query_db('SELECT * FROM classes ORDER BY class_name')
    except:
        classes = []

    return render_template('edit_student.html', student=student, classes=classes)


@app.route('/students/delete/<int:sid>', methods=['POST'])
@login_required
def delete_student(sid):
    try:
        query_db('DELETE FROM students WHERE id = %s', (sid,), commit=True)
        flash('Student deleted successfully.', 'success')
    except Exception as e:
        flash('Error deleting student: ' + str(e), 'error')
    return redirect(url_for('view_students'))


@app.route('/students/view/<int:sid>')
@login_required
def student_detail(sid):
    try:
        student = query_db('SELECT * FROM students WHERE id = %s', (sid,), one=True)
        if not student:
            flash('Student not found.', 'error')
            return redirect(url_for('view_students'))
        fees = query_db('SELECT * FROM fees WHERE student_id = %s ORDER BY payment_date DESC', (sid,))
        results = query_db('''
            SELECT r.*, s.subject_name, e.exam_type, e.exam_date
            FROM results r
            LEFT JOIN subjects s ON r.subject_id = s.id
            LEFT JOIN exams e ON r.exam_id = e.id
            WHERE r.student_id = %s
            ORDER BY e.exam_date DESC
        ''', (sid,))
        attendance = query_db('''
            SELECT a.*, c.course_name FROM attendance a
            LEFT JOIN courses c ON a.course_id = c.id
            WHERE a.student_id = %s ORDER BY a.date DESC LIMIT 20
        ''', (sid,))
    except Exception as e:
        flash('Error loading student: ' + str(e), 'error')
        return redirect(url_for('view_students'))

    return render_template('student_detail.html', student=student, fees=fees, results=results, attendance=attendance)


# ─── REPORTS ───────────────────────────────────────────────────────────────────
@app.route('/reports')
@login_required
def reports():
    try:
        dept_stats    = query_db('SELECT department, COUNT(*) as cnt FROM students GROUP BY department ORDER BY cnt DESC')
        gender_stats  = query_db('SELECT gender, COUNT(*) as cnt FROM students GROUP BY gender')
        class_stats   = query_db('''
            SELECT cl.class_name, COUNT(s.id) as cnt
            FROM classes cl LEFT JOIN students s ON s.class_id = cl.id
            GROUP BY cl.class_name ORDER BY cnt DESC
        ''')
        fee_summary   = query_db('''
            SELECT payment_status, COUNT(*) as cnt, SUM(amount) as total
            FROM fees GROUP BY payment_status
        ''')
        monthly_admissions = query_db('''
            SELECT TO_CHAR(admission_date, 'YYYY-MM') as month, COUNT(*) as cnt
            FROM students WHERE admission_date IS NOT NULL
            GROUP BY month ORDER BY month DESC LIMIT 12
        ''')
    except Exception as e:
        flash('Error loading reports: ' + str(e), 'error')
        dept_stats = gender_stats = class_stats = fee_summary = monthly_admissions = []

    return render_template('reports.html',
        dept_stats=dept_stats,
        gender_stats=gender_stats,
        class_stats=class_stats,
        fee_summary=fee_summary,
        monthly_admissions=monthly_admissions
    )


# ─── API ENDPOINTS (for Chart.js) ──────────────────────────────────────────────
@app.route('/api/dept-stats')
@login_required
def api_dept_stats():
    data = query_db('SELECT department, COUNT(*) as cnt FROM students GROUP BY department')
    return jsonify([dict(r) for r in data])

@app.route('/api/gender-stats')
@login_required
def api_gender_stats():
    data = query_db('SELECT gender, COUNT(*) as cnt FROM students GROUP BY gender')
    return jsonify([dict(r) for r in data])


# ─── ABOUT / HELP ──────────────────────────────────────────────────────────────
@app.route('/about')
@login_required
def about():
    return render_template('about.html')


# ─── PROFILE ───────────────────────────────────────────────────────────────────
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        full_name    = request.form.get('full_name', '').strip()
        email        = request.form.get('email', '').strip()
        new_password = request.form.get('new_password', '').strip()

        try:
            if new_password:
                hashed = generate_password_hash(new_password)
                query_db(
                    'UPDATE users SET full_name=%s, email=%s, password_hash=%s WHERE id=%s',
                    (full_name, email, hashed, session['user_id']), commit=True
                )
            else:
                query_db(
                    'UPDATE users SET full_name=%s, email=%s WHERE id=%s',
                    (full_name, email, session['user_id']), commit=True
                )
            session['full_name'] = full_name
            flash('Profile updated successfully!', 'success')
        except Exception as e:
            flash('Error updating profile: ' + str(e), 'error')

    try:
        user = query_db('SELECT * FROM users WHERE id=%s', (session['user_id'],), one=True)
    except:
        user = {}

    return render_template('profile.html', user=user)


if __name__ == "__main__":
    # Render will assign a port automatically; fallback to 5000 locally
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
