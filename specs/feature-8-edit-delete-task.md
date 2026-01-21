# Feature: Edit and Delete Task

## Feature Description
Enhance the task card interface by adding interactive icons that allow users to edit and delete existing tasks. A pencil icon will enable users to modify task details through the same creation modal (repurposed with edit capabilities), while a trash can icon will allow users to delete tasks after confirming their intent. This feature transforms the weekly planner from a create-only system into a full CRUD (Create, Read, Update, Delete) task management application.

## User Story
As a weekly planner user
I want to edit and delete tasks that I've already created
So that I can correct mistakes, update task details as plans change, and remove tasks that are no longer relevant

## Problem Statement
The current weekly planner allows users to create and view tasks but provides no mechanism to modify or remove them after creation. Users who need to update task details (change date, title, description, or type) or delete obsolete tasks have no way to do so, making the application impractical for real-world task management where changes and corrections are common.

## Solution Statement
Add two action icons to each task card: a pencil icon for editing and a trash can icon for deletion. Clicking the pencil icon will open the existing "Add New Task" modal in edit mode, pre-populated with the task's current data, allowing users to modify any field and save changes via the existing PATCH /api/tasks/:id endpoint. Clicking the trash can icon will display a confirmation dialog to prevent accidental deletions, and upon confirmation, will delete the task via the existing DELETE /api/tasks/:id endpoint. Both operations will refresh the task list to reflect the changes immediately.

## Relevant Files
Use these files to implement the feature:

### Frontend Files
- `app/client/src/app/app.component.ts` - Main component logic (lines 1-167)
  - Add property to track edit mode state (`isEditMode: boolean`, `editingTaskId: number | null`)
  - Create `openEditModal(task: Task)` method to populate form with task data and set edit mode
  - Modify `openModal()` method to handle both create and edit modes
  - Modify `onSubmit()` method to detect edit mode and call appropriate service method
  - Create `confirmDelete(task: Task)` method to show confirmation and handle deletion
  - Add `updateTask()` method to call service and refresh tasks on success
  - Add `deleteTask()` method to call service and refresh tasks on success
  - Update `closeModal()` to reset edit mode state

- `app/client/src/app/app.component.html` - Main component template (lines 1-103)
  - Add action icons container within each task card (pencil and trash can)
  - Add click handlers for edit and delete icons
  - Modify modal header to display "Edit Task" when in edit mode vs "Add New Task"
  - Modify submit button text to display "Update Task" when in edit mode vs "Create Task"
  - Add confirmation dialog structure for delete confirmation (overlay with message and buttons)

- `app/client/src/app/app.component.css` - Component styling (lines 1-386)
  - Add styles for task action icons container (`.task-actions`)
  - Add styles for individual action icons (`.action-icon`, `.edit-icon`, `.delete-icon`)
  - Add hover effects and transitions for action icons
  - Add styles for delete confirmation dialog (`.confirm-dialog`, `.confirm-dialog-content`)
  - Add styles for confirmation dialog buttons
  - Ensure icons are properly positioned within task cards
  - Add responsive considerations for icon sizing on smaller screens

- `app/client/src/app/services/task.service.ts` - HTTP service for task operations (lines 1-40)
  - Add `updateTask(id: number, task: Partial<Task>): Observable<Task>` method to PATCH updates to the API
  - Add `deleteTask(id: number): Observable<void>` method to DELETE tasks via the API
  - Use consistent error handling with existing methods

- `app/client/src/app/models/task.model.ts` - TypeScript task interfaces (lines 1-19)
  - No changes needed - existing Task interface already includes id field required for edit/delete operations

### Backend Files
- `app/server/routers/tasks.py` - API endpoints (lines 1-106)
  - No changes needed - PATCH /api/tasks/:id endpoint already exists (lines 46-77)
  - No changes needed - DELETE /api/tasks/:id endpoint already exists (lines 79-106)

