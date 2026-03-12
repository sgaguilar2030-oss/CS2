import json
import os

# -----------------------------
# JSON file setup
# -----------------------------
DATA_FILE = "grades.json"

if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
else:
    data = {}

# -----------------------------
# Helper Functions
# -----------------------------
def get_valid_number(prompt, min_val, max_val):
    while True:
        try:
            value = int(input(prompt))
            if min_val <= value <= max_val:
                return value
            else:
                print(f"ERROR: Value must be between {min_val} and {max_val}.")
        except ValueError:
            print("Invalid input. Please enter an integer.")

def get_valid_grade(prompt):
    while True:
        try:
            grade = float(input(prompt))
            if 0 <= grade <= 100:
                return grade
            else:
                print("ERROR: Grade must be between 0 and 100.")
        except ValueError:
            print("Invalid input. Please enter a number.")

# -----------------------------
# Assessment Calculations
# -----------------------------
def calculate_assessment(assessment_name, max_count):
    print(f"\n{assessment_name} assessments")

    count = get_valid_number(
        f"Enter how many {assessment_name.lower()} assessments you took: ", 0, max_count
    )

    if count == 0:
        return 0, 0

    weight = get_valid_number(
        f"Enter total weight of {assessment_name.lower()} assessments to your final GWA (%): ", 0, 100
    )

    total = 0
    for i in range(count):
        grade = get_valid_grade(
            f"Enter grade for {assessment_name.lower()} assessment #{i + 1}: "
        )
        total += grade

    average = total / count
    contribution = average * (weight / 100)

    return contribution, weight


def calculate_multiple_tests(test_name, max_count):
    print(f"\n{test_name} assessments")

    took_test = get_valid_number(
        f"Did you take any {test_name.lower()}? (1 = yes, 2 = no): ", 1, 2
    )

    if took_test == 2:
        return 0, 0

    count = get_valid_number(
        f"How many {test_name.lower()} did you take?: ", 1, max_count
    )

    weight = get_valid_number(
        f"Enter total weight of {test_name.lower()} (%): ", 0, 100
    )

    total = 0
    for i in range(count):
        grade = get_valid_grade(
            f"Enter score for {test_name.lower()} #{i + 1}: "
        )
        total += grade

    average = total / count
    contribution = average * (weight / 100)

    return contribution, weight


def calculate_exam(exam_name):
    take_exam = get_valid_number(
        f"Did you take a {exam_name} exam? (1 = yes, 2 = no): ", 1, 2
    )

    if take_exam == 1:
        weight = get_valid_number(
            f"Enter weight of {exam_name} exam (%): ", 0, 100
        )

        score = get_valid_grade(
            f"Enter your score in the {exam_name} exam (%): "
        )

        contribution = score * (weight / 100)

        return contribution, weight

    return 0, 0


# -----------------------------
# Subject Calculation
# -----------------------------
def calculate_subject_gwa(subject_name):

    print(f"\n--- Calculating {subject_name} ---")

    total_contribution = 0
    total_weight = 0

    fa_contrib, fa_weight = calculate_assessment("Formative", 10)
    total_contribution += fa_contrib
    total_weight += fa_weight

    aa_contrib, aa_weight = calculate_assessment("Alternative", 7)
    total_contribution += aa_contrib
    total_weight += aa_weight

    lt_contrib, lt_weight = calculate_multiple_tests("Long Test", 10)
    total_contribution += lt_contrib
    total_weight += lt_weight

    pr_contrib, pr_weight = calculate_multiple_tests("Practical Exam", 10)
    total_contribution += pr_contrib
    total_weight += pr_weight

    midterm_contrib, midterm_weight = calculate_exam("Midterm")
    total_contribution += midterm_contrib
    total_weight += midterm_weight

    final_contrib, final_weight = calculate_exam("Final")
    total_contribution += final_contrib
    total_weight += final_weight

    bonus = float(input("Enter bonus points for this subject (0 if none): "))
    total_contribution += bonus

    gwa = total_contribution

    print(f"\nYour GWA percentage for {subject_name} is: {gwa:.2f}%")
    print("Status:", "PASSED ✅" if gwa >= 60 else "FAILED ❌")

    return gwa


# -----------------------------
# Save Grades
# -----------------------------
def save_grade_json(user_id, user_name, grade_level, section, quarter, subjects, overall_gwa):

    if user_id not in data:
        data[user_id] = {
            "name": user_name,
            "grade_level": grade_level,
            "section": section,
            "quarters": {}
        }

    data[user_id]["quarters"][quarter] = {
        "subjects": subjects,
        "overall_gwa": overall_gwa
    }

    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

    print(f"\nGrades saved for {user_name} ({user_id}) in {quarter}.")


# -----------------------------
# Main Program
# -----------------------------
print("Reminder: Please enter grades in percentage form (0-100).")

while True:

    print("\n===== GWA CALCULATOR =====")

    user_name = input("Enter your full name: ")
    user_id = input("Enter your ID: ")

    grade_level = input("Enter your grade level: ")
    section = input("Enter your section: ")

    num_sub = get_valid_number(
        "Enter number of subjects: ", 1, 15
    )

    subjects = []

    for i in range(num_sub):

        print(f"\nSubject #{i+1}")

        subject_name = input(
            "Enter subject name: "
        )

        gwa = calculate_subject_gwa(
            subject_name
        )

        subjects.append({
            "name": subject_name,
            "gwa": gwa
        })

    overall_gwa = sum(
        subj['gwa'] for subj in subjects
    ) / len(subjects)

    print(
        f"\nYour overall GWA for this quarter: {overall_gwa:.2f}%"
    )

    quarter = input(
        "Enter quarter (Q1, Q2, Q3, Q4): "
    )

    save_grade_json(
        user_id,
        user_name,
        grade_level,
        section,
        quarter,
        subjects,
        overall_gwa
    )

    loop_choice = get_valid_number(
        "Do you want to calculate again? (1 = yes, 2 = no): ",
        1,
        2
    )

    if loop_choice == 2:
        print("\nThank you for using the GWA calculator!")
        break
