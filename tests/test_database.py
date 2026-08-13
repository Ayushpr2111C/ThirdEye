from app.database.database import Database


db = Database()

event_id = db.create_event(
    person_id=1,
    start_time="2026-08-12 00:40:00",
    confirmed_time="2026-08-12 00:40:15"
)

print("Created event:", event_id)

db.finish_event(
    event_id=event_id,
    end_time="2026-08-12 00:41:10",
    duration=70,
    recording_path="data/recordings/test.mp4"
)

db.update_person_name(
    event_id=event_id,
    person_name="Unknown"
)

print("\nEvents:")

for event in db.get_events():
    print(event)

db.close()