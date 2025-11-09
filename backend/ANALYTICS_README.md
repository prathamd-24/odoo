# Analytics API - Complete Documentation

Comprehensive analytics endpoints for project management, tasks, timesheets, and expenses.

## Analytics Endpoints

All analytics endpoints require authentication. Use `-b cookies.txt` to include session cookies.

---

## Project Analytics

### 1. Projects Overview
**GET** `/analytics/projects/overview`

Get overall statistics for all projects.

```bash
curl -X GET http://localhost:5000/analytics/projects/overview \
  -H "Content-Type: application/json" \
  -b cookies.txt
```

**Response (200):**
```json
{
  "total_projects": 5,
  "projects_by_status": {
    "active": 3,
    "completed": 1,
    "on_hold": 1
  },
  "total_budget": 250000.0,
  "average_duration_days": 120.5
}
```

---

### 2. Project Summary
**GET** `/analytics/projects/<project_id>/summary`

Get detailed analytics for a specific project including tasks, timesheets, expenses, and budget analysis.

```bash
curl -X GET http://localhost:5000/analytics/projects/1/summary \
  -H "Content-Type: application/json" \
  -b cookies.txt
```

**Response (200):**
```json
{
  "project": {
    "id": 1,
    "project_code": "PROJ001",
    "name": "Website Redesign",
    "status": "active",
    "budget_amount": 50000.0,
    "start_date": "2025-01-01",
    "end_date": "2025-06-30",
    "duration_days": 180
  },
  "team": {
    "team_size": 5,
    "project_manager_id": 1
  },
  "tasks": {
    "total_tasks": 25,
    "overdue_tasks": 3,
    "by_state": {
      "todo": 8,
      "in_progress": 10,
      "done": 7
    },
    "by_priority": {
      "low": 5,
      "medium": 12,
      "high": 6,
      "urgent": 2
    }
  },
  "timesheets": {
    "total_hours": 450.5,
    "billable_hours": 380.0,
    "non_billable_hours": 70.5,
    "total_cost": 33787.5
  },
  "expenses": {
    "total_expenses": 5250.0,
    "approved_expenses": 4500.0,
    "pending_expenses": 750.0,
    "billable_expenses": 4800.0
  },
  "budget_analysis": {
    "budget_amount": 50000.0,
    "total_cost": 39037.5,
    "remaining_budget": 10962.5,
    "budget_utilization_percent": 78.08
  }
}
```

---

### 3. Projects Timeline
**GET** `/analytics/projects/timeline`

Get timeline data for all projects with start and end dates.

```bash
curl -X GET http://localhost:5000/analytics/projects/timeline \
  -H "Content-Type: application/json" \
  -b cookies.txt
```

**Response (200):**
```json
{
  "timeline": [
    {
      "id": 1,
      "project_code": "PROJ001",
      "name": "Website Redesign",
      "status": "active",
      "start_date": "2025-01-01",
      "end_date": "2025-06-30",
      "duration_days": 180,
      "budget_amount": 50000.0
    },
    {
      "id": 2,
      "project_code": "PROJ002",
      "name": "Mobile App",
      "status": "active",
      "start_date": "2025-02-01",
      "end_date": "2025-08-31",
      "duration_days": 211,
      "budget_amount": 75000.0
    }
  ],
  "total_projects": 2
}
```

---

## Task Analytics

### 4. Tasks Overview
**GET** `/analytics/tasks/overview`

Get overall statistics for all tasks.

```bash
curl -X GET http://localhost:5000/analytics/tasks/overview \
  -H "Content-Type: application/json" \
  -b cookies.txt
```

**Response (200):**
```json
{
  "total_tasks": 100,
  "overdue_tasks": 12,
  "tasks_due_this_week": 8,
  "tasks_by_state": {
    "todo": 25,
    "in_progress": 40,
    "review": 15,
    "done": 20
  },
  "tasks_by_priority": {
    "low": 20,
    "medium": 45,
    "high": 25,
    "urgent": 10
  },
  "average_assignments_per_task": 2.3
}
```

---

### 5. User Task Analytics
**GET** `/analytics/tasks/user/<user_id>`

Get task analytics for a specific user.

```bash
curl -X GET http://localhost:5000/analytics/tasks/user/2 \
  -H "Content-Type: application/json" \
  -b cookies.txt
```

