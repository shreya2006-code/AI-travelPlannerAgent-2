import pandas as pd


class AttractionSelector:

    def select(

        self,

        attractions: pd.DataFrame,

        preferences: dict

    ):

        excluded = preferences.get(
            "excluded_categories",
            []
        )

        preferred = preferences.get(
            "preferred_categories",
            []
        )

        data = attractions.copy()

        if excluded:

            data = data[
                ~data["category"].isin(excluded)
            ]

        if preferred:

            pref = data[
                data["category"].isin(preferred)
            ]

            other = data[
                ~data["category"].isin(preferred)
            ]

            data = pd.concat(
                [pref, other]
            )

        days = preferences.get("days", 3)

        # Approximate attractions needed
        required = days * 3
        
        # Don't exceed available attractions
        data = data.head(required)
        
        return data.to_dict("records")