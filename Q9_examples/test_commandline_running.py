import pytest
import subprocess
import json
from deepdiff import DeepDiff


def run_command_and_compare(command, expected_file):
    """
    Runs a shell command and compares the JSON output with an expected JSON file.

    Args:
        command (str): The shell command to execute.
        expected_file (str): Path to the JSON file containing the expected output.

    Returns:
        (bool, dict): A tuple where the first value indicates success (True/False),
                      and the second value contains any differences if the test fails.
    """
    # Run the command using subprocess and capture the output
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    # Ensure the command executed successfully
    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {command}\nError: {result.stderr}")

    # Parse the output JSON from the command
    output_json = json.loads(result.stdout.strip())

    # Load the expected JSON from the file
    with open(expected_file, "r") as file:
        expected_json = json.load(file)

    # Compare the two JSONs using DeepDiff, which handles structured differences
    diff = DeepDiff(expected_json, output_json, ignore_order=True)

    # If no differences, return True (success). Otherwise, return False and the differences.
    if not diff:
        return True, None
    else:
        return False, diff


# Parameterized pytest for Task 1
@pytest.mark.parametrize("command,expected_file", [
    # Test case 1: Task 1, Example 1
    (
            "c:/WinPython/WPy64-3920/python-3.9.2.amd64/python.exe c:/Intro2CS/FinalProject/main.py -t 1 -s Q1_examples/example_1/sentences_small_1.csv -n Q1_examples/example_1/people_small_1.csv -r REMOVEWORDS.csv",
            "Q1_examples/example_1/Q1_result1.json"
    ),
    # Test case 2: Task 1, Example 2
    (
            "c:/WinPython/WPy64-3920/python-3.9.2.amd64/python.exe c:/Intro2CS/FinalProject/main.py -t 1 -s Q1_examples/example_2/sentences_small_2.csv -n Q1_examples/example_2/people_small_2.csv -r REMOVEWORDS.csv",
            "Q1_examples/example_2/Q1_result2.json"
    ),
    # Test case 3: Task 1, Example 3
    (
            "c:/WinPython/WPy64-3920/python-3.9.2.amd64/python.exe c:/Intro2CS/FinalProject/main.py -t 1 -s Q1_examples/example_3/sentences_small_3.csv -n Q1_examples/example_3/people_small_3.csv -r REMOVEWORDS.csv",
            "Q1_examples/example_3/Q1_result3.json"
    )
])
def test_task1_commandline(command, expected_file):
    """
    Runs Task 1 command-line tests, comparing the JSON output with the expected results.

    Args:
        command (str): The shell command to execute.
        expected_file (str): Path to the JSON file containing the expected output.
    """
    # Run the command and compare the output with the expected result
    passed, diff = run_command_and_compare(command, expected_file)

    # If the test fails, raise an assertion error with detailed differences
    if not passed:
        pytest.fail(f" Test failed for command: {command}\nDifferences:\n{diff}")


# Parameterized pytest for Task 2
@pytest.mark.parametrize("command,expected_file", [
    # Test case 1: Task 2, Example 1
    (
            "c:/WinPython/WPy64-3920/python-3.9.2.amd64/python.exe c:/Intro2CS/FinalProject/main.py -t 2 --maxk 3 -s Q2_examples/example_1/sentences_small_1.csv -r REMOVEWORDS.csv",
            "Q2_examples/example_1/Q2_result1.json"
    ),
    # Test case 2: Task 2, Example 2
    (
            "c:/WinPython/WPy64-3920/python-3.9.2.amd64/python.exe c:/Intro2CS/FinalProject/main.py -t 2 --maxk 4 -s Q2_examples/example_2/sentences_small_2.csv -r REMOVEWORDS.csv",
            "Q2_examples/example_2/Q2_result2.json"
    ),
    # Test case 3: Task 2, Example 3
    (
            "c:/WinPython/WPy64-3920/python-3.9.2.amd64/python.exe c:/Intro2CS/FinalProject/main.py -t 2 --maxk 5 -s Q2_examples/example_3/sentences_small_3.csv -r REMOVEWORDS.csv",
            "Q2_examples/example_3/Q2_result3.json"
    )
])
def test_task2_commandline(command, expected_file):
    """
    Runs Task 2 command-line tests, comparing the JSON output with the expected results.

    Args:
        command (str): The shell command to execute.
        expected_file (str): Path to the JSON file containing the expected output.
    """
    # Run the command and compare the output with the expected result
    passed, diff = run_command_and_compare(command, expected_file)

    # If the test fails, raise an assertion error with detailed differences
    if not passed:
        pytest.fail(f" Test failed for command: {command}\nDifferences:\n{diff}")


