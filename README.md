# 📚 Student Record Management System (SRMS)
**Mini Project — VCACS College | Shruti V. Bhosale, SY BSc(CS), Roll No: 41**

---

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.9+
- A [Supabase](https://supabase.com) account (free tier works)

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Supabase Database
1. Create a new project on [supabase.com](https://supabase.com)
2. Go to **SQL Editor** and paste the contents of `schema.sql`
3. Run the SQL to create all tables
4. Copy your **Connection String** from:
   - Project Settings → Database → Connection string → URI

### 4. Configure Environment
```bash
# Option A: Set environment variable (recommended)
export DATABASE_URL="postgresql://postgres:YOUR_PASSWORD@db.YOUR_PROJECT.supabase.co:5432/postgres"
export SECRET_KEY="any-random-secret-string"

# Option B: Edit app.py directly and replace the DATABASE_URL default value
```

### 5. Seed Admin User
```bash
python seed.py
```
This creates:
- Admin login: `admin` / `admin123`
- Sample classes and courses

### 6. Run the App
```bash
python app.py
```
Visit: **http://localhost:5000**

---

## 📁 Project Structure

```
student_rms/
├── app.py              # Flask application (routes, logic)
├── schema.sql          # PostgreSQL table definitions
├── seed.py             # Creates admin user + sample data
├── requirements.txt    # Python dependencies
├── README.md
├── templates/
│   ├── base.html       # Layout with sidebar
│   ├── login.html      # Login page
│   ├── dashboard.html  # Main dashboard
│   ├── students.html   # Student list + search
│   ├── add_student.html
│   ├── edit_student.html
│   ├── student_detail.html
│   ├── reports.html    # Charts & analytics
│   ├── profile.html
│   └── about.html
└── static/
    ├── css/main.css
    └── js/main.js
```

---

## 🗄️ Database Schema

| Table        | Description                            |
|-------------|----------------------------------------|
| `users`      | Admin accounts with hashed passwords  |
| `students`   | Core student records (12 fields)       |
| `classes`    | Class/section definitions              |
| `teachers`   | Teacher records with specialization    |
| `courses`    | Course catalog                         |
| `subjects`   | Subjects linked to classes/teachers    |
| `enrollment` | Student-course enrollment              |
| `exams`      | Exam definitions                       |
| `results`    | Student marks and grades               |
| `attendance` | Per-student attendance records         |
| `fees`       | Fee payment tracking                   |

---

## 📄 Pages

| Page              | URL                     | Description                        |
|------------------|-------------------------|------------------------------------|
| Login             | `/login`                | Admin authentication               |
| Dashboard         | `/dashboard`            | Stats overview + recent admissions |
| View Students     | `/students`             | Table with search/filter           |
| Add Student       | `/students/add`         | Multi-section form                 |
| Edit Student      | `/students/edit/<id>`   | Pre-filled edit form               |
| Student Profile   | `/students/view/<id>`   | Full profile with results/fees     |
| Reports           | `/reports`              | Charts + department stats          |
| Profile           | `/profile`              | Admin account settings             |
| About / Help      | `/about`                | Project info + setup guide         |

---

## 🛡️ Security Notes
- Passwords are hashed with Werkzeug's `generate_password_hash` (scrypt)
- All routes (except login) are protected with `@login_required`
- Change the default admin password immediately after first login
- Set a strong `SECRET_KEY` in production

---

## 📦 Tech Stack
- **Backend**: Python 3 / Flask 3
- **Database**: PostgreSQL via Supabase
- **DB Driver**: psycopg2
- **Frontend**: HTML5, CSS3, Vanilla JS
- **Templates**: Jinja2
- **Charts**: Chart.js 4
- **Fonts**: Syne + DM Sans (Google Fonts)
