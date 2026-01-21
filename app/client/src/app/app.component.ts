import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DayInfo } from './models/task.model';

@Component({
  selector: 'app-root',
  imports: [CommonModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent implements OnInit {
  weekNumber: number = 0;
  weekTitle: string = '';
  days: DayInfo[] = [];

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
}
