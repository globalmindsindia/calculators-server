def calculate_german_grade(best_grade, min_passing_grade, your_grade):
    try:
        best_grade = float(best_grade)
        min_passing_grade = float(min_passing_grade)
        your_grade = float(your_grade)
    except ValueError:
        return "Invalid input: Please enter numeric values."
 
    if best_grade <= min_passing_grade:
        return "Invalid input: Best grade must be greater than minimum passing grade."
 
    german_grade = 1 + 3 * ((best_grade - your_grade) / (best_grade - min_passing_grade))
    german_grade = round(min(german_grade, 4.0), 2)
    return german_grade