import os
import json
import math

def main():
    Voltage = 0.5
    sample_type = input("Enter sample type: ")
    if sample_type == "new":
        sample_type = new_equation()
    eq = get_equation(sample_type)
    if eq:
        try:
            print("OD = ", eval(eq, {"math": math, "Voltage": Voltage}))
        except Exception as e:
            print(f"Error evaluating equation: {e}")

def get_equation(sample_type):
    equations = load_equations()
    return equations.get(sample_type, "Equation not found")

def load_equations():
    """Load calibration equations from a JSON file."""
    try:
        # Use a relative path to ensure the file is found in the same folder
        file_path = os.path.join(os.path.dirname(__file__), 'Equations.json')
        with open(file_path, 'r') as file:
            return json.load(file)  # Load the JSON data
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return {}  # Return empty dictionary if the file does not exist
    except json.JSONDecodeError as e:
        print(f"Error loading JSON: {e}")
        return {}

def new_equation():
    """Save new calibration equation to a JSON file."""
    sample_type = input("Enter new sample type: ")
    equation = input("Enter the equation: ")
    equations = load_equations()
    equations[sample_type] = equation  # Save new equation for the sample type
    save_equations(equations)
    return sample_type

def save_equations(equations):
    """Save calibration equations to a JSON file."""
    file_path = os.path.join(os.path.dirname(__file__), 'Equations.json')
    with open(file_path, 'w') as file:
        json.dump(equations, file, indent=4)  # Write updated equations to JSON file

if __name__ == "__main__":
    main()