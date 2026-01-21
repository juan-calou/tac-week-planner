# Feature: Add New Task

## Feature Description
Implement a comprehensive task creation and display system that allows users to add new tasks through a modal dialog. Tasks can be assigned to specific dates within the current week, include a title, description, and categorization by type (personal, work, or other). Once created, tasks are stored in the database and displayed as cards within their respective date boxes in the weekly view.

This feature transforms the weekly planner from a static display into an interactive task management system where users can easily create, view, and organize their weekly tasks.

## User Story
As a weekly planner user
I want to add tasks to specific days of the week with relevant details
So that I can organize and track my personal, work, and other commitments throughout the week

## Problem Statement
The current weekly planner displays a week view with date boxes but lacks any mechanism for users to create and manage tasks. Users can see the week structure but cannot add, view, or interact with tasks, making the application non-functional for its intended purpose of weekly task planning.

## Solution Statement
Implement a complete task management workflow by adding an "Add New Task" button that opens a modal dialog with a form for entering task details. The form captures the task's date (automatically mapped to day_of_week), title, description, and type classification. Upon submission, the task is saved via the existing POST /api/tasks endpoint. The application then fetches all week tasks using the GET /api/tasks endpoint and displays them as visually distinct cards within their corresponding date boxes, organized by the task type.

## Relevant Files
Use these files to implement the feature:

### Backend Files
- `app/server/models.py` - Task data models and validation
  - Add a `task_type` field to TaskBase model to support personal/work/other categorization
  - Ensure the field is properly validated with allowed values

- `app/server/database.py` - Database schema and connection management
  - Add `task_type` column to the tasks table in the init_db() function
  - Update schema to support the new field

- `app/server/crud.py` - Database operations (CRUD functions)
  - Update create_task() to handle the new task_type field in INSERT statement
  - Update get_all_tasks() to include task_type in SELECT query
  - Update get_task_by_id() to include task_type in SELECT query
  - Update update_task() to handle optional task_type updates

- `app/server/tests/test_api.py` - API endpoint tests
  - Add task_type field to all test task data objects
  - Create tests specifically for task_type validation (valid and invalid values)
  - Verify task_type is correctly returned in API responses

### Frontend Files
- `app/client/src/app/models/task.model.ts` - TypeScript task interfaces
  - Add task_type field to the Task interface with proper typing

- `app/client/src/app/services/task.service.ts` - HTTP service for task operations
  - Add createTask() method to POST new tasks to the API
  - Implement proper error handling for task creation

- `app/client/src/app/app.component.ts` - Main component logic
  - Add properties for modal state management (isModalOpen boolean)
  - Inject TaskService for API communication
  - Implement loadTasks() method to fetch tasks from API
  - Implement createTask() method to handle form submission
  - Add logic to organize fetched tasks into the appropriate day's tasks array
  - Call loadTasks() during ngOnInit() to display existing tasks on page load

- `app/client/src/app/app.component.html` - Main component template
  - Add "Add New Task" button in the header or main section
  - Create modal dialog structure with overlay and dialog container
  - Build task creation form with fields for date, title, description, and type
  - Add form validation and error messaging
  - Display tasks as cards within date boxes with styling based on task_type
  - Show task details including title, description, and type indicator

- `app/client/src/app/app.component.css` - Component styling
  - Style the "Add New Task" button with hover states
  - Create modal overlay and dialog box styles
  - Style form inputs, labels, and buttons
  - Design task card layout with visual differentiation by type
  - Add responsive design considerations

### New Files
- None required - all functionality can be implemented using existing files

## Implementation Plan

### Phase 1: Foundation - Backend Schema and Model Updates
Update the backend data model to support task type categorization. This requires adding a new field to the database schema, models, and CRUD operations to ensure tasks can be properly classified and stored.

- Modify database schema to add task_type column
- Update Pydantic models to include and validate task_type field
- Update all CRUD operations to handle the new field
- Update existing tests to work with the new field

### Phase 2: Core Implementation - Task Creation UI
Build the user interface components for task creation, including the trigger button, modal dialog, and form. This phase focuses on creating a user-friendly interface for capturing task information.

- Add "Add New Task" button to the main page
- Implement modal dialog component with proper show/hide logic
- Create comprehensive form with all required fields
- Add form validation and user feedback
- Implement task creation API integration

### Phase 3: Integration - Task Display and Full Workflow
Connect all pieces together by implementing task fetching and display logic. This phase completes the full user workflow from task creation to visualization in the weekly view.

- Implement task fetching from API on component initialization
- Add logic to organize tasks by day of week
- Create task card display within date boxes
- Style task cards with visual indicators for task types
- Test complete workflow from creation to display

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### 1. Update Backend Database Schema
- Open `app/server/database.py`
- Locate the CREATE TABLE statement in the init_db() function
- Add a new column: `task_type TEXT NOT NULL` after the time_slot column
- This column will store 'personal', 'work', or 'other' values
- Note: Existing database will need to be migrated or recreated for testing

