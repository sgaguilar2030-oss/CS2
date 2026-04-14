# CHANGELOG
This file displays all changes and updates that have been made to our Advanced Grade Calculator project.
---
## Version v1.0.0 - July 15, 2025
- First version of the program.
- User can:
  - Enter a student's name and grade
  - Calculate and display the final grade

## Version v1.0.1 - November 21, 2025
- Second version of the program
- User can:
  - Enter amount of subjects it will calculate
  - Enter subject names
  - Enter the amount, weight, and grade for each assessment (formative, alternative, midterms, finals)
  - Ask to show the GWA table
- Updates:
  - User can not divide by 0
  - Fixed bug where text is repeating 

## Version v1.0.2 - December 2, 2025
- Third version of the program
- User can:
  - Enter amount of subjects it will calculate
  - Enter subject names
  - Enter the amount, weight, and grade for each assessment (formative, alternative, midterms, finals)
  - Ask to show the GWA table
- Updates:
  - Fixed bug where the code can't determine if the grade is pass or fail

## Version v1.0.3 - December 3, 2025
- Fourth version of the program.
- User can: 
  - Ask to see the GWA Table
- Updates:
  - Added GWA Table conversion

## Version v.1.0.4 - December 4, 2025
- Fifth version of the program.
- User can:
    - See if they failed / Passed
- Updates:
    - Edited accuracy of the GWA Table
## Version v.1.0.5 - January 29, 2026
- Updates:
  - Edited grammar

## Version v.1.0.6 - February 16, 2026
- Sixth version of the program.
- User can:
  - Loop the program
- Updates:
  - Added a feature that allows the user to loop the program when prompted.

## Version v1.0.7 - February 26. 2026
- Seventh version of the program.
- Allows users to:
  - Input a target or desired final grade.
  - Save and access grades from previous quarters.
  - Save grades and related information in a database.
- Updates:
  - Calculates the required percentage needed on upcoming, ungraded, or final exams.
  - Ensures data is retained even after exiting the program.
  - Displays grades, computations, and results in a table format.
  - Improves clarity, organization, and readability of outputs.

## Version v.1.0.8 - March 12, 2026
- Eighth version of the program.
- Allows the user to:
  - Input bonus points (if applicable)
  - Asks the user if they take long tests, midterms, or practical exams
- User can:
  - Input grade level and section

## Version v.1.0.9 - March 18, 2026
- Ninth version of the program.
- Enabled code to calculate the current quarter grade using 1/3 of the previous quarter grade and 2/3 of the current quarter tentative grade to accomodate the PSHS grading system.

## Version v.1.1.0 - March 19, 2026
- Tenth version of the program.
- Fixed a bug, program now takes float values for direct conversion

## Version v.1.1.1 - March 25, 2026
- Eleventh version of the program
- Added a feature wwhere if GWA > 100%, it caps to 100%
- Fixed a bug, function now takes one positional argument instead of 0

## Version v.1.1.2 - April 13, 2026
- Twelfth version of the program
- Fixed a bug, JSON loading crash: added try-except to handle JSONDecodeError when grades.json is empty or corrupted.
- Fixed a bug, Normalized GWA using: gwa = (total_contribution / total_weight) * 100.
- Fixed a bug, Added check for "quarters" key before accessing it.

## Version v.1.1.3 - April 14, 2026
- Thirteenth version of the program
- Fixed a bug, Used .items() when looping through quarters to correctly access key-value pairs.
- Updates:
  - Added feature, Bonus cap system: limited bonus points by 5.
  - Added feature, User identity mismatch warning that prevents silent overwriting of user identity.
- Added note, Clarification for grade calculator: Enter your CURRENT WEIGHTED grade.
