import time


class VisitorManager:

    def __init__(self, stay_time=15, exit_grace=3):
        self.stay_time = stay_time
        self.exit_grace = exit_grace

        self.visitors = {}

    def update(self, detected_persons):

        now = time.monotonic()

        events = []
        current_ids = set()

        # Process currently detected people
        for person in detected_persons:

            person_id = person["id"]
            current_ids.add(person_id)

            # New tracked person
            if person_id not in self.visitors:

                self.visitors[person_id] = {
                    "first_seen": now,
                    "last_seen": now,
                    "confirmed": False
                }

            visitor = self.visitors[person_id]

            # Person is visible right now
            visitor["last_seen"] = now

            # Calculate how long this person has been visible
            elapsed = now - visitor["first_seen"]

            # Confirm after 15 seconds
            if not visitor["confirmed"] and elapsed >= self.stay_time:

                visitor["confirmed"] = True

                events.append({
                    "type": "visitor_confirmed",
                    "person_id": person_id
                })

        # Handle people temporarily disappearing
        for person_id in list(self.visitors.keys()):

            if person_id not in current_ids:

                visitor = self.visitors[person_id]

                missing_time = now - visitor["last_seen"]

                # Don't immediately delete the person.
                # ByteTrack can temporarily lose a detection.
                if missing_time >= self.exit_grace:

                    events.append({
                        "type": "visitor_left",
                        "person_id": person_id
                    })

                    del self.visitors[person_id]

        return events