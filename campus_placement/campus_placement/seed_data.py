"""
Seed data script for Campus Placement Portal
Run this to populate the database with sample companies and questions
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "placement_config.settings")
django.setup()

from placement.models import Company, Question


def seed_companies():
    """Seed sample companies"""
    companies_data = [
        {
            "name": "Google",
            "role": "Software Engineer",
            "min_cgpa": 8.5,
            "required_skills": "Python, Java, Data Structures, Algorithms, SQL",
            "description": "Looking for talented software engineers with strong problem-solving skills.",
        },
        {
            "name": "Microsoft",
            "role": "Software Development Engineer",
            "min_cgpa": 8.0,
            "required_skills": "C#, .NET, Python, SQL, Azure",
            "description": "Join our team and build innovative software solutions.",
        },
        {
            "name": "Amazon",
            "role": "SDE-1 (Software Development Engineer)",
            "min_cgpa": 7.5,
            "required_skills": "Java, Python, SQL, Data Structures, System Design",
            "description": "Work on large-scale distributed systems at Amazon Web Services.",
        },
        {
            "name": "Infosys",
            "role": "Systems Engineer",
            "min_cgpa": 6.5,
            "required_skills": "Python, Java, SQL, HTML, CSS, JavaScript",
            "description": "Entry-level position for fresh graduates with good aptitude.",
        },
        {
            "name": "TCS",
            "role": "Assistant System Engineer",
            "min_cgpa": 6.0,
            "required_skills": "Python, Java, C, SQL, Basic Programming",
            "description": "Join TCS Ignite program and start your IT career.",
        },
        {
            "name": "Wipro",
            "role": "Project Engineer",
            "min_cgpa": 6.0,
            "required_skills": "Java, Python, SQL, Web Development, Testing",
            "description": "Build your career with Wipro comprehensive training programs.",
        },
        {
            "name": "Accenture",
            "role": "Software Analyst",
            "min_cgpa": 6.5,
            "required_skills": "Python, Java, SQL, Cloud Computing, DevOps",
            "description": "Work with cutting-edge technologies at Fortune 500 companies.",
        },
        {
            "name": "Deloitte",
            "role": "Analyst",
            "min_cgpa": 7.0,
            "required_skills": "Python, SQL, Data Analysis, Excel, Communication",
            "description": "Join our consulting firm and solve complex business problems.",
        },
        {
            "name": "IBM",
            "role": "Associate System Engineer",
            "min_cgpa": 7.0,
            "required_skills": "Java, Python, Cloud, Data Science, Machine Learning",
            "description": "Work on innovative projects in Cloud, AI, and Data Science.",
        },
        {
            "name": "Oracle",
            "role": "Software Developer",
            "min_cgpa": 7.5,
            "required_skills": "Java, SQL, Database Management, PL/SQL, Cloud",
            "description": "Build and maintain database systems for enterprise clients.",
        },
    ]

    for company_data in companies_data:
        company, created = Company.objects.get_or_create(
            name=company_data["name"],
            defaults={
                "role": company_data["role"],
                "min_cgpa": company_data["min_cgpa"],
                "required_skills": company_data["required_skills"],
                "description": company_data["description"],
            },
        )
        if created:
            print(f"[OK] Created company: {company.name}")
        else:
            print(f"[SKIP] Company already exists: {company.name}")


def seed_questions():
    """Seed sample aptitude and technical questions"""
    questions_data = [
        {
            "text": "What is the time complexity of binary search in the worst case?",
            "option_a": "O(1)",
            "option_b": "O(log n)",
            "option_c": "O(n)",
            "option_d": "O(n log n)",
            "correct_option": "B",
            "question_type": "aptitude",
        },
        {
            "text": "Which data structure uses LIFO (Last In First Out)?",
            "option_a": "Queue",
            "option_b": "Stack",
            "option_c": "Linked List",
            "option_d": "Array",
            "correct_option": "B",
            "question_type": "technical",
        },
        {
            "text": "What is the output of print(2 ** 3) in Python?",
            "option_a": "6",
            "option_b": "8",
            "option_c": "9",
            "option_d": "5",
            "correct_option": "B",
            "question_type": "technical",
        },
        {
            "text": "Which HTTP method is typically used to update data?",
            "option_a": "GET",
            "option_b": "POST",
            "option_c": "PUT",
            "option_d": "DELETE",
            "correct_option": "B",
            "question_type": "technical",
        },
        {
            "text": "What is the primary key in a database?",
            "option_a": "A unique identifier for each record",
            "option_b": "The first column of a table",
            "option_c": "An indexed field",
            "option_d": "A foreign key",
            "correct_option": "A",
            "question_type": "aptitude",
        },
        {
            "text": "Which sorting algorithm has the best average-case time complexity?",
            "option_a": "Bubble Sort",
            "option_b": "Merge Sort",
            "option_c": "Quick Sort",
            "option_d": "Selection Sort",
            "correct_option": "C",
            "question_type": "aptitude",
        },
        {
            "text": "What is the correct syntax to create a list in Python?",
            "option_a": "list = []",
            "option_b": "list = ()",
            "option_c": "list = {}",
            "option_d": "list = <>",
            "correct_option": "A",
            "question_type": "technical",
        },
        {
            "text": "Which protocol is used for secure communication over the web?",
            "option_a": "HTTP",
            "option_b": "FTP",
            "option_c": "HTTPS",
            "option_d": "SMTP",
            "correct_option": "C",
            "question_type": "technical",
        },
        {
            "text": "What is the average time complexity of quicksort?",
            "option_a": "O(n log n)",
            "option_b": "O(n)",
            "option_c": "O(n²)",
            "option_d": "O(1)",
            "correct_option": "A",
            "question_type": "aptitude",
        },
        {
            "text": "Which SQL clause is used to filter results?",
            "option_a": "GROUP BY",
            "option_b": "ORDER BY",
            "option_c": "WHERE",
            "option_d": "HAVING",
            "correct_option": "C",
            "question_type": "technical",
        },
        {
            "text": "A train travels 120 km in 2 hours. What is its speed?",
            "option_a": "40 km/h",
            "option_b": "50 km/h",
            "option_c": "60 km/h",
            "option_d": "70 km/h",
            "correct_option": "C",
            "question_type": "quantitative",
        },
        {
            "text": "In Python, which keyword is used to define a function?",
            "option_a": "function",
            "option_b": "def",
            "option_c": "func",
            "option_d": "define",
            "correct_option": "B",
            "question_type": "technical",
        },
        {
            "text": "If A = 5, B = 3, then A ^ B (bitwise XOR) equals?",
            "option_a": "6",
            "option_b": "7",
            "option_c": "8",
            "option_d": "2",
            "correct_option": "A",
            "question_type": "aptitude",
        },
        {
            "text": "Which CSS property is used to change text color?",
            "option_a": "font-style",
            "option_b": "text-decoration",
            "option_c": "color",
            "option_d": "font-size",
            "correct_option": "C",
            "question_type": "technical",
        },
        {
            "text": "What is 15% of 200?",
            "option_a": "25",
            "option_b": "30",
            "option_c": "35",
            "option_d": "20",
            "correct_option": "B",
            "question_type": "quantitative",
        },
    ]

    for question_data in questions_data:
        question, created = Question.objects.get_or_create(
            text=question_data["text"],
            defaults={
                "option_a": question_data["option_a"],
                "option_b": question_data["option_b"],
                "option_c": question_data["option_c"],
                "option_d": question_data["option_d"],
                "correct_option": question_data["correct_option"],
                "question_type": question_data["question_type"],
            },
        )
        if created:
            print(f"[OK] Created question: {question.text[:50]}...")
        else:
            print(f"[SKIP] Question already exists: {question.text[:50]}...")


def main():
    print("=== Campus Placement Portal - Seed Data ===\n")

    print("Seeding Companies...")
    seed_companies()

    print("\nSeeding Questions...")
    seed_questions()

    print(f"\n[SUCCESS] Seed data completed!")
    print(f"Total Companies: {Company.objects.count()}")
    print(f"Total Questions: {Question.objects.count()}")


if __name__ == "__main__":
    main()
