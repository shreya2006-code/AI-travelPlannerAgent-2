import pandas as pd


class DatasetSearch:
    """
    Handles searching across the travel datasets.
    """

    def __init__(self, loader):
        self.loader = loader

    def find_place(self, place_name: str):
        """
        Find a place by name (case-insensitive).
        Returns a DataFrame.
        """

        result = self.loader.places[
            self.loader.places["place_name"]
            .str.lower()
            .str.strip()
            == place_name.lower().strip()
        ]

        return result

    def find_hotels(self, place_id, budget=None, hotel_type=None):

        hotels = self.loader.hotels[
            self.loader.hotels["place_id"] == place_id
        ]

        if hotel_type:

            hotels = hotels[
                hotels["hotel_type"]
                .str.lower()
                ==
                hotel_type.lower()
            ]

        if budget:
            hotels["min_price"] = (hotels["min_price"].astype(str).str.replace(",", "", regex=False).astype(int))
            hotels = hotels[
                hotels["min_price"] <= budget
            ]

        return hotels

    def find_attractions(
        self,
        place_id,
        excluded_categories=None,
        preferred_categories=None
    ):

        attractions = self.loader.attractions[
            self.loader.attractions["place_id"] == place_id
        ]

        if excluded_categories:

            attractions = attractions[
                ~attractions["category"].isin(
                    excluded_categories
                )
            ]

        if preferred_categories:

            preferred = attractions[
                attractions["category"].isin(
                    preferred_categories
                )
            ]

            others = attractions[
                ~attractions["category"].isin(
                    preferred_categories
                )
            ]

            attractions = pd.concat(
                [preferred, others]
            )

        return attractions