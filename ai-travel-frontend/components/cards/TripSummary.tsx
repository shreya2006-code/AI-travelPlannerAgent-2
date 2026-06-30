import { useTrip } from "@/context/TripContext";
import { exportItineraryPDF } from "@/lib/exportPDF";

type Trip = {
  destination?: {
    place_name: string;
  };

  hotel?: {
    hotel_name: string;
  };

  budget?: {
    total: number;
  };

  days?: number;

  itinerary?: {
    [day: string]: {
      attraction_name: string;
      category: string;
      time_required: string;
      entry_fee: number;
    }[];
  };
};

export default function TripSummary() {
  const { trip } = useTrip();

  return (
    <div id="itinerary-pdf" className="p-4 space-y-4">

      <div className="mb-4 flex items-center justify-between">
        <h2 className="text-xl font-semibold">
          📌 Trip Summary
        </h2>

        <button
          id="export-btn"
          onClick={() => exportItineraryPDF("itinerary-pdf")}
          className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-blue-700"
        >
          📄 Export PDF
        </button>
      </div>

      {/* Four Summary Cards */}
      <div className="grid grid-cols-2 gap-3">

        {/* Destination */}
        <div className="rounded-xl bg-zinc-900 p-3">
          <p className="text-xs text-zinc-400">Destination</p>
          <p className="font-medium">{trip?.destination?.place_name ?? "—"}</p>
        </div>

        {/* Hotel */}
        <div className="rounded-xl bg-zinc-900 p-3">
          <p className="text-xs text-zinc-400">Hotel</p>
          <p className="font-medium">{trip?.hotel?.hotel_name ?? "—"}</p>
        </div>

        {/* Budget */}
        <div className="rounded-xl bg-zinc-900 p-3">
          <p className="text-xs text-zinc-400">Budget</p>
          <p className="font-medium">
            {trip?.budget?.total != null ? `₹${trip.budget.total}` : "—"}
          </p>
        </div>

        {/* Duration */}
        <div className="rounded-xl bg-zinc-900 p-3">
          <p className="text-xs text-zinc-400">Duration</p>
          <p className="font-medium">
            {trip?.days != null ? `${trip.days} days` : "—"}
          </p>
        </div>

      </div>

      {/* Itinerary Section — dynamic, all days */}
      <div className="mt-8 space-y-6">
        {trip?.itinerary &&
          Object.entries(trip.itinerary).map(([day, places]) => (
            <div key={day}>
              <h3 className="mb-3 text-lg font-semibold">
                📅 {day}
              </h3>

              <div className="space-y-3">
                {places.map((place, index) => (
                  <div
                    key={index}
                    className="rounded-xl border border-zinc-800 bg-zinc-900 p-4"
                  >
                    <h4 className="font-semibold text-white">
                      {place.attraction_name}
                    </h4>

                    <p className="mt-1 text-sm text-zinc-400">
                      {place.category}
                    </p>

                    <div className="mt-2 flex justify-between text-xs text-zinc-500">
                      <span>⏱ {place.time_required}</span>
                      <span>
                        🎟 ₹{place.entry_fee === 0 ? "Free" : place.entry_fee}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}
      </div>

    </div>
  );
}