**Response (200):**
```json
{
  "user_id": 2,
  "email": "jane@example.com",
  "total_assigned_tasks": 15,
  "completed_tasks": 8,
  "completion_rate_percent": 53.33,
  "overdue_tasks": 2,
  "tasks_by_state": {
    "todo": 3,
    "in_progress": 4,
    "done": 8
  },
  "tasks_by_priority": {
    "low": 2,
    "medium": 8,
    "high": 4,
    "urgent": 1
  }
}
```

---

### 6. Project Task Timeline
**GET** `/analytics/tasks/project/<project_id>/timeline`

Get task timeline for a specific project.

```bash
curl -X GET http://localhost:5000/analytics/tasks/project/1/timeline \
  -H "Content-Type: application/json" \
  -b cookies.txt
```

**Response (200):**
```json
{
  "project_id": 1,
  "project_name": "Website Redesign",
  "task_timeline": [
    {
      "id": 1,
      "title": "Design Homepage",
      "priority": "high",
      "state": "in_progress",
      "due_date": "2025-01-15",
      "created_at": "2025-11-08T10:30:45.123456",
      "is_overdue": false,
      "assigned_users_count": 2
    },
    {
      "id": 2,
      "title": "Implement Backend API",
      "priority": "urgent",
      "state": "todo",
      "due_date": "2025-01-20",
      "created_at": "2025-11-08T11:00:00.000000",
      "is_overdue": false,
      "assigned_users_count": 3
    }
  ],
  "total_tasks": 2
}
```

---

## Timesheet Analytics

### 7. Timesheets Overview
**GET** `/analytics/timesheets/overview?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD`

Get overall timesheet statistics. Supports optional date filtering.

```bash
curl -X GET "http://localhost:5000/analytics/timesheets/overview?start_date=2025-01-01&end_date=2025-01-31" \
  -H "Content-Type: application/json" \
  -b cookies.txt
```

**Response (200):**
```json
{
  "total_hours": 1250.5,
  "billable_hours": 1050.0,
  "non_billable_hours": 200.5,
  "billable_percentage": 83.97,
  "total_cost": 93787.5,
  "hours_by_project": {
    "Website Redesign": 450.5,
    "Mobile App": 600.0,
    "Marketing Campaign": 200.0
  },
  "filters": {
    "start_date": "2025-01-01",
    "end_date": "2025-01-31"
  }
}
```

---

### 8. User Timesheet Analytics
**GET** `/analytics/timesheets/user/<user_id>?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD`

Get timesheet analytics for a specific user.

```bash
curl -X GET "http://localhost:5000/analytics/timesheets/user/2?start_date=2025-01-01&end_date=2025-01-31" \
  -H "Content-Type: application/json" \
  -b cookies.txt
```

**Response (200):**
```json
{
  "user_id": 2,
  "email": "jane@example.com",
  "total_hours": 180.5,
  "billable_hours": 160.0,
  "non_billable_hours": 20.5,
  "days_worked": 22,
  "average_hours_per_day": 8.2,
  "hours_by_project": {
    "Website Redesign": 120.5,
    "Mobile App": 60.0
  },
  "filters": {
    "start_date": "2025-01-01",
    "end_date": "2025-01-31"
  }
}
```

---

### 9. Project Timesheet Analytics
**GET** `/analytics/timesheets/project/<project_id>?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD`

Get timesheet analytics for a specific project.

```bash
curl -X GET "http://localhost:5000/analytics/timesheets/project/1?start_date=2025-01-01&end_date=2025-01-31" \
  -H "Content-Type: application/json" \
  -b cookies.txt
```

**Response (200):**
```json
{
  "project_id": 1,
  "project_name": "Website Redesign",
  "total_hours": 450.5,
  "total_cost": 33787.5,
  "hours_by_user": {
    "john@example.com": 180.0,
    "jane@example.com": 120.5,
    "bob@example.com": 150.0
  },
  "hours_by_task": {
    "Design Homepage": 80.0,
    "Implement Backend API": 120.5,
    "Frontend Development": 200.0,
    "Testing": 50.0
  },
  "filters": {
    "start_date": "2025-01-01",
    "end_date": "2025-01-31"
  }
}
```

---

## Expense Analytics

### 10. Expenses Overview
**GET** `/analytics/expenses/overview?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD`

Get overall expense statistics. Supports optional date filtering.

