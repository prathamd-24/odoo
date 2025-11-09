# Project Management API - Complete Documentation

A comprehensive Flask application with SQLAlchemy for project management, task tracking, and expense management with session-based authentication.

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

The server will start on `http://localhost:5000`

## Database Schema

The application uses SQLite with the following tables:

### users
- `id`, `email`, `password_hash`, `is_active`, `created_at`

### projects
- `id`, `project_code`, `name`, `description`, `project_manager_id` (FK), `start_date`, `end_date`, `status`, `budget_amount`, `created_at`, `updated_at`

### project_members
- `id`, `project_id` (FK), `user_id` (FK), `role_in_project`, `added_at`

### tasks
- `id`, `project_id` (FK), `title`, `description`, `priority`, `state`, `due_date`, `created_by` (FK), `created_at`, `updated_at`

### task_assignments
- `id`, `task_id` (FK), `user_id` (FK), `assigned_at`

### task_comments
- `id`, `task_id` (FK), `user_id` (FK), `comment`, `created_at`

### task_attachments
- `id`, `task_id` (FK), `uploaded_by` (FK), `file_name`, `file_url`, `created_at`

### timesheets
- `id`, `project_id` (FK), `task_id` (FK), `user_id` (FK), `work_date`, `hours`, `billable`, `internal_cost_rate`, `cost_amount`, `status`, `linked_invoice_line_id`, `notes`, `created_at`

### expenses
- `id`, `project_id` (FK), `task_id` (FK), `submitted_by` (FK), `approved_by` (FK), `expense_date`, `description`, `amount`, `billable`, `status`, `receipt_url`, `linked_invoice_line_id`

---

## Authentication Endpoints

### 1. Register User
**POST** `/register`

```bash
curl -X POST http://localhost:5000/register \
  -H "Content-Type: application/json" \
  -d '{"email": "john@example.com", "password": "pass123"}'
```

**Response (201):**
```json
{
  "message": "User registered successfully",
  "user": {"id": 1, "email": "john@example.com", "is_active": true}
}
```

### 2. Login
**POST** `/login`

```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{"email": "john@example.com", "password": "pass123"}'
```

**Response (200):**
```json
{
  "message": "Login successful",
  "user": {"id": 1, "email": "john@example.com", "is_active": true}
}
```

### 3. Logout
**POST** `/logout`

```bash
curl -X POST http://localhost:5000/logout \
  -H "Content-Type: application/json" \
  -b cookies.txt
```

---

## Project Management Endpoints

### 4. Create Project
**POST** `/projects`

```bash
curl -X POST http://localhost:5000/projects \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "project_code": "PROJ001",
    "name": "Website Redesign",
    "description": "Complete website redesign project",
    "project_manager_id": 1,
    "start_date": "2025-01-01",
    "end_date": "2025-06-30",
    "status": "active",
    "budget_amount": 50000.00
  }'
```

**Response (201):**
```json
{
  "message": "Project created successfully",
  "project": {
    "id": 1,
    "project_code": "PROJ001",
    "name": "Website Redesign",
    "description": "Complete website redesign project",
    "project_manager_id": 1,
    "start_date": "2025-01-01",
    "end_date": "2025-06-30",
    "status": "active",
    "budget_amount": 50000.0
  }
}
```

### 5. Get All Projects
**GET** `/projects`

```bash
curl -X GET http://localhost:5000/projects \
  -H "Content-Type: application/json" \
  -b cookies.txt
```

**Response (200):**
```json
{
  "projects": [
    {
      "id": 1,
      "project_code": "PROJ001",
      "name": "Website Redesign",
      "description": "Complete website redesign project",
      "project_manager_id": 1,
      "start_date": "2025-01-01",
      "end_date": "2025-06-30",
      "status": "active",
      "budget_amount": 50000.0,
      "created_at": "2025-11-08T10:30:45.123456"
    }
  ]
}
```

### 6. Get Specific Project
**GET** `/projects/<project_id>`

```bash
curl -X GET http://localhost:5000/projects/1 \
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
    "description": "Complete website redesign project",
    "project_manager_id": 1,
    "project_manager_email": "john@example.com",
    "start_date": "2025-01-01",
    "end_date": "2025-06-30",
    "status": "active",
    "budget_amount": 50000.0,
    "created_at": "2025-11-08T10:30:45.123456",
    "members": [
      {
        "id": 1,
        "user_id": 2,
        "user_email": "jane@example.com",
        "role_in_project": "Developer",
        "added_at": "2025-11-08T11:00:00.000000"
      }
    ]
  }
}
```

