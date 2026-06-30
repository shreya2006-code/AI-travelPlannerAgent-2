from app.services.preference_extractor import PreferenceExtractor
from app.services.hotel_selector import HotelSelector
from app.services.attraction_selector import AttractionSelector
from app.services.itinerary_generator import ItineraryGenerator
from app.services.llm_service import LLMService
from app.memory.trip_context import TripContext
from app.memory.session_manager import SessionManager
from app.utils.logger import logger


class Planner:

    def __init__(self, search_engine):

        self.search = search_engine

        self.extractor = PreferenceExtractor()

        self.hotel_selector = HotelSelector()

        self.attraction_selector = AttractionSelector()

        self.generator = ItineraryGenerator()
        self.session_manager = SessionManager()

        #self.memory = TripContext()

        self.llm = LLMService()

    def generate_trip(self, session_id, user_message):

        try:
            self.memory = self.session_manager.get_context(session_id)

            # 1. Extract preferences
            new_preferences = self.extractor.extract(user_message)
            print("Extracted:", new_preferences)

            current_trip = self.memory.get_trip()

            is_followup = (
            current_trip is not None and
                any(
                    word in user_message.lower()
                    for word in [
                        "remove", "add", "change", "instead",
                        "exclude", "include", "replace",
                        "increase", "decrease",
                        "extend", "shorten",
                        "more", "less"
                    ]
                )
            )

            self.memory.update_preferences(new_preferences)

            preferences = self.memory.get_preferences()
            current_trip = self.memory.get_trip()

            if (
                not preferences.get("destination")
                and current_trip is None
            ):
                return {
                    "success": False,
                    "message": "Please start by planning a trip first."
                }

            print("\n===== PREFERENCES =====")
            print(preferences)
            print("=======================\n")

            if is_followup:
                return self.handle_followup(
                    session_id,
                    user_message
                )

            place = self.search.find_place(
                preferences["destination"]
            )

            if place is None or place.empty:
                return {
                    "success": False,
                    "message": "Destination not found.",
                    "response": None,
                    "trip": None
                }

            place_id = place.iloc[0]["place_id"]

            hotels = self.search.find_hotels(
                place_id,
                preferences.get("budget"),
                preferences.get("hotel_type")
            )

            attractions = self.search.find_attractions(
                place_id,
                preferences.get("excluded_categories"),
                preferences.get("preferred_categories")
            )

            hotel = self.hotel_selector.select(
                hotels,
                preferences
            )

            selected_attractions = self.attraction_selector.select(
                attractions,
                preferences
            )

            for a in selected_attractions:
                print(a["attraction_name"], "-", a["category"])

            itinerary = self.generator.generate(
                preferences,
                place,
                hotel,
                selected_attractions
            )
            user_budget = preferences.get("budget")

            if (
                user_budget
                and itinerary["estimated_budget"] > user_budget
            ):
                logger.warning(
                    f"Trip exceeds budget. Estimated: {itinerary['estimated_budget']} | User: {user_budget}"
                )

            self.memory.save_trip(itinerary)

            if is_followup:
                response = self.llm.format_updated_trip(
                    current_trip=current_trip,
                    updated_trip=itinerary,
                    user_request=user_message
                )
            else:
                chat_response = self.llm.generate_chat_response(itinerary)

                full_itinerary = self.llm.format_response(itinerary)

                import json

                print("\n========== TRIP ==========")
                print(json.dumps(itinerary, indent=2))
                print("==========================\n")
                return {
                    "chat_response": chat_response,
                    "itinerary": full_itinerary,
                    "trip": itinerary
                }

        except Exception as e:
            import traceback
            traceback.print_exc()

            return {
                "success": False,
                "message": f"{type(e).__name__}: {e}"
            }
    def handle_followup(self, session_id, user_message):
        self.memory = self.session_manager.get_context(session_id)
        # Extract only the new preferences
        new_preferences = self.extractor.extract(user_message)

        # Merge them into memory
        self.memory.update_preferences(new_preferences)

        preferences = self.memory.get_preferences()

        place = self.search.find_place(
            preferences["destination"]
        )

        if place is None or place.empty:
            return {
                "success": False,
                "message": "Destination not found.",
                "response": None,
                "trip": None
            }   

        place_id = place.iloc[0]["place_id"]

        hotels = self.search.find_hotels(
            place_id,
            preferences.get("budget"),
            preferences.get("hotel_type")
        )

        attractions = self.search.find_attractions(
            place_id,
            preferences.get("excluded_categories"),
            preferences.get("preferred_categories")
        )


        changes = []

        if new_preferences.get("budget") is not None:
            changes.append("budget")        

        if new_preferences.get("hotel_type") is not None:
            changes.append("hotel")     

        if new_preferences.get("days") is not None:
            changes.append("days")      

        if new_preferences.get("preferred_categories"):
            changes.append("attractions")       

        if new_preferences.get("excluded_categories"):
            changes.append("attractions")

        print("\n===== CHANGES DETECTED =====")
        print(changes)
        print("============================\n")

        hotel = self.hotel_selector.select(
            hotels,
            preferences
        )

        selected_attractions = self.attraction_selector.select(
            attractions,
            preferences
        )

        itinerary = self.generator.generate(
            preferences,
            place,
            hotel,
            selected_attractions
        )
        old_trip = self.memory.get_trip()
        

        chat_response = self.llm.format_updated_trip(
            old_trip,
            itinerary,
            user_message
        )

        full_itinerary = self.llm.format_response(itinerary)
        self.memory.save_trip(itinerary)

        return {
            "chat_response": chat_response,
            "itinerary": full_itinerary,
            "trip": itinerary
        }
    
    def reset_session(self, session_id):

        self.session_manager.clear_context(session_id)

        return {
            "success": True,
            "message": "Session reset successfully."
        }