import random
import tkinter as tk
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pytest

# Set the variables for the input space
input_space_min = 20
input_space_max = 30

def generate_test_cases_with_ml(min_value, max_value):
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

    # Generate ML-based test cases
    ml_test_cases = generate_ml_based_test_cases()
    test_cases.extend(ml_test_cases)

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

def generate_ml_based_test_cases():
    # Generate dataset for ML-based test cases
    X = [random.randint(input_space_min, input_space_max) for _ in range(100)]
    y = ['Valid' if value % 2 == 0 else 'Invalid' for value in X]

    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train a simple RandomForestClassifier
    clf = RandomForestClassifier()
    clf.fit([[x] for x in X_train], y_train)

    # Predict on the test set
    y_pred = clf.predict([[x] for x in X_test])

    # Evaluate accuracy
    accuracy = accuracy_score(y_test, y_pred)

    return [(X_test[i], 'ML-Based Test', 'Valid' if y_pred[i] == 'Valid' else 'Invalid') for i in range(len(X_test))]

# Pytest for validation
def test_validate_input_space():
    assert validate_input_space(10, 20) == True
    assert validate_input_space(20, 10) == False
    assert validate_input_space(10, 13) == False
    assert validate_input_space(-10, 10) == False

# GUI using Tkinter
class TestCaseGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Test Case Generator")

        self.min_label = tk.Label(root, text="Min Value:")
        self.min_entry = tk.Entry(root)

        self.max_label = tk.Label(root, text="Max Value:")
        self.max_entry = tk.Entry(root)

        self.generate_button = tk.Button(root, text="Generate Test Cases", command=self.generate_test_cases)

        self.result_text = tk.Text(root, height=20, width=50)

        self.min_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)
        self.min_entry.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)
        self.max_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)
        self.max_entry.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)
        self.generate_button.grid(row=2, column=0, columnspan=2, pady=10)
        self.result_text.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

    def generate_test_cases(self):
        min_value = int(self.min_entry.get())
        max_value = int(self.max_entry.get())

        test_cases = generate_test_cases_with_ml(min_value, max_value)

        result_text_content = ""
        for i, test_case in enumerate(test_cases):
            value, test_type, expected_output = test_case
            result_text_content += f"Test Case {i + 1}: {value} (Type: {test_type}, Expected: {expected_output})\n"

        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result_text_content)

# Run the Tkinter app
if __name__ == "__main__":
    root = tk.Tk()
    app = TestCaseGeneratorApp(root)
    root.mainloop()
