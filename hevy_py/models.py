"""
Data models for Hevy API using Pydantic.
"""

from typing import Optional, List, Union
from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum


class CustomExerciseType(str, Enum):
    WEIGHT_REPS = "weight_reps"
    REPS_ONLY = "reps_only"
    BODYWEIGHT_REPS = "bodyweight_reps"
    BODYWEIGHT_ASSISTED_REPS = "bodyweight_assisted_reps"
    DURATION = "duration"
    WEIGHT_DURATION = "weight_duration"
    DISTANCE_DURATION = "distance_duration"
    SHORT_DISTANCE_WEIGHT = "short_distance_weight"


class MuscleGroup(str, Enum):
    ABDOMINALS = "abdominals"
    SHOULDERS = "shoulders"
    BICEPS = "biceps"
    TRICEPS = "triceps"
    FOREARMS = "forearms"
    QUADRICEPS = "quadriceps"
    HAMSTRINGS = "hamstrings"
    CALVES = "calves"
    GLUTES = "glutes"
    ABDUCTORS = "abductors"
    ADDUCTORS = "adductors"
    LATS = "lats"
    UPPER_BACK = "upper_back"
    TRAPS = "traps"
    LOWER_BACK = "lower_back"
    CHEST = "chest"
    CARDIO = "cardio"
    NECK = "neck"
    FULL_BODY = "full_body"
    OTHER = "other"


class EquipmentCategory(str, Enum):
    NONE = "none"
    BARBELL = "barbell"
    DUMBBELL = "dumbbell"
    KETTLEBELL = "kettlebell"
    MACHINE = "machine"
    PLATE = "plate"
    RESISTANCE_BAND = "resistance_band"
    SUSPENSION = "suspension"
    OTHER = "other"


class SetType(str, Enum):
    WARMUP = "warmup"
    NORMAL = "normal"
    FAILURE = "failure"
    DROPSET = "dropset"


class RPE(float, Enum):
    SIX = 6.0
    SIX_FIVE = 6.5
    SEVEN = 7.0
    SEVEN_FIVE = 7.5
    EIGHT = 8.0
    EIGHT_FIVE = 8.5
    NINE = 9.0
    NINE_FIVE = 9.5
    TEN = 10.0


# Base set models
class BaseSet(BaseModel):
    type: SetType = Field(..., example="normal")
    weight_kg: Optional[float] = Field(None, example=100.0)
    reps: Optional[int] = Field(None, example=10)
    distance_meters: Optional[int] = Field(None, example=None)
    duration_seconds: Optional[int] = Field(None, example=None)
    custom_metric: Optional[float] = Field(None, example=None)
    rpe: Optional[RPE] = Field(None, example=None)


class PostWorkoutsRequestSet(BaseSet):
    pass


class PostRoutinesRequestSet(BaseSet):
    rep_range: Optional[dict] = Field(None, example={"start": 8, "end": 12})


class PutRoutinesRequestSet(BaseSet):
    rep_range: Optional[dict] = Field(None, example={"start": 8, "end": 12})


# Set models for responses
class Set(BaseModel):
    index: int = Field(..., example=0)
    type: SetType = Field(..., example="normal")
    weight_kg: Optional[float] = Field(None, example=100.0)
    reps: Optional[int] = Field(None, example=10)
    distance_meters: Optional[int] = Field(None, example=None)
    duration_seconds: Optional[int] = Field(None, example=None)
    rpe: Optional[RPE] = Field(None, example=9.5)
    custom_metric: Optional[float] = Field(None, example=50)


class RoutineSet(BaseModel):
    index: int = Field(..., example=0)
    type: SetType = Field(..., example="normal")
    weight_kg: Optional[float] = Field(None, example=100.0)
    reps: Optional[int] = Field(None, example=10)
    rep_range: Optional[dict] = Field(None, example={"start": 8, "end": 12})
    distance_meters: Optional[int] = Field(None, example=None)
    duration_seconds: Optional[int] = Field(None, example=None)
    rpe: Optional[RPE] = Field(None, example=9.5)
    custom_metric: Optional[float] = Field(None, example=50)


# Exercise models
class BaseExercise(BaseModel):
    exercise_template_id: str = Field(..., example="D04AC939")
    superset_id: Optional[int] = Field(None, example=None)
    notes: Optional[str] = Field(None, example="Felt good today. Form was on point.")


class PostWorkoutsRequestExercise(BaseExercise):
    sets: List[PostWorkoutsRequestSet] = Field(...)


class PostRoutinesRequestExercise(BaseExercise):
    rest_seconds: Optional[int] = Field(None, example=90)
    sets: List[PostRoutinesRequestSet] = Field(...)


class PutRoutinesRequestExercise(BaseExercise):
    rest_seconds: Optional[int] = Field(None, example=90)
    sets: List[PutRoutinesRequestSet] = Field(...)


# Response exercise models
class Exercise(BaseModel):
    index: int = Field(..., example=0)
    title: str = Field(..., example="Bench Press (Barbell)")
    notes: Optional[str] = Field(None, example="Paid closer attention to form today. Felt great!")
    exercise_template_id: str = Field(..., example="05293BCA")
    supersets_id: Optional[int] = Field(None, example=0)
    sets: List[Set] = Field(...)


class RoutineExercise(BaseModel):
    index: int = Field(..., example=0)
    title: str = Field(..., example="Bench Press (Barbell)")
    rest_seconds: Optional[int] = Field(None, example=60)
    notes: Optional[str] = Field(None, example="Focus on form. Go down to 90 degrees.")
    exercise_template_id: str = Field(..., example="05293BCA")
    supersets_id: Optional[int] = Field(None, example=0)
    sets: List[RoutineSet] = Field(...)


