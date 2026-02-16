DOCUMENTATION

- Updated feature list (reflecting any additions or removals)

Core Features
Computes subject GWA percentage.
Supports multiple subjects (1–15 subjects).

Accepts:
Formative assessments (maximum of 10)
Alternative assessments (maximum of 7)
Midterm examination
Final examination
Allows custom weight input for each assessment type.

Validates user input for:
Integer ranges
Grade range (0–100)
Displays formatted GWA table based on the institutional grading scale.
Includes looping feature to recompute new GWA sets.

Additions / Revisions:
Implemented get_valid_number() for numeric validation.
Implemented get_valid_grade() to prevent invalid grade entries.
Modularized computation using separate functions.
Added optional GWA table display.
Added loop control for repeated usage.

Removed Features:
No features were removed from the original proposal.




- Revised file/function structure
  
The project has one main file, gwa_calculator.py, where all the code is written, and a README.md file for documentation. The program is divided into simple functions to handle input checking, grade calculations, and final GWA computation. The main part of the program runs the loop for multiple subjects and displays the results.



- Any new technologies or tools introduced

New Technologies / Tools Introduced
Python 3 – Main programming language

Built-in Python features:
try and except for error handling
while loops for repeated input validation
Lists for storing subject GWAs and grading table data

No external libraries were introduced to maintain simplicity and compatibility.


- Use of APA-style referencing for any sources used
  
Philippine Science High School System. (n.d.). Institutional grading system reference.










DETAILED METHODOLOGY SECTION

- How core features were implemented

The core features were implemented using separate functions for each major task. Input validation is handled by get_valid_number() and get_valid_grade() to ensure users enter correct values. The calculate_assessment() function computes weighted grades for formative and alternative assessments, while calculate_exam() computes the weighted contribution of exams. All computed values are combined in calculate_subject_gwa() to produce the final GWA percentage for each subject. The main loop allows users to calculate multipl subjects and optionally display the grading table.



- Technologies used (with justification)

The program was developed using Python 3 because it is simple, readable, and suitable for numerical calculations.

Built-in Python features used include:
Functions for organizing code
While loops for repeated input
Lists for storing results

No external libraries were used to keep the program simple and easy to run.



- Key design decisions or trade-offs

The program was designed as a CLI instead of a graphical interface to keep development simple and focused on computation.

No external libraries were used to avoid dependency issues and ensure compatibility.

The code was divided into functions to make it more organized and easier to understand.



- Reference to ethical considerations in programming choices (e.g., user privacy, accessibility)

The program does not store or share user data. All information is used only during runtime.

Input validation ensures fair and accurate calculations.

A reminder is included that the GWA table may not perfectly match official institutional grading systems, preventing misuse of the results.
