from flask import Blueprint, request, jsonify, session
from models import db, Project, Task, TaskAssignment, Timesheet, Expense, User
from sqlalchemy import func, case, extract
from datetime import datetime, timedelta
import calendar

analytics_bp = Blueprint('analytics', __name__)

# Helper function to check authentication
def require_auth():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    return None


# ==================== PROJECT ANALYTICS ====================

@analytics_bp.route('/analytics/projects/overview', methods=['GET'])
def projects_overview():
    """Get overall project statistics"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    total_projects = Project.query.count()
    
    # Projects by status
    status_counts = db.session.query(
        Project.status,
        func.count(Project.id)
    ).group_by(Project.status).all()
    
    # Total budget
    total_budget = db.session.query(func.sum(Project.budget_amount)).scalar() or 0
    
    # Average project duration (in days)
    projects_with_dates = Project.query.filter(
        Project.start_date.isnot(None),
        Project.end_date.isnot(None)
    ).all()
    
    avg_duration = 0
    if projects_with_dates:
        durations = [(p.end_date - p.start_date).days for p in projects_with_dates]
        avg_duration = sum(durations) / len(durations)
    
    return jsonify({
        'total_projects': total_projects,
        'projects_by_status': {status: count for status, count in status_counts},
        'total_budget': total_budget,
        'average_duration_days': round(avg_duration, 2)
    }), 200


@analytics_bp.route('/analytics/projects/<int:project_id>/summary', methods=['GET'])
def project_summary(project_id):
    """Get detailed analytics for a specific project"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    project = Project.query.get(project_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    
    # Task statistics
    total_tasks = Task.query.filter_by(project_id=project_id).count()
    
    tasks_by_state = db.session.query(
        Task.state,
        func.count(Task.id)
    ).filter(Task.project_id == project_id).group_by(Task.state).all()
    
    tasks_by_priority = db.session.query(
        Task.priority,
        func.count(Task.id)
    ).filter(Task.project_id == project_id).group_by(Task.priority).all()
    
    # Overdue tasks
    overdue_tasks = Task.query.filter(
        Task.project_id == project_id,
        Task.due_date < datetime.now().date(),
        Task.state.notin_(['done', 'completed', 'closed'])
    ).count()
    
    # Timesheet statistics
    total_hours = db.session.query(func.sum(Timesheet.hours)).filter(
        Timesheet.project_id == project_id
    ).scalar() or 0
    
    billable_hours = db.session.query(func.sum(Timesheet.hours)).filter(
        Timesheet.project_id == project_id,
        Timesheet.billable == True
    ).scalar() or 0
    
    total_cost = db.session.query(func.sum(Timesheet.cost_amount)).filter(
        Timesheet.project_id == project_id
    ).scalar() or 0
    
    # Expense statistics
    total_expenses = db.session.query(func.sum(Expense.amount)).filter(
        Expense.project_id == project_id
    ).scalar() or 0
    
    approved_expenses = db.session.query(func.sum(Expense.amount)).filter(
        Expense.project_id == project_id,
        Expense.status == 'approved'
    ).scalar() or 0
    
    billable_expenses = db.session.query(func.sum(Expense.amount)).filter(
        Expense.project_id == project_id,
        Expense.billable == True
    ).scalar() or 0
    
    # Team members count
    team_size = len(project.members) + (1 if project.project_manager_id else 0)
    
    # Project duration
    duration_days = None
    if project.start_date and project.end_date:
        duration_days = (project.end_date - project.start_date).days
    
    return jsonify({
        'project': {
            'id': project.id,
            'project_code': project.project_code,
            'name': project.name,
            'status': project.status,
            'budget_amount': project.budget_amount,
            'start_date': project.start_date.isoformat() if project.start_date else None,
            'end_date': project.end_date.isoformat() if project.end_date else None,
            'duration_days': duration_days
        },
        'team': {
            'team_size': team_size,
            'project_manager_id': project.project_manager_id
        },
        'tasks': {
            'total_tasks': total_tasks,
            'overdue_tasks': overdue_tasks,
            'by_state': {state: count for state, count in tasks_by_state},
            'by_priority': {priority: count for priority, count in tasks_by_priority}
        },
        'timesheets': {
            'total_hours': float(total_hours),
            'billable_hours': float(billable_hours),
            'non_billable_hours': float(total_hours - billable_hours),
            'total_cost': float(total_cost)
        },
        'expenses': {
            'total_expenses': float(total_expenses),
            'approved_expenses': float(approved_expenses),
            'pending_expenses': float(total_expenses - approved_expenses),
            'billable_expenses': float(billable_expenses)
        },
        'budget_analysis': {
            'budget_amount': float(project.budget_amount),
            'total_cost': float(total_cost + total_expenses),
            'remaining_budget': float(project.budget_amount - (total_cost + total_expenses)),
            'budget_utilization_percent': round((total_cost + total_expenses) / project.budget_amount * 100, 2) if project.budget_amount > 0 else 0
        }
    }), 200