- `app/server/crud.py` - Database operations (lines 1-133)
  - No changes needed - update_task() function already exists (lines 76-125)
  - No changes needed - delete_task() function already exists (lines 127-133)

- `app/server/tests/test_api.py` - API endpoint tests
  - Add test for updating task via frontend service method
  - Add test for deleting task via frontend service method
  - Verify edit and delete operations don't create regressions

### New Files
None required - all functionality can be implemented using existing files and endpoints

## Implementation Plan

### Phase 1: Foundation - Service Layer Updates
Update the TaskService to support edit and delete operations by adding methods that call the existing backend PATCH and DELETE endpoints. This provides the foundation for the UI components to interact with the API.

- Add updateTask() method to TaskService for PATCH requests
- Add deleteTask() method to TaskService for DELETE requests
- Ensure error handling is consistent with existing service methods

### Phase 2: Core Implementation - Edit Functionality
Implement the edit feature by adding a pencil icon to task cards and modifying the modal to support both create and edit modes. The modal will pre-populate with existing task data when editing and submit updates to the PATCH endpoint.

- Add edit icon to task cards with click handler
- Create edit mode state management in component
- Implement openEditModal() method to populate form with task data
- Modify onSubmit() to detect edit mode and call updateTask() service
- Update modal title and button text based on edit mode
- Test complete edit workflow

### Phase 3: Integration - Delete Functionality
Implement the delete feature by adding a trash can icon to task cards and creating a confirmation dialog to prevent accidental deletions. Upon confirmation, the task will be removed via the DELETE endpoint.

- Add delete icon to task cards with click handler
- Create confirmation dialog UI structure
- Implement confirmDelete() method to show confirmation
- Implement deleteTask() method to call service and refresh tasks
- Add delete confirmation state management
- Style confirmation dialog and action icons
- Test complete delete workflow with confirmation

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### 1. Add Update and Delete Methods to TaskService
- Open `app/client/src/app/services/task.service.ts`
- After the `createTask()` method (after line 25), add a new method:
  ```typescript
  updateTask(id: number, task: Partial<Omit<Task, 'id' | 'created_at' | 'updated_at'>>): Observable<Task> {
    return this.http.patch<Task>(`${this.apiUrl}/tasks/${id}`, task).pipe(
      catchError(this.handleError)
    );
  }
  ```
