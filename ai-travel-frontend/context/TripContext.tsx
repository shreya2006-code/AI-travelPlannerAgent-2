"use client";

import { createContext, useContext, useState } from "react";

type TripContextType = {
  trip: any;
  setTrip: (trip: any) => void;
  clearTrip: () => void;
};

const TripContext = createContext<TripContextType | null>(null);

export function TripProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  const [trip, setTrip] = useState(null);

  return (
    <TripContext.Provider
        value={{
        trip,
        setTrip,
        clearTrip: () => setTrip(null),
    }}
    >
      {children}
    </TripContext.Provider>
  );
}

export function useTrip() {
  const context = useContext(TripContext);

  if (!context) {
    throw new Error("useTrip must be used inside TripProvider");
  }

  return context;
}