@analytics_bp.route('/analytics/projects/timeline', methods=['GET'])
def projects_timeline():
    """Get project timeline data"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    projects = Project.query.filter(
        Project.start_date.isnot(None),
        Project.end_date.isnot(None)
    ).all()
    
    timeline = [{
        'id': p.id,
        'project_code': p.project_code,
        'name': p.name,
        'status': p.status,
        'start_date': p.start_date.isoformat(),
        'end_date': p.end_date.isoformat(),
        'duration_days': (p.end_date - p.start_date).days,
        'budget_amount': float(p.budget_amount)
    } for p in projects]
    
    return jsonify({
        'timeline': timeline,
        'total_projects': len(timeline)
    }), 200


# ==================== TASK ANALYTICS ====================

@analytics_bp.route('/analytics/tasks/overview', methods=['GET'])
def tasks_overview():
    """Get overall task statistics"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    total_tasks = Task.query.count()
    
    # Tasks by state
    tasks_by_state = db.session.query(
        Task.state,
        func.count(Task.id)
    ).group_by(Task.state).all()
    
    # Tasks by priority
    tasks_by_priority = db.session.query(
        Task.priority,
        func.count(Task.id)
    ).group_by(Task.priority).all()
    
    # Overdue tasks
    overdue_tasks = Task.query.filter(
        Task.due_date < datetime.now().date(),
        Task.state.notin_(['done', 'completed', 'closed'])
    ).count()
    
    # Tasks due this week
    today = datetime.now().date()
    week_end = today + timedelta(days=7)
    tasks_due_this_week = Task.query.filter(
        Task.due_date >= today,
        Task.due_date <= week_end,
        Task.state.notin_(['done', 'completed', 'closed'])
    ).count()
    
    # Average task assignments
    avg_assignments = db.session.query(
        func.avg(func.count(TaskAssignment.id))
    ).group_by(TaskAssignment.task_id).scalar() or 0
    
    return jsonify({
        'total_tasks': total_tasks,
        'overdue_tasks': overdue_tasks,
        'tasks_due_this_week': tasks_due_this_week,
        'tasks_by_state': {state: count for state, count in tasks_by_state},
        'tasks_by_priority': {priority: count for priority, count in tasks_by_priority},
        'average_assignments_per_task': round(float(avg_assignments), 2)
    }), 200


@analytics_bp.route('/analytics/tasks/user/<int:user_id>', methods=['GET'])
def user_task_analytics(user_id):
    """Get task analytics for a specific user"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Get user's task assignments
    assignments = TaskAssignment.query.filter_by(user_id=user_id).all()
    task_ids = [a.task_id for a in assignments]
    
    if not task_ids:
        return jsonify({
            'user_id': user_id,
            'email': user.email,
            'total_assigned_tasks': 0,
            'tasks_by_state': {},
            'tasks_by_priority': {},
            'overdue_tasks': 0
        }), 200
    
    # Tasks by state
    tasks_by_state = db.session.query(
        Task.state,
        func.count(Task.id)
    ).filter(Task.id.in_(task_ids)).group_by(Task.state).all()
    
    # Tasks by priority
    tasks_by_priority = db.session.query(
        Task.priority,
        func.count(Task.id)
    ).filter(Task.id.in_(task_ids)).group_by(Task.priority).all()
    
    # Overdue tasks
    overdue_tasks = Task.query.filter(
        Task.id.in_(task_ids),
        Task.due_date < datetime.now().date(),
        Task.state.notin_(['done', 'completed', 'closed'])
    ).count()
    
    # Completion rate
    completed_tasks = Task.query.filter(
        Task.id.in_(task_ids),
        Task.state.in_(['done', 'completed', 'closed'])
    ).count()
    
    completion_rate = (completed_tasks / len(task_ids) * 100) if task_ids else 0
    
    return jsonify({
        'user_id': user_id,
        'email': user.email,
        'total_assigned_tasks': len(task_ids),
        'completed_tasks': completed_tasks,
        'completion_rate_percent': round(completion_rate, 2),
        'overdue_tasks': overdue_tasks,
        'tasks_by_state': {state: count for state, count in tasks_by_state},
        'tasks_by_priority': {priority: count for priority, count in tasks_by_priority}
    }), 200


@analytics_bp.route('/analytics/tasks/project/<int:project_id>/timeline', methods=['GET'])
def project_task_timeline(project_id):
    """Get task timeline for a project"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    project = Project.query.get(project_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    
    tasks = Task.query.filter_by(project_id=project_id).filter(
        Task.due_date.isnot(None)
    ).order_by(Task.due_date).all()
    
    timeline = [{
        'id': t.id,
        'title': t.title,
        'priority': t.priority,
        'state': t.state,
        'due_date': t.due_date.isoformat(),
        'created_at': t.created_at.isoformat(),
        'is_overdue': t.due_date < datetime.now().date() and t.state not in ['done', 'completed', 'closed'],
        'assigned_users_count': len(t.assignments)
    } for t in tasks]
    
    return jsonify({
        'project_id': project_id,
        'project_name': project.name,
        'task_timeline': timeline,
        'total_tasks': len(timeline)
    }), 200


