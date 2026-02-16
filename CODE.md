# START
print("Reminder: Please use percentage form! This is very crucial to this program")

# Subject Number
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

# Grade
def get_valid_grade(prompt):
    while True:
        try:
            grade = float(input(prompt))
            if 0 <= grade <= 100:
                return grade
            else:
                print("ERROR. Grade must be between 0 and 100.")
        except ValueError:
            print("Invalid input. Please enter a number.")

# Assessment
def calculate_assessment(assessment_name, max_count):
    print(f"\n{assessment_name} assessments")
    count = get_valid_number(
        f"Enter how many {assessment_name.lower()} assessments you took: ", 0, max_count
    )

    if count == 0:
        return 0

    weight = get_valid_number(
        f"Enter the weight of the {assessment_name.lower()} assessment to your final GWA: ", 0, 100
    )

    total = 0
    for i in range(count):
        grade = get_valid_grade(
            f"Enter grade for {assessment_name.lower()} assessment #{i + 1}: "
        )
        if assessment_name.lower() == "formative":
            total += grade * (weight / count)
        else:
            total += grade

    if assessment_name.lower() == "formative":
        return total / 100
    else:
        average = total / count
        return average * (weight / 100)

# Exam
def calculate_exam(exam_name):
    take_exam = get_valid_number(
        f"Did you take a {exam_name} examination? (1 = yes, 2 = no): ", 1, 2
    )
    if take_exam == 1:
        weight = get_valid_number(
            f"Enter the weight of the {exam_name} exam to your final GWA: ", 0, 100
        )
        score = get_valid_grade(f"Enter your score in the {exam_name} exam: ")
        return score * (weight / 100)
    return 0

# Subject GWA
def calculate_subject_gwa(subject_name):
    fa_contrib = calculate_assessment("Formative", 10)
    aa_contrib = calculate_assessment("Alternative", 7)
    midterm_contrib = calculate_exam("midterm")
    final_taken = get_valid_number(
        "Did you take a final examination? (1 = yes, 2 = no): ", 1, 2
    )
    final_contrib = calculate_exam("final") if final_taken == 1 else 0

    gwa = fa_contrib + aa_contrib + midterm_contrib + final_contrib
    print(f"\nYour GWA percentage for {subject_name} is: {gwa:.2f}")
    return gwa


# ==================================================
# Main Program 
# ==================================================

while True:

    num_sub = get_valid_number(
        "Enter the amount of subjects you will be calculating: ", 1, 15
    )

    subject_gwas = []

    for i in range(num_sub):
        print(f"\nSubject #{i + 1}")
        subject_name = input("Enter subject name: ")
        gwa = calculate_subject_gwa(subject_name)
        subject_gwas.append(gwa)

    # Show table?
    while True:
        try:
            showTable = int(input("\nShow GWA table? (1 = yes, 2 = no): "))
            if showTable in [1, 2]:
                break
            else:
                print("Invalid input. Please enter 1 for yes or 2 for no.")
        except ValueError:
            print("Invalid input. Please enter 1 or 2.")

    GWA = [
        ["96-100", "1.00"],
        ["90-95", "1.25"],
        ["84-89", "1.50"],
        ["78-83", "1.75"],
        ["72-77", "2.00"],
        ["66-71", "2.25"],
        ["60-65", "2.50"],
        ["55-59", "2.75"],
        ["Below 55", "3.00 or below"],
    ]

    if showTable == 1:
        print("\n===== PISAY GWA TABLE =====")
        print("{:<15} {:<15}".format("Percentage", "GWA"))
        print("-" * 30)

        for row in GWA:
            print("{:<15} {:<15}".format(row[0], row[1]))

        print("-" * 30)
        print("Remember that the GWA table may have inaccuracies.")

    while True:
        try:
            choice = int(input("Would you like to loop? (1 = yes, 2 = no): "))
            if choice in (1, 2):
                break
            else:
                print("Please enter 1 or 2 only.")
        except ValueError:
            print("Invalid input.")
            
    if choice == 2:
        print("\nThank you for using the GWA calculator! (｡･∀･)ﾉﾞ")
        break