### 2. Update Backend Models
- Open `app/server/models.py`
- In the TaskBase class, add a new field: `task_type: str = Field(..., pattern="^(personal|work|other)$")`
- Place this field after the time_slot field to maintain logical ordering
- The pattern validation ensures only valid task types are accepted
- TaskCreate will automatically inherit this field
- Add task_type as an Optional field in TaskUpdate class: `task_type: Optional[str] = Field(None, pattern="^(personal|work|other)$")`

### 3. Update Backend CRUD Operations
- Open `app/server/crud.py`
- In create_task() function:
  - Add task_type to the INSERT statement column list after time_slot
  - Add task_data.task_type to the VALUES tuple in the correct position
- In get_all_tasks() function:
  - Add task_type to the SELECT column list
- In get_task_by_id() function:
  - Add task_type to the SELECT column list
- In update_task() function:
  - Add conditional logic to handle task_type updates similar to other fields
  - Check if task_data.task_type is not None, add "task_type = ?" to update_fields, and append value

### 4. Update Backend Tests
- Open `app/server/tests/test_api.py`
- Add task_type field with value "work" to all existing test task data dictionaries
- Add a new test function test_create_task_invalid_type() to verify invalid task_type values are rejected
- Add a new test function test_create_task_with_different_types() to verify all valid types (personal, work, other) are accepted
- Update assertions in existing tests to verify task_type is returned correctly in responses

### 5. Run Backend Tests to Verify Schema Changes
- Execute `cd app/server && uv run pytest` to ensure all backend tests pass
- Fix any test failures related to the new task_type field
- Note: May need to delete app/server/tasks.db to recreate schema if tests fail due to schema mismatch

### 6. Update Frontend Task Model
- Open `app/client/src/app/models/task.model.ts`
- In the Task interface, add a new property: `task_type: 'personal' | 'work' | 'other';`
- Place this field after the time_slot property
- The union type ensures type safety on the frontend

### 7. Update Frontend Task Service
- Open `app/client/src/app/services/task.service.ts`
- Add a new method createTask(task: Omit<Task, 'id' | 'created_at' | 'updated_at'>): Observable<Task>
- Implement the method to POST to `${this.apiUrl}/tasks` with the task data
- Use .pipe(catchError(this.handleError)) for consistent error handling
- Return the Observable<Task> for component subscription

### 8. Update Frontend Component Logic for Task Management
- Open `app/client/src/app/app.component.ts`
- Import TaskService and inject it in the constructor: `constructor(private taskService: TaskService) {}`
- Add properties for modal state: `isModalOpen: boolean = false;`
- Add properties for form data: `newTask = { date: new Date(), title: '', description: '', task_type: 'personal' as const };`
- Add property for form errors: `formErrors: string[] = [];`
- Create openModal() method that sets isModalOpen = true and resets form data
- Create closeModal() method that sets isModalOpen = false and clears form errors
- Create validateForm() method that checks all required fields and returns boolean
- Create onSubmit() method that:
  - Validates the form using validateForm()
  - Converts the date to day_of_week string (use day names from the days array)
  - Maps form data to API format (with day_of_week, time_slot as "12:00 PM" default)
  - Calls taskService.createTask() with the mapped data
  - Subscribes to the response, on success: closes modal, reloads tasks, on error: displays error message
- Create loadTasks() method that:
  - Calls taskService.getTasks()
  - Subscribes to the response
  - Loops through returned tasks and assigns each to the correct day in the days array based on day_of_week
  - Handles errors appropriately
- Update ngOnInit() to call loadTasks() after initializing the days array

### 9. Update Frontend Component Template for Button and Modal
- Open `app/client/src/app/app.component.html`
- Add an "Add New Task" button inside the header, after the h1 element:
  - `<button class="add-task-btn" (click)="openModal()">+ Add New Task</button>`
- Add modal structure at the end of the main section (before closing main tag):
  - Create a modal overlay div with *ngIf="isModalOpen" and (click)="closeModal()"
  - Inside overlay, create a modal dialog div with (click)="$event.stopPropagation()" to prevent closing when clicking inside
  - Add modal header with title "Add New Task" and close button
  - Add form with (ngSubmit)="onSubmit()"
  - Create form fields for: date (input type="date"), title (input type="text"), description (textarea), task_type (select with options: personal, work, other)
  - Add form validation error display area
  - Add form buttons: Cancel (calls closeModal()) and Create Task (submit button)
- Update the tasks-container section to display task cards:
  - Replace the @if empty state with an @for loop over day.tasks
  - Create task card div for each task with class bindings based on task_type
  - Display task title, description, and type indicator

### 10. Update Frontend Component Styles
- Open `app/client/src/app/app.component.css`
- Add styles for .add-task-btn with primary color, padding, border-radius, and hover effects
- Add styles for .modal-overlay with fixed positioning, full screen, backdrop filter, and z-index
- Add styles for .modal-dialog with centered positioning, white background, border-radius, box-shadow, and max-width
- Add styles for .modal-header with flex layout, border-bottom, and close button styling
- Add styles for .modal-form with proper spacing, label/input layout
- Add styles for form inputs, textarea, and select with consistent sizing and border styles
- Add styles for .form-error to display validation errors in red
- Add styles for .modal-actions with button layout and spacing
- Add styles for .task-card with padding, margin, border-radius, and box-shadow
- Add styles for task-type variants: .task-card.personal, .task-card.work, .task-card.other with different background colors or border colors
- Add styles for task card content: title (bold), description (smaller text), type indicator