# ==================== TIMESHEET ANALYTICS ====================

@analytics_bp.route('/analytics/timesheets/overview', methods=['GET'])
def timesheets_overview():
    """Get overall timesheet statistics"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    # Get date range from query params
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = Timesheet.query
    
    if start_date:
        query = query.filter(Timesheet.work_date >= datetime.strptime(start_date, '%Y-%m-%d').date())
    if end_date:
        query = query.filter(Timesheet.work_date <= datetime.strptime(end_date, '%Y-%m-%d').date())
    
    total_hours = db.session.query(func.sum(Timesheet.hours)).filter(
        query.whereclause if query.whereclause is not None else True
    ).scalar() or 0
    
    billable_hours = db.session.query(func.sum(Timesheet.hours)).filter(
        Timesheet.billable == True
    )
    if start_date:
        billable_hours = billable_hours.filter(Timesheet.work_date >= datetime.strptime(start_date, '%Y-%m-%d').date())
    if end_date:
        billable_hours = billable_hours.filter(Timesheet.work_date <= datetime.strptime(end_date, '%Y-%m-%d').date())
    billable_hours = billable_hours.scalar() or 0
    
    total_cost = db.session.query(func.sum(Timesheet.cost_amount)).filter(
        query.whereclause if query.whereclause is not None else True
    ).scalar() or 0
    
    # Hours by project
    hours_by_project = db.session.query(
        Project.name,
        func.sum(Timesheet.hours)
    ).join(Project).group_by(Project.id, Project.name)
    
    if start_date:
        hours_by_project = hours_by_project.filter(Timesheet.work_date >= datetime.strptime(start_date, '%Y-%m-%d').date())
    if end_date:
        hours_by_project = hours_by_project.filter(Timesheet.work_date <= datetime.strptime(end_date, '%Y-%m-%d').date())
    
    hours_by_project = hours_by_project.all()
    
    return jsonify({
        'total_hours': float(total_hours),
        'billable_hours': float(billable_hours),
        'non_billable_hours': float(total_hours - billable_hours),
        'billable_percentage': round((billable_hours / total_hours * 100) if total_hours > 0 else 0, 2),
        'total_cost': float(total_cost),
        'hours_by_project': {name: float(hours) for name, hours in hours_by_project},
        'filters': {
            'start_date': start_date,
            'end_date': end_date
        }
    }), 200


@analytics_bp.route('/analytics/timesheets/user/<int:user_id>', methods=['GET'])
def user_timesheet_analytics(user_id):
    """Get timesheet analytics for a specific user"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Get date range from query params
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = Timesheet.query.filter_by(user_id=user_id)
    
    if start_date:
        query = query.filter(Timesheet.work_date >= datetime.strptime(start_date, '%Y-%m-%d').date())
    if end_date:
        query = query.filter(Timesheet.work_date <= datetime.strptime(end_date, '%Y-%m-%d').date())
    
    total_hours = db.session.query(func.sum(Timesheet.hours)).filter(
        query.whereclause
    ).scalar() or 0
    
    billable_hours = db.session.query(func.sum(Timesheet.hours)).filter(
        Timesheet.user_id == user_id,
        Timesheet.billable == True
    )
    if start_date:
        billable_hours = billable_hours.filter(Timesheet.work_date >= datetime.strptime(start_date, '%Y-%m-%d').date())
    if end_date:
        billable_hours = billable_hours.filter(Timesheet.work_date <= datetime.strptime(end_date, '%Y-%m-%d').date())
    billable_hours = billable_hours.scalar() or 0
    
    # Hours by project
    hours_by_project = db.session.query(
        Project.name,
        func.sum(Timesheet.hours)
    ).join(Project).filter(Timesheet.user_id == user_id)
    
    if start_date:
        hours_by_project = hours_by_project.filter(Timesheet.work_date >= datetime.strptime(start_date, '%Y-%m-%d').date())
    if end_date:
        hours_by_project = hours_by_project.filter(Timesheet.work_date <= datetime.strptime(end_date, '%Y-%m-%d').date())
    
    hours_by_project = hours_by_project.group_by(Project.id, Project.name).all()
    
    # Average hours per day
    days_worked = db.session.query(func.count(func.distinct(Timesheet.work_date))).filter(
        query.whereclause
    ).scalar() or 0
    
    avg_hours_per_day = (total_hours / days_worked) if days_worked > 0 else 0
    
    return jsonify({
        'user_id': user_id,
        'email': user.email,
        'total_hours': float(total_hours),
        'billable_hours': float(billable_hours),
        'non_billable_hours': float(total_hours - billable_hours),
        'days_worked': days_worked,
        'average_hours_per_day': round(float(avg_hours_per_day), 2),
        'hours_by_project': {name: float(hours) for name, hours in hours_by_project},
        'filters': {
            'start_date': start_date,
            'end_date': end_date
        }
    }), 200


