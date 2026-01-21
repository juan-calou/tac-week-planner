# Chore: Add Dates to Title

## Chore Description
Update the main page title to include the date range for the current week. The title currently displays only "Week ##" but should now display "Week ## (MM/DD/YYYY to MM/DD/YYYY)" where the dates represent the Monday (start) and Sunday (end) of the current week using the MM/DD/YYYY date format.

This enhancement provides users with immediate context about the exact date range they are viewing, making the weekly planner more informative and easier to use when planning tasks.

## Relevant Files
Use these files to resolve the chore:

- `app/client/src/app/app.component.ts` - Main component TypeScript file
  - Add a new property to store the formatted date range string
  - Create a helper method to format dates in MM/DD/YYYY format
  - Update the ngOnInit() method to calculate and store the week's start date (Monday) and end date (Sunday)
  - Generate the complete title string with the date range

- `app/client/src/app/app.component.html` - Main component template file
  - Update the header section to display the new title format with dates
  - Replace `<h1>Week {{ weekNumber }}</h1>` with `<h1>{{ weekTitle }}</h1>` to show the complete title including date range

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### 1. Update App Component TypeScript
- Open `app/client/src/app/app.component.ts`
- Add a new property `weekTitle: string = '';` to store the complete title with date range
- Create a new helper method `formatDateMMDDYYYY(date: Date): string` that:
  - Takes a Date object as input
  - Returns a string in MM/DD/YYYY format
  - Uses zero-padding for single-digit months and days (e.g., "01/05/2026" not "1/5/2026")
- Update the `ngOnInit()` method to:
  - Calculate the Monday of the current week (already done with getMonday method)
  - Calculate the Sunday of the current week by adding 6 days to Monday
  - Format both Monday and Sunday dates using the new formatDateMMDDYYYY method
  - Build the complete title string: `Week ${weekNumber} (${mondayFormatted} to ${sundayFormatted})`
  - Assign this string to the weekTitle property

### 2. Update App Component HTML
- Open `app/client/src/app/app.component.html`
- Locate the header section containing `<h1>Week {{ weekNumber }}</h1>`
- Replace `{{ weekNumber }}` with `{{ weekTitle }}` so the line reads: `<h1>{{ weekTitle }}</h1>`
- This change will display the complete title with date range instead of just the week number

### 3. Run Validation Commands
- Execute all validation commands listed below to ensure the chore is complete with zero regressions
- Verify the application compiles without TypeScript errors
- Verify server tests pass to ensure no backend regressions
- Start the application and manually verify the title displays in the correct format: "Week ## (MM/DD/YYYY to MM/DD/YYYY)"

## Validation Commands
Execute every command to validate the chore is complete with zero regressions.

- `cd app/client && npm run build` - Build the Angular client to validate TypeScript compilation and catch any errors
- `cd app/server && uv run pytest` - Run server tests to validate the chore is complete with zero regressions
- `./scripts/start.sh` - Start both client and server to manually verify the title displays correctly at http://localhost:4200 with the format "Week ## (MM/DD/YYYY to MM/DD/YYYY)"

## Notes
- The MM/DD/YYYY format requires zero-padding (e.g., "01/05/2026" not "1/5/2026")
- The week always starts on Monday and ends on Sunday, consistent with the existing week calculation logic
- The existing weekNumber property is still used to calculate the week number, but the display now uses the weekTitle property
- This is a display-only change and does not affect any backend functionality or data models
- The date range will automatically update based on the current date when the component initializes