# Parameterized pytest for Task 3
@pytest.mark.parametrize("command,expected_file", [
    # Test case 1: Task 3, Example 1
    (
            "c:/WinPython/WPy64-3920/python-3.9.2.amd64/python.exe c:/Intro2CS/FinalProject/main.py -t 3 -s Q3_examples/example_1/sentences_small_1.csv -n Q3_examples/example_1/people_small_1.csv -r REMOVEWORDS.csv",
            "Q3_examples/example_1/Q3_result1.json"
    ),
    # Test case 2: Task 3, Example 2
    (
            "c:/WinPython/WPy64-3920/python-3.9.2.amd64/python.exe c:/Intro2CS/FinalProject/main.py -t 3 -s Q3_examples/example_2/sentences_small_2.csv -n Q3_examples/example_2/people_small_2.csv -r REMOVEWORDS.csv",
            "Q3_examples/example_2/Q3_result2.json"
    ),
    # Test case 3: Task 3, Example 3
    (
            "c:/WinPython/WPy64-3920/python-3.9.2.amd64/python.exe c:/Intro2CS/FinalProject/main.py -t 3 -s Q3_examples/example_3/sentences_small_3.csv -n Q3_examples/example_3/people_small_3.csv -r REMOVEWORDS.csv",
            "Q3_examples/example_3/Q3_result3.json"
    ),
    # Test case 4: Task 3, Example 4
    (
            "c:/WinPython/WPy64-3920/python-3.9.2.amd64/python.exe c:/Intro2CS/FinalProject/main.py -t 3 -s Q3_examples/example_4/sentences_small_4.csv -n Q3_examples/example_4/people_small_4.csv -r REMOVEWORDS.csv",
            "Q3_examples/example_4/Q3_result4.json"
    )
])
def test_task3_commandline(command, expected_file):
    """
    Runs Task 3 command-line tests, comparing the JSON output with the expected results.

    Args:
        command (str): The shell command to execute.
        expected_file (str): Path to the JSON file containing the expected output.
    """
    # Run the command and compare the output with the expected result
    passed, diff = run_command_and_compare(command, expected_file)

    # If the test fails, raise an assertion error with detailed differences
    if not passed:
        pytest.fail(f"Test failed for command: {command}\nDifferences:\n{diff}")


