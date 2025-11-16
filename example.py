#!/usr/bin/env python3
"""
Example usage of the Hevy SDK
"""

import logging
import os
from hevy_py import HevyClient
from hevy_py.models import *

# Set up logging
logging.basicConfig(level=logging.INFO)

# Initialize client with API key from environment variable
API_KEY = os.getenv("HEVY_API_KEY")
if not API_KEY:
    print("Please set your HEVY_API_KEY environment variable")
    exit(1)

client = HevyClient(API_KEY)

def list_workouts_example():
    """Example: List workouts"""
    print("Listing workouts...")
    try:
        workouts = client.get_workouts(page=1, page_size=5)
        print(f"Found {len(workouts.workouts)} workouts")
        for workout in workouts.workouts:
            print(f"- {workout.title} ({workout.id})")
    except Exception as e:
        print(f"Error: {e}")

def get_workout_count_example():
    """Example: Get workout count"""
    print("\nGetting workout count...")
    try:
        count = client.get_workout_count()
        print(f"Total workouts: {count.workout_count}")
    except Exception as e:
        print(f"Error: {e}")

def get_single_workout_example():
    """Example: Get a single workout"""
    print("\nGetting first workout...")
    try:
        workouts = client.get_workouts(page=1, page_size=1)
        if workouts.workouts:
            workout_id = workouts.workouts[0].id
            workout = client.get_workout(workout_id)
            print(f"Workout: {workout.title}")
            print(f"Exercises: {len(workout.exercises)}")
        else:
            print("No workouts found")
    except Exception as e:
        print(f"Error: {e}")

def list_routines_example():
    """Example: List routines"""
    print("\nListing routines...")
    try:
        routines = client.get_routines(page=1, page_size=5)
        print(f"Found {len(routines.routines)} routines")
        for routine in routines.routines:
            print(f"- {routine.title} ({routine.id})")
    except Exception as e:
        print(f"Error: {e}")

def list_exercise_templates_example():
    """Example: List exercise templates"""
    print("\nListing exercise templates...")
    try:
        templates = client.get_exercise_templates(page=1, page_size=10)
        print(f"Found {len(templates.exercise_templates)} exercise templates")
        for template in templates.exercise_templates:
            print(f"- {template.title} ({template.id}) - {template.primary_muscle_group}")
    except Exception as e:
        print(f"Error: {e}")

def list_routine_folders_example():
    """Example: List routine folders"""
    print("\nListing routine folders...")
    try:
        folders = client.get_routine_folders(page=1, page_size=5)
        print(f"Found {len(folders.routine_folders)} routine folders")
        for folder in folders.routine_folders:
            print(f"- {folder.title} ({folder.id})")
    except Exception as e:
        print(f"Error: {e}")

def get_exercise_history_example():
    """Example: Get exercise history"""
    print("\nGetting exercise history...")
    try:
        # First get an exercise template
        templates = client.get_exercise_templates(page=1, page_size=1)
        if templates.exercise_templates:
            template_id = templates.exercise_templates[0].id
            history = client.get_exercise_history(template_id)
            print(f"Found {len(history['exercise_history'])} history entries")
        else:
            print("No exercise templates found")
    except Exception as e:
        print(f"Error: {e}")

def webhook_example():
    """Example: Set up webhook subscription and handler"""
    print("\nSetting up webhook subscription...")
    try:
        from hevy_py import HevyWebhookHandler
        from hevy_sdk.models import WebhookRequestBody

        # Set up webhook subscription
        webhook_data = WebhookRequestBody(
            authToken="Bearer myauthtoken",
            url="https://mywebhook.com/notify"
        )
        client.create_webhook_subscription(webhook_data)
        print("Webhook subscription created")

        # Create webhook handler
        handler = HevyWebhookHandler()

        def handle_notification(notification):
            print(f"Received workout notification: {notification.workout_id}")
            # Here you could process the new workout
            try:
                workout = client.get_workout(notification.workout_id)
                print(f"New workout: {workout.title}")
            except Exception as e:
                print(f"Error fetching workout: {e}")

        handler.register_callback(handle_notification)

        # Note: In a real application, you would run this in a separate thread/process
        # handler.run(host='0.0.0.0', port=5000, debug=True)
        print("Webhook handler ready (not started in example)")

    except Exception as e:
        print(f"Error setting up webhook: {e}")

if __name__ == "__main__":
    print("Hevy SDK Example")
    print("=" * 50)

    list_workouts_example()
    get_workout_count_example()
    get_single_workout_example()
    list_routines_example()
    list_exercise_templates_example()
    list_routine_folders_example()
    get_exercise_history_example()
    webhook_example()

    print("\nExample completed!")