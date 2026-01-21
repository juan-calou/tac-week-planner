export interface Task {
  id: number;
  title: string;
  description: string | null;
  day_of_week: 'Monday' | 'Tuesday' | 'Wednesday' | 'Thursday' | 'Friday' | 'Saturday' | 'Sunday';
  time_slot: string;
  completed: boolean;
  created_at: string;
  updated_at: string;
}

export interface DayInfo {
  dayName: string;
  date: Date;
  dateString: string;
  tasks: Task[];
}
