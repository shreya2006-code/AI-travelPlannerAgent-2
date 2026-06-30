AI Travel Planner Flow

1. Receive user message.

2. Determine whether:
   - New trip request
   - Follow-up modification
   - General travel question

3. If it is a new trip:
   - Extract user preferences
   - Search Places dataset
   - Search Hotels dataset
   - Search Attractions dataset
   - Generate itinerary
   - Save Trip Context

4. If it is a follow-up:
   - Load Trip Context
   - Update user preferences
   - Regenerate itinerary
   - Save updated Trip Context

5. Return the response in conversational chat format.