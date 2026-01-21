import pytest
from datetime import datetime


def test_health_check(client):
    """Test health check endpoint returns 200."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["database"] == "connected"
    assert "timestamp" in data


def test_create_task(client):
    """Test POST /api/tasks creates task successfully."""
    task_data = {
        "title": "Team Meeting",
        "description": "Weekly team sync",
        "day_of_week": "Monday",
        "time_slot": "10:00 AM",
        "completed": False
    }

    response = client.post("/api/tasks", json=task_data)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == task_data["title"]
    assert data["description"] == task_data["description"]
    assert data["day_of_week"] == task_data["day_of_week"]
    assert data["time_slot"] == task_data["time_slot"]
    assert data["completed"] == task_data["completed"]
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_get_all_tasks(client):
    """Test GET /api/tasks returns all tasks."""
    # Create some test tasks
    tasks = [
        {
            "title": "Task 1",
            "description": "First task",
            "day_of_week": "Monday",
            "time_slot": "09:00 AM",
            "completed": False
        },
        {
            "title": "Task 2",
            "description": "Second task",
            "day_of_week": "Tuesday",
            "time_slot": "02:00 PM",
            "completed": True
        }
    ]

    for task in tasks:
        client.post("/api/tasks", json=task)

    response = client.get("/api/tasks")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Task 1"
    assert data[1]["title"] == "Task 2"


def test_update_task(client):
    """Test PATCH /api/tasks/{id} updates task."""
    # Create a task
    task_data = {
        "title": "Original Task",
        "description": "Original description",
        "day_of_week": "Wednesday",
        "time_slot": "11:00 AM",
        "completed": False
    }

    create_response = client.post("/api/tasks", json=task_data)
    task_id = create_response.json()["id"]

    # Update the task
    update_data = {
        "title": "Updated Task",
        "completed": True
    }

    response = client.patch(f"/api/tasks/{task_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Task"
    assert data["completed"] is True
    assert data["description"] == "Original description"  # Should remain unchanged
    assert data["day_of_week"] == "Wednesday"  # Should remain unchanged


def test_delete_task(client):
    """Test DELETE /api/tasks/{id} removes task."""
    # Create a task
    task_data = {
        "title": "Task to Delete",
        "description": "Will be deleted",
        "day_of_week": "Friday",
        "time_slot": "03:00 PM",
        "completed": False
    }

    create_response = client.post("/api/tasks", json=task_data)
    task_id = create_response.json()["id"]

    # Delete the task
    response = client.delete(f"/api/tasks/{task_id}")
    assert response.status_code == 204

    # Verify task is deleted
    get_response = client.get("/api/tasks")
    tasks = get_response.json()
    assert len(tasks) == 0


def test_update_nonexistent_task(client):
    """Test updating a non-existent task returns 404."""
    update_data = {
        "title": "Updated Task"
    }

    response = client.patch("/api/tasks/999", json=update_data)
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_delete_nonexistent_task(client):
    """Test deleting a non-existent task returns 404."""
    response = client.delete("/api/tasks/999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_create_task_invalid_data(client):
    """Test creating task with invalid data returns 422."""
    invalid_task = {
        "title": "",  # Empty title should fail validation
        "day_of_week": "Invalid Day",  # Invalid day
        "time_slot": "10:00 AM"
    }

    response = client.post("/api/tasks", json=invalid_task)
    assert response.status_code == 422


def test_create_task_invalid_day_of_week(client):
    """Test creating task with invalid day_of_week returns 422."""
    invalid_task = {
        "title": "Test Task",
        "day_of_week": "Funday",  # Invalid day
        "time_slot": "10:00 AM",
        "completed": False
    }

    response = client.post("/api/tasks", json=invalid_task)
    assert response.status_code == 422


def test_tasks_ordered_by_day_and_time(client):
    """Test that tasks are returned ordered by day of week."""
    tasks = [
        {
            "title": "Friday Task",
            "day_of_week": "Friday",
            "time_slot": "10:00 AM",
            "completed": False
        },
        {
            "title": "Monday Task",
            "day_of_week": "Monday",
            "time_slot": "09:00 AM",
            "completed": False
        },
        {
            "title": "Wednesday Task",
            "day_of_week": "Wednesday",
            "time_slot": "02:00 PM",
            "completed": False
        }
    ]

    for task in tasks:
        client.post("/api/tasks", json=task)

    response = client.get("/api/tasks")
    data = response.json()

    # Should be ordered Monday, Wednesday, Friday
    assert data[0]["day_of_week"] == "Monday"
    assert data[1]["day_of_week"] == "Wednesday"
    assert data[2]["day_of_week"] == "Friday"
