"""
Hevy API Client
"""

import requests
import logging
from typing import Optional, Dict, Any
import json
from .models import *

logger = logging.getLogger(__name__)


class HevyAPIError(Exception):
    """Base exception for Hevy API errors"""
    pass


class HevyClient:
    """Client for interacting with the Hevy API"""

    BASE_URL = "https://api.hevyapp.com"

    def __init__(self, api_key: str):
        """
        Initialize the Hevy client.

        Args:
            api_key: Your Hevy API key (UUID format)
        """
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "api-key": api_key,
            "Content-Type": "application/json"
        })

        # Set up logging
        self.logger = logging.getLogger(__name__)

    def _make_request(self, method: str, endpoint: str,
                     data: Optional[Dict[str, Any]] = None,
                     params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a request to the Hevy API"""
        url = f"{self.BASE_URL}{endpoint}"

        logger.debug(f"Making {method} request to {url}")
        if data:
            logger.debug(f"Request data: {data}")
        if params:
            logger.debug(f"Request params: {params}")

        try:
            response = self.session.request(method, url, json=data, params=params)
            response.raise_for_status()
            result = response.json()
            logger.debug(f"Response: {result}")
            return result
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP Error {e.response.status_code}: {e.response.text}")
            try:
                error_data = e.response.json()
                raise HevyAPIError(f"API Error: {error_data.get('error', str(e))}")
            except json.JSONDecodeError:
                raise HevyAPIError(f"HTTP Error: {e}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Request Error: {e}")
            raise HevyAPIError(f"Request Error: {e}")

    # Workouts endpoints
    def get_workouts(self, page: int = 1, page_size: int = 5) -> PaginatedWorkouts:
        """Get a paginated list of workouts"""
        params = {"page": page, "pageSize": page_size}
        response = self._make_request("GET", "/v1/workouts", params=params)
        return PaginatedWorkouts(**response)

    def get_workout_count(self) -> WorkoutCount:
        """Get the total number of workouts"""
        response = self._make_request("GET", "/v1/workouts/count")
        return WorkoutCount(**response)

    def get_workout(self, workout_id: str) -> Workout:
        """Get a single workout by ID"""
        response = self._make_request("GET", f"/v1/workouts/{workout_id}")
        return Workout(**response)

    def create_workout(self, workout_data: PostWorkoutsRequestBody) -> Workout:
        """Create a new workout"""
        data = workout_data.dict()
        response = self._make_request("POST", "/v1/workouts", data=data)
        return Workout(**response)

    def update_workout(self, workout_id: str, workout_data: PostWorkoutsRequestBody) -> Workout:
        """Update an existing workout"""
        data = workout_data.dict()
        response = self._make_request("PUT", f"/v1/workouts/{workout_id}", data=data)
        return Workout(**response)

    def get_workout_events(self, page: int = 1, page_size: int = 5, since: str = "1970-01-01T00:00:00Z") -> PaginatedWorkoutEvents:
        """Get workout events since a given date"""
        params = {"page": page, "pageSize": page_size, "since": since}
        response = self._make_request("GET", "/v1/workouts/events", params=params)
        return PaginatedWorkoutEvents(**response)

    # Routines endpoints
    def get_routines(self, page: int = 1, page_size: int = 5) -> PaginatedRoutines:
        """Get a paginated list of routines"""
        params = {"page": page, "pageSize": page_size}
        response = self._make_request("GET", "/v1/routines", params=params)
        return PaginatedRoutines(**response)

    def get_routine(self, routine_id: str) -> dict:
        """Get a single routine by ID"""
        response = self._make_request("GET", f"/v1/routines/{routine_id}")
        return response  # Returns {"routine": Routine}

    def create_routine(self, routine_data: PostRoutinesRequestBody) -> Routine:
        """Create a new routine"""
        data = routine_data.dict()
        response = self._make_request("POST", "/v1/routines", data=data)
        return Routine(**response)

    def update_routine(self, routine_id: str, routine_data: PutRoutinesRequestBody) -> Routine:
        """Update an existing routine"""
        data = routine_data.dict()
        response = self._make_request("PUT", f"/v1/routines/{routine_id}", data=data)
        return Routine(**response)

    # Exercise Templates endpoints
    def get_exercise_templates(self, page: int = 1, page_size: int = 5) -> PaginatedExerciseTemplates:
        """Get a paginated list of exercise templates"""
        params = {"page": page, "pageSize": page_size}
        response = self._make_request("GET", "/v1/exercise_templates", params=params)
        return PaginatedExerciseTemplates(**response)

    def get_exercise_template(self, exercise_template_id: str) -> ExerciseTemplate:
        """Get a single exercise template by ID"""
        response = self._make_request("GET", f"/v1/exercise_templates/{exercise_template_id}")
        return ExerciseTemplate(**response)

    def create_custom_exercise_template(self, exercise_data: CreateCustomExerciseRequestBody) -> dict:
        """Create a new custom exercise template"""
        data = exercise_data.dict()
        response = self._make_request("POST", "/v1/exercise_templates", data=data)
        return response  # Returns {"id": int}

    # Routine Folders endpoints
    def get_routine_folders(self, page: int = 1, page_size: int = 5) -> PaginatedRoutineFolders:
        """Get a paginated list of routine folders"""
        params = {"page": page, "pageSize": page_size}
        response = self._make_request("GET", "/v1/routine_folders", params=params)
        return PaginatedRoutineFolders(**response)

    def get_routine_folder(self, folder_id: int) -> RoutineFolder:
        """Get a single routine folder by ID"""
        response = self._make_request("GET", f"/v1/routine_folders/{folder_id}")
        return RoutineFolder(**response)

    def create_routine_folder(self, folder_data: PostRoutineFolderRequestBody) -> RoutineFolder:
        """Create a new routine folder"""
        data = folder_data.dict()
        response = self._make_request("POST", "/v1/routine_folders", data=data)
        return RoutineFolder(**response)

    # Webhook endpoints
    def create_webhook_subscription(self, webhook_data: WebhookRequestBody) -> None:
        """Create a webhook subscription"""
        data = webhook_data.dict()
        self._make_request("POST", "/v1/webhook-subscription", data=data)

    def get_webhook_subscription(self) -> WebhookSubscription:
        """Get the current webhook subscription"""
        response = self._make_request("GET", "/v1/webhook-subscription")
        return WebhookSubscription(**response)

    def delete_webhook_subscription(self) -> None:
        """Delete the webhook subscription"""
        self._make_request("DELETE", "/v1/webhook-subscription")

    # Exercise History endpoint
    def get_exercise_history(self, exercise_template_id: str,
                           start_date: Optional[str] = None,
                           end_date: Optional[str] = None) -> dict:
        """Get exercise history for a specific exercise template"""
        params = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date

        response = self._make_request("GET", f"/v1/exercise_history/{exercise_template_id}", params=params)
        return response  # Returns {"exercise_history": List[ExerciseHistoryEntry]}