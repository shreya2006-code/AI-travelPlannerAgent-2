import json
import os

from dotenv import load_dotenv
from groq import Groq
from app.config import Config

load_dotenv()


class LLMService:
    """
    Handles all communication with the Groq LLM.
    """

    def __init__(self):
        
        self.client = Groq(
            api_key=Config.GROQ_API_KEY
        )

        self.model = Config.MODEL_NAME

    def generate(self, system_prompt: str, user_prompt: str):
        try:

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )

            return response.choices[0].message.content

        except Exception as e:

            raise Exception(f"LLM Error: {str(e)}")

        return response.choices[0].message.content
    
    def format_response(self, itinerary):

        previous_context = ""

        # if modification and previous_trip:

        #     previous_context = f"""
        # Previous itinerary:

        # {previous_trip}

        # Modify this itinerary instead of creating a new one.

        # Keep everything else unchanged unless the user requested it.
        # """

        system_prompt = """
       You are an experienced travel consultant and itinerary formatter.

        Your goal is to make the itinerary feel warm, premium and conversational while staying completely faithful to the structured trip data.

        The traveller should feel like they are chatting with a knowledgeable travel expert, not reading a generated report.

        Your ONLY job is to convert the provided structured trip JSON into a beautiful, readable itinerary.

        STRICT RULES:

        1. Use ONLY the destination, hotel and attractions present in the input.
        2. NEVER invent attractions.
        3. NEVER invent hotels.
        4. NEVER invent restaurants.
        5. NEVER invent lakes, stations, viewpoints or markets.
        6. NEVER replace attractions with better-known places.
        7. NEVER add extra sightseeing locations.
        8. If an attraction is not present in the JSON, DO NOT mention it.
        9. Keep the same hotel.
        10. Keep the same destination.
        11. Use every attraction exactly once.
        12. Do not repeat attractions.
        13. Mention approximate duration and entry fee if available.
        14. Format the itinerary nicely using headings and bullet points.
        15. At the end, include the budget breakdown exactly as provided.

        You are ONLY formatting the provided itinerary.

        Never invent information.

        Never modify hotels.

        Never modify attractions.

        Never change timings.

        Never change the destination.

        Make the response warm, conversational and premium while remaining completely faithful to the provided data.

        End with one friendly sentence inviting the traveller to ask for modifications such as changing the budget, hotel, pace, attractions or trip duration.
        """

        return self.generate(
        system_prompt,
        json.dumps(
            itinerary,
            indent=2
        )
        )
    def format_updated_trip(
        self,
        current_trip,
        updated_trip,
        user_request
    ):

        system_prompt = f"""
        You are an experienced AI travel consultant.

        The traveller already has a trip planned and has requested a modification.

        Your job is NOT to create a new itinerary.

        Instead:

        1. Briefly acknowledge the user's request in a natural, friendly way.
        2. Clearly explain what changed.
        3. Mention what stayed the same (hotel, destination, duration etc.) whenever applicable.
        4. Present the updated itinerary in a clean format.
        5. Use ONLY the information present in the updated trip JSON.
        6. Never invent attractions, hotels or destinations.
        7. Never repeat attractions.
        8. Never add additional sightseeing places.
        9. Keep the response conversational and helpful, like a real travel consultant.

        Examples of tone:

        "Great idea! I've removed the forts while keeping the rest of your Jaipur trip unchanged."

        "Done! I've switched your hotel to a more budget-friendly option while preserving the sightseeing plan."

        "Absolutely! I've added more temple visits and kept the overall pace of the trip similar."

        Updated Trip JSON:

        {json.dumps(updated_trip, indent=2)}
        """

        return self.generate(
            system_prompt,
            user_request
        )

    def chat(self, system_prompt, user_prompt):
        return self.generate(system_prompt, user_prompt)
    

    def generate_chat_response(self, trip):
        system_prompt = """
    You are a friendly AI travel planner.

    The frontend already displays the complete itinerary separately.

    Your ONLY job is to reply naturally like a real travel assistant.

    Keep the reply SHORT.

    2-4 sentences maximum.

    Mention:
    - destination
    - duration
    - budget (if available)

    Do NOT repeat the itinerary.

    Do NOT list attractions.

    Invite the user to continue the conversation.

    Example:

    "Great choice! 🌴

    I've planned a 3-day trip to Goa within your budget.

    Your itinerary, hotel and budget have been updated.

    If you'd like to change the hotel, budget, attractions or trip duration, just let me know!"
    """

        return self.generate(
            system_prompt,
            json.dumps(trip, indent=2)
        )