# Parameterized pytest for Task 4
@pytest.mark.parametrize("command,expected_file", [
    # Test case 1: Task 4, Example 1
    (
            "c:/WinPython/WPy64-3920/python-3.9.2.amd64/python.exe c:/Intro2CS/FinalProject/main.py -t 4 -s Q4_examples/example_1/sentences_small_1.csv --qsek_query_path Q4_examples/example_1/kseq_query_keys_1.json -r REMOVEWORDS.csv",
            "Q4_examples/example_1/Q4_result1.json"
    ),
    # Test case 2: Task 4, Example 2
    (
            "c:/WinPython/WPy64-3920/python-3.9.2.amd64/python.exe c:/Intro2CS/FinalProject/main.py -t 4 -s Q4_examples/example_2/sentences_small_2.csv --qsek_query_path Q4_examples/example_2/kseq_query_keys_2.json -r REMOVEWORDS.csv",
            "Q4_examples/example_2/Q4_result2.json"
    ),
    # Test case 3: Task 4, Example 3
    (
            "c:/WinPython/WPy64-3920/python-3.9.2.amd64/python.exe c:/Intro2CS/FinalProject/main.py -t 4 -s Q4_examples/example_3/sentences_small_3.csv --qsek_query_path Q4_examples/example_3/kseq_query_keys_3.json -r REMOVEWORDS.csv",
            "Q4_examples/example_3/Q4_result3.json"
    ),
    # Test case 4: Task 4, Example 4
    (
            "c:/WinPython/WPy64-3920/python-3.9.2.amd64/python.exe c:/Intro2CS/FinalProject/main.py -t 4 -s Q4_examples/example_4/sentences_small_4.csv --qsek_query_path Q4_examples/example_4/kseq_query_keys_4.json -r REMOVEWORDS.csv",
            "Q4_examples/example_4/Q4_result4.json"
    )
])
def test_task4_commandline(command, expected_file):
    """
    Runs Task 4 command-line tests, comparing the JSON output with the expected results.

    Args:
        command (str): The shell command to execute.
        expected_file (str): Path to the JSON file containing the expected output.
    """
    # Run the command and compare the output with the expected result
    passed, diff = run_command_and_compare(command, expected_file)

    # If the test fails, raise an assertion error with detailed differences
    if not passed:
        pytest.fail(f"Test failed for command: {command}\nDifferences:\n{diff}")

# Parameterized pytest for Task 5
@pytest.mark.parametrize("command,expected_file", [
    # Test case 1: Task 5, Example 1
    (
        "c:/WinPython/WPy64-3920/python-3.9.2.amd64/python.exe c:/Intro2CS/FinalProject/main.py -t 5 -s Q5_examples/example_1/sentences_small_1.csv -n Q5_examples/example_1/people_small_1.csv -r REMOVEWORDS.csv --maxk 3",
        "Q5_examples/example_1/Q5_result1.json"
    ),
    # Test case 2: Task 5, Example 2
    (
        "c:/WinPython/WPy64-3920/python-3.9.2.amd64/python.exe c:/Intro2CS/FinalProject/main.py -t 5 -s Q5_examples/example_2/sentences_small_2.csv -n Q5_examples/example_2/people_small_2.csv -r REMOVEWORDS.csv --maxk 4",
        "Q5_examples/example_2/Q5_result2.json"
    ),
    # Test case 3: Task 5, Example 3
    (
        "c:/WinPython/WPy64-3920/python-3.9.2.amd64/python.exe c:/Intro2CS/FinalProject/main.py -t 5 -s Q5_examples/example_3/sentences_small_3.csv -n Q5_examples/example_3/people_small_3.csv -r REMOVEWORDS.csv --maxk 5",
        "Q5_examples/example_3/Q5_result3.json"
    ),
    # Test case 4: Task 5, Example 4
    (
        "c:/WinPython/WPy64-3920/python-3.9.2.amd64/python.exe c:/Intro2CS/FinalProject/main.py -t 5 -s Q5_examples/example_4/sentences_small_4.csv -n Q5_examples/example_4/people_small_4.csv -r REMOVEWORDS.csv --maxk 6",
        "Q5_examples/example_4/Q5_result4.json"
    )
])
def test_task5_commandline(command, expected_file):
    passed, diff = run_command_and_compare(command, expected_file)
    if not passed:
        pytest.fail(f"Test failed for command: {command}\nDifferences:\n{diff}")


