# Advanced Grade Calculator Suited for Pisay Scholars

 ## Project Description
  This advanced calculator is a python program that helps students and teachers calculate grades based on formative and alternative assessments. It also includes showing the GWA table and indicate if you passed or failed. This code applies basic programming concepts learned in the first quarter, including variables, conditionals, loops, functions, and concepts in the second quarter like functions and libraries, while also including databases we learned from the third quarter.

## Features
1. Input amount of subjects to calculate
2. Input name for the first subject
3. Input grade and section
4. Input ID
5. Input the weight and grades of the formative and alternative assessments (in percentage)
6. Enter the weight and grades for midterm, long test, or practical exams, and final examination (if any)
7. Repeat for all other subjects
8. Compute and calculate the GWA based of given percentages and scores
9. Display GWA percentage
10. Display GWA table
11. Asks user whether they want to convert their percentage into GWA
12. Indicates if you passed or failed
13. Asks user whether they want to loop or not
14. Allows users to save and access grades from past quarters
15. Displays saved grades from all quarters
16. 1/3 2/3 carry-on GWA implementation
17. Displays saved grades from all quarters
18. Includes input validation system
19. Handles JSON corruption recovery
20. Added bonus points, maximum 5

## How to run the code
1. Make sure you have Python installed.
2. Download the 'CODE.py' file
3. Open a terminal or command prompt.
4. Run the program by pressing F5 or clicking 'Run' 
5. Follow the instructions for all inputs

## Alternative way to run the code
1. Make sure you have internet or data
2. Open onlinegdb.com
3. Click language and select 'Python 3'
4. Copy and paste the code from the file 'CODE.py'
5. Click run
6. Follow the instructions for all inputs

## Example Output
Reminder: Please enter grades in percentage form (0-100).

===== GWA CALCULATOR =====
Enter your full name: Christine M. Galela
Enter your ID: 1234567
Enter your grade level: 8
Enter your section: Carnation
Enter number of subjects: 2

Subject #1
Enter subject name: Computer Science 2

--- Calculating Computer Science 2 ---

Formative assessments
Enter how many formative assessments you took: 2
Enter weight (remaining 100%): 40
Enter grade for formative assessment #1: 90
Enter grade for formative assessment #2: 90

Alternative assessments
Enter how many alternative assessments you took: 2
Enter weight (remaining 60%): 40
Enter grade for alternative assessment #1: 80
Enter grade for alternative assessment #2: 90
Did you take any Long Test? (1 = yes, 2 = no): 1
How many Long Test did you take?: 1
Enter weight (remaining 20%): 10
Enter score for Long Test #1: 67
Did you take any Practical Exam? (1 = yes, 2 = no): 1
How many Practical Exam did you take?: 1
Enter weight (remaining 10%): 10
Enter score for Practical Exam #1: 90
All weights have been assigned.

Your GWA percentage for Computer Science 2 is: 85.70%
Status: PASSED ✅

Subject #2
Enter subject name: English

--- Calculating English ---

Formative assessments
Enter how many formative assessments you took: 2
Enter weight (remaining 100%): 40
Enter grade for formative assessment #1: 100
Enter grade for formative assessment #2: 100

Alternative assessments
Enter how many alternative assessments you took: 1
Enter weight (remaining 60%): 30
Enter grade for alternative assessment #1: 100
Did you take any Long Test? (1 = yes, 2 = no): 2
Did you take any Practical Exam? (1 = yes, 2 = no): 2
Did you take any Midterm? (1 = yes, 2 = no): 1
How many Midterm did you take?: 1
Enter weight (remaining 30%): 15
Enter score for Midterm #1: 100
Did you take a Final exam? (1 = yes, 2 = no): 1
Enter weight (remaining 15%): 50
ERROR: Value must be between 0 and 15.
Enter weight (remaining 15%): 15
Enter your score in the Final exam: 100
All weights have been assigned.

Your GWA percentage for English is: 100.00%
Status: PASSED ✅
Enter quarter (e.g., Q1, Q2, Q3, Q4): Q3

Your overall GWA for this quarter: 92.85%

Grades saved for Christine M. Galela (1234567) in Q3.
Would you like to convert the percentage into GWA? (1 = yes, 2 = no): 1
GWA Equivalent: 1.25
Show GWA table? (1 = yes, 2 = no): 1

===== PISAY GWA TABLE =====
Percentage      GWA            
------------------------------
96-100          1.00           
90-95           1.25           
84-89           1.50           
78-83           1.75           
72-77           2.00           
66-71           2.25           
60-65           2.50           
55-59           2.75           
Below 55        3.00 or below  
------------------------------
Do you want to calculate required score for desired grade? (1 = yes, 2 = no): 1
Enter your current grade: 1.25
Enter your desired final grade: 1.00
Enter remaining weight (%): 20
NOTE: Enter your CURRENT WEIGHTED grade.
You have already surpassed your desired grade!
Do you want to view all saved grades? (1 = yes, 2 = no): 1

===== SAVED GRADES =====

User: asdsada (ID: 12321523)
Grade Level: 4, Section: 13241
 Quarter: Q1
  - 1243: 100.00%
 Overall GWA: 100.00%

User: Diane Cruz (ID: 122421423523)
Grade Level: 8, Section: Anthu

User: Christine M. Galela (ID: 1234567)
Grade Level: 8, Section: Carnation
 Quarter: Q3
  - Computer Science 2: 85.70%
  - English: 100.00%
 Overall GWA: 92.85%
Do you want to calculate again? (1 = yes, 2 = no): 2

Thank you for using the GWA calculator! (｡･∀･)ﾉﾞ again? (1 = yes, 2 = no): 2