### 11. Add Required Angular Imports
- Open `app/client/src/app/app.component.ts`
- Add FormsModule to the imports array in the @Component decorator for ngModel support
- Ensure CommonModule is already imported (it should be from previous work)

### 12. Test Task Creation End-to-End
- Start the application using `./scripts/start.sh`
- Navigate to http://localhost:4200
- Click the "Add New Task" button
- Fill in the form with test data for each field
- Submit the form and verify:
  - Modal closes
  - Task appears in the correct day box
  - Task displays with correct styling based on type
- Create multiple tasks of different types across different days
- Verify all tasks display correctly
- Refresh the page and verify tasks persist (loaded from database)

### 13. Run All Validation Commands
- Execute all validation commands listed below to ensure zero regressions
- Backend tests must pass
- Frontend must build without errors
- Manual testing must confirm full workflow functions correctly

## Testing Strategy

### Unit Tests
- Backend model validation tests for task_type field (valid values: personal, work, other)
- Backend model validation tests for invalid task_type values
- Backend CRUD operation tests for creating tasks with task_type
- Backend CRUD operation tests for updating task_type field
- Frontend service tests for createTask() method (mock HTTP calls)
- Frontend component tests for form validation logic
- Frontend component tests for modal open/close functionality

### Integration Tests
- End-to-end test for complete task creation workflow: button click -> form fill -> submit -> display
- Test task creation with all three task_type values
- Test task display organization by day_of_week
- Test task persistence across page refreshes
- Test error handling when API calls fail
- Test form validation prevents submission with missing required fields

### Edge Cases
- Creating task with very long title (test max_length validation)
- Creating task with empty description (optional field should work)
- Creating task with invalid date selection
- Submitting form multiple times rapidly (prevent duplicate submissions)
- Network errors during task creation (display error message, don't close modal)
- Creating tasks for all 7 days of the week (verify proper organization)
- Page load when no tasks exist (should show "No tasks yet" in all day boxes)
- Page load when tasks exist (should properly distribute tasks to correct days)

## Acceptance Criteria
- An "Add New Task" button is prominently displayed on the main page
- Clicking the button opens a modal dialog with a task creation form
- The form includes functional inputs for: date (within current week), title, description, and type (dropdown with personal/work/other)
- All form fields are validated (title, date, type are mandatory; description is optional)
- Submitting the form with valid data creates a task via POST /api/tasks endpoint
- Modal closes automatically after successful task creation
- Created task immediately appears in the correct day box without page refresh
- Tasks are displayed as cards with visual differentiation by type
- Task cards show title, description, and type indicator
- Existing tasks are loaded and displayed when the page loads (GET /api/tasks)
- Tasks are correctly organized by day_of_week in their respective day boxes
- Multiple tasks can be added to the same day
- Form validation errors are clearly displayed to the user
- Cancel button closes modal without creating task
- Clicking overlay outside modal closes the modal
- Backend tests pass with 100% success rate
- Frontend builds without TypeScript compilation errors

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- `cd app/server && rm tasks.db && uv run pytest` - Delete old database schema and run server tests to validate the feature works with zero regressions
- `cd app/client && npm run build` - Build the Angular client to validate TypeScript compilation and catch any errors
- `./scripts/start.sh` - Start both client and server, then manually test the complete workflow:
  1. Open http://localhost:4200
  2. Click "Add New Task" button
  3. Fill in form (select today's date, enter "Test Task" as title, "Test description" as description, select "work" as type)
  4. Click "Create Task" button
  5. Verify task appears in the correct day box
  6. Create 2-3 more tasks with different types and dates
  7. Verify all tasks display correctly with appropriate styling
  8. Refresh the page
  9. Verify all tasks persist and load correctly

## Notes
- The existing backend schema uses `day_of_week` (Monday-Sunday strings) rather than actual dates, so the date input must be converted to the corresponding day name
- Consider adding a default `time_slot` value (e.g., "12:00 PM") for new tasks since the feature description doesn't mention time selection but the backend requires it
- The form should restrict date selection to only dates within the current week (Monday to Sunday) to maintain consistency with the weekly view
- Task cards should have distinct visual styling (colors or icons) for each task_type to make categorization immediately apparent
- Consider adding loading states while tasks are being fetched or created
- Consider adding success/error toast notifications for better user feedback
- The database schema change requires dropping and recreating the tasks table or writing a migration - for this feature, recommend dropping app/server/tasks.db and letting it recreate
- May want to add a delete/edit button to task cards in a future iteration
- Consider adding form field for time_slot in future if users need more granular scheduling
- For MVP, using a fixed time_slot like "All Day" or "12:00 PM" is acceptable