# Parameterized pytest for Task 6 (Finding Direct Connections Between People)
@pytest.mark.parametrize("command,expected_file", [
    # Test case 1: Task 6, Example 1
    (
        "c:/WinPython/WPy64-3920/python-3.9.2.amd64/python.exe c:/Intro2CS/FinalProject/main.py -t 6 -s Q6_examples/example_1/sentences_small_1.csv -n Q6_examples/example_1/people_small_1.csv -r REMOVEWORDS.csv --windowsize 4 --threshold 4",
        "Q6_examples/example_1/Q6_result1_w4_t4.json"
    ),
    # Test case 2: Task 6, Example 2
    (
        "c:/WinPython/WPy64-3920/python-3.9.2.amd64/python.exe c:/Intro2CS/FinalProject/main.py -t 6 --s Q6_examples/example_2/sentences_small_2.csv -n Q6_examples/example_2/people_small_2.csv -r REMOVEWORDS.csv --windowsize 3 --threshold 2",
        "Q6_examples/example_2/Q6_result2_w3_t2.json"
    ),
    # Test case 3: Task 6, Example 3
    (
        "c:/WinPython/WPy64-3920/python-3.9.2.amd64/python.exe c:/Intro2CS/FinalProject/main.py -t 6 -s Q6_examples/example_3/sentences_small_3.csv -n Q6_examples/example_3/people_small_3.csv -r REMOVEWORDS.csv --windowsize 5 --threshold 2",
        "Q6_examples/example_3/Q6_result2_w5_t2.json"
    ),
    # Test case 4: Task 6, Example 4
    (
        "c:/WinPython/WPy64-3920/python-3.9.2.amd64/python.exe c:/Intro2CS/FinalProject/main.py -t 6 -s Q6_examples/example_4/sentences_small_4.csv -n Q6_examples/example_4/people_small_4.csv -r REMOVEWORDS.csv --windowsize 5 --threshold 1",
        "Q6_examples/example_4/Q6_result2_w5_t1.json"
    )
])
def test_task6_commandline(command, expected_file):
    passed, diff = run_command_and_compare(command, expected_file)
    if not passed:
        pytest.fail(f"Task 6 failed for command: {command}\nDifferences:\n{diff}")


# Parameterized pytest for Task 7 (Determining Indirect Connections)
@pytest.mark.parametrize("command,expected_file", [
    # Test case 1: Task 7, Example 1
    (
        "c:/WinPython/WPy64-3920/python-3.9.2.amd64/python.exe c:/Intro2CS/FinalProject/main.py -t 7 -s Q7_examples/example_1/sentences_small_1.csv -n Q7_examples/example_1/people_small_1.csv --pairs Q7_examples/example_1/people_connections_1.json -r REMOVEWORDS.csv --windowsize 5 --threshold 2 --maximal_distance 1000",
        "Q7_examples/example_1/Q7_result1_w5_t2.json"
    ),
    # Test case 2: Task 7, Example 2
    (
        "c:/WinPython/WPy64-3920/python-3.9.2.amd64/python.exe c:/Intro2CS/FinalProject/main.py -t 7 -s Q7_examples/example_2/sentences_small_2.csv -n Q7_examples/example_2/people_small_2.csv --pairs Q7_examples/example_2/people_connections_2.json -r REMOVEWORDS.csv --windowsize 3 --threshold 2 --maximal_distance 1000",
        "Q7_examples/example_2/Q7_result2_w3_t2.json"
    ),
    # Test case 3: Task 7, Example 3
    (
        "c:/WinPython/WPy64-3920/python-3.9.2.amd64/python.exe c:/Intro2CS/FinalProject/main.py -t 7 -s Q7_examples/example_3/sentences_small_3.csv -n Q7_examples/example_3/people_small_3.csv --pairs Q7_examples/example_3/people_connections_3.json -r REMOVEWORDS.csv --windowsize 5 --threshold 2 --maximal_distance 1000",
        "Q7_examples/example_3/Q7_result3_w5_t1.json"
    ),
    # Test case 4: Task 7, Example 4
    (
        "c:/WinPython/WPy64-3920/python-3.9.2.amd64/python.exe c:/Intro2CS/FinalProject/main.py -t 7 -s Q7_examples/example_4/sentences_small_4.csv -n Q7_examples/example_4/people_small_4.csv --pairs Q7_examples/example_4/people_connections_4.json -r REMOVEWORDS.csv --windowsize 5 --threshold 2 --maximal_distance 1000",
        "Q7_examples/example_4/Q7_result4_w5_t2.json"
    )
])
def test_task7_commandline(command, expected_file):
    passed, diff = run_command_and_compare(command, expected_file)
    if not passed:
        pytest.fail(f"Task 7 failed for command: {command}\nDifferences:\n{diff}")