@analytics_bp.route('/analytics/timesheets/project/<int:project_id>', methods=['GET'])
def project_timesheet_analytics(project_id):
    """Get timesheet analytics for a specific project"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    project = Project.query.get(project_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    
    # Get date range from query params
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = Timesheet.query.filter_by(project_id=project_id)
    
    if start_date:
        query = query.filter(Timesheet.work_date >= datetime.strptime(start_date, '%Y-%m-%d').date())
    if end_date:
        query = query.filter(Timesheet.work_date <= datetime.strptime(end_date, '%Y-%m-%d').date())
    
    total_hours = db.session.query(func.sum(Timesheet.hours)).filter(
        query.whereclause
    ).scalar() or 0
    
    total_cost = db.session.query(func.sum(Timesheet.cost_amount)).filter(
        query.whereclause
    ).scalar() or 0
    
    # Hours by user
    hours_by_user = db.session.query(
        User.email,
        func.sum(Timesheet.hours)
    ).join(User).filter(Timesheet.project_id == project_id)
    
    if start_date:
        hours_by_user = hours_by_user.filter(Timesheet.work_date >= datetime.strptime(start_date, '%Y-%m-%d').date())
    if end_date:
        hours_by_user = hours_by_user.filter(Timesheet.work_date <= datetime.strptime(end_date, '%Y-%m-%d').date())
    
    hours_by_user = hours_by_user.group_by(User.id, User.email).all()
    
    # Hours by task
    hours_by_task = db.session.query(
        Task.title,
        func.sum(Timesheet.hours)
    ).join(Task, Timesheet.task_id == Task.id).filter(Timesheet.project_id == project_id)
    
    if start_date:
        hours_by_task = hours_by_task.filter(Timesheet.work_date >= datetime.strptime(start_date, '%Y-%m-%d').date())
    if end_date:
        hours_by_task = hours_by_task.filter(Timesheet.work_date <= datetime.strptime(end_date, '%Y-%m-%d').date())
    
    hours_by_task = hours_by_task.group_by(Task.id, Task.title).all()
    
    return jsonify({
        'project_id': project_id,
        'project_name': project.name,
        'total_hours': float(total_hours),
        'total_cost': float(total_cost),
        'hours_by_user': {email: float(hours) for email, hours in hours_by_user},
        'hours_by_task': {title: float(hours) for title, hours in hours_by_task},
        'filters': {
            'start_date': start_date,
            'end_date': end_date
        }
    }), 200


# ==================== EXPENSE ANALYTICS ====================

@analytics_bp.route('/analytics/expenses/overview', methods=['GET'])
def expenses_overview():
    """Get overall expense statistics"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    # Get date range from query params
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = Expense.query
    
    if start_date:
        query = query.filter(Expense.expense_date >= datetime.strptime(start_date, '%Y-%m-%d').date())
    if end_date:
        query = query.filter(Expense.expense_date <= datetime.strptime(end_date, '%Y-%m-%d').date())
    
    total_expenses = db.session.query(func.sum(Expense.amount)).filter(
        query.whereclause if query.whereclause is not None else True
    ).scalar() or 0
    
    # Expenses by status
    expenses_by_status = db.session.query(
        Expense.status,
        func.sum(Expense.amount)
    )
    if start_date:
        expenses_by_status = expenses_by_status.filter(Expense.expense_date >= datetime.strptime(start_date, '%Y-%m-%d').date())
    if end_date:
        expenses_by_status = expenses_by_status.filter(Expense.expense_date <= datetime.strptime(end_date, '%Y-%m-%d').date())
    expenses_by_status = expenses_by_status.group_by(Expense.status).all()
    
    # Billable vs non-billable
    billable_expenses = db.session.query(func.sum(Expense.amount)).filter(
        Expense.billable == True
    )
    if start_date:
        billable_expenses = billable_expenses.filter(Expense.expense_date >= datetime.strptime(start_date, '%Y-%m-%d').date())
    if end_date:
        billable_expenses = billable_expenses.filter(Expense.expense_date <= datetime.strptime(end_date, '%Y-%m-%d').date())
    billable_expenses = billable_expenses.scalar() or 0
    
    # Expenses by project
    expenses_by_project = db.session.query(
        Project.name,
        func.sum(Expense.amount)
    ).join(Project)
    
    if start_date:
        expenses_by_project = expenses_by_project.filter(Expense.expense_date >= datetime.strptime(start_date, '%Y-%m-%d').date())
    if end_date:
        expenses_by_project = expenses_by_project.filter(Expense.expense_date <= datetime.strptime(end_date, '%Y-%m-%d').date())
    
    expenses_by_project = expenses_by_project.group_by(Project.id, Project.name).all()
    
    return jsonify({
        'total_expenses': float(total_expenses),
        'billable_expenses': float(billable_expenses),
        'non_billable_expenses': float(total_expenses - billable_expenses),
        'expenses_by_status': {status: float(amount) for status, amount in expenses_by_status},
        'expenses_by_project': {name: float(amount) for name, amount in expenses_by_project},
        'filters': {
            'start_date': start_date,
            'end_date': end_date
        }
    }), 200