### 7. Update Project
**PUT** `/projects/<project_id>`

```bash
curl -X PUT http://localhost:5000/projects/1 \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "status": "in_progress",
    "budget_amount": 55000.00
  }'
```

**Response (200):**
```json
{
  "message": "Project updated successfully",
  "project": {
    "id": 1,
    "project_code": "PROJ001",
    "name": "Website Redesign",
    "status": "in_progress"
  }
}
```

### 8. Delete Project
**DELETE** `/projects/<project_id>`

```bash
curl -X DELETE http://localhost:5000/projects/1 \
  -H "Content-Type: application/json" \
  -b cookies.txt
```

**Response (200):**
```json
{
  "message": "Project deleted successfully"
}
```

### 9. Get User's Projects
**GET** `/users/<user_id>/projects`

```bash
curl -X GET http://localhost:5000/users/1/projects \
  -H "Content-Type: application/json" \
  -b cookies.txt
```

**Response (200):**
```json
{
  "user_id": 1,
  "email": "john@example.com",
  "managed_projects": [
    {
      "id": 1,
      "project_code": "PROJ001",
      "name": "Website Redesign",
      "description": "Complete website redesign project",
      "role": "Project Manager",
      "status": "active",
      "start_date": "2025-01-01",
      "end_date": "2025-06-30",
      "budget_amount": 50000.0
    }
  ],
  "member_projects": [
    {
      "id": 2,
      "project_code": "PROJ002",
      "name": "Mobile App",
      "description": "Mobile app development",
      "role": "Developer",
      "status": "active",
      "start_date": "2025-02-01",
      "end_date": "2025-08-31",
      "added_at": "2025-11-08T11:00:00.000000"
    }
  ],
  "total_projects": 2
}
```

---

## Project Members Endpoints

### 10. Add Project Member
**POST** `/projects/<project_id>/members`

```bash
curl -X POST http://localhost:5000/projects/1/members \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "user_id": 2,
    "role_in_project": "Developer"
  }'
```

**Response (201):**
```json
{
  "message": "Member added successfully",
  "member": {
    "id": 1,
    "project_id": 1,
    "user_id": 2,
    "user_email": "jane@example.com",
    "role_in_project": "Developer",
    "added_at": "2025-11-08T11:00:00.000000"
  }
}
```

### 11. Remove Project Member
**DELETE** `/projects/<project_id>/members/<member_id>`

```bash
curl -X DELETE http://localhost:5000/projects/1/members/1 \
  -H "Content-Type: application/json" \
  -b cookies.txt
```

**Response (200):**
```json
{
  "message": "Member removed successfully"
}
```

---

## Task Management Endpoints

### 12. Create Task
**POST** `/projects/<project_id>/tasks`

```bash
curl -X POST http://localhost:5000/projects/1/tasks \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "title": "Design Homepage",
    "description": "Create mockups for new homepage design",
    "priority": "high",
    "state": "todo",
    "due_date": "2025-01-15"
  }'
```

**Response (201):**
```json
{
  "message": "Task created successfully",
  "task": {
    "id": 1,
    "project_id": 1,
    "title": "Design Homepage",
    "description": "Create mockups for new homepage design",
    "priority": "high",
    "state": "todo",
    "due_date": "2025-01-15",
    "created_by": 1
  }
}
```

### 13. Get Project Tasks
**GET** `/projects/<project_id>/tasks`

```bash
curl -X GET http://localhost:5000/projects/1/tasks \
  -H "Content-Type: application/json" \
  -b cookies.txt
```

**Response (200):**
```json
{
  "project_id": 1,
  "tasks": [
    {
      "id": 1,
      "title": "Design Homepage",
      "description": "Create mockups for new homepage design",
      "priority": "high",
      "state": "todo",
      "due_date": "2025-01-15",
      "created_by": 1,
      "creator_email": "john@example.com",
      "created_at": "2025-11-08T10:30:45.123456",
      "assignments_count": 2,
      "comments_count": 5
    }
  ]
}
```

### 14. Get Specific Task
**GET** `/tasks/<task_id>`

```bash
curl -X GET http://localhost:5000/tasks/1 \
  -H "Content-Type: application/json" \
  -b cookies.txt
```

