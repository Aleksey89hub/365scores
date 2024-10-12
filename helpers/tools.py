import pandas as pd
import allure
from faker import Faker
import logging

faker = Faker()
logger = logging.getLogger()


@allure.step("Log the user's email")
def log_email(email: str, user_id: str) -> None:
    """Log the user's email to the console and attach it to Allure report."""
    logger.info(f"User ID: {user_id}, Email: {email}")
    allure.attach(f"User ID: {user_id}, Email: {email}", name="User Email")


def read_data(csv_data_path: str = "../mock_data.csv") -> pd.DataFrame:
    """Read the data from the CSV file and return it as a Pandas DataFrame."""
    try:
        data = pd.read_csv(csv_data_path)
        return data
    except FileNotFoundError:
        logger.info(f"Error: The file {csv_data_path} was not found.")
        return pd.DataFrame()


def get_parametrized_data(csv_data: pd.DataFrame) -> list[tuple[str, str]]:
    """Extract 'title' and 'body' values from the provided CSV data."""
    return [(data['title'], data['body']) for data in csv_data.to_dict(orient='records')]