@analytics_bp.route('/analytics/expenses/user/<int:user_id>', methods=['GET'])
def user_expense_analytics(user_id):
    """Get expense analytics for a specific user"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Get date range from query params
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = Expense.query.filter_by(submitted_by=user_id)
    
    if start_date:
        query = query.filter(Expense.expense_date >= datetime.strptime(start_date, '%Y-%m-%d').date())
    if end_date:
        query = query.filter(Expense.expense_date <= datetime.strptime(end_date, '%Y-%m-%d').date())
    
    total_expenses = db.session.query(func.sum(Expense.amount)).filter(
        query.whereclause
    ).scalar() or 0
    
    # Expenses by status
    expenses_by_status = db.session.query(
        Expense.status,
        func.sum(Expense.amount),
        func.count(Expense.id)
    ).filter(Expense.submitted_by == user_id)
    
    if start_date:
        expenses_by_status = expenses_by_status.filter(Expense.expense_date >= datetime.strptime(start_date, '%Y-%m-%d').date())
    if end_date:
        expenses_by_status = expenses_by_status.filter(Expense.expense_date <= datetime.strptime(end_date, '%Y-%m-%d').date())
    
    expenses_by_status = expenses_by_status.group_by(Expense.status).all()
    
    # Expenses by project
    expenses_by_project = db.session.query(
        Project.name,
        func.sum(Expense.amount)
    ).join(Project).filter(Expense.submitted_by == user_id)
    
    if start_date:
        expenses_by_project = expenses_by_project.filter(Expense.expense_date >= datetime.strptime(start_date, '%Y-%m-%d').date())
    if end_date:
        expenses_by_project = expenses_by_project.filter(Expense.expense_date <= datetime.strptime(end_date, '%Y-%m-%d').date())
    
    expenses_by_project = expenses_by_project.group_by(Project.id, Project.name).all()
    
    return jsonify({
        'user_id': user_id,
        'email': user.email,
        'total_expenses': float(total_expenses),
        'expenses_by_status': {
            status: {
                'amount': float(amount),
                'count': count
            } for status, amount, count in expenses_by_status
        },
        'expenses_by_project': {name: float(amount) for name, amount in expenses_by_project},
        'filters': {
            'start_date': start_date,
            'end_date': end_date
        }
    }), 200


@analytics_bp.route('/analytics/expenses/project/<int:project_id>', methods=['GET'])
def project_expense_analytics(project_id):
    """Get expense analytics for a specific project"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    project = Project.query.get(project_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    
    # Get date range from query params
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = Expense.query.filter_by(project_id=project_id)
    
    if start_date:
        query = query.filter(Expense.expense_date >= datetime.strptime(start_date, '%Y-%m-%d').date())
    if end_date:
        query = query.filter(Expense.expense_date <= datetime.strptime(end_date, '%Y-%m-%d').date())
    
    total_expenses = db.session.query(func.sum(Expense.amount)).filter(
        query.whereclause
    ).scalar() or 0
    
    # Expenses by status
    expenses_by_status = db.session.query(
        Expense.status,
        func.sum(Expense.amount),
        func.count(Expense.id)
    ).filter(Expense.project_id == project_id)
    
    if start_date:
        expenses_by_status = expenses_by_status.filter(Expense.expense_date >= datetime.strptime(start_date, '%Y-%m-%d').date())
    if end_date:
        expenses_by_status = expenses_by_status.filter(Expense.expense_date <= datetime.strptime(end_date, '%Y-%m-%d').date())
    
    expenses_by_status = expenses_by_status.group_by(Expense.status).all()
    
    # Expenses by user
    expenses_by_user = db.session.query(
        User.email,
        func.sum(Expense.amount),
        func.count(Expense.id)
    ).join(User, Expense.submitted_by == User.id).filter(Expense.project_id == project_id)
    
    if start_date:
        expenses_by_user = expenses_by_user.filter(Expense.expense_date >= datetime.strptime(start_date, '%Y-%m-%d').date())
    if end_date:
        expenses_by_user = expenses_by_user.filter(Expense.expense_date <= datetime.strptime(end_date, '%Y-%m-%d').date())
    
    expenses_by_user = expenses_by_user.group_by(User.id, User.email).all()
    
    return jsonify({
        'project_id': project_id,
        'project_name': project.name,
        'project_budget': float(project.budget_amount),
        'total_expenses': float(total_expenses),
        'expenses_by_status': {
            status: {
                'amount': float(amount),
                'count': count
            } for status, amount, count in expenses_by_status
        },
        'expenses_by_user': {
            email: {
                'amount': float(amount),
                'count': count
            } for email, amount, count in expenses_by_user
        },
        'filters': {
            'start_date': start_date,
            'end_date': end_date
        }
    }), 200


