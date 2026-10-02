from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Avg, Count, Q
from .models import StudentProfile, Company, Question, TestResult

# ============ Helper Functions ============


def calculate_placement_probability(student_profile):
    """
    Calculate placement probability using the EXACT formula specified:
    - CGPA Score (40%): (Student CGPA / 10.0) * 40
    - Skill Score (40%): Average Skill Match % across all companies * 0.4
    - Test Score (20%): Mock Test Percentage * 0.2
    - Final Probability: CGPA Score + Skill Score + Test Score

    Args:
        student_profile: StudentProfile instance

    Returns:
        dict: Contains probability percentage and classification
    """
    # Get student's latest test score
    latest_test = student_profile.test_results.first()
    test_percentage = latest_test.percentage if latest_test else 0.0

    # Calculate CGPA Score (40%)
    cgpa_score = (student_profile.cgpa / 10.0) * 40

    # Calculate Skill Score (40%)
    # Average skill match percentage across all companies
    companies = Company.objects.all()
    skill_match_percentages = []

    for company in companies:
        if company.required_skills_list:
            match_pct = student_profile.get_skill_match_percentage(
                company.required_skills_list
            )
            skill_match_percentages.append(match_pct)

    if skill_match_percentages:
        avg_skill_match = sum(skill_match_percentages) / len(skill_match_percentages)
        skill_score = avg_skill_match * 0.4
    else:
        skill_score = 0.0

    # Calculate Test Score (20%)
    test_score = test_percentage * 0.2

    # Calculate Final Probability
    final_probability = cgpa_score + skill_score + test_score

    # Classify probability
    if final_probability >= 75:
        classification = "High"
    elif final_probability >= 50:
        classification = "Medium"
    elif final_probability >= 35:
        classification = "Low"
    else:
        classification = "Very Low"

    return {
        "probability": round(final_probability, 2),
        "classification": classification,
        "cgpa_score": round(cgpa_score, 2),
        "skill_score": round(skill_score, 2),
        "test_score": round(test_score, 2),
        "test_percentage": round(test_percentage, 2),
    }


def check_eligibility(student_profile):
    """
    Check student eligibility for all companies
    Returns list of companies with eligibility status
    """
    companies = Company.objects.all()
    eligibility_list = []

    for company in companies:
        # Check 1: CGPA requirement
        cgpa_eligible = student_profile.cgpa >= company.min_cgpa

        # Check 2: Skill match percentage
        skill_match_pct = 0
        if company.required_skills_list:
            skill_match_pct = student_profile.get_skill_match_percentage(
                company.required_skills_list
            )

        # Determine overall eligibility
        is_eligible = cgpa_eligible

        eligibility_list.append(
            {
                "company": company,
                "is_eligible": is_eligible,
                "cgpa_eligible": cgpa_eligible,
                "skill_match_pct": round(skill_match_pct, 2),
            }
        )

    return eligibility_list


# ============ Authentication Views ============


def home(request):
    """Landing page"""
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            return redirect("placement:admin_dashboard")
        else:
            return redirect("placement:dashboard")
    return render(request, "placement/home.html")


