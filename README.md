# Hevy Py

A complete Python SDK for the Hevy API.

A complete Python SDK for the Hevy API (https://api.hevyapp.com/docs/).

## Features

- Complete coverage of all Hevy API endpoints
- Type-safe data models using Pydantic
- Comprehensive error handling and logging
- Easy to use Pythonic interface
- Supports all workout, routine, exercise template, and webhook operations

## Installation

```bash
pip install hevy-py
```

Or install from source:

```bash
git clone https://github.com/your-repo/hevy-py.git
cd hevy-py
pip install .
```

## Quick Start

```python
from hevy_py import HevyClient

# Initialize client with your API key
client = HevyClient("your-api-key-here")

# Get your workouts
workouts = client.get_workouts(page=1, page_size=10)
for workout in workouts.workouts:
    print(f"Workout: {workout.title}")

# Get workout count
count = client.get_workout_count()
print(f"Total workouts: {count.workout_count}")

# Get routines
routines = client.get_routines(page=1, page_size=5)
for routine in routines.routines:
    print(f"Routine: {routine.title}")
```

## Authentication

You need a Hevy Pro account to use the API. Get your API key from https://hevy.com/settings?developer.

Set your API key as an environment variable:

```bash
export HEVY_API_KEY="your-api-key-here"
```

Then use it in your code:

```python
import os
client = HevyClient(os.getenv("HEVY_API_KEY"))
```

## API Reference

### Workouts

#### List Workouts
```python
workouts = client.get_workouts(page=1, page_size=5)
```

#### Get Single Workout
```python
workout = client.get_workout("workout-id")
```

#### Create Workout
```python
from hevy_py.models import PostWorkoutsRequestBody

workout_data = PostWorkoutsRequestBody(...)
new_workout = client.create_workout(workout_data)
```

#### Update Workout
```python
updated_workout = client.update_workout("workout-id", workout_data)
```

#### Get Workout Count
```python
count = client.get_workout_count()
```

#### Get Workout Events
```python
events = client.get_workout_events(page=1, page_size=5, since="2024-01-01T00:00:00Z")
```

### Routines

#### List Routines
```python
routines = client.get_routines(page=1, page_size=5)
```

#### Get Single Routine
```python
routine = client.get_routine("routine-id")
```

#### Create Routine
```python
from hevy_py.models import PostRoutinesRequestBody, PutRoutinesRequestBody

routine_data = PostRoutinesRequestBody(...)
new_routine = client.create_routine(routine_data)
```

#### Update Routine
```python
updated_routine = client.update_routine("routine-id", routine_data)
```

### Exercise Templates

#### List Exercise Templates
```python
templates = client.get_exercise_templates(page=1, page_size=10)
```

#### Get Single Exercise Template
```python
template = client.get_exercise_template("template-id")
```

#### Create Custom Exercise Template
```python
from hevy_sdk.models import CreateCustomExerciseRequestBody

exercise_data = CreateCustomExerciseRequestBody(...)
response = client.create_custom_exercise_template(exercise_data)
```

### Routine Folders

#### List Routine Folders
```python
folders = client.get_routine_folders(page=1, page_size=5)
```

#### Get Single Routine Folder
```python
folder = client.get_routine_folder(123)
```

#### Create Routine Folder
```python
from hevy_sdk.models import PostRoutineFolderRequestBody

folder_data = PostRoutineFolderRequestBody(...)
new_folder = client.create_routine_folder(folder_data)
```

### Webhooks

#### Create Webhook Subscription
```python
from hevy_py.models import WebhookRequestBody

webhook_data = WebhookRequestBody(authToken="Bearer myauthtoken", url="https://mywebhook.com/notify")
client.create_webhook_subscription(webhook_data)
```

#### Get Webhook Subscription
```python
subscription = client.get_webhook_subscription()
```

#### Delete Webhook Subscription
```python
client.delete_webhook_subscription()
```

#### Handle Webhook Notifications
```python
from hevy_py import HevyWebhookHandler

# Create webhook handler
handler = HevyWebhookHandler()

def handle_notification(notification):
    print(f"New workout created: {notification.workout_id}")
    # Process the workout...

handler.register_callback(handle_notification)

# Run the webhook server (in production, run in separate thread/process)
handler.run(host='0.0.0.0', port=5000, debug=True)
```

When a new workout is created, Hevy will send a POST request to your webhook URL with this JSON payload:
```json
{
  "id": "00000000-0000-0000-0000-000000000001",
  "payload": {
    "workoutId": "f1085cdb-32b2-4003-967d-53a3af8eaecb"
  }
}
```

### Exercise History

#### Get Exercise History
```python
history = client.get_exercise_history("exercise-template-id", start_date="2024-01-01T00:00:00Z")
```

## Error Handling

The SDK raises `HevyAPIError` for API-related errors:

```python
from hevy_sdk import HevyClient, HevyAPIError

try:
    workouts = client.get_workouts()
except HevyAPIError as e:
    print(f"API Error: {e}")
```

## Logging

The SDK uses Python's logging module. Enable debug logging to see request/response details:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Data Models

All API responses are parsed into Pydantic models for type safety. See `hevy_sdk.models` for the complete list of models.

## Examples

See `example.py` for a comprehensive example demonstrating all SDK features.

## License

This project is not affiliated with Hevy. Use at your own risk as per the Hevy API terms.

## Contributing

Contributions are welcome! Please open issues or submit pull requests.