import sqlite3
import os
from datetime import datetime


class Database:

    def __init__(self, db_path="data/events.db"):

        os.makedirs(
            os.path.dirname(db_path),
            exist_ok=True
        )

        self.db_path = db_path

        self.connection = sqlite3.connect(
            self.db_path,
            check_same_thread=False
        )

        self.create_tables()

    def create_tables(self):

        cursor = self.connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS events (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                person_id INTEGER,

                start_time TEXT,

                confirmed_time TEXT,

                end_time TEXT,

                duration REAL,

                recording_path TEXT,

                person_name TEXT DEFAULT 'Unknown',

                suspicious INTEGER DEFAULT 0,

                suspicion_reason TEXT,

                summary TEXT
            )
        """)

        self.connection.commit()

    def create_event(
        self,
        person_id,
        start_time,
        confirmed_time
    ):

        cursor = self.connection.cursor()

        cursor.execute("""
            INSERT INTO events (
                person_id,
                start_time,
                confirmed_time
            )

            VALUES (?, ?, ?)
        """, (
            person_id,
            start_time,
            confirmed_time
        ))

        self.connection.commit()

        return cursor.lastrowid

    def finish_event(
        self,
        event_id,
        end_time,
        duration,
        recording_path
    ):

        cursor = self.connection.cursor()

        cursor.execute("""
            UPDATE events

            SET
                end_time = ?,
                duration = ?,
                recording_path = ?

            WHERE id = ?
        """, (
            end_time,
            duration,
            recording_path,
            event_id
        ))

        self.connection.commit()

    def update_person_name(
        self,
        event_id,
        person_name
    ):

        cursor = self.connection.cursor()

        cursor.execute("""
            UPDATE events

            SET person_name = ?

            WHERE id = ?
        """, (
            person_name,
            event_id
        ))

        self.connection.commit()

    def mark_suspicious(
        self,
        event_id,
        reason
    ):

        cursor = self.connection.cursor()

        cursor.execute("""
            UPDATE events

            SET
                suspicious = 1,
                suspicion_reason = ?

            WHERE id = ?
        """, (
            reason,
            event_id
        ))

        self.connection.commit()

    def add_summary(
        self,
        event_id,
        summary
    ):

        cursor = self.connection.cursor()

        cursor.execute("""
            UPDATE events

            SET summary = ?

            WHERE id = ?
        """, (
            summary,
            event_id
        ))

        self.connection.commit()

    def get_events(self):

        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT *
            FROM events
            ORDER BY id DESC
        """)

        return cursor.fetchall()

    def close(self):

        self.connection.close()