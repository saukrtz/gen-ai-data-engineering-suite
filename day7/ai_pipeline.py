import pandas as pd
import logging
from logging.handlers import RotatingFileHandler
import os

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a rotating file handler
file_handler = RotatingFileHandler('pipeline.log', maxBytes=1024*1024*10, backupCount=5)
file_handler.setLevel(logging.INFO)

# Create a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create a formatter and attach it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

def load_data(file_path):
    """
    Load patient data from a CSV file.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Loaded patient data.
    """
    try:
        logger.info(f"Loading data from {file_path}")
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        logger.error(f"Failed to load data: {str(e)}")
        raise

def clean_data(data):
    """
    Clean patient data by removing duplicates and handling nulls.

    Args:
        data (pd.DataFrame): Patient data.

    Returns:
        pd.DataFrame: Cleaned patient data.
    """
    try:
        logger.info("Cleaning data")
        # Remove duplicates
        data = data.drop_duplicates()

        # Handle nulls
        data['age'] = data['age'].fillna(data['age'].mean())
        data['billing_amount'] = data['billing_amount'].fillna(0)

        return data
    except Exception as e:
        logger.error(f"Failed to clean data: {str(e)}")
        raise

def aggregate_billing(data):
    """
    Aggregate total billing per 'diagnosis' AND 'hospital_id'.

    Args:
        data (pd.DataFrame): Patient data.

    Returns:
        pd.DataFrame: Aggregated billing data.
    """
    try:
        logger.info("Aggregating billing")
        aggregated_data = data.groupby(['diagnosis', 'hospital_id'])['billing_amount'].sum().reset_index()
        return aggregated_data
    except Exception as e:
        logger.error(f"Failed to aggregate billing: {str(e)}")
        raise

def generate_daily_counts(data):
    """
    Generate daily patient counts based on 'visit_date'.

    Args:
        data (pd.DataFrame): Patient data.

    Returns:
        pd.DataFrame: Daily patient counts.
    """
    try:
        logger.info("Generating daily counts")
        daily_counts = data.groupby('visit_date')['patient_id'].nunique().reset_index()
        return daily_counts
    except Exception as e:
        logger.error(f"Failed to generate daily counts: {str(e)}")
        raise

def save_data(data, file_path):
    """
    Save patient data to a CSV file.

    Args:
        data (pd.DataFrame): Patient data.
        file_path (str): Path to the CSV file.
    """
    try:
        logger.info(f"Saving data to {file_path}")
        data.to_csv(file_path, index=False)
    except Exception as e:
        logger.error(f"Failed to save data: {str(e)}")
        raise

def main():
    # Load patient data
    data = load_data('patients.csv')

    # Clean patient data
    cleaned_data = clean_data(data)

    # Aggregate billing
    aggregated_data = aggregate_billing(cleaned_data)

    # Generate daily counts
    daily_counts = generate_daily_counts(cleaned_data)

    # Save data
    save_data(aggregated_data, 'billing_enhanced.csv')
    save_data(daily_counts, 'daily_enhanced.csv')

if __name__ == "__main__":
    main()