- After the `updateTask()` method, add another method:
  ```typescript
  deleteTask(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/tasks/${id}`).pipe(
      catchError(this.handleError)
    );
  }
  ```
- These methods will communicate with the existing backend PATCH and DELETE endpoints

### 2. Add Edit Mode State to Component
- Open `app/client/src/app/app.component.ts`
- After line 17 (`isModalOpen: boolean = false;`), add new properties:
  ```typescript
  isEditMode: boolean = false;
  editingTaskId: number | null = null;
  isDeleteConfirmOpen: boolean = false;
  taskToDelete: Task | null = null;
  ```
- These properties track whether the modal is in edit mode, which task is being edited, and delete confirmation state

### 3. Update openModal Method for Create Mode
- In `app/client/src/app/app.component.ts`, modify the `openModal()` method (lines 87-96)
- Update it to explicitly set create mode:
  ```typescript
  openModal(): void {
    this.isModalOpen = true;
    this.isEditMode = false;
    this.editingTaskId = null;
    this.newTask = {
      date: new Date(),
      title: '',
      description: '',
      task_type: 'personal'
    };
    this.formErrors = [];
  }
  ```

### 4. Add openEditModal Method for Edit Mode
- In `app/client/src/app/app.component.ts`, after the `openModal()` method, add a new method:
  ```typescript
  openEditModal(task: Task): void {
    this.isModalOpen = true;
    this.isEditMode = true;
    this.editingTaskId = task.id;

    // Convert day_of_week back to a date within the current week
    const dayIndex = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
      .indexOf(task.day_of_week);
    const monday = this.getMonday(new Date());
    const taskDate = new Date(monday);
    taskDate.setDate(monday.getDate() + dayIndex);

    this.newTask = {
      date: taskDate,
      title: task.title,
      description: task.description || '',
      task_type: task.task_type
    };
    this.formErrors = [];
  }
  ```

### 5. Update closeModal to Reset Edit State
- In `app/client/src/app/app.component.ts`, modify the `closeModal()` method (lines 98-101)
- Add reset for edit mode state:
  ```typescript
  closeModal(): void {
    this.isModalOpen = false;
    this.isEditMode = false;
    this.editingTaskId = null;
    this.formErrors = [];
  }
  ```

### 6. Modify onSubmit to Handle Both Create and Edit
- In `app/client/src/app/app.component.ts`, modify the `onSubmit()` method (lines 121-146)
- Update it to detect edit mode and call the appropriate service method:
  ```typescript
  onSubmit(): void {
    if (!this.validateForm()) {
      return;
    }

    const dayOfWeek = this.getDayOfWeekFromDate(this.newTask.date);

    const taskData = {
      title: this.newTask.title,
      description: this.newTask.description || null,
      day_of_week: dayOfWeek,
      time_slot: '12:00 PM',
      task_type: this.newTask.task_type,
      completed: false
    };

    if (this.isEditMode && this.editingTaskId !== null) {
      // Update existing task
      this.taskService.updateTask(this.editingTaskId, taskData).subscribe({
        next: () => {
          this.closeModal();
          this.loadTasks();
        },
        error: (error) => {
          this.formErrors = ['Failed to update task: ' + error.message];
        }
      });
    } else {
      // Create new task
      this.taskService.createTask(taskData).subscribe({
        next: () => {
          this.closeModal();
          this.loadTasks();
        },
        error: (error) => {
          this.formErrors = ['Failed to create task: ' + error.message];
        }
      });
    }
  }
  ```

### 7. Add Delete Confirmation Methods
- In `app/client/src/app/app.component.ts`, after the `loadTasks()` method, add new methods:
  ```typescript
  openDeleteConfirmation(task: Task): void {
    this.isDeleteConfirmOpen = true;
    this.taskToDelete = task;
  }

  closeDeleteConfirmation(): void {
    this.isDeleteConfirmOpen = false;
    this.taskToDelete = null;
  }

  confirmDeleteTask(): void {
    if (this.taskToDelete) {
      this.taskService.deleteTask(this.taskToDelete.id).subscribe({
        next: () => {
          this.closeDeleteConfirmation();
          this.loadTasks();
        },
        error: (error) => {
          console.error('Failed to delete task:', error);
          this.closeDeleteConfirmation();
        }
      });
    }
  }
  ```

### 8. Import Task Model in Component
- In `app/client/src/app/app.component.ts`, verify the import statement at line 4 includes Task:
  ```typescript
  import { DayInfo, Task } from './models/task.model';
  ```
- If Task is not imported, update the import statement to include it

### 9. Add Action Icons to Task Cards
- Open `app/client/src/app/app.component.html`
- Locate the task card structure (lines 21-27)
- Replace the task card content with:
  ```html
  <div class="task-card" [ngClass]="'task-type-' + task.task_type">
    <div class="task-content">
      <h3 class="task-title">{{ task.title }}</h3>
      @if (task.description) {
        <p class="task-description">{{ task.description }}</p>
      }
      <span class="task-type-badge">{{ task.task_type }}</span>
    </div>
    <div class="task-actions">
      <button class="action-icon edit-icon" (click)="openEditModal(task)" title="Edit task">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
          <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
        </svg>
      </button>
      <button class="action-icon delete-icon" (click)="openDeleteConfirmation(task)" title="Delete task">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="3 6 5 6 21 6"></polyline>
          <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
        </svg>
      </button>
    </div>
  </div>
  ```

### 10. Update Modal Header to Show Edit vs Create Mode
- Open `app/client/src/app/app.component.html`
- Locate the modal header (line 39)
- Replace the h2 element with:
  ```html
  <h2>{{ isEditMode ? 'Edit Task' : 'Add New Task' }}</h2>
  ```

### 11. Update Submit Button Text for Edit Mode
- In `app/client/src/app/app.component.html`
- Locate the submit button (line 96)
- Replace the button text with:
  ```html
  <button type="submit" class="btn-primary">{{ isEditMode ? 'Update Task' : 'Create Task' }}</button>
  ```

### 12. Add Delete Confirmation Dialog
- Open `app/client/src/app/app.component.html`
- After the closing `@if` for the modal (after line 101), add the confirmation dialog:
  ```html
  @if (isDeleteConfirmOpen && taskToDelete) {
    <div class="modal-overlay" (click)="closeDeleteConfirmation()">
      <div class="confirm-dialog" (click)="$event.stopPropagation()">
        <div class="confirm-dialog-header">
          <h3>Confirm Delete</h3>
        </div>
        <div class="confirm-dialog-content">
          <p>Are you sure you want to delete the task "{{ taskToDelete.title }}"?</p>
          <p class="confirm-warning">This action cannot be undone.</p>
        </div>
        <div class="confirm-dialog-actions">
          <button type="button" class="btn-secondary" (click)="closeDeleteConfirmation()">Cancel</button>
          <button type="button" class="btn-danger" (click)="confirmDeleteTask()">Delete</button>
        </div>
      </div>
    </div>
  }
  ```

### 13. Add Styles for Task Actions Container
- Open `app/client/src/app/app.component.css`
- After the task card styles (after line 155), add:
  ```css
  .task-content {
    flex: 1;
  }

  .task-actions {
    display: flex;
    gap: 0.5rem;
    margin-top: 0.5rem;
    padding-top: 0.5rem;
    border-top: 1px solid #f0f0f0;
  }

  .action-icon {
    background: none;
    border: none;
    padding: 0.375rem;
    cursor: pointer;
    border-radius: 4px;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background-color 0.2s ease, transform 0.2s ease;
    color: #666;
  }

  .action-icon:hover {
    background-color: #f5f5f5;
    transform: scale(1.1);
  }

  .edit-icon:hover {
    color: #4a90e2;
  }

  .delete-icon:hover {
    color: #e74c3c;
  }

  .action-icon svg {
    display: block;
  }
  ```

### 14. Modify Task Card Layout to Support Actions
- In `app/client/src/app/app.component.css`
- Update the `.task-card` rule (around line 129) to use flexbox:
  ```css
  .task-card {
    background-color: #ffffff;
    border-left: 4px solid #4a90e2;
    border-radius: 4px;
    padding: 0.75rem;
    margin-bottom: 0.75rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    display: flex;
    flex-direction: column;
  }
  ```

### 15. Add Styles for Delete Confirmation Dialog
- In `app/client/src/app/app.component.css`, after the modal styles (after line 347), add:
  ```css
  /* Delete Confirmation Dialog */
  .confirm-dialog {
    background-color: #ffffff;
    border-radius: 12px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    width: 90%;
    max-width: 400px;
    overflow: hidden;
  }

  .confirm-dialog-header {
    padding: 1.25rem 1.5rem;
    border-bottom: 1px solid #e0e0e0;
    background-color: #fafafa;
  }

  .confirm-dialog-header h3 {
    margin: 0;
    font-size: 1.25rem;
    color: #333;
    font-weight: 600;
  }

  .confirm-dialog-content {
    padding: 1.5rem;
  }

  .confirm-dialog-content p {
    margin: 0 0 1rem 0;
    font-size: 0.9375rem;
    color: #333;
    line-height: 1.5;
  }

  .confirm-dialog-content p:last-child {
    margin-bottom: 0;
  }

  .confirm-warning {
    font-size: 0.875rem;
    color: #e74c3c;
    font-weight: 500;
  }

  .confirm-dialog-actions {
    display: flex;
    gap: 0.75rem;
    justify-content: flex-end;
    padding: 1rem 1.5rem;
    background-color: #fafafa;
    border-top: 1px solid #e0e0e0;
  }

  .btn-danger {
    background-color: #e74c3c;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 0.625rem 1.25rem;
    font-size: 0.9375rem;
    font-weight: 600;
    cursor: pointer;
    transition: background-color 0.2s ease, transform 0.2s ease;
  }

  .btn-danger:hover {
    background-color: #c0392b;
    transform: translateY(-2px);
  }

  .btn-danger:active {
    transform: translateY(0);
  }
  ```

### 16. Add Responsive Styles for Action Icons
- In `app/client/src/app/app.component.css`, update the responsive section (after line 386):
  ```css
  @media (max-width: 480px) {
    .week-grid {
      grid-template-columns: 1fr;
    }

    header {
      padding: 1.5rem 1rem;
      flex-direction: column;
      gap: 1rem;
    }

    header h1 {
      font-size: 1.75rem;
    }

    .day-card {
      min-height: 250px;
    }

    .action-icon {
      padding: 0.5rem;
    }

    .action-icon svg {
      width: 14px;
      height: 14px;
    }

    .confirm-dialog {
      max-width: 95%;
    }
  }
  ```

### 17. Test Edit Functionality End-to-End
- Start the application using `./scripts/start.sh`
- Navigate to http://localhost:4200
- Create a test task if none exist
- Click the pencil icon on an existing task
- Verify the modal opens with "Edit Task" title
- Verify the form is pre-populated with the task's current data
- Modify the title, description, date, or type
- Click "Update Task"
- Verify the modal closes
- Verify the task updates with the new data in the correct day column
- Test editing tasks across different days and task types

### 18. Test Delete Functionality End-to-End
- With the application still running at http://localhost:4200
- Click the trash can icon on an existing task
- Verify the confirmation dialog appears with the task title
- Verify the warning message is displayed
- Click "Cancel" and verify the dialog closes without deleting
- Click the trash can icon again
- Click "Delete" and verify the dialog closes
- Verify the task is removed from the day column
- Verify no other tasks are affected
- Test deleting tasks from different days

### 19. Test Edge Cases
- Test editing a task and changing its date to move it to a different day
- Test clicking multiple edit/delete buttons rapidly
- Test opening edit modal, closing it, and opening delete confirmation
- Test editing and deleting the last task in a day (should show "No tasks yet")
- Test with very long task titles and descriptions in the confirmation dialog
- Verify clicking outside the confirmation dialog closes it
- Verify the X button closes the edit modal properly

### 20. Run All Validation Commands
- Execute `cd app/server && uv run pytest` to ensure backend tests pass
- Execute `cd app/client && npm run build` to validate TypeScript compilation
- Perform manual end-to-end testing as described in the validation commands
- Verify no regressions in existing create task functionality

## Testing Strategy

### Unit Tests
- TaskService updateTask() method with valid task ID and data
- TaskService deleteTask() method with valid task ID
- TaskService error handling for update and delete operations
- Component openEditModal() method populates form correctly
- Component edit mode state management (isEditMode flag)
- Component delete confirmation state management
- Date conversion logic when editing tasks (day_of_week to Date)

### Integration Tests
- Complete edit workflow: click edit icon → modal opens with data → modify fields → submit → task updates
- Complete delete workflow: click delete icon → confirmation shows → confirm → task deleted
- Delete cancellation: click delete icon → confirmation shows → cancel → task remains
- Edit mode vs create mode: verify modal title and button text change appropriately
- Task list refresh after update and delete operations
- Edit task and move it to a different day (change date field)

### Edge Cases
- Editing the only task in a day and moving it to another day (original day shows "No tasks yet")
- Deleting the only task in a day (day shows "No tasks yet")
- Editing a task with very long title and description (form handles overflow)
- Rapidly clicking edit and delete icons (no duplicate requests or UI glitches)
- Opening edit modal and then closing it without saving (no state corruption)
- Network error during update operation (error message shown, modal stays open)
- Network error during delete operation (error logged, confirmation closes)
- Clicking outside confirmation dialog (dialog closes, task remains)
- Task with null description in edit mode (form handles null values)
- Editing task type and verifying visual styling updates correctly

## Acceptance Criteria
- Each task card displays a pencil icon for editing
- Each task card displays a trash can icon for deletion
- Clicking the pencil icon opens the modal in edit mode with pre-populated data
- Modal title changes to "Edit Task" when in edit mode
- Submit button text changes to "Update Task" when in edit mode
- All task fields (date, title, description, type) can be edited
- Submitting the edit form updates the task via PATCH /api/tasks/:id endpoint
- Updated task appears in the correct day column after editing
- Modal closes automatically after successful update
- Clicking the trash can icon displays a confirmation dialog
- Confirmation dialog shows the task title and a warning message
- Clicking "Cancel" in confirmation closes dialog without deleting
- Clicking "Delete" in confirmation removes the task via DELETE /api/tasks/:id endpoint
- Deleted task is immediately removed from the UI
- Task list refreshes after both edit and delete operations
- Action icons have hover effects and proper visual feedback
- Icons are properly sized and positioned within task cards
- Confirmation dialog can be closed by clicking outside of it
- No regressions in existing task creation functionality
- Backend tests continue to pass with 100% success rate
- Frontend builds without TypeScript compilation errors

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- `cd app/server && uv run pytest` - Run server tests to validate the feature works with zero regressions
- `cd app/client && npm run build` - Build the Angular client to validate TypeScript compilation succeeds
- `./scripts/start.sh` - Start both client and server, then manually test the complete workflows:

  **Edit Workflow:**
  1. Open http://localhost:4200
  2. Create a test task if none exist (use "Add New Task" button)
  3. Click the pencil icon on any task card
  4. Verify modal opens with "Edit Task" title
  5. Verify form is pre-filled with task's current data
  6. Change the title to "Updated Task Title"
  7. Change the date to a different day of the week
  8. Click "Update Task" button
  9. Verify modal closes and task appears in the new day column with updated title
  10. Click the pencil icon again and verify all changes persisted

  **Delete Workflow:**
  1. Click the trash can icon on any task card
  2. Verify confirmation dialog appears with task title
  3. Verify warning message "This action cannot be undone" is displayed
  4. Click "Cancel" and verify dialog closes, task remains
  5. Click trash can icon again
  6. Click "Delete" button
  7. Verify dialog closes and task is removed from the day column
  8. Refresh the page (Ctrl/Cmd+R)
  9. Verify the deleted task does not reappear (deletion persisted)

  **Edge Case Testing:**
  1. Edit a task and move it from Monday to Friday
  2. Verify Monday updates to show "No tasks yet" if it was the only task
  3. Verify Friday shows the moved task
  4. Create multiple tasks on one day
  5. Delete all tasks from that day one by one
  6. Verify "No tasks yet" appears after the last deletion
  7. Test clicking outside the confirmation dialog to cancel deletion

## Notes
- The backend PATCH and DELETE endpoints already exist and are fully functional (app/server/routers/tasks.py)
- The CRUD operations (update_task, delete_task) are already implemented in app/server/crud.py
- Only frontend changes are needed to expose these existing capabilities through the UI
- The same modal form used for creation can be reused for editing by tracking edit mode state
- Icon SVGs are inline to avoid external dependencies and ensure they always load
- Consider using iconography libraries like Font Awesome or Material Icons in future iterations for more icon options
- The confirmation dialog prevents accidental deletions, which is especially important on mobile devices where touch targets may be smaller
- Edit mode preserves the current task's completed status (not exposed in UI yet but maintained in backend)
- Future enhancement: Add undo functionality after deletion
- Future enhancement: Add keyboard shortcuts (e.g., Escape to close modals)
- Future enhancement: Add loading states during update and delete operations
- Consider adding animation transitions when tasks are removed or moved between days
- The pencil and trash can icons are universally recognized symbols for edit and delete actions
