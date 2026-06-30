from pathlib import Path
import pandas as pd


class DatasetLoader:
    """
    Loads all travel datasets into memory.
    The datasets are loaded once when the application starts.
    """

    def __init__(self, dataset_path: str):
        self.dataset_path = Path(dataset_path)

        self.places = None
        self.hotels = None
        self.attractions = None

    def load_datasets(self):
        """Load all CSV files."""

        self.places = pd.read_csv(self.dataset_path / "places.csv")

        self.hotels = pd.read_csv(self.dataset_path / "hotels.csv")

        self.attractions = pd.read_csv(
            self.dataset_path / "attractions.csv"
        )

        print("✅ Travel datasets loaded successfully.")