```bash
curl -X GET "http://localhost:5000/analytics/expenses/overview?start_date=2025-01-01&end_date=2025-01-31" \
  -H "Content-Type: application/json" \
  -b cookies.txt
```

**Response (200):**
```json
{
  "total_expenses": 15250.0,
  "billable_expenses": 12500.0,
  "non_billable_expenses": 2750.0,
  "expenses_by_status": {
    "approved": 10500.0,
    "pending": 3250.0,
    "rejected": 1500.0
  },
  "expenses_by_project": {
    "Website Redesign": 5250.0,
    "Mobile App": 7000.0,
    "Marketing Campaign": 3000.0
  },
  "filters": {
    "start_date": "2025-01-01",
    "end_date": "2025-01-31"
  }
}
```

---

### 11. User Expense Analytics
**GET** `/analytics/expenses/user/<user_id>?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD`

Get expense analytics for a specific user.

```bash
curl -X GET "http://localhost:5000/analytics/expenses/user/2?start_date=2025-01-01&end_date=2025-01-31" \
  -H "Content-Type: application/json" \
  -b cookies.txt
```

**Response (200):**
```json
{
  "user_id": 2,
  "email": "jane@example.com",
  "total_expenses": 3250.0,
  "expenses_by_status": {
    "approved": {
      "amount": 2500.0,
      "count": 5
    },
    "pending": {
      "amount": 750.0,
      "count": 2
    }
  },
  "expenses_by_project": {
    "Website Redesign": 1250.0,
    "Mobile App": 2000.0
  },
  "filters": {
    "start_date": "2025-01-01",
    "end_date": "2025-01-31"
  }
}
```

---

### 12. Project Expense Analytics
**GET** `/analytics/expenses/project/<project_id>?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD`

Get expense analytics for a specific project.

```bash
curl -X GET "http://localhost:5000/analytics/expenses/project/1?start_date=2025-01-01&end_date=2025-01-31" \
  -H "Content-Type: application/json" \
  -b cookies.txt
```

**Response (200):**
```json
{
  "project_id": 1,
  "project_name": "Website Redesign",
  "project_budget": 50000.0,
  "total_expenses": 5250.0,
  "expenses_by_status": {
    "approved": {
      "amount": 4500.0,
      "count": 8
    },
    "pending": {
      "amount": 750.0,
      "count": 2
    }
  },
  "expenses_by_user": {
    "john@example.com": {
      "amount": 1500.0,
      "count": 3
    },
    "jane@example.com": {
      "amount": 2250.0,
      "count": 4
    },
    "bob@example.com": {
      "amount": 1500.0,
      "count": 3
    }
  },
  "filters": {
    "start_date": "2025-01-01",
    "end_date": "2025-01-31"
  }
}
```

---

## Combined Analytics

### 13. Analytics Dashboard
**GET** `/analytics/dashboard`

Get high-level combined analytics across all entities.

```bash
curl -X GET http://localhost:5000/analytics/dashboard \
  -H "Content-Type: application/json" \
  -b cookies.txt
```

**Response (200):**
```json
{
  "projects": {
    "total": 5,
    "active": 3,
    "total_budget": 250000.0
  },
  "tasks": {
    "total": 100,
    "overdue": 12
  },
  "timesheets": {
    "total_hours": 2500.5,
    "total_cost": 187537.5
  },
  "expenses": {
    "total_expenses": 35250.0,
    "pending_expenses": 5750.0
  },
  "financial_summary": {
    "total_budget": 250000.0,
    "total_costs": 222787.5,
    "remaining_budget": 27212.5
  }
}
```

---

## Complete Testing Flow

