import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { DayInfo, Task } from './models/task.model';
import { TaskService } from './services/task.service';

@Component({
  selector: 'app-root',
  imports: [CommonModule, FormsModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent implements OnInit {
  weekNumber: number = 0;
  weekTitle: string = '';
  days: DayInfo[] = [];
  isModalOpen: boolean = false;
  isEditMode: boolean = false;
  editingTaskId: number | null = null;
  isDeleteConfirmOpen: boolean = false;
  taskToDelete: Task | null = null;
  newTask: {
    date: Date;
    title: string;
    description: string;
    task_type: 'personal' | 'work' | 'other';
  } = {
    date: new Date(),
    title: '',
    description: '',
    task_type: 'personal'
  };
  formErrors: string[] = [];

  constructor(private taskService: TaskService) {}

  ngOnInit(): void {
    const today = new Date();
    this.weekNumber = this.getWeekNumber(today);

    const monday = this.getMonday(today);
    const sunday = new Date(monday);
    sunday.setDate(monday.getDate() + 6);

    const mondayFormatted = this.formatDateMMDDYYYY(monday);
    const sundayFormatted = this.formatDateMMDDYYYY(sunday);
    this.weekTitle = `Week ${this.weekNumber} (${mondayFormatted} to ${sundayFormatted})`;

    this.days = [];

    const dayNames = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];

    for (let i = 0; i < 7; i++) {
      const date = new Date(monday);
      date.setDate(monday.getDate() + i);

      this.days.push({
        dayName: dayNames[i],
        date: date,
        dateString: this.formatDate(date),
        tasks: []
      });
    }

    this.loadTasks();
  }

  getWeekNumber(date: Date): number {
    const d = new Date(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate()));
    const dayNum = d.getUTCDay() || 7;
    d.setUTCDate(d.getUTCDate() + 4 - dayNum);
    const yearStart = new Date(Date.UTC(d.getUTCFullYear(), 0, 1));
    const weekNo = Math.ceil((((d.getTime() - yearStart.getTime()) / 86400000) + 1) / 7);
    return weekNo;
  }

  getMonday(date: Date): Date {
    const d = new Date(date);
    const day = d.getDay();
    const diff = d.getDate() - day + (day === 0 ? -6 : 1);
    return new Date(d.setDate(diff));
  }

  formatDate(date: Date): string {
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    return `${months[date.getMonth()]} ${date.getDate()}`;
  }

  formatDateMMDDYYYY(date: Date): string {
    const month = (date.getMonth() + 1).toString().padStart(2, '0');
    const day = date.getDate().toString().padStart(2, '0');
    const year = date.getFullYear();
    return `${month}/${day}/${year}`;
  }

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

  closeModal(): void {
    this.isModalOpen = false;
    this.isEditMode = false;
    this.editingTaskId = null;
    this.formErrors = [];
  }

  validateForm(): boolean {
    this.formErrors = [];

    if (!this.newTask.title || this.newTask.title.trim().length === 0) {
      this.formErrors.push('Title is required');
    }

    if (!this.newTask.date) {
      this.formErrors.push('Date is required');
    }

    if (!this.newTask.task_type) {
      this.formErrors.push('Task type is required');
    }

    return this.formErrors.length === 0;
  }

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

  getDayOfWeekFromDate(date: Date): 'Monday' | 'Tuesday' | 'Wednesday' | 'Thursday' | 'Friday' | 'Saturday' | 'Sunday' {
    const dayNames: ('Sunday' | 'Monday' | 'Tuesday' | 'Wednesday' | 'Thursday' | 'Friday' | 'Saturday')[] =
      ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
    return dayNames[new Date(date).getUTCDay()] as 'Monday' | 'Tuesday' | 'Wednesday' | 'Thursday' | 'Friday' | 'Saturday' | 'Sunday';
  }

  loadTasks(): void {
    this.taskService.getTasks().subscribe({
      next: (tasks) => {
        this.days.forEach(day => {
          day.tasks = tasks.filter(task => task.day_of_week === day.dayName);
        });
      },
      error: (error) => {
        console.error('Failed to load tasks:', error);
      }
    });
  }

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
}
