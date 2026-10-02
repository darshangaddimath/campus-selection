from django.contrib import admin
from .models import StudentProfile, Company, Question, TestResult


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "cgpa", "skills_preview", "created_at"]
    list_filter = ["created_at", "cgpa"]
    search_fields = ["user__username", "user__email", "skills"]
    readonly_fields = ["created_at", "updated_at"]

    def skills_preview(self, obj):
        skills = obj.skills_list
        if skills:
            return ", ".join(skills[:5]) + ("..." if len(skills) > 5 else "")
        return "No skills"

    skills_preview.short_description = "Skills"


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ["name", "role", "min_cgpa", "required_skills_preview", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["name", "role", "description"]

    def required_skills_preview(self, obj):
        skills = obj.required_skills_list
        if skills:
            return ", ".join(skills[:5])
        return "None"

    required_skills_preview.short_description = "Required Skills"


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ["text_preview", "question_type", "correct_option", "created_at"]
    list_filter = ["question_type", "created_at"]
    search_fields = ["text"]

    def text_preview(self, obj):
        return obj.text[:100] + "..." if len(obj.text) > 100 else obj.text

    text_preview.short_description = "Question"


@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ["student", "score", "total_questions", "percentage", "date_taken"]
    list_filter = ["date_taken"]
    search_fields = ["student__user__username"]

    def percentage(self, obj):
        return f"{obj.percentage:.1f}%"

    percentage.short_description = "Score %"
