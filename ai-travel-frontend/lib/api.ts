const API_URL = "http://127.0.0.1:8000/chat";

const SESSION_ID = "user123";

export async function sendMessage(message: string) {
  const response = await fetch(API_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      session_id: SESSION_ID,
      message,
    }),
  });

  if (!response.ok) {
    throw new Error("Failed to connect to backend.");
  }

  return response.json();
}