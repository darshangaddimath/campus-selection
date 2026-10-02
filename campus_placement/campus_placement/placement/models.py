from django.db import models
from django.contrib.auth.models import User


class StudentProfile(models.Model):
    """
    Student profile linked to User model
    Stores academic information and skills
    """

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="student_profile"
    )
    cgpa = models.FloatField(help_text="Student's CGPA out of 10")
    skills = models.TextField(
        help_text="Comma-separated skills (e.g., 'Python, SQL, Java')"
    )
    projects = models.TextField(blank=True, help_text="Student's project details")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Student Profile"
        verbose_name_plural = "Student Profiles"

    def __str__(self):
        return f"{self.user.username}'s Profile (CGPA: {self.cgpa})"

    @property
    def skills_list(self):
        """Return skills as a Python list"""
        if self.skills:
            return [skill.strip() for skill in self.skills.split(",") if skill.strip()]
        return []

    def get_skill_match_percentage(self, required_skills):
        """
        Calculate skill match percentage against company requirements
        Args:
            required_skills: List of skills required by company
        Returns:
            Float: Percentage of skills matched (0-100)
        """
        student_skills = set(skill.lower().strip() for skill in self.skills_list)
        company_skills = set(skill.lower().strip() for skill in required_skills)

        if not company_skills:
            return 0.0

        matched_skills = student_skills.intersection(company_skills)
        return (len(matched_skills) / len(company_skills)) * 100


class Company(models.Model):
    """
    Company hiring criteria and requirements
    """

    name = models.CharField(max_length=200, unique=True)
    role = models.CharField(max_length=200, help_text="Job role offered")
    min_cgpa = models.FloatField(help_text="Minimum CGPA required (out of 10)")
    required_skills = models.TextField(help_text="Comma-separated required skills")
    description = models.TextField(
        blank=True, help_text="Company description and job details"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} - {self.role} (Min CGPA: {self.min_cgpa})"

    @property
    def required_skills_list(self):
        """Return required skills as a Python list"""
        if self.required_skills:
            return [
                skill.strip()
                for skill in self.required_skills.split(",")
                if skill.strip()
            ]
        return []


class Question(models.Model):
    """
    Mock aptitude test questions
    """

    QUESTION_TYPES = [
        ("aptitude", "Aptitude"),
        ("technical", "Technical"),
        ("reasoning", "Reasoning"),
        ("quantitative", "Quantitative"),
    ]

    text = models.CharField(max_length=500, help_text="Question text")
    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200)
    option_d = models.CharField(max_length=200)
    correct_option = models.CharField(
        max_length=1,
        choices=[("A", "A"), ("B", "B"), ("C", "C"), ("D", "D")],
        help_text="Correct answer (A, B, C, or D)",
    )
    question_type = models.CharField(
        max_length=20, choices=QUESTION_TYPES, default="aptitude"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"
        ordering = ["id"]

    def __str__(self):
        return f"{self.text[:50]}... ({self.correct_option})"


class TestResult(models.Model):
    """
    Store student test results
    """

    student = models.ForeignKey(
        StudentProfile, on_delete=models.CASCADE, related_name="test_results"
    )
    score = models.IntegerField(help_text="Number of correct answers")
    total_questions = models.IntegerField(help_text="Total number of questions")
    date_taken = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Test Result"
        verbose_name_plural = "Test Results"
        ordering = ["-date_taken"]

    def __str__(self):
        return f"{self.student.user.username} - {self.score}/{self.total_questions} ({self.date_taken.strftime('%Y-%m-%d')})"

    @property
    def percentage(self):
        """Calculate test percentage"""
        if self.total_questions > 0:
            return (self.score / self.total_questions) * 100
        return 0.0
