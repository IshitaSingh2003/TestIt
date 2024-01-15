import random

# Set the variables for the input space
input_space_min = 20
input_space_max = 30

def generate_test_cases(min_value, max_value):
    test_cases = []

    # Validate input space
    if not validate_input_space(min_value, max_value):
        print("Invalid input space:")
        if max_value <= min_value:
            print("   - Maximum value should be greater than the minimum value.")
        if max_value <= min_value + 3:
            print("   - Maximum value should be at least 3 greater than the minimum value.")
        if min_value < 0 or max_value < 0:
            print("   - Values must be positive integers.")
        return test_cases

    # Equivalence Partitioning
    partitions = divide_into_partitions()
    for partition in partitions:
        test_cases.extend(generate_test_cases_for_partition(partition, "Equivalence Partitioning"))

    # Boundary Value Analysis
    boundaries = find_boundary_values()
    for boundary in boundaries:
        test_cases.append(boundary)

    # Non-numeric Values
    non_numeric_values = generate_non_numeric_values()
    for value in non_numeric_values:
        test_cases.append((value, "Non-Numeric Value", "Invalid"))

    return test_cases

# Helper functions

def validate_input_space(min_value, max_value):
    if max_value <= min_value:
        return False
    if max_value <= min_value + 3:
        return False
    if min_value < 0 or max_value < 0:
        return False
    return True

def divide_into_partitions():
    partitions = []
    partitions.append(("Valid Values", input_space_min, (input_space_min + input_space_max) // 2, input_space_max))  # Values within the range
    partitions.append(("Invalid Values", -input_space_min, -(input_space_min + input_space_max) // 2, -input_space_max))  # Negative values of the valid cases
    return partitions

def generate_test_cases_for_partition(partition, test_type):
    test_cases = []
    partition_type, *values = partition

    if partition_type == "Invalid Values":
        for value in values:
            test_cases.append((value, test_type, "Invalid"))
    elif partition_type == "Valid Values":
        for value in values:
            test_cases.append((value, test_type, "Valid"))

    return test_cases

def find_boundary_values():
    boundaries = []
    boundaries.extend([(input_space_min - 1, 'Boundary Value Analysis', 'Invalid'),  # One step below the lower boundary
                       (input_space_min, 'Boundary Value Analysis', 'Valid'),  # Lower boundary
                       (input_space_min + 1, 'Boundary Value Analysis', 'Valid'),  # One step above the lower boundary
                       (input_space_max - 1, 'Boundary Value Analysis', 'Valid'),  # One step below the upper boundary
                       (input_space_max, 'Boundary Value Analysis', 'Valid'),  # Upper boundary
                       (input_space_max + 1, 'Boundary Value Analysis', 'Invalid')])  # One step above the upper boundary
    return boundaries

def generate_non_numeric_values():
    non_numeric_values = []
    non_numeric_values.extend(['A', '@'])  # Example non-numeric values
    return non_numeric_values

def generate_test_case_output():
    min_value = input_space_min
    max_value = input_space_max

    test_cases = generate_test_cases(min_value, max_value)

    for i, test_case in enumerate(test_cases):
        value, test_type, expected_output = test_case
        print(f"Test Case {i+1}: {value} (Type: {test_type}, Expected: {expected_output})")

generate_test_case_output()
