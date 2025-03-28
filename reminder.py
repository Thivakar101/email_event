import schedule
import time
import logging

logging.basicConfig(level=logging.INFO)

def schedule_reminder(event_name, date, event_time, venue):
    try:
        schedule.every().day.at(event_time).do(
            lambda: logging.info(f"Reminder: {event_name} at {venue} on {date} at {event_time}")
        )
        logging.info(f"Reminder scheduled for {event_name} at {event_time} on {date} in {venue}")
    except schedule.ScheduleValueError:
        logging.error(f"Invalid time format: {event_time}. Using default time 09:00 instead.")
        schedule.every().day.at("09:00").do(
            lambda: logging.info(f"Reminder: {event_name} at {venue} on {date} at 09:00")
        )
