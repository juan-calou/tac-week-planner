# Bug: Fix Add Task Bugs

## Bug Description
There are two bugs in the add task functionality:

1. **Wrong Day Assignment**: When adding a task by selecting a date in the modal, the task appears in the previous day instead of the selected day. For example, selecting Wednesday's date results in the task appearing on Tuesday.

2. **Missing Right Margin in Modal**: The form inputs in the "Add New Task" modal extend fully to the right edge without proper spacing, creating a cramped appearance and poor visual balance.

## Problem Statement
The date-to-day-of-week conversion has a timezone issue causing tasks to be assigned to the wrong day, and the modal form inputs need proper spacing for better UI/UX.

## Solution Statement
Fix the timezone handling in the `getDayOfWeekFromDate()` method to use the date string directly without timezone conversion, and add proper padding/box-sizing to the modal form inputs to create appropriate right margin spacing.

## Steps to Reproduce

### Bug 1: Wrong Day Assignment
1. Open the application in the browser
2. Click "Add New Task" button
3. Select any date (e.g., Wednesday, January 22, 2026)
4. Fill in title, description, and task type
5. Click "Create Task"
6. Observe the task appears in the previous day (Tuesday) instead of the selected day (Wednesday)

### Bug 2: Missing Right Margin
1. Open the application in the browser
2. Click "Add New Task" button
3. Observe the modal form inputs (date, title, description, task type dropdown)
4. Notice the input fields extend all the way to the right edge without proper spacing

## Root Cause Analysis

### Bug 1: Timezone Issue
The root cause is in `app/client/src/app/app.component.ts:148-152`. The `getDayOfWeekFromDate()` method receives a date from the date input field, which is a string in format "YYYY-MM-DD". When this string is converted to a JavaScript Date object using `new Date(date)`, it's treated as UTC midnight. The `.getDay()` method then returns the day in the local timezone, which can shift the day backward by one if the local timezone is behind UTC.

For example:
- Selected date: "2026-01-22" (Wednesday)
- `new Date("2026-01-22")` creates a Date at UTC midnight
- `.getDay()` converts to local timezone (e.g., PST = UTC-8)
- Result: 2026-01-21 23:00:00 PST (Tuesday)

### Bug 2: CSS Box Model Issue
The root cause is in `app/client/src/app/app.component.css:270-280`. The form inputs use `width: 100%` which makes them extend to fill the entire container width. While there is left padding from the `.modal-form` (1.5rem), the inputs themselves don't account for their own padding and border in the width calculation, and there's no explicit right margin or padding consideration.

## Relevant Files
Use these files to fix the bug:

- **app/client/src/app/app.component.ts** - Contains the `getDayOfWeekFromDate()` method that needs timezone fix. This method converts the selected date to a day of week name (line 148-152).

- **app/client/src/app/app.component.css** - Contains the modal and form styling. The `.form-group input, .form-group textarea, .form-group select` rules (line 270-280) need adjustment for proper spacing.

## Step by Step Tasks

### Fix Date Timezone Issue
- Modify the `getDayOfWeekFromDate()` method in `app/client/src/app/app.component.ts` to handle date strings properly without timezone conversion
- Instead of using `new Date(date).getDay()` which causes timezone issues, parse the date string directly or use UTC methods to ensure the correct day is selected
- The fix should extract the day of week from the date input value without timezone shifts

### Fix Modal Form Input Spacing
- Update the CSS rules for form inputs in `app/client/src/app/app.component.css`
- Change the `.form-group input, .form-group textarea, .form-group select` width from `100%` to `calc(100% - 1rem)` or add `box-sizing: border-box` with appropriate right margin
- Ensure all form inputs have consistent right spacing that matches the visual balance of the left spacing
- Verify the modal looks properly spaced on different screen sizes

### Validation and Testing
- Test the date-to-day conversion fix by creating tasks for each day of the week and verifying they appear in the correct day column
- Verify that selecting Monday through Sunday dates results in tasks appearing in the correct corresponding day
- Check the modal appearance to ensure form inputs have proper right margin spacing
- Test on different screen sizes to ensure responsive behavior is maintained
- Run the validation commands to ensure no regressions

## Validation Commands
Execute every command to validate the bug is fixed with zero regressions.

- Manual test: Open the app, click "Add New Task", select various dates across the week, create tasks, and verify each task appears in the correct day column matching the selected date
- Manual test: Open the app, click "Add New Task", inspect the modal form inputs to confirm there is appropriate right margin/spacing (approximately 1.5rem to match left padding)
- `cd app/server && uv run pytest` - Run server tests to validate the bug is fixed with zero regressions

## Notes
- The date input field in HTML returns a string in "YYYY-MM-DD" format, not a Date object
- When converting date strings to Date objects, be mindful of timezone interpretations (ISO format without time is treated as UTC)
- For UI consistency, the right spacing in the modal should mirror the left spacing provided by `.modal-form` padding (1.5rem)
- Consider using `box-sizing: border-box` which is a best practice for form inputs to include padding and border in the width calculation
