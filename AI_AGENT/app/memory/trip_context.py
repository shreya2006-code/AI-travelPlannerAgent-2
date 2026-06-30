class TripContext:

    def __init__(self):

        self.preferences = {}

        self.current_trip = None

    def update_preferences(self, new_preferences):

        for key, value in new_preferences.items():

            if value in [None, "", [], {}]:
                continue

            if key == "preferred_categories":

                current = set(self.preferences.get("preferred_categories", []))
                current.update(value)

                # Remove from excluded if user is adding them back
                excluded = set(self.preferences.get("excluded_categories", []))
                excluded -= set(value)

                self.preferences["preferred_categories"] = list(current)
                self.preferences["excluded_categories"] = list(excluded)

            elif key == "excluded_categories":

                current = set(self.preferences.get("excluded_categories", []))
                current.update(value)

                # Remove from preferred if user excludes them
                preferred = set(self.preferences.get("preferred_categories", []))
                preferred -= set(value)

                self.preferences["excluded_categories"] = list(current)
                self.preferences["preferred_categories"] = list(preferred)

            else:

                self.preferences[key] = value

    def get_preferences(self):

        return self.preferences

    def save_trip(self, trip):

        self.current_trip = trip

    def get_trip(self):

        return self.current_trip

    def clear(self):

        self.preferences = {}

        self.current_trip = None