import time
from datetime import datetime


class VisitorManager:

    def __init__(self, stay_time=15, exit_grace=3):
        self.stay_time = stay_time
        self.exit_grace = exit_grace

        self.visitors = {}

    def update(self, detected_persons):

        now = time.monotonic()
        events = []
        current_ids = set()

        for person in detected_persons:

            person_id = person["id"]
            current_ids.add(person_id)

            # New person
            if person_id not in self.visitors:

                self.visitors[person_id] = {
                    "first_seen": now,
                    "first_seen_time": datetime.now().isoformat(
                        timespec="seconds"
                    ),
                    "last_seen": now,
                    "confirmed": False
                }

            visitor = self.visitors[person_id]

            visitor["last_seen"] = now

            elapsed = now - visitor["first_seen"]

            # Person has stayed for 15 seconds
            if (
                not visitor["confirmed"]
                and elapsed >= self.stay_time
            ):

                visitor["confirmed"] = True

                events.append({
                    "type": "visitor_confirmed",
                    "person_id": person_id,
                    "first_seen_time": visitor["first_seen_time"]
                })

        # Check people who disappeared
        for person_id in list(self.visitors.keys()):

            visitor = self.visitors[person_id]

            if person_id not in current_ids:

                missing_time = now - visitor["last_seen"]

                if missing_time >= self.exit_grace:

                    events.append({
                        "type": "visitor_left",
                        "person_id": person_id
                    })

                    del self.visitors[person_id]

        return events