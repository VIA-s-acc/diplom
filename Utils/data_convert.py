import pandas as pd
import os
def check_path(path):
    """
    Check if the path exists.

    Args:
        path (str): Path to check.

    Returns:
        bool: True if the path exists, False otherwise.
    """
    if os.path.exists(path):
        return True
    else:
        os.makedirs(path)
        return False

def dict_to_csv(data, filename):
    """
    Convert dictionary to CSV file.

    Args:
        data (dict): Dictionary to save as CSV.
        filename (str): Name of the output CSV file.
    """
    check_path(os.path.dirname(filename))
    df = pd.DataFrame(data)
    df.to_csv(filename)
    print(f"Data saved to {filename}")
    
def dict_to_excel(data, filename):
    """
    Convert dictionary to Excel file.

    Args:
        data (dict): Dictionary to save as Excel.
        filename (str): Name of the output Excel file.
    """
    check_path(os.path.dirname(filename))
    df = pd.DataFrame(data)
    df.to_excel(filename)
    print(f"Data saved to {filename}")
    
def dict_to_json(data, filename):
    """
    Convert dictionary to JSON file.

    Args:
        data (dict): Dictionary to save as JSON.
        filename (str): Name of the output JSON file.
    """
    check_path(os.path.dirname(filename))
    df = pd.DataFrame(data)
    df.to_json(filename)
    print(f"Data saved to {filename}")
    


