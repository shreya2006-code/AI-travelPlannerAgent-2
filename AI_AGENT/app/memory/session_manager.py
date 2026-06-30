from app.memory.trip_context import TripContext


class SessionManager:

    def __init__(self):

        self.sessions = {}

    def get_context(self, session_id):

        if session_id not in self.sessions:

            self.sessions[session_id] = TripContext()

        return self.sessions[session_id]

    def clear_context(self, session_id):

        if session_id in self.sessions:

            del self.sessions[session_id]