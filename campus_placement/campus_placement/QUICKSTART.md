# Campus Placement Portal - Quick Start Guide

## 🚀 Launch the Application

### Step 1: Navigate to Project
```bash
cd C:\Users\270356\OneDrive\Desktop\BCA_Projects\campus_placement
```

### Step 2: Start Server
```bash
python manage.py runserver
```

### Step 3: Open in Browser
```
http://127.0.0.1:8000/
```

## 🔑 Login Credentials

**Admin Account:**
- Username: `admin`
- Password: `admin123`

**To Create Student Account:**
1. Go to: http://127.0.0.1:8000/register/
2. Fill in details
3. Login with new credentials

## 📱 Key Pages

### For Students:
- **Dashboard**: `/dashboard/` - View placement probability
- **Profile**: `/profile/` - Update CGPA and skills
- **Mock Test**: `/test/` - Take practice test
- **Eligibility**: `/eligibility/` - Check company eligibility
- **Prediction**: `/prediction/` - Detailed prediction analysis

### For Admins:
- **Dashboard**: `/admin/dashboard/` - Overview statistics
- **Companies**: `/admin/companies/` - Manage companies
- **Tests**: `/admin/tests/` - Manage questions
- **Django Admin**: `/admin/` - Advanced database management

## 🧪 Quick Test Walkthrough

### 1. Register as Student:
```
Username: demo_student
Name: Demo Student
CGPA: 7.8
Skills: Python, Java, SQL, HTML, CSS
```

### 2. Take Mock Test:
- Go to Mock Test page
- Answer 15 questions
- Submit and see score

### 3. View Dashboard:
- See placement probability
- Check eligible companies
- View charts

### 4. Update Profile:
- Increase CGPA
- Add more skills
- See probability update

## 🎯 Expected Results

### With CGPA 7.8, Skills: "Python, Java, SQL, HTML, CSS":

**Prediction:**
- CGPA Score: (7.8/10) × 40 = 31.2
- Skill Score: Average 50% match × 0.4 = 20.0
- Test Score: 80% × 0.2 = 16.0
- **Final: 67.2% (Medium)**

**Eligibility:**
- Google: ❌ (CGPA too low)
- Microsoft: ❌ (CGPA too low)
- Amazon: ✅ Eligible
- Infosys: ✅ Eligible
- TCS: ✅ Eligible
- Wipro: ✅ Eligible

## 🔧 Admin Tasks

### Add Company:
1. Go to Companies page
2. Click "Add Company"
3. Fill details:
   - Name: "Meta"
   - Role: "Software Engineer"
   - Min CGPA: 8.0
   - Skills: "Python, React, SQL, System Design"
   - Description: "Build the future of social connection"

### Add Question:
1. Go to Tests page
2. Click "Add Question"
3. Fill question and options
4. Set correct answer

## 📊 What Makes This Special?

✅ **Exact Formula Implementation**
- CGPA: 40% weight
- Skills: 40% weight (average match %)
- Test: 20% weight

✅ **Real-time Calculations**
- Instant eligibility checking
- Dynamic probability updates
- Visual skill gap analysis

✅ **Professional UI**
- Bootstrap 5 responsive design
- Chart.js visualizations
- Mobile-friendly interface

✅ **Complete Admin Panel**
- Company management
- Test creation
- Performance analytics

## 🎓 Perfect for BCA Final Year

- ✅ Full-stack Django application
- ✅ Database design and relationships
- ✅ Weighted algorithm implementation
- ✅ Data visualization
- ✅ User authentication
- ✅ Admin/student roles
- ✅ CRUD operations
- ✅ Responsive frontend

## 🚨 Troubleshooting

### Server won't start?
```bash
# Check if port 8000 is free
# Or use different port:
python manage.py runserver 8001
```

### Charts not showing?
- Check internet connection (CDN)
- Open browser console (F12) for errors
- Ensure Chart.js loaded

### Login not working?
- Clear browser cache
- Check if running on correct port
- Verify credentials

---

**Ready to impress! 🎓✨**