# ==================== COMBINED ANALYTICS ====================

@analytics_bp.route('/analytics/dashboard', methods=['GET'])
def analytics_dashboard():
    """Get combined analytics dashboard"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    # Project stats
    total_projects = Project.query.count()
    active_projects = Project.query.filter_by(status='active').count()
    
    # Task stats
    total_tasks = Task.query.count()
    overdue_tasks = Task.query.filter(
        Task.due_date < datetime.now().date(),
        Task.state.notin_(['done', 'completed', 'closed'])
    ).count()
    
    # Timesheet stats
    total_hours = db.session.query(func.sum(Timesheet.hours)).scalar() or 0
    total_cost = db.session.query(func.sum(Timesheet.cost_amount)).scalar() or 0
    
    # Expense stats
    total_expenses = db.session.query(func.sum(Expense.amount)).scalar() or 0
    pending_expenses = db.session.query(func.sum(Expense.amount)).filter(
        Expense.status == 'pending'
    ).scalar() or 0
    
    # Total budget
    total_budget = db.session.query(func.sum(Project.budget_amount)).scalar() or 0
    
    return jsonify({
        'projects': {
            'total': total_projects,
            'active': active_projects,
            'total_budget': float(total_budget)
        },
        'tasks': {
            'total': total_tasks,
            'overdue': overdue_tasks
        },
        'timesheets': {
            'total_hours': float(total_hours),
            'total_cost': float(total_cost)
        },
        'expenses': {
            'total_expenses': float(total_expenses),
            'pending_expenses': float(pending_expenses)
        },
        'financial_summary': {
            'total_budget': float(total_budget),
            'total_costs': float(total_cost + total_expenses),
            'remaining_budget': float(total_budget - (total_cost + total_expenses))
        }
    }), 200