def register(request):
    """Student registration"""
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")

        # Validation
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return render(request, "placement/register.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return render(request, "placement/register.html")

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        # Create student profile with default values
        StudentProfile.objects.create(user=user, cgpa=0.0, skills="", projects="")

        messages.success(request, "Registration successful! Please login.")
        return redirect("placement:login")

    return render(request, "placement/register.html")


def user_login(request):
    """User login"""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Redirect based on user type
            if user.is_staff or user.is_superuser:
                return redirect("placement:admin_dashboard")
            else:
                return redirect("placement:dashboard")
        else:
            messages.error(request, "Invalid username or password!")

    return render(request, "placement/login.html")


@login_required
def user_logout(request):
    """User logout"""
    logout(request)
    messages.success(request, "You have been logged out successfully!")
    return redirect("placement:home")


# ============ Student Views ============


@login_required
def dashboard(request):
    """
    Main student dashboard with placement probability
    """
    # Check if user is staff
    if request.user.is_staff or request.user.is_superuser:
        return redirect("placement:admin_dashboard")

    # Get or create student profile
    try:
        student_profile = request.user.student_profile
    except StudentProfile.DoesNotExist:
        student_profile = StudentProfile.objects.create(
            user=request.user, cgpa=0.0, skills="", projects=""
        )

    # Calculate placement probability
    prediction = calculate_placement_probability(student_profile)

    # Get eligibility information
    eligibility_list = check_eligibility(student_profile)
    eligible_companies = [e for e in eligibility_list if e["is_eligible"]]
    not_eligible_companies = [e for e in eligibility_list if not e["is_eligible"]]

    # Get latest test result
    latest_test = student_profile.test_results.first()

    context = {
        "student": student_profile,
        "prediction": prediction,
        "eligible_companies": eligible_companies,
        "not_eligible_companies": not_eligible_companies,
        "latest_test": latest_test,
        "total_companies": Company.objects.count(),
    }

    return render(request, "placement/dashboard.html", context)


@login_required
def profile(request):
    """View and edit student profile"""
    try:
        student_profile = request.user.student_profile
    except StudentProfile.DoesNotExist:
        student_profile = StudentProfile.objects.create(
            user=request.user, cgpa=0.0, skills="", projects=""
        )

    context = {
        "student": student_profile,
    }
    return render(request, "placement/profile.html", context)


@login_required
def update_profile(request):
    """Update student profile"""
    try:
        student_profile = request.user.student_profile
    except StudentProfile.DoesNotExist:
        student_profile = StudentProfile.objects.create(
            user=request.user, cgpa=0.0, skills="", projects=""
        )

    if request.method == "POST":
        cgpa = request.POST.get("cgpa")
        skills = request.POST.get("skills")
        projects = request.POST.get("projects", "")

        # Update profile
        student_profile.cgpa = float(cgpa) if cgpa else 0.0
        student_profile.skills = skills
        student_profile.projects = projects
        student_profile.save()

        messages.success(request, "Profile updated successfully!")
        return redirect("placement:dashboard")

    return redirect("placement:profile")


@login_required
def mock_test(request):
    """
    Mock aptitude test page
    """
    # Check if user is staff
    if request.user.is_staff or request.user.is_superuser:
        messages.error(request, "Admin cannot take mock tests!")
        return redirect("placement:admin_dashboard")

    # Get random questions (limit to 10 for demo)
    questions = Question.objects.all()[:10]

    if not questions.exists():
        messages.warning(request, "No questions available. Please contact admin.")
        return render(request, "placement/test.html", {"questions": []})

    context = {
        "questions": questions,
    }

    return render(request, "placement/test.html", context)


@login_required
def submit_test(request):
    """
    Submit mock test and calculate score
    """
    if request.method != "POST":
        return redirect("placement:mock_test")

    # Check if user is staff
    if request.user.is_staff or request.user.is_superuser:
        messages.error(request, "Admin cannot take mock tests!")
        return redirect("placement:admin_dashboard")

    try:
        student_profile = request.user.student_profile
    except StudentProfile.DoesNotExist:
        messages.error(request, "Please complete your profile first!")
        return redirect("placement:profile")

    # Get answers from POST
    answers = {}
    for key in request.POST:
        if key.startswith("question_"):
            question_id = key.split("_")[1]
            answers[question_id] = request.POST.get(key)

    # Get all questions
    question_ids = list(answers.keys())
    questions = Question.objects.filter(id__in=question_ids)

    # Calculate score
    correct_count = 0
    for question in questions:
        if str(question.id) in answers:
            user_answer = answers[str(question.id)]
            if user_answer == question.correct_option:
                correct_count += 1

    total_questions = questions.count()

    # Save test result
    TestResult.objects.create(
        student=student_profile, score=correct_count, total_questions=total_questions
    )

    messages.success(
        request, f"Test submitted! Your score: {correct_count}/{total_questions}"
    )
    return redirect("placement:dashboard")


@login_required
def eligibility_checker(request):
    """
    Detailed eligibility checker page
    """
    # Check if user is staff
    if request.user.is_staff or request.user.is_superuser:
        messages.error(request, "Admin cannot check eligibility!")
        return redirect("placement:admin_dashboard")

    try:
        student_profile = request.user.student_profile
    except StudentProfile.DoesNotExist:
        messages.error(request, "Please complete your profile first!")
        return redirect("placement:profile")

    # Get eligibility information
    eligibility_list = check_eligibility(student_profile)

    context = {
        "student": student_profile,
        "eligibility_list": eligibility_list,
    }

    return render(request, "placement/eligibility.html", context)


@login_required
def placement_prediction(request):
    """
    Detailed placement prediction page
    """
    # Check if user is staff
    if request.user.is_staff or request.user.is_superuser:
        messages.error(request, "Admin cannot view placement prediction!")
        return redirect("placement:admin_dashboard")

    try:
        student_profile = request.user.student_profile
    except StudentProfile.DoesNotExist:
        messages.error(request, "Please complete your profile first!")
        return redirect("placement:profile")

    # Calculate detailed prediction
    prediction = calculate_placement_probability(student_profile)

    # Get skill gap analysis
    companies = Company.objects.all()
    student_skills = set(skill.lower() for skill in student_profile.skills_list)

    all_required_skills = set()
    for company in companies:
        all_required_skills.update(company.required_skills_list)

    missing_skills = all_required_skills - student_skills

    # Get latest test
    latest_test = student_profile.test_results.first()
    all_tests = student_profile.test_results.all()[:5]

    context = {
        "student": student_profile,
        "prediction": prediction,
        "companies": companies,
        "student_skills": student_profile.skills_list,
        "missing_skills": list(missing_skills),
        "latest_test": latest_test,
        "all_tests": all_tests,
    }

    return render(request, "placement/prediction.html", context)


# ============ Admin Views ============


@login_required
def admin_dashboard(request):
    """
    Admin dashboard with analytics
    """
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, "Access denied. Admin only.")
        return redirect("placement:home")

    # Get statistics
    total_students = StudentProfile.objects.count()
    total_companies = Company.objects.count()
    total_questions = Question.objects.count()
    total_tests = TestResult.objects.count()

    # Average test scores
    avg_test_score = (
        TestResult.objects.aggregate(avg_score=Avg("score"))["avg_score"] or 0
    )

    # Student statistics
    students = StudentProfile.objects.select_related("user").all()

    # Calculate average CGPA
    avg_cgpa = students.aggregate(avg=Avg("cgpa"))["avg"] or 0

    # Top performers
    top_performers = []
    for student in students:
        prediction = calculate_placement_probability(student)
        top_performers.append(
            {
                "name": student.user.get_full_name() or student.user.username,
                "cgpa": student.cgpa,
                "probability": prediction["probability"],
            }
        )

    # Sort by probability and get top 5
    top_performers = sorted(
        top_performers, key=lambda x: x["probability"], reverse=True
    )[:5]

    context = {
        "total_students": total_students,
        "total_companies": total_companies,
        "total_questions": total_questions,
        "total_tests": total_tests,
        "avg_test_score": round(avg_test_score, 2),
        "avg_cgpa": round(avg_cgpa, 2),
        "top_performers": top_performers,
        "students": students[:10],
    }

    return render(request, "placement/admin_dashboard.html", context)


