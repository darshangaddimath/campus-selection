# 🎓 Campus Placement Analytics & Preparation Portal

A comprehensive Django-based web platform for BCA final year project that provides students with placement probability predictions, eligibility checking, and mock test capabilities.

## 🚀 Features

### Student Module
- ✅ **Profile Management**: Update CGPA, skills, and project details
- ✅ **Mock Aptitude Tests**: Take practice tests with 15 questions
- ✅ **Eligibility Checker**: Check eligibility against 10+ companies
- ✅ **Placement Prediction**: AI-driven probability calculation using exact formula
- ✅ **Interactive Dashboard**: Visual analytics with Chart.js

### Admin Module
- ✅ **Company Management**: Add/update/delete company requirements
- ✅ **Test Management**: Manage mock test questions
- ✅ **Analytics Dashboard**: View overall student performance
- ✅ **Top Performers**: Identify high-potential students

## 📊 Placement Prediction Formula (Exact Implementation)

The placement probability is calculated using the **EXACT weighted scoring algorithm**:

```
CGPA Score (40%)     = (Student CGPA / 10.0) × 40
Skill Score (40%)    = (Average Skill Match % across all companies) × 0.4
Test Score (20%)     = (Mock Test Percentage) × 0.2
─────────────────────────────────────────────────────────────
Final Probability     = CGPA Score + Skill Score + Test Score

Classification:
- High:      75% and above
- Medium:    50% - 74%
- Low:       35% - 49%
- Very Low:  Below 35%
```

## 🛠️ Tech Stack

- **Backend**: Django 4.2+ (Python)
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Styling**: Bootstrap 5 (CDN)
- **Visualization**: Chart.js 4.4+
- **Icons**: Bootstrap Icons

## 📋 Database Schema

### StudentProfile
- `user` (OneToOne to User)
- `cgpa` (FloatField) - Out of 10
- `skills` (TextField) - Comma-separated
- `projects` (TextField)

### Company
- `name` (CharField)
- `role` (CharField)
- `min_cgpa` (FloatField)
- `required_skills` (TextField)
- `description` (TextField)

### Question
- `text` (CharField)
- `option_a, option_b, option_c, option_d` (CharField)
- `correct_option` (CharField)
- `question_type` (CharField)

### TestResult
- `student` (ForeignKey to StudentProfile)
- `score` (IntegerField)
- `total_questions` (IntegerField)
- `date_taken` (DateTimeField)

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Step 1: Navigate to Project
```bash
cd campus_placement
```

### Step 2: Install Dependencies
```bash
pip install Django
```

### Step 3: Run Migrations
```bash
python manage.py migrate
```

### Step 4: Create Superuser (Admin)
```bash
python manage.py createsuperuser
```
- Username: `admin`
- Email: `admin@campus.com`
- Password: `admin123`

### Step 5: Seed Sample Data
```bash
python seed_data.py
```
This creates:
- **10 Companies**: Google, Microsoft, Amazon, Infosys, TCS, Wipro, Accenture, Deloitte, IBM, Oracle
- **15 Questions**: Mix of aptitude, technical, quantitative, and reasoning

### Step 6: Run Development Server
```bash
python manage.py runserver
```

### Step 7: Access the Application
- **Main URL**: http://127.0.0.1:8000/
- **Admin Login**: http://127.0.0.1:8000/login/ (use admin credentials)
- **Student Register**: http://127.0.0.1:8000/register/

## 📱 How to Use

### For Students

1. **Register**: Create a student account
2. **Update Profile**:
   - Add your CGPA (out of 10)
   - List your technical skills (comma-separated)
   - Describe your projects
3. **Take Mock Test**:
   - Go to Mock Test page
   - Answer 15 questions
   - Get immediate score
4. **View Dashboard**:
   - See your placement probability
   - Check eligible companies
   - View skill gap analysis
   - Track test performance

### For Admins

1. **Login**: Use admin credentials
2. **Manage Companies**:
   - Add new companies with requirements
   - Set CGPA cutoff
   - Define required skills
3. **Manage Tests**:
   - Add/delete questions
   - Set correct answers
   - Organize by type
4. **View Analytics**:
   - Overall statistics
   - Top performers
   - Average scores

## 🎯 Example Usage Scenario

### Student Journey:

1. **Registration**
   ```
   Username: john_doe
   CGPA: 8.2
   Skills: "Python, Java, SQL, Data Structures"
   ```

2. **Take Mock Test**
   ```
   Score: 12/15 (80%)
   ```

3. **Placement Calculation**
   ```
   CGPA Score    = (8.2 / 10.0) × 40 = 32.8
   Skill Score   = Average match 60% × 0.4 = 24.0
   Test Score    = 80% × 0.2 = 16.0
   ─────────────────────────────────────────
   Final         = 32.8 + 24.0 + 16.0 = 72.8%
   Classification: HIGH
   ```

4. **Eligibility Check**
   ```
   Google:    Not Eligible (CGPA 8.2 < 8.5)
   Microsoft:  Eligible (CGPA 8.2 >= 8.0)
   Infosys:   Eligible (CGPA 8.2 >= 6.5)
   ```