**Response (200):**
```json
{
  "task": {
    "id": 1,
    "project_id": 1,
    "project_name": "Website Redesign",
    "title": "Design Homepage",
    "description": "Create mockups for new homepage design",
    "priority": "high",
    "state": "todo",
    "due_date": "2025-01-15",
    "created_by": 1,
    "creator_email": "john@example.com",
    "created_at": "2025-11-08T10:30:45.123456",
    "updated_at": "2025-11-08T10:30:45.123456",
    "assignments": [
      {
        "id": 1,
        "user_id": 2,
        "user_email": "jane@example.com",
        "assigned_at": "2025-11-08T11:00:00.000000"
      }
    ],
    "comments": [
      {
        "id": 1,
        "user_id": 2,
        "user_email": "jane@example.com",
        "comment": "Started working on this",
        "created_at": "2025-11-08T12:00:00.000000"
      }
    ],
    "attachments": [
      {
        "id": 1,
        "file_name": "design_mockup.png",
        "file_url": "https://example.com/files/mockup.png",
        "uploaded_by": 2,
        "uploader_email": "jane@example.com",
        "created_at": "2025-11-08T13:00:00.000000"
      }
    ]
  }
}
```

### 15. Update Task
**PUT** `/tasks/<task_id>`

```bash
curl -X PUT http://localhost:5000/tasks/1 \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "state": "in_progress",
    "priority": "urgent"
  }'
```

**Response (200):**
```json
{
  "message": "Task updated successfully",
  "task": {
    "id": 1,
    "title": "Design Homepage",
    "state": "in_progress",
    "priority": "urgent"
  }
}
```

### 16. Delete Task
**DELETE** `/tasks/<task_id>`

```bash
curl -X DELETE http://localhost:5000/tasks/1 \
  -H "Content-Type: application/json" \
  -b cookies.txt
```

**Response (200):**
```json
{
  "message": "Task deleted successfully"
}
```

### 17. Get User's Tasks
**GET** `/users/<user_id>/tasks`

```bash
curl -X GET http://localhost:5000/users/2/tasks \
  -H "Content-Type: application/json" \
  -b cookies.txt
```

**Response (200):**
```json
{
  "user_id": 2,
  "email": "jane@example.com",
  "assigned_tasks": [
    {
      "id": 1,
      "title": "Design Homepage",
      "description": "Create mockups for new homepage design",
      "priority": "high",
      "state": "in_progress",
      "due_date": "2025-01-15",
      "project_id": 1,
      "project_name": "Website Redesign",
      "assigned_at": "2025-11-08T11:00:00.000000"
    }
  ],
  "total_tasks": 1
}
```

---

## Task Assignment Endpoints

### 18. Assign Task to User
**POST** `/tasks/<task_id>/assignments`

```bash
curl -X POST http://localhost:5000/tasks/1/assignments \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"user_id": 2}'
```

**Response (201):**
```json
{
  "message": "Task assigned successfully",
  "assignment": {
    "id": 1,
    "task_id": 1,
    "user_id": 2,
    "user_email": "jane@example.com",
    "assigned_at": "2025-11-08T11:00:00.000000"
  }
}
```

### 19. Unassign Task
**DELETE** `/tasks/<task_id>/assignments/<assignment_id>`

```bash
curl -X DELETE http://localhost:5000/tasks/1/assignments/1 \
  -H "Content-Type: application/json" \
  -b cookies.txt
```

**Response (200):**
```json
{
  "message": "Assignment removed successfully"
}
```

---

## Task Comments Endpoints

### 20. Add Task Comment
**POST** `/tasks/<task_id>/comments`

```bash
curl -X POST http://localhost:5000/tasks/1/comments \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"comment": "Started working on the homepage mockups"}'
```

**Response (201):**
```json
{
  "message": "Comment added successfully",
  "comment": {
    "id": 1,
    "task_id": 1,
    "user_id": 2,
    "user_email": "jane@example.com",
    "comment": "Started working on the homepage mockups",
    "created_at": "2025-11-08T12:00:00.000000"
  }
}
```

### 21. Get Task Comments
**GET** `/tasks/<task_id>/comments`

```bash
curl -X GET http://localhost:5000/tasks/1/comments \
  -H "Content-Type: application/json" \
  -b cookies.txt
```

**Response (200):**
```json
{
  "task_id": 1,
  "comments": [
    {
      "id": 1,
      "user_id": 2,
      "user_email": "jane@example.com",
      "comment": "Started working on the homepage mockups",
      "created_at": "2025-11-08T12:00:00.000000"
    }
  ]
}
```

### 22. Delete Task Comment
**DELETE** `/tasks/<task_id>/comments/<comment_id>`

```bash
curl -X DELETE http://localhost:5000/tasks/1/comments/1 \
  -H "Content-Type: application/json" \
  -b cookies.txt
```

