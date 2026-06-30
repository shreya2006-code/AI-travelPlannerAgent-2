class ItineraryGenerator:

    def extract_price(self, price_range):

        if not price_range:
            return 0

        price_range = (
            str(price_range)
            .replace("₹", "")
            .replace(",", "")
        )

        if "–" in price_range:
            low, high = price_range.split("–")
        elif "-" in price_range:
            low, high = price_range.split("-")
        else:
            return int(price_range)

        return (int(low) + int(high)) // 2


    def calculate_budget(
        self,
        hotel,
        attractions,
        days
    ):

        hotel_cost = self.extract_price(
            hotel.get("price_per_night", 0)
        ) * days

        entry_fee = 0

        for attraction in attractions:

            fee = str(
                attraction.get("entry_fee", "0")
            ).replace("₹", "").replace(",", "")

            try:
                entry_fee += int(fee)
            except:
                pass

        hotel_type = hotel.get(
            "hotel_type",
            "Mid-range"
        )

        if hotel_type == "Budget":
            food_per_day = 700
        elif hotel_type == "Luxury":
            food_per_day = 2500
        else:
            food_per_day = 1200

        food = food_per_day * days

        transport = 600 * days

        subtotal = (
            hotel_cost
            + entry_fee
            + food
            + transport
        )

        miscellaneous = int(subtotal * 0.10)

        total = subtotal + miscellaneous

        return {
            "hotel": hotel_cost,
            "food": food,
            "transport": transport,
            "entry_fee": entry_fee,
            "miscellaneous": miscellaneous,
            "total": total
        }
    def generate(
        self,
        preferences,
        place,
        hotel,
        attractions,
        previous_trip=None,
        modification=False
    ):

        days = preferences.get("days") or 3

        itinerary = {}

        index = 0

        per_day = max(
            1,
            len(attractions) // days
        )

        for day in range(1, days + 1):

            itinerary[f"Day {day}"] = []

            for _ in range(per_day):

                if index < len(attractions):

                    itinerary[f"Day {day}"].append(
                        attractions[index]
                    )

                    index += 1

        budget = self.calculate_budget(
            hotel,
            attractions,
            days
        )

        return {

            "destination": place.iloc[0].to_dict(),

            "hotel": hotel,

            "days": days,

            "estimated_budget": budget["total"],

            "budget": budget,

            "itinerary": itinerary

        }