# Workout models
class PostWorkoutsRequestBody(BaseModel):
    workout: dict = Field(...)


class PostRoutinesRequestBody(BaseModel):
    routine: dict = Field(...)


class PutRoutinesRequestBody(BaseModel):
    routine: dict = Field(...)


class PostRoutineFolderRequestBody(BaseModel):
    routine_folder: dict = Field(...)


class WebhookRequestBody(BaseModel):
    authToken: str = Field(..., example="Bearer mytoken")
    url: str = Field(..., example="https://example.com/hevy-webhook")


class CreateCustomExerciseRequestBody(BaseModel):
    exercise: dict = Field(...)


# Response models
class Workout(BaseModel):
    id: str = Field(..., example="b459cba5-cd6d-463c-abd6-54f8eafcadcb")
    title: str = Field(..., example="Morning Workout 💪")
    routine_id: str = Field(..., example="b459cba5-cd6d-463c-abd6-54f8eafcadcb")
    description: Optional[str] = Field(None, example="Pushed myself to the limit today!")
    start_time: str = Field(..., example="2021-09-14T12:00:00Z")
    end_time: str = Field(..., example="2021-09-14T12:00:00Z")
    updated_at: str = Field(..., example="2021-09-14T12:00:00Z")
    created_at: str = Field(..., example="2021-09-14T12:00:00Z")
    exercises: List[Exercise] = Field(...)


class Routine(BaseModel):
    id: str = Field(..., example="b459cba5-cd6d-463c-abd6-54f8eafcadcb")
    title: str = Field(..., example="Upper Body 💪")
    folder_id: Optional[int] = Field(None, example=42)
    updated_at: str = Field(..., example="2021-09-14T12:00:00Z")
    created_at: str = Field(..., example="2021-09-14T12:00:00Z")
    exercises: List[RoutineExercise] = Field(...)


class ExerciseTemplate(BaseModel):
    id: str = Field(..., example="b459cba5-cd6d-463c-abd6-54f8eafcadcb")
    title: str = Field(..., example="Bench Press (Barbell)")
    type: str = Field(..., example="weight_reps")
    primary_muscle_group: str = Field(..., example="chest")
    secondary_muscle_groups: List[str] = Field(...)
    is_custom: bool = Field(..., example=False)


class RoutineFolder(BaseModel):
    id: int = Field(..., example=42)
    index: int = Field(..., example=1)
    title: str = Field(..., example="Push Pull 🏋️‍♂️")
    updated_at: str = Field(..., example="2021-09-14T12:00:00Z")
    created_at: str = Field(..., example="2021-09-14T12:00:00Z")


class ExerciseHistoryEntry(BaseModel):
    workout_id: str = Field(..., example="b459cba5-cd6d-463c-abd6-54f8eafcadcb")
    workout_title: str = Field(..., example="Morning Workout 💪")
    workout_start_time: str = Field(..., example="2024-01-01T12:00:00Z")
    workout_end_time: str = Field(..., example="2024-01-01T13:00:00Z")
    exercise_template_id: str = Field(..., example="D04AC939")
    weight_kg: Optional[float] = Field(None, example=100.0)
    reps: Optional[int] = Field(None, example=10)
    distance_meters: Optional[int] = Field(None, example=None)
    duration_seconds: Optional[int] = Field(None, example=None)
    rpe: Optional[RPE] = Field(None, example=8.5)
    custom_metric: Optional[float] = Field(None, example=None)
    set_type: str = Field(..., example="normal")


# Pagination models
class PaginatedWorkouts(BaseModel):
    page: int = Field(..., example=1)
    page_count: int = Field(..., example=5)
    workouts: List[Workout] = Field(...)


class PaginatedRoutines(BaseModel):
    page: int = Field(..., example=1)
    page_count: int = Field(..., example=5)
    routines: List[Routine] = Field(...)


class PaginatedExerciseTemplates(BaseModel):
    page: int = Field(..., example=1)
    page_count: int = Field(..., example=5)
    exercise_templates: List[ExerciseTemplate] = Field(...)


class PaginatedRoutineFolders(BaseModel):
    page: int = Field(..., example=1)
    page_count: int = Field(..., example=5)
    routine_folders: List[RoutineFolder] = Field(...)


# Event models
class UpdatedWorkout(BaseModel):
    type: str = Field(..., example="updated")
    workout: Workout = Field(...)


class DeletedWorkout(BaseModel):
    type: str = Field(..., example="deleted")
    id: str = Field(..., example="efe6801c-4aee-4959-bcdd-fca3f272821b")
    deleted_at: str = Field(..., example="2021-09-13T12:00:00Z")


class PaginatedWorkoutEvents(BaseModel):
    page: int = Field(..., example=1)
    page_count: int = Field(..., example=5)
    events: List[Union[UpdatedWorkout, DeletedWorkout]] = Field(...)


# Other response models
class WorkoutCount(BaseModel):
    workout_count: int = Field(default=42)


class WebhookSubscription(BaseModel):
    url: str = Field(..., example="https://example.com/hevy-webhook")
    auth_token: str = Field(..., example="Bearer mytoken")


class WebhookNotification(BaseModel):
    id: str = Field(..., example="00000000-0000-0000-0000-000000000001")
    payload: dict = Field(..., example={"workoutId": "f1085cdb-32b2-4003-967d-53a3af8eaecb"})

    @property
    def workout_id(self) -> str:
        """Convenience property to get the workout ID from the payload"""
        return self.payload.get("workoutId", "")