**Response (200):**
```json
{
  "message": "Comment deleted successfully"
}
```

---

## Task Attachments Endpoints

### 23. Add Task Attachment
**POST** `/tasks/<task_id>/attachments`

```bash
curl -X POST http://localhost:5000/tasks/1/attachments \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "file_name": "homepage_mockup.png",
    "file_url": "https://example.com/files/mockup.png"
  }'
```

**Response (201):**
```json
{
  "message": "Attachment added successfully",
  "attachment": {
    "id": 1,
    "task_id": 1,
    "file_name": "homepage_mockup.png",
    "file_url": "https://example.com/files/mockup.png",
    "uploaded_by": 2,
    "created_at": "2025-11-08T13:00:00.000000"
  }
}
```

### 24. Delete Task Attachment
**DELETE** `/tasks/<task_id>/attachments/<attachment_id>`

```bash
curl -X DELETE http://localhost:5000/tasks/1/attachments/1 \
  -H "Content-Type: application/json" \
  -b cookies.txt
```

**Response (200):**
```json
{
  "message": "Attachment deleted successfully"
}
```

---

## Expense Management Endpoints

### 25. Create Expense
**POST** `/projects/<project_id>/expenses`

```bash
curl -X POST http://localhost:5000/projects/1/expenses \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "task_id": 1,
    "expense_date": "2025-01-10",
    "description": "Design software license",
    "amount": 299.99,
    "billable": true,
    "status": "pending",
    "receipt_url": "https://example.com/receipts/receipt1.pdf"
  }'
```

**Response (201):**
```json
{
  "message": "Expense created successfully",
  "expense": {
    "id": 1,
    "project_id": 1,
    "task_id": 1,
    "submitted_by": 2,
    "expense_date": "2025-01-10",
    "description": "Design software license",
    "amount": 299.99,
    "billable": true,
    "status": "pending"
  }
}
```

### 26. Get Project Expenses
**GET** `/projects/<project_id>/expenses`

```bash
curl -X GET http://localhost:5000/projects/1/expenses \
  -H "Content-Type: application/json" \
  -b cookies.txt
```

**Response (200):**
```json
{
  "project_id": 1,
  "expenses": [
    {
      "id": 1,
      "task_id": 1,
      "task_title": "Design Homepage",
      "submitted_by": 2,
      "submitter_email": "jane@example.com",
      "approved_by": null,
      "approver_email": null,
      "expense_date": "2025-01-10",
      "description": "Design software license",
      "amount": 299.99,
      "billable": true,
      "status": "pending",
      "receipt_url": "https://example.com/receipts/receipt1.pdf"
    }
  ],
  "total_amount": 299.99
}
```

### 27. Get Specific Expense
**GET** `/expenses/<expense_id>`

```bash
curl -X GET http://localhost:5000/expenses/1 \
  -H "Content-Type: application/json" \
  -b cookies.txt
```

**Response (200):**
```json
{
  "expense": {
    "id": 1,
    "project_id": 1,
    "project_name": "Website Redesign",
    "task_id": 1,
    "task_title": "Design Homepage",
    "submitted_by": 2,
    "submitter_email": "jane@example.com",
    "approved_by": 1,
    "approver_email": "john@example.com",
    "expense_date": "2025-01-10",
    "description": "Design software license",
    "amount": 299.99,
    "billable": true,
    "status": "approved",
    "receipt_url": "https://example.com/receipts/receipt1.pdf"
  }
}
```

### 28. Update Expense
**PUT** `/expenses/<expense_id>`

```bash
curl -X PUT http://localhost:5000/expenses/1 \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "status": "approved",
    "approved_by": 1
  }'
```

**Response (200):**
```json
{
  "message": "Expense updated successfully",
  "expense": {
    "id": 1,
    "description": "Design software license",
    "amount": 299.99,
    "status": "approved"
  }
}
```

### 29. Delete Expense
**DELETE** `/expenses/<expense_id>`

```bash
curl -X DELETE http://localhost:5000/expenses/1 \
  -H "Content-Type: application/json" \
  -b cookies.txt
```

**Response (200):**
```json
{
  "message": "Expense deleted successfully"
}
```

### 30. Get User's Expenses
**GET** `/users/<user_id>/expenses`

```bash
curl -X GET http://localhost:5000/users/2/expenses \
  -H "Content-Type: application/json" \
  -b cookies.txt
```

