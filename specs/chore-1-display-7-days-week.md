# Chore: Display 7 Days of the Week

## Chore Description
Update the client main page to display a weekly planner view showing 7 days of the week. Each day should display:
- The day of the week name (Monday through Sunday)
- The date for that day
- A box/container where tasks for that day will be displayed

The title of the page should show the week number of the year (1-52). This creates the foundation for a weekly task planner interface where users can visualize and manage their tasks across the entire week.

## Relevant Files
Use these files to resolve the chore:

- `app/client/src/app/app.component.ts` - Main component that will contain the weekly planner logic
  - Add logic to calculate the current week number (1-52)
  - Add logic to generate an array of 7 days starting from Monday of the current week
  - Add logic to format dates and day names
  - Add data structures to hold day information (day name, date, tasks)

- `app/client/src/app/app.component.html` - Main component template that will display the weekly view
  - Replace the placeholder Angular template with the weekly planner UI
  - Display the week number as the title
  - Use Angular's `@for` control flow to loop through the 7 days
  - Display each day's name and date
  - Create task containers for each day

- `app/client/src/app/app.component.css` - Main component styles for the weekly planner
  - Replace the placeholder styles with custom styles for the weekly planner
  - Add layout styles for the week grid (7 columns for 7 days)
  - Add card/box styles for each day container
  - Add styles for the week number title
  - Add responsive styles for mobile/tablet views
  - Add task container placeholder styles

- `app/client/src/app/app.config.ts` - Application configuration
  - Add HttpClient provider to enable API communication (needed for future task loading)

### New Files
- `app/client/src/app/services/task.service.ts` - Service to manage task data and API communication
  - Create an Angular service to handle API calls to the backend
  - Add methods to fetch tasks from the API
  - Add data models/interfaces for tasks
  - This service will be used in future stories to load and manage tasks

- `app/client/src/app/models/task.model.ts` - TypeScript interfaces for task data
  - Define the Task interface matching the backend model
  - Include properties: id, title, description, day_of_week, time_slot, completed, created_at, updated_at
  - This ensures type safety across the application

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### 1. Create TypeScript Models
- Create `app/client/src/app/models/task.model.ts` file
- Define the `Task` interface with properties matching the backend API model:
  - id: number
  - title: string
  - description: string | null
  - day_of_week: 'Monday' | 'Tuesday' | 'Wednesday' | 'Thursday' | 'Friday' | 'Saturday' | 'Sunday'
  - time_slot: string
  - completed: boolean
  - created_at: string
  - updated_at: string
- Define a `DayInfo` interface to represent each day in the week view:
  - dayName: string (e.g., "Monday")
  - date: Date
  - dateString: string (formatted date like "Jan 20")
  - tasks: Task[] (array of tasks for that day, initially empty)

### 2. Create Task Service
- Create `app/client/src/app/services/task.service.ts` file
- Implement an Angular service with `@Injectable({ providedIn: 'root' })`
- Inject HttpClient for API communication
- Define the API base URL (http://localhost:5173/api)
- Create a `getTasks()` method that returns an Observable<Task[]>
- Add proper error handling for API calls
- This service provides a foundation for future task management features

### 3. Update App Configuration
- Update `app/client/src/app/app.config.ts`
- Import `provideHttpClient` from '@angular/common/http'
- Add `provideHttpClient()` to the providers array
- This enables HTTP communication for the task service

### 4. Update App Component TypeScript
- Update `app/client/src/app/app.component.ts`
- Import necessary Angular modules (CommonModule for date formatting)
- Import the Task and DayInfo models
- Add a property `weekNumber: number` to store the current week number (1-52)
- Add a property `days: DayInfo[]` to store the 7 days of the week
- Implement `ngOnInit()` lifecycle hook:
  - Calculate the current week number using ISO 8601 week date standard
  - Get the current date
  - Find the Monday of the current week (start of week)
  - Generate an array of 7 DayInfo objects (Monday through Sunday)
  - For each day, calculate the date and format it appropriately
- Add helper method `getWeekNumber(date: Date): number` to calculate ISO week number
- Add helper method `getMonday(date: Date): Date` to get the Monday of a given date's week
- Add helper method `formatDate(date: Date): string` to format dates as "MMM DD" (e.g., "Jan 20")

### 5. Update App Component HTML
- Update `app/client/src/app/app.component.html`
- Remove all placeholder Angular content (the entire template from lines 1-336)
- Create a new structure with:
  - Header section displaying "Week {{ weekNumber }}" as the main title
  - Main content section with a grid layout for the 7 days
  - Use `@for` directive to loop through the days array: `@for (day of days; track day.dayName)`
  - For each day, create a card/box containing:
    - Day name header (e.g., "Monday")
    - Date display (e.g., "Jan 20")
    - Tasks container (empty placeholder with a message like "No tasks yet")
- Add semantic HTML structure (header, main, section, article elements)

### 6. Update App Component CSS
- Update `app/client/src/app/app.component.css`
- Remove all placeholder Angular styles (the entire :host style block from lines 11-177)
- Create new styles for the weekly planner:
  - Container styles with proper padding and max-width for readability
  - Header styles for the week number title (centered, large font, proper spacing)
  - Grid layout for the 7 days (use CSS Grid with 7 columns on desktop)
  - Day card styles with borders, padding, shadows, and hover effects
  - Day name header styles (bold, centered, background color)
  - Date display styles (smaller font, gray color, centered)
  - Task container placeholder styles (min-height, border, padding)
  - Responsive styles using media queries:
    - Tablet: 3-4 columns
    - Mobile: 1-2 columns (stacked layout)
  - Color scheme that is clean and professional (neutral colors with subtle accents)

### 7. Run Validation Commands
- Execute all validation commands listed below to ensure the chore is complete with zero regressions
- Verify the application starts without errors
- Check the browser at http://localhost:4200 to visually confirm the weekly view displays correctly
- Verify server tests pass to ensure no backend regressions

## Validation Commands
Execute every command to validate the chore is complete with zero regressions.

- `cd app/client && npm run build` - Build the Angular client to validate TypeScript compilation and catch any errors
- `cd app/server && uv run pytest` - Run server tests to validate the chore is complete with zero regressions
- `./scripts/start.sh` - Start both client and server to manually verify the weekly view displays correctly at http://localhost:4200

## Notes
- This chore focuses solely on the UI structure and week calculation logic. Task management functionality (add, edit, delete) will be implemented in future stories.
- The week number calculation should use the ISO 8601 standard where weeks start on Monday and the first week of the year is the week containing the first Thursday.
- The dates displayed should be dynamic based on the current date, showing the current week's Monday through Sunday.
- The task containers are placeholders for now. They will be populated with actual tasks in future iterations when task loading and management features are implemented.
- The Angular application uses standalone components (Angular 19+), so imports should be included directly in the component decorator.
- The backend API already exists and supports task management, but this chore does not integrate with it yet. The task service is created as a foundation for future integration.
- Consider accessibility: use semantic HTML, proper heading hierarchy, and ARIA labels where appropriate.
- The styling should be responsive and work well on desktop, tablet, and mobile devices.
