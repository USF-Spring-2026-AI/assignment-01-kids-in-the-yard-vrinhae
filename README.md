# AI Assignment 01 - Kids in the Yard

1. I used ChatGPT Pro.
2. "Generate a Python implementation of a family tree simulator using object-oriented design with three classes: Person, PersonFactory, and FamilyTree.
The tree starts with two people born in 1950 with the last name "Jones", generate descendants until 2120 or no more children can be generated, and read demographic data from 6 CSV files in the current directory

CSV file structures:
life_expectancy.csv: columns Year, Period life expectancy at birth
first_names.csv: columns decade, gender, name, frequency
last_names.csv: columns Decade, Rank, LastName
rank_to_probability.csv: single row of 30 comma-separated probabilities (no header)
birth_and_marriage_rates.csv: columns decade, birth_rate, marriage_rate
gender_name_probability.csv: columns decade, gender, probability

Rules:
Death year = birth year + life expectancy ± 10 random years
Number of children = birth_rate ± 1.5 rounded up
Children born evenly spread between parent age 25-45
Partners created within ±10 years of child's birth year
Descendants keep "Jones", partners get random last name

Interactive menu should support:

Total people in tree
People by decade
Duplicate names
Quit"
3.  ChatGPT used @dataclass instead of a regular class for Person as well as numeric IDs to track people instead of an object reference. Additionally, they used an iterative queue for generation. ChatGPT also added more error handling and file validation. Main() and run_menu() was seperated as standalone functions outside of the class
4. add get_birth_rate public method to fix encapsulation and add better error handling for missing files
5. using numeric IDs as it makes the program less readable. using a queue instead of recursion as the logical with recursive is simpler and easier to read. using @dataclass as it lacks protection and also does not fufill the requirement of accessor and mutator method.