@login_required
def manage_companies(request):
    """Manage companies"""
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, "Access denied. Admin only.")
        return redirect("placement:home")

    companies = Company.objects.all()

    context = {
        "companies": companies,
    }

    return render(request, "placement/manage_companies.html", context)


@login_required
def add_company(request):
    """Add new company"""
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, "Access denied. Admin only.")
        return redirect("placement:home")

    if request.method == "POST":
        name = request.POST.get("name")
        role = request.POST.get("role")
        min_cgpa = request.POST.get("min_cgpa")
        required_skills = request.POST.get("required_skills")
        description = request.POST.get("description", "")

        Company.objects.create(
            name=name,
            role=role,
            min_cgpa=float(min_cgpa),
            required_skills=required_skills,
            description=description,
        )

        messages.success(request, f'Company "{name}" added successfully!')
        return redirect("placement:manage_companies")

    return render(request, "placement/add_company.html")


@login_required
def edit_company(request, company_id):
    """Edit company"""
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, "Access denied. Admin only.")
        return redirect("placement:home")

    company = get_object_or_404(Company, id=company_id)

    if request.method == "POST":
        company.name = request.POST.get("name")
        company.role = request.POST.get("role")
        company.min_cgpa = float(request.POST.get("min_cgpa"))
        company.required_skills = request.POST.get("required_skills")
        company.description = request.POST.get("description", "")
        company.save()

        messages.success(request, f'Company "{company.name}" updated successfully!')
        return redirect("placement:manage_companies")

    context = {
        "company": company,
    }

    return render(request, "placement/edit_company.html", context)


@login_required
def delete_company(request, company_id):
    """Delete company"""
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, "Access denied. Admin only.")
        return redirect("placement:home")

    company = get_object_or_404(Company, id=company_id)

    if request.method == "POST":
        company_name = company.name
        company.delete()
        messages.success(request, f'Company "{company_name}" deleted successfully!')
        return redirect("placement:manage_companies")

    context = {
        "company": company,
    }

    return render(request, "placement/delete_company.html", context)


@login_required
def manage_tests(request):
    """Manage test questions"""
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, "Access denied. Admin only.")
        return redirect("placement:home")

    questions = Question.objects.all()

    context = {
        "questions": questions,
    }

    return render(request, "placement/manage_tests.html", context)


@login_required
def add_question(request):
    """Add new question"""
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, "Access denied. Admin only.")
        return redirect("placement:home")

    if request.method == "POST":
        text = request.POST.get("text")
        option_a = request.POST.get("option_a")
        option_b = request.POST.get("option_b")
        option_c = request.POST.get("option_c")
        option_d = request.POST.get("option_d")
        correct_option = request.POST.get("correct_option")
        question_type = request.POST.get("question_type", "aptitude")

        Question.objects.create(
            text=text,
            option_a=option_a,
            option_b=option_b,
            option_c=option_c,
            option_d=option_d,
            correct_option=correct_option,
            question_type=question_type,
        )

        messages.success(request, "Question added successfully!")
        return redirect("placement:manage_tests")

    return render(request, "placement/add_question.html")


@login_required
def delete_question(request, question_id):
    """Delete question"""
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, "Access denied. Admin only.")
        return redirect("placement:home")

    question = get_object_or_404(Question, id=question_id)

    if request.method == "POST":
        question.delete()
        messages.success(request, "Question deleted successfully!")
        return redirect("placement:manage_tests")

    return redirect("placement:manage_tests")
