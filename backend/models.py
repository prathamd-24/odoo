from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    managed_projects = db.relationship('Project', back_populates='project_manager', foreign_keys='Project.project_manager_id')
    project_memberships = db.relationship('ProjectMember', back_populates='user', cascade='all, delete-orphan')
    created_tasks = db.relationship('Task', back_populates='creator', foreign_keys='Task.created_by')
    task_assignments = db.relationship('TaskAssignment', back_populates='user', cascade='all, delete-orphan')
    task_comments = db.relationship('TaskComment', back_populates='user')
    uploaded_attachments = db.relationship('TaskAttachment', back_populates='uploader')
    timesheets = db.relationship('Timesheet', back_populates='user')
    submitted_expenses = db.relationship('Expense', back_populates='submitter', foreign_keys='Expense.submitted_by')
    approved_expenses = db.relationship('Expense', back_populates='approver', foreign_keys='Expense.approved_by')


class Project(db.Model):
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    project_code = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    project_manager_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    status = db.Column(db.String(50), default='active')
    budget_amount = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    project_manager = db.relationship('User', back_populates='managed_projects', foreign_keys=[project_manager_id])
    members = db.relationship('ProjectMember', back_populates='project', cascade='all, delete-orphan')
    tasks = db.relationship('Task', back_populates='project', cascade='all, delete-orphan')
    timesheets = db.relationship('Timesheet', back_populates='project')
    expenses = db.relationship('Expense', back_populates='project')


class ProjectMember(db.Model):
    __tablename__ = 'project_members'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    role_in_project = db.Column(db.String(100))
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    project = db.relationship('Project', back_populates='members')
    user = db.relationship('User', back_populates='project_memberships')


class Task(db.Model):
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    priority = db.Column(db.String(50), default='medium')
    state = db.Column(db.String(50), default='todo')
    due_date = db.Column(db.Date)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='RESTRICT'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    project = db.relationship('Project', back_populates='tasks')
    creator = db.relationship('User', back_populates='created_tasks', foreign_keys=[created_by])
    assignments = db.relationship('TaskAssignment', back_populates='task', cascade='all, delete-orphan')
    comments = db.relationship('TaskComment', back_populates='task', cascade='all, delete-orphan')
    attachments = db.relationship('TaskAttachment', back_populates='task', cascade='all, delete-orphan')
    timesheets = db.relationship('Timesheet', back_populates='task', cascade='all, delete-orphan')
    expenses = db.relationship('Expense', back_populates='task')


class TaskAssignment(db.Model):
    __tablename__ = 'task_assignments'
    
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    assigned_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    task = db.relationship('Task', back_populates='assignments')
    user = db.relationship('User', back_populates='task_assignments')


class TaskComment(db.Model):
    __tablename__ = 'task_comments'
    
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))
    comment = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    task = db.relationship('Task', back_populates='comments')
    user = db.relationship('User', back_populates='task_comments')


class TaskAttachment(db.Model):
    __tablename__ = 'task_attachments'
    
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id', ondelete='CASCADE'), nullable=False)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))
    file_name = db.Column(db.String(255), nullable=False)
    file_url = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    task = db.relationship('Task', back_populates='attachments')
    uploader = db.relationship('User', back_populates='uploaded_attachments')


class Timesheet(db.Model):
    __tablename__ = 'timesheets'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id', ondelete='RESTRICT'), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id', ondelete='CASCADE'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='RESTRICT'), nullable=False)
    work_date = db.Column(db.Date, nullable=False)
    hours = db.Column(db.Float, nullable=False)
    billable = db.Column(db.Boolean, default=True)
    internal_cost_rate = db.Column(db.Float)
    cost_amount = db.Column(db.Float)
    status = db.Column(db.String(50), default='draft')
    linked_invoice_line_id = db.Column(db.Integer)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    project = db.relationship('Project', back_populates='timesheets')
    task = db.relationship('Task', back_populates='timesheets')
    user = db.relationship('User', back_populates='timesheets')


class Expense(db.Model):
    __tablename__ = 'expenses'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id', ondelete='RESTRICT'), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id', ondelete='SET NULL'))
    submitted_by = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='RESTRICT'), nullable=False)
    approved_by = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))
    expense_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    billable = db.Column(db.Boolean, default=True)
    status = db.Column(db.String(50), default='pending')
    receipt_url = db.Column(db.String(500))
    linked_invoice_line_id = db.Column(db.Integer)
    
    # Relationships
    project = db.relationship('Project', back_populates='expenses')
    task = db.relationship('Task', back_populates='expenses')
    submitter = db.relationship('User', back_populates='submitted_expenses', foreign_keys=[submitted_by])
    approver = db.relationship('User', back_populates='approved_expenses', foreign_keys=[approved_by])