# Parameterized pytest for Task 8 (Checking Fixed-Length Paths Between People)
@pytest.mark.parametrize("command,expected_file", [
    # Test case 1: Task 8, Example 1
    (
        "c:/WinPython/WPy64-3920/python-3.9.2.amd64/python.exe c:/Intro2CS/FinalProject/main.py -t 8 -s Q8_examples/example_1/sentences_small_1.csv -n Q8_examples/example_1/people_small_1.csv -r REMOVEWORDS.csv --windowsize 3 --threshold 2 --fixed_length 2 --pairs Q8_examples/example_1/people_connections_1.json",
        "Q8_examples/example_1/Q8_example_1_w_3_threshold_2_fixed_length_2.json"
    ),
    # Test case 2: Task 8, Example 2
    (
        "c:/WinPython/WPy64-3920/python-3.9.2.amd64/python.exe c:/Intro2CS/FinalProject/main.py -t 8 -s Q8_examples/example_2/sentences_small_2.csv -n Q8_examples/example_2/people_small_2.csv -r REMOVEWORDS.csv --windowsize 3 --threshold 2 --fixed_length 3 --pairs Q8_examples/example_2/people_connections_2.json",
        "Q8_examples/example_2/Q8_example_2_w_3_threshold_2_fixed_length_3.json"
    ),
    # Test case 3: Task 8, Example 3
    (
        "c:/WinPython/WPy64-3920/python-3.9.2.amd64/python.exe c:/Intro2CS/FinalProject/main.py -t 8 -s Q8_examples/example_3/sentences_small_3.csv -n Q8_examples/example_3/people_small_3.csv -r REMOVEWORDS.csv --windowsize 3 --threshold 2 --fixed_length 8 --pairs Q8_examples/example_3/people_connections_3.json",
        "Q8_examples/example_3/Q8_example_3_w_3_threshold_2_fixed_length_8.json"
    )
])
def test_task8_commandline(command, expected_file):
    passed, diff = run_command_and_compare(command, expected_file)
    if not passed:
        pytest.fail(f"Task 8 failed for command: {command}\nDifferences:\n{diff}")


# Parameterized pytest for Task 9 (Grouping Sentences by Shared Words)
@pytest.mark.parametrize("command,expected_file", [
    # Test case 1: Task 9, Example 1
    (
        "c:/WinPython/WPy64-3920/python-3.9.2.amd64/python.exe c:/Intro2CS/FinalProject/main.py -t 9 -s Q9_examples/example_1/sentences_small_1.csv -r REMOVEWORDS.csv --threshold 1",
        "Q9_examples/example_1/Q9_result1.json"
    ),
    # Test case 2: Task 9, Example 2
    (
        "c:/WinPython/WPy64-3920/python-3.9.2.amd64/python.exe c:/Intro2CS/FinalProject/main.py -t 9 -s Q9_examples/example_2/sentences_small_2.csv -r REMOVEWORDS.csv --threshold 3",
        "Q9_examples/example_2/Q9_result2.json"
    ),
    # Test case 3: Task 9, Example 3
    (
        "c:/WinPython/WPy64-3920/python-3.9.2.amd64/python.exe c:/Intro2CS/FinalProject/main.py -t 9 -s Q9_examples/example_3/sentences_small_3.csv -r REMOVEWORDS.csv --threshold 6",
        "Q9_examples/example_3/Q9_result3.json"
    )
])
def test_task9_commandline(command, expected_file):
    passed, diff = run_command_and_compare(command, expected_file)
    if not passed:
        pytest.fail(f"Task 9 failed for command: {command}\nDifferences:\n{diff}")

