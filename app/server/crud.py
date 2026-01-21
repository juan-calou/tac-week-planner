from sqlite3 import Connection
from datetime import datetime
from typing import List, Optional, Dict, Any
import pandas as pd
from models import TaskCreate, TaskUpdate


def create_task(conn: Connection, task_data: TaskCreate) -> int:
    """Create a new task in the database."""
    cursor = conn.cursor()
    now = datetime.now().isoformat()
    cursor.execute("""
        INSERT INTO tasks (title, description, day_of_week, time_slot, completed, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        task_data.title,
        task_data.description,
        task_data.day_of_week,
        task_data.time_slot,
        int(task_data.completed),
        now,
        now
    ))
    conn.commit()
    return cursor.lastrowid


def get_all_tasks(conn: Connection) -> List[Dict[str, Any]]:
    """Retrieve all tasks from the database."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, title, description, day_of_week, time_slot, completed, created_at, updated_at
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

    rows = cursor.fetchall()

    # Convert to list of dictionaries using pandas for data transformation
    if rows:
        df = pd.DataFrame([dict(row) for row in rows])
        # Convert completed from int to bool
        df['completed'] = df['completed'].astype(bool)
        return df.to_dict('records')
    return []


def get_task_by_id(conn: Connection, task_id: int) -> Optional[Dict[str, Any]]:
    """Get a single task by ID."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, title, description, day_of_week, time_slot, completed, created_at, updated_at
        FROM tasks
        WHERE id = ?
    """, (task_id,))

    row = cursor.fetchone()
    if row:
        task = dict(row)
        task['completed'] = bool(task['completed'])
        return task
    return None


def update_task(conn: Connection, task_id: int, task_data: TaskUpdate) -> bool:
    """Update an existing task."""
    # Get current task to check if it exists
    existing_task = get_task_by_id(conn, task_id)
    if not existing_task:
        return False

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
        values.append(int(task_data.completed))

    # Always update updated_at
    update_fields.append("updated_at = ?")
    values.append(datetime.now().isoformat())

    # Add task_id for WHERE clause
    values.append(task_id)

    query = f"UPDATE tasks SET {', '.join(update_fields)} WHERE id = ?"

    cursor = conn.cursor()
    cursor.execute(query, values)
    conn.commit()

    return cursor.rowcount > 0


def delete_task(conn: Connection, task_id: int) -> bool:
    """Delete a task by ID."""
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    return cursor.rowcount > 0
