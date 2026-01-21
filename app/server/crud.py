from datetime import datetime
from typing import List, Optional, Dict, Any
from models import TaskCreate, TaskUpdate


def create_task(db, task_data: TaskCreate) -> Dict[str, Any]:
    """Create a new task in the database."""
    now = datetime.utcnow().isoformat()

    result = db.execute("""
        INSERT INTO tasks (title, description, day_of_week, time_slot, task_type, completed, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, [
        task_data.title,
        task_data.description,
        task_data.day_of_week,
        task_data.time_slot,
        task_data.task_type,
        1 if task_data.completed else 0,
        now,
        now
    ])

    # Get the created task
    task_id = result.last_insert_rowid
    return get_task_by_id(db, task_id)


def get_all_tasks(db) -> List[Dict[str, Any]]:
    """Retrieve all tasks from the database."""
    result = db.execute("""
        SELECT id, title, description, day_of_week, time_slot, task_type, completed, created_at, updated_at
        FROM tasks
        ORDER BY
            CASE day_of_week
                WHEN 'Monday' THEN 1
                WHEN 'Tuesday' THEN 2
                WHEN 'Wednesday' THEN 3
                WHEN 'Thursday' THEN 4
                WHEN 'Friday' THEN 5
                WHEN 'Saturday' THEN 6
                WHEN 'Sunday' THEN 7
            END,
            time_slot
    """)

    tasks = []
    for row in result.rows:
        tasks.append({
            'id': row[0],
            'title': row[1],
            'description': row[2],
            'day_of_week': row[3],
            'time_slot': row[4],
            'task_type': row[5],
            'completed': bool(row[6]),
            'created_at': row[7],
            'updated_at': row[8]
        })

    return tasks


def get_task_by_id(db, task_id: int) -> Optional[Dict[str, Any]]:
    """Get a single task by ID."""
    result = db.execute("""
        SELECT id, title, description, day_of_week, time_slot, task_type, completed, created_at, updated_at
        FROM tasks
        WHERE id = ?
    """, [task_id])

    if result.rows:
        row = result.rows[0]
        return {
            'id': row[0],
            'title': row[1],
            'description': row[2],
            'day_of_week': row[3],
            'time_slot': row[4],
            'task_type': row[5],
            'completed': bool(row[6]),
            'created_at': row[7],
            'updated_at': row[8]
        }
    return None


def update_task(db, task_id: int, task_data: TaskUpdate) -> Optional[Dict[str, Any]]:
    """Update an existing task."""
    # Get current task to check if it exists
    existing_task = get_task_by_id(db, task_id)
    if not existing_task:
        return None

    # Build update query dynamically based on provided fields
    update_fields = []
    values = []

    if task_data.title is not None:
        update_fields.append("title = ?")
        values.append(task_data.title)

    if task_data.description is not None:
        update_fields.append("description = ?")
        values.append(task_data.description)

    if task_data.day_of_week is not None:
        update_fields.append("day_of_week = ?")
        values.append(task_data.day_of_week)

    if task_data.time_slot is not None:
        update_fields.append("time_slot = ?")
        values.append(task_data.time_slot)

    if task_data.completed is not None:
        update_fields.append("completed = ?")
        values.append(1 if task_data.completed else 0)

    if task_data.task_type is not None:
        update_fields.append("task_type = ?")
        values.append(task_data.task_type)

    # Always update updated_at
    update_fields.append("updated_at = ?")
    values.append(datetime.utcnow().isoformat())

    # Add task_id for WHERE clause
    values.append(task_id)

    query = f"UPDATE tasks SET {', '.join(update_fields)} WHERE id = ?"

    db.execute(query, values)

    return get_task_by_id(db, task_id)


def delete_task(db, task_id: int) -> bool:
    """Delete a task by ID."""
    result = db.execute("DELETE FROM tasks WHERE id = ?", [task_id])
    return result.rows_affected > 0
