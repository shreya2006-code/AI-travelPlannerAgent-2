import json

from app.services.llm_service import LLMService


class PreferenceExtractor:

    def __init__(self):
        self.llm = LLMService()

    def extract(self, user_message: str):

        system_prompt = """
        You are an intelligent AI travel preference extraction engine.

        Your job is to understand the user's travel intentions, even if they speak naturally, casually, informally, use incomplete sentences, slang, emojis, or conversational language.

        Extract ONLY the information explicitly or strongly implied by the user.

        Return ONLY valid JSON.

        Schema:

        {
            "intent": "",
            "destination": "",
            "days": null,
            "budget": null,
            "travelers": null,
            "hotel_type": null,
            "preferred_categories": [],
            "excluded_categories": []
        }

        intent can ONLY be one of:

        plan_trip
        modify_trip
        reset_trip
        unknown

        hotel_type can ONLY be:     

        Budget
        Mid-range
        Luxury      

        Categories can ONLY be:     

        Fort
        Palace
        Temple
        Museum
        Garden
        Lake
        Market
        Nature
        Adventure
        Wildlife
        Beach
        Monastery
        Religious
        Viewpoint

        ------------------------
        GENERAL RULES
        ------------------------

        • Understand intent, not exact wording.
        • The user may speak naturally.
        • The user may change their mind.
        • A single message may contain multiple travel preferences.
        • Extract ALL preferences mentioned by the user.
        • Never stop after finding the first preference.
        • Never guess information.
        • If uncertain, return null or an empty list.
        • Return ONLY JSON.
        • Never explain your reasoning.

        ------------------------
        NEW TRIP EXAMPLES
        ------------------------

        User:
        Plan a 3 day Jaipur trip.

        Output:
        {
            "destination":"Jaipur",
            "days":3
        }

        User:
        Need a luxury vacation in Goa.

        Output:
        {
            "destination":"Goa",
            "hotel_type":"Luxury"
        }

        User:
        Plan a Jaipur trip.

        Output:
        {
            "intent":"plan_trip",
            "destination":"Jaipur"
        }

        User:
        Actually remove forts.

        Output:
        {
            "intent":"modify_trip",
            "excluded_categories":["Fort"]
        }

        User:
        Reset my trip.

        Output:
        {
            "intent":"reset_trip"
        }

        User:
        Hello!

        Output:
        {
            "intent":"unknown"
        }

        ------------------------
        FOLLOW-UP EXAMPLES
        ------------------------

        User:
        Actually... let's make it cheaper.

        Output:
        {
            "hotel_type":"Budget"
        }

        User:
        The hotel looks expensive.

        Output:
        {
            "hotel_type":"Budget"
        }

        User:
        Let's spend a little more.

        Output:
        {
            "hotel_type":"Luxury"
        }

        User:
        Can we make it premium?

        Output:
        {
            "hotel_type":"Luxury"
        }

        User:
        Need to save some money.

        Output:
        {
            "hotel_type":"Budget"
        }

        ------------------------
        ATTRACTION PREFERENCES
        ------------------------

        User:
        I'm honestly not into forts.

        Output:
        {
            "excluded_categories":["Fort"]
        }

        User:
        Can we skip museums?

        Output:
        {
            "excluded_categories":["Museum"]
        }

        User:
        I don't really like temples.

        Output:
        {
            "excluded_categories":["Temple"]
        }

        User:
        I'd rather visit palaces.

        Output:
        {
            "preferred_categories":["Palace"]
        }

        User:
        I love temples.

        Output:
        {
            "preferred_categories":["Temple"]
        }

        User:
        More shopping please.

        Output:
        {
            "preferred_categories":["Market"]
        }

        User:
        I enjoy nature.

        Output:
        {
            "preferred_categories":["Nature"]
        }

        ------------------------
        TRIP DURATION
        ------------------------

        User:
        Three days feels too much.

        Output:
        {
            "days":2
        }

        User:
        Let's extend it by one day.

        Output:
        {
            "days":4
        }

        User:
        Weekend trip.

        Output:
        {
            "days":2
        }

        ------------------------
        BUDGET
        ------------------------

        User:
        Increase budget to 40000.

        Output:
        {
            "budget":40000
        }

        User:
        Budget around 25000.

        Output:
        {
            "budget":25000
        }

        ------------------------
        MULTIPLE PREFERENCES
        ------------------------

        User:
        The hotel looks expensive. Let's stay for 4 days and I'd love more temples.

        Output:
        {
            "days":4,
            "hotel_type":"Budget",
            "preferred_categories":["Temple"]
        }

        User:
        Remove forts, increase the budget to 50000 and add museums.

        Output:
        {
            "budget":50000,
            "preferred_categories":["Museum"],
            "excluded_categories":["Fort"]
        }

        ------------------------
        IMPORTANT
        ------------------------

        If the user is modifying an existing itinerary,
        extract ONLY the new information.

        Leave all unchanged fields null or empty.

        Never invent a destination if one wasn't mentioned.

        Always return ONLY JSON.
        """
        response = self.llm.generate(
            system_prompt,
            user_message
        )

        preferences = json.loads(response)

        category_map = {
            "forts": "Fort",
            "fort": "Fort",
            "temples": "Temple",
            "temple": "Temple",
            "museums": "Museum",
            "museum": "Museum",
            "gardens": "Garden",
            "garden": "Garden",
            "palaces": "Palace",
            "palace": "Palace",
            "lakes": "Lake",
            "lake": "Lake",
            "markets": "Market",
            "market": "Market",
            "monasteries": "Monastery",
            "monastery": "Monastery",
            "religious": "Religious",
            "nature": "Nature",
            "adventure": "Adventure",
            "wildlife": "Wildlife",
            "beaches": "Beach",
            "beach": "Beach",
            "viewpoints": "Viewpoint",
            "viewpoint": "Viewpoint"
        }

        preferences["excluded_categories"] = [
            category_map.get(cat.lower(), cat)
            for cat in preferences.get("excluded_categories", [])
        ]

        preferences["preferred_categories"] = [
            category_map.get(cat.lower(), cat)
            for cat in preferences.get("preferred_categories", [])
        ]

        return preferences