**Response (200):**
```json
{
  "user_id": 2,
  "email": "jane@example.com",
  "expenses": [
    {
      "id": 1,
      "project_id": 1,
      "project_name": "Website Redesign",
      "task_id": 1,
      "task_title": "Design Homepage",
      "expense_date": "2025-01-10",
      "description": "Design software license",
      "amount": 299.99,
      "billable": true,
      "status": "approved",
      "approved_by": 1,
      "approver_email": "john@example.com"
    }
  ],
  "total_expenses": 1,
  "total_amount": 299.99
}
```

---

## Complete Testing Flow

```bash
# 1. Register users
curl -X POST http://localhost:5000/register \
  -H "Content-Type: application/json" \
  -d '{"email": "john@example.com", "password": "pass123"}'

curl -X POST http://localhost:5000/register \
  -H "Content-Type: application/json" \
  -d '{"email": "jane@example.com", "password": "pass456"}'

# 2. Login as john
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{"email": "john@example.com", "password": "pass123"}'

# 3. Create a project
curl -X POST http://localhost:5000/projects \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"project_code": "PROJ001", "name": "Website Redesign", "description": "Complete redesign", "project_manager_id": 1, "start_date": "2025-01-01", "end_date": "2025-06-30", "status": "active", "budget_amount": 50000.00}'

# 4. Add jane as project member
curl -X POST http://localhost:5000/projects/1/members \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"user_id": 2, "role_in_project": "Developer"}'

# 5. Create a task
curl -X POST http://localhost:5000/projects/1/tasks \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"title": "Design Homepage", "description": "Create mockups", "priority": "high", "state": "todo", "due_date": "2025-01-15"}'

# 6. Assign task to jane
curl -X POST http://localhost:5000/tasks/1/assignments \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"user_id": 2}'

# 7. Add comment to task
curl -X POST http://localhost:5000/tasks/1/comments \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"comment": "Started working on this task"}'

# 8. Add attachment to task
curl -X POST http://localhost:5000/tasks/1/attachments \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"file_name": "mockup.png", "file_url": "https://example.com/mockup.png"}'

# 9. Create an expense
curl -X POST http://localhost:5000/projects/1/expenses \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"task_id": 1, "expense_date": "2025-01-10", "description": "Design software", "amount": 299.99, "billable": true, "status": "pending"}'

# 10. Get john's projects
curl -X GET http://localhost:5000/users/1/projects \
  -H "Content-Type: application/json" \
  -b cookies.txt

# 11. Get jane's tasks
curl -X GET http://localhost:5000/users/2/tasks \
  -H "Content-Type: application/json" \
  -b cookies.txt

# 12. Get task with all details
curl -X GET http://localhost:5000/tasks/1 \
  -H "Content-Type: application/json" \
  -b cookies.txt

# 13. Get project expenses
curl -X GET http://localhost:5000/projects/1/expenses \
  -H "Content-Type: application/json" \
  -b cookies.txt

# 14. Get user's expenses
curl -X GET http://localhost:5000/users/1/expenses \
  -H "Content-Type: application/json" \
  -b cookies.txt

# 15. Update task status
curl -X PUT http://localhost:5000/tasks/1 \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"state": "in_progress"}'

# 16. Approve expense
curl -X PUT http://localhost:5000/expenses/1 \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"status": "approved", "approved_by": 1}'
```

---

## Features

✅ **User Management**
- Registration, login, logout with session-based auth
- Password hashing

✅ **Project Management**
- Full CRUD operations for projects
- Project members management
- Get all projects for a user (as manager or member)

✅ **Task Management**
- Full CRUD operations for tasks
- Task assignments to users
- Task comments with user tracking
- Task attachments
- Get all tasks assigned to a user
- Get tasks by project

✅ **Expense Management**
- Full CRUD operations for expenses
- Link expenses to projects and tasks
- Expense approval workflow
- Get all expenses for a project
- Get all expenses submitted by a user
- Track billable vs non-billable expenses

✅ **Relationships**
- Projects linked to managers and members
- Tasks linked to projects, creators, and assignees
- Comments and attachments linked to tasks and users
- Expenses linked to projects, tasks, submitters, and approvers

---

## Database Relationships

- **Users** can manage multiple projects
- **Users** can be members of multiple projects
- **Projects** have many tasks
- **Tasks** can be assigned to multiple users
- **Tasks** can have multiple comments and attachments
- **Expenses** are linked to projects, tasks, and users
- All foreign keys respect cascading delete rules as per schema

---

## Notes

- Session-based authentication with cookies
- SQLite database created automatically
- All protected routes require login
- Proper foreign key relationships with cascade rules
- ISO format dates for all datetime fields
- Comprehensive error handling