## 📊 Sample Companies

| Company | Role | Min CGPA | Required Skills |
|---------|------|----------|-----------------|
| Google | Software Engineer | 8.5 | Python, Java, DS, Algo, SQL |
| Microsoft | SDE | 8.0 | C#, .NET, Python, SQL, Azure |
| Amazon | SDE-1 | 7.5 | Java, Python, SQL, DS, System Design |
| Infosys | Systems Engineer | 6.5 | Python, Java, SQL, HTML, CSS, JS |
| TCS | Assistant SE | 6.0 | Python, Java, C, SQL, Programming |

## 🔑 Default Credentials

**Admin Account:**
- Username: `admin`
- Password: `admin123`
- Access: Full admin privileges

## 📁 Project Structure

```
campus_placement/
├── placement/                    # Django app
│   ├── models.py                 # Database models
│   ├── views.py                  # Business logic & formulas
│   ├── urls.py                   # URL routing
│   ├── admin.py                  # Admin interface
│   └── migrations/                # Database migrations
├── templates/placement/          # HTML templates
│   ├── base.html                 # Base template
│   ├── home.html                 # Landing page
│   ├── login.html                # Login page
│   ├── register.html             # Registration
│   ├── dashboard.html            # Student dashboard
│   ├── profile.html              # Profile management
│   ├── test.html                 # Mock test
│   └── admin_dashboard.html      # Admin panel
├── static/                       # Static files (CSS/JS)
├── placement_config/              # Django settings
├── manage.py                     # Django management
├── seed_data.py                  # Sample data generator
└── README.md                     # This file
```

## 🎨 Key Features Explained

### 1. Eligibility Checker
- **CGPA Check**: `Student.CGPA >= Company.Min_CGPA`
- **Skill Match**: `(Matching Skills / Total Required Skills) × 100`
- **Status**: Shows "Eligible" or "Not Eligible" with reasons

### 2. Placement Prediction
- **CGPA Score (40%)**: Rewards academic performance
- **Skill Score (40%)**: Average skill match across all companies
- **Test Score (20%)**: Mock test performance
- **Classification**: High, Medium, Low, Very Low

### 3. Visual Analytics
- **Bar Chart**: Student skills vs company requirements
- **Doughnut Chart**: Mock test performance (Correct vs Incorrect)
- **Real-time Updates**: Charts update based on latest data

## 🧪 Testing the Application

### Test Student Account:
1. Register with username: `test_student`
2. Set CGPA: 8.0
3. Skills: "Python, Java, SQL"
4. Take mock test
5. View dashboard predictions

### Test Admin Features:
1. Login as admin
2. Add new company
3. Add questions
4. View analytics dashboard

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Kill process on port 8000
# Or use different port:
python manage.py runserver 8001
```

### Migration Errors
```bash
# Delete database and start fresh
rm db.sqlite3
python manage.py migrate
python seed_data.py
```

### Static Files Not Loading
```bash
python manage.py collectstatic
```

## 📝 Customization

### Add More Companies:
```python
# Via admin panel or seed_data.py
Company.objects.create(
    name='Your Company',
    role='Role',
    min_cgpa=7.0,
    required_skills='Skill1, Skill2, Skill3'
)
```

### Modify Prediction Formula:
Edit `calculate_placement_probability()` in `views.py`

### Add More Questions:
```python
Question.objects.create(
    text='Your question?',
    option_a='A',
    option_b='B',
    option_c='C',
    option_d='D',
    correct_option='A',
    question_type='technical'
)
```

## 🎓 Academic Project Features

### BCA Final Year Requirements Met:
- ✅ Complete Django web application
- ✅ Database design and implementation
- ✅ Frontend with responsive UI
- ✅ Data analytics and visualization
- ✅ User authentication and authorization
- ✅ Real-time calculations and predictions
- ✅ Admin panel for data management
- ✅ Mock test/quiz functionality

### Project Highlights:
- **AI Logic**: Exact weighted scoring algorithm as specified
- **Eligibility Logic**: CGPA and skill matching
- **Data Visualization**: Interactive charts with Chart.js
- **Responsive Design**: Mobile-friendly Bootstrap 5 UI
- **User Management**: Student and Admin roles
- **Database**: SQLite with proper relationships
- **Security**: CSRF protection, authentication

## 📧 Contact & Support

For issues or questions:
- Project Directory: `C:\Users\270356\OneDrive\Desktop\BCA_Projects\campus_placement`
- Django Documentation: https://docs.djangoproject.com/
- Bootstrap 5: https://getbootstrap.com/
- Chart.js: https://www.chartjs.org/

---

## 🚀 Quick Start Commands

```bash
# Navigate to project
cd campus_placement

# Install dependencies
pip install Django

# Run migrations
python manage.py migrate

# Seed sample data
python seed_data.py

# Start server
python manage.py runserver

# Access application
# Open browser: http://127.0.0.1:8000/
```

---

**Built with ❤️ using Django & Bootstrap 5**

Perfect for BCA Final Year Project Submission! 🎓✨
