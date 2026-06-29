import TravelPlannerLayout from "@/components/layout/TravelPlannerLayout";
import { TripProvider } from "@/context/TripContext";

export default function Home() {
  return (
    <TripProvider>
      <TravelPlannerLayout />
    </TripProvider>
  );
}