```bash
# 1. Login first
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{"email": "john@example.com", "password": "pass123"}'

# 2. Get overall dashboard
curl -X GET http://localhost:5000/analytics/dashboard \
  -H "Content-Type: application/json" \
  -b cookies.txt

# 3. Get projects overview
curl -X GET http://localhost:5000/analytics/projects/overview \
  -H "Content-Type: application/json" \
  -b cookies.txt

# 4. Get specific project summary
curl -X GET http://localhost:5000/analytics/projects/1/summary \
  -H "Content-Type: application/json" \
  -b cookies.txt

# 5. Get projects timeline
curl -X GET http://localhost:5000/analytics/projects/timeline \
  -H "Content-Type: application/json" \
  -b cookies.txt

# 6. Get tasks overview
curl -X GET http://localhost:5000/analytics/tasks/overview \
  -H "Content-Type: application/json" \
  -b cookies.txt

# 7. Get user task analytics
curl -X GET http://localhost:5000/analytics/tasks/user/2 \
  -H "Content-Type: application/json" \
  -b cookies.txt

# 8. Get project task timeline
curl -X GET http://localhost:5000/analytics/tasks/project/1/timeline \
  -H "Content-Type: application/json" \
  -b cookies.txt

# 9. Get timesheets overview (with date filter)
curl -X GET "http://localhost:5000/analytics/timesheets/overview?start_date=2025-01-01&end_date=2025-01-31" \
  -H "Content-Type: application/json" \
  -b cookies.txt

# 10. Get user timesheet analytics
curl -X GET "http://localhost:5000/analytics/timesheets/user/2?start_date=2025-01-01&end_date=2025-01-31" \
  -H "Content-Type: application/json" \
  -b cookies.txt

# 11. Get project timesheet analytics
curl -X GET "http://localhost:5000/analytics/timesheets/project/1?start_date=2025-01-01&end_date=2025-01-31" \
  -H "Content-Type: application/json" \
  -b cookies.txt

# 12. Get expenses overview
curl -X GET "http://localhost:5000/analytics/expenses/overview?start_date=2025-01-01&end_date=2025-01-31" \
  -H "Content-Type: application/json" \
  -b cookies.txt

# 13. Get user expense analytics
curl -X GET "http://localhost:5000/analytics/expenses/user/2?start_date=2025-01-01&end_date=2025-01-31" \
  -H "Content-Type: application/json" \
  -b cookies.txt

# 14. Get project expense analytics
curl -X GET "http://localhost:5000/analytics/expenses/project/1?start_date=2025-01-01&end_date=2025-01-31" \
  -H "Content-Type: application/json" \
  -b cookies.txt
```

---

## Features

✅ **Project Analytics**
- Overall project statistics
- Detailed project summaries with budget analysis
- Project timeline visualization
- Tasks, timesheets, and expenses breakdown per project

✅ **Task Analytics**
- Overall task statistics
- User-specific task analytics with completion rates
- Task timeline by project
- Overdue task tracking
- Task distribution by state and priority

✅ **Timesheet Analytics**
- Overall timesheet statistics with billable/non-billable breakdown
- User-specific timesheet analytics
- Project-specific timesheet analytics
- Hours distribution by user and task
- Date range filtering support

✅ **Expense Analytics**
- Overall expense statistics
- Expense tracking by status (approved, pending, rejected)
- User-specific expense analytics
- Project-specific expense analytics
- Billable vs non-billable expense tracking
- Date range filtering support

✅ **Combined Dashboard**
- High-level overview of all analytics
- Financial summary with budget utilization
- Quick insights across projects, tasks, timesheets, and expenses

✅ **Advanced Features**
- Date range filtering for timesheets and expenses
- Budget utilization calculations
- Team productivity metrics
- Cost analysis and tracking
- Overdue task identification
- Completion rate calculations

---

## Query Parameters

Many analytics endpoints support optional query parameters for filtering:

- **start_date** (YYYY-MM-DD): Filter data from this date onwards
- **end_date** (YYYY-MM-DD): Filter data up to this date

Example:
```bash
curl -X GET "http://localhost:5000/analytics/timesheets/overview?start_date=2025-01-01&end_date=2025-03-31" \
  -H "Content-Type: application/json" \
  -b cookies.txt
```

---

## Use Cases

### 1. Project Manager Dashboard
- Get project summary to track budget, tasks, and team performance
- Monitor overdue tasks and pending expenses
- Analyze timesheet hours and costs

### 2. Resource Planning
- View user task analytics to balance workload
- Check user timesheet analytics for availability
- Track average hours per day per user

### 3. Financial Reporting
- Generate expense reports by project or user
- Track budget utilization across projects
- Analyze billable vs non-billable hours

### 4. Performance Tracking
- Monitor task completion rates by user
- Track project progress by task state
- Identify bottlenecks with overdue task analytics

---

## Notes

- All analytics endpoints require authentication
- Dates should be in ISO format (YYYY-MM-DD)
- Financial values are returned as floats
- Counts and IDs are returned as integers
- All datetime values are in ISO format
- Empty results return 0 or empty objects, never null
