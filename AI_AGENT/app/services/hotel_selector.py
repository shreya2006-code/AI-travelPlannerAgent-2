import pandas as pd


class HotelSelector:

    def select(
        self,
        hotels: pd.DataFrame,
        preferences: dict
    ):

        if hotels.empty:
            return None

        filtered = hotels.copy()

        budget = preferences.get("budget")
        hotel_type = preferences.get("hotel_type")
        days = preferences.get("days") or 3

        # -------------------------------------------------
        # 1. If user explicitly requested a hotel type
        # -------------------------------------------------

        if hotel_type:

            filtered = filtered[
                filtered["hotel_type"].str.lower()
                == hotel_type.lower()
            ]

        # -------------------------------------------------
        # 2. If budget is given, keep only hotels that fit
        # -------------------------------------------------

        if budget:
            # Allocate only 55% of the total budget to the hotel
            hotel_budget = budget * 0.55

            filtered = filtered[
                (filtered["min_price"] * days) <= hotel_budget
            ]

        # -------------------------------------------------
        # 3. Default to Mid-range if user gave neither
        # -------------------------------------------------

        if (
            not hotel_type
            and budget is None
        ):

            mid = filtered[
                filtered["hotel_type"] == "Mid-range"
            ]

            if not mid.empty:
                filtered = mid

        # -------------------------------------------------
        # 4. Fallback
        # -------------------------------------------------

        if filtered.empty:

            # No hotel fits the budget.
            # Pick the cheapest hotel instead of ignoring the budget.
            filtered = hotels.sort_values(
                by="min_price",
                ascending=True
            )

        # -------------------------------------------------
        # 5. Pick highest rated
        # -------------------------------------------------

        filtered = filtered.sort_values(
            by=[
                "star_rating",
                "min_price"
            ],
            ascending=[
                False,
                True
            ]
        )

        return filtered.iloc[0].to_dict()