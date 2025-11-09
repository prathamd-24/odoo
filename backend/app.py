from flask import Flask, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
import os
from models import db, User, Project, ProjectMember, Task, TaskAssignment, TaskComment, TaskAttachment, Timesheet, Expense
from analytics import analytics_bp
from sales_routes import sales_purchase_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project_management.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(24)  # For session management

db.init_app(app)

# Register blueprints
app.register_blueprint(analytics_bp)
app.register_blueprint(sales_purchase_bp)

# Create tables
with app.app_context():
    db.create_all()


# Helper function to check authentication
def require_auth():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    return None

# Route

@app.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password are required'}), 400
    
    email = data.get('email')
    password = data.get('password')
    
    # Check if user already exists
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'User already exists'}), 409
    
    # Create new user
    password_hash = generate_password_hash(password)
    new_user = User(
        email=email,
        password_hash=password_hash,
        is_active=data.get('is_active', True)
    )
    
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({
            'message': 'User registered successfully',
            'user': {
                'id': new_user.id,
                'email': new_user.email,
                'is_active': new_user.is_active
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/login', methods=['POST'])
def login():
    """Login user"""
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password are required'}), 400
    
    email = data.get('email')
    password = data.get('password')
    
    # Find user
    user = User.query.filter_by(email=email).first()
    
    if not user:
        return jsonify({'error': 'Invalid email or password'}), 401
    
    # Check if user is active
    if not user.is_active:
        return jsonify({'error': 'User account is not active'}), 403
    
    # Verify password
    if not check_password_hash(user.password_hash, password):
        return jsonify({'error': 'Invalid email or password'}), 401
    
    # Create session
    session['user_id'] = user.id
    session['email'] = user.email
    
    return jsonify({
        'message': 'Login successful',
        'user': {
            'id': user.id,
            'email': user.email,
            'is_active': user.is_active
        }
    }), 200


@app.route('/logout', methods=['POST'])
def logout():
    """Logout user"""
    session.clear()
    return jsonify({'message': 'Logout successful'}), 200


@app.route('/profile', methods=['GET'])
def profile():
    """Get user profile (protected route)"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    user = User.query.get(session['user_id'])
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'user': {
            'id': user.id,
            'email': user.email,
            'is_active': user.is_active,
            'created_at': user.created_at.isoformat()
        }
    }), 200


@app.route('/users', methods=['GET'])
def get_users():
    """Get all users (protected route)"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    users = User.query.all()
    return jsonify({
        'users': [{
            'id': user.id,
            'email': user.email,
            'is_active': user.is_active,
            'created_at': user.created_at.isoformat()
        } for user in users]
    }), 200


@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Update user (protected route)"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    
    if 'email' in data:
        # Check if email is already taken by another user
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user and existing_user.id != user_id:
            return jsonify({'error': 'Email already exists'}), 409
        user.email = data['email']
    
    if 'password' in data:
        user.password_hash = generate_password_hash(data['password'])
    
    if 'is_active' in data:
        user.is_active = data['is_active']
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'User updated successfully',
            'user': {
                'id': user.id,
                'email': user.email,
                'is_active': user.is_active
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete user (protected route)"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ==================== PROJECT MANAGEMENT ROUTES ====================

@app.route('/projects', methods=['POST'])
def create_project():
    """Create a new project"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    data = request.get_json()
    
    if not data or not data.get('project_code') or not data.get('name'):
        return jsonify({'error': 'Project code and name are required'}), 400
    
    # Check if project code already exists
    if Project.query.filter_by(project_code=data['project_code']).first():
        return jsonify({'error': 'Project code already exists'}), 409
    
    try:
        project = Project(
            project_code=data['project_code'],
            name=data['name'],
            description=data.get('description'),
            project_manager_id=data.get('project_manager_id'),
            start_date=datetime.strptime(data['start_date'], '%Y-%m-%d').date() if data.get('start_date') else None,
            end_date=datetime.strptime(data['end_date'], '%Y-%m-%d').date() if data.get('end_date') else None,
            status=data.get('status', 'active'),
            budget_amount=data.get('budget_amount', 0.0)
        )
        
        db.session.add(project)
        db.session.commit()
        
        return jsonify({
            'message': 'Project created successfully',
            'project': {
                'id': project.id,
                'project_code': project.project_code,
                'name': project.name,
                'description': project.description,
                'project_manager_id': project.project_manager_id,
                'start_date': project.start_date.isoformat() if project.start_date else None,
                'end_date': project.end_date.isoformat() if project.end_date else None,
                'status': project.status,
                'budget_amount': project.budget_amount
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/projects', methods=['GET'])
def get_projects():
    """Get all projects"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    projects = Project.query.all()
    return jsonify({
        'projects': [{
            'id': p.id,
            'project_code': p.project_code,
            'name': p.name,
            'description': p.description,
            'project_manager_id': p.project_manager_id,
            'start_date': p.start_date.isoformat() if p.start_date else None,
            'end_date': p.end_date.isoformat() if p.end_date else None,
            'status': p.status,
            'budget_amount': p.budget_amount,
            'created_at': p.created_at.isoformat()
        } for p in projects]
    }), 200


@app.route('/projects/<int:project_id>', methods=['GET'])
def get_project(project_id):
    """Get a specific project with members"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    project = Project.query.get(project_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    
    members = [{
        'id': m.id,
        'user_id': m.user_id,
        'user_email': m.user.email if m.user else None,
        'role_in_project': m.role_in_project,
        'added_at': m.added_at.isoformat()
    } for m in project.members]
    
    return jsonify({
        'project': {
            'id': project.id,
            'project_code': project.project_code,
            'name': project.name,
            'description': project.description,
            'project_manager_id': project.project_manager_id,
            'project_manager_email': project.project_manager.email if project.project_manager else None,
            'start_date': project.start_date.isoformat() if project.start_date else None,
            'end_date': project.end_date.isoformat() if project.end_date else None,
            'status': project.status,
            'budget_amount': project.budget_amount,
            'created_at': project.created_at.isoformat(),
            'members': members
        }
    }), 200


@app.route('/projects/<int:project_id>', methods=['PUT'])
def update_project(project_id):
    """Update a project"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    project = Project.query.get(project_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    
    data = request.get_json()
    
    try:
        if 'project_code' in data:
            existing = Project.query.filter_by(project_code=data['project_code']).first()
            if existing and existing.id != project_id:
                return jsonify({'error': 'Project code already exists'}), 409
            project.project_code = data['project_code']
        
        if 'name' in data:
            project.name = data['name']
        if 'description' in data:
            project.description = data['description']
        if 'project_manager_id' in data:
            project.project_manager_id = data['project_manager_id']
        if 'start_date' in data:
            project.start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date() if data['start_date'] else None
        if 'end_date' in data:
            project.end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date() if data['end_date'] else None
        if 'status' in data:
            project.status = data['status']
        if 'budget_amount' in data:
            project.budget_amount = data['budget_amount']
        
        project.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Project updated successfully',
            'project': {
                'id': project.id,
                'project_code': project.project_code,
                'name': project.name,
                'status': project.status
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/projects/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    """Delete a project"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    project = Project.query.get(project_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    
    try:
        db.session.delete(project)
        db.session.commit()
        return jsonify({'message': 'Project deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/users/<int:user_id>/projects', methods=['GET'])
def get_user_projects(user_id):
    """Get all projects for a specific user (as manager or member)"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Projects where user is manager
    managed_projects = [{
        'id': p.id,
        'project_code': p.project_code,
        'name': p.name,
        'description': p.description,
        'role': 'Project Manager',
        'status': p.status,
        'start_date': p.start_date.isoformat() if p.start_date else None,
        'end_date': p.end_date.isoformat() if p.end_date else None,
        'budget_amount': p.budget_amount
    } for p in user.managed_projects]
    
    # Projects where user is member
    member_projects = [{
        'id': m.project.id,
        'project_code': m.project.project_code,
        'name': m.project.name,
        'description': m.project.description,
        'role': m.role_in_project,
        'status': m.project.status,
        'start_date': m.project.start_date.isoformat() if m.project.start_date else None,
        'end_date': m.project.end_date.isoformat() if m.project.end_date else None,
        'added_at': m.added_at.isoformat()
    } for m in user.project_memberships]
    
    return jsonify({
        'user_id': user_id,
        'email': user.email,
        'managed_projects': managed_projects,
        'member_projects': member_projects,
        'total_projects': len(managed_projects) + len(member_projects)
    }), 200


# ==================== PROJECT MEMBERS ROUTES ====================

@app.route('/projects/<int:project_id>/members', methods=['POST'])
def add_project_member(project_id):
    """Add a member to a project"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    project = Project.query.get(project_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    
    data = request.get_json()
    
    if not data or not data.get('user_id'):
        return jsonify({'error': 'User ID is required'}), 400
    
    # Check if user exists
    user = User.query.get(data['user_id'])
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Check if already a member
    existing = ProjectMember.query.filter_by(project_id=project_id, user_id=data['user_id']).first()
    if existing:
        return jsonify({'error': 'User is already a member of this project'}), 409
    
    try:
        member = ProjectMember(
            project_id=project_id,
            user_id=data['user_id'],
            role_in_project=data.get('role_in_project', 'Member')
        )
        
        db.session.add(member)
        db.session.commit()
        
        return jsonify({
            'message': 'Member added successfully',
            'member': {
                'id': member.id,
                'project_id': member.project_id,
                'user_id': member.user_id,
                'user_email': member.user.email,
                'role_in_project': member.role_in_project,
                'added_at': member.added_at.isoformat()
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/projects/<int:project_id>/members/<int:member_id>', methods=['DELETE'])
def remove_project_member(project_id, member_id):
    """Remove a member from a project"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    member = ProjectMember.query.filter_by(id=member_id, project_id=project_id).first()
    if not member:
        return jsonify({'error': 'Member not found'}), 404
    
    try:
        db.session.delete(member)
        db.session.commit()
        return jsonify({'message': 'Member removed successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ==================== TASK MANAGEMENT ROUTES ====================

@app.route('/projects/<int:project_id>/tasks', methods=['POST'])
def create_task(project_id):
    """Create a new task"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    project = Project.query.get(project_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    
    data = request.get_json()
    
    if not data or not data.get('title'):
        return jsonify({'error': 'Title is required'}), 400
    
    try:
        task = Task(
            project_id=project_id,
            title=data['title'],
            description=data.get('description'),
            priority=data.get('priority', 'medium'),
            state=data.get('state', 'todo'),
            due_date=datetime.strptime(data['due_date'], '%Y-%m-%d').date() if data.get('due_date') else None,
            created_by=session['user_id']
        )
        
        db.session.add(task)
        db.session.commit()
        
        return jsonify({
            'message': 'Task created successfully',
            'task': {
                'id': task.id,
                'project_id': task.project_id,
                'title': task.title,
                'description': task.description,
                'priority': task.priority,
                'state': task.state,
                'due_date': task.due_date.isoformat() if task.due_date else None,
                'created_by': task.created_by
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/projects/<int:project_id>/tasks', methods=['GET'])
def get_project_tasks(project_id):
    """Get all tasks for a project"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    project = Project.query.get(project_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    
    tasks = Task.query.filter_by(project_id=project_id).all()
    
    return jsonify({
        'project_id': project_id,
        'tasks': [{
            'id': t.id,
            'title': t.title,
            'description': t.description,
            'priority': t.priority,
            'state': t.state,
            'due_date': t.due_date.isoformat() if t.due_date else None,
            'created_by': t.created_by,
            'creator_email': t.creator.email if t.creator else None,
            'created_at': t.created_at.isoformat(),
            'assignments_count': len(t.assignments),
            'comments_count': len(t.comments)
        } for t in tasks]
    }), 200


@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Get a specific task with all details"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    assignments = [{
        'id': a.id,
        'user_id': a.user_id,
        'user_email': a.user.email if a.user else None,
        'assigned_at': a.assigned_at.isoformat()
    } for a in task.assignments]
    
    comments = [{
        'id': c.id,
        'user_id': c.user_id,
        'user_email': c.user.email if c.user else None,
        'comment': c.comment,
        'created_at': c.created_at.isoformat()
    } for c in task.comments]
    
    attachments = [{
        'id': a.id,
        'file_name': a.file_name,
        'file_url': a.file_url,
        'uploaded_by': a.uploaded_by,
        'uploader_email': a.uploader.email if a.uploader else None,
        'created_at': a.created_at.isoformat()
    } for a in task.attachments]
    
    return jsonify({
        'task': {
            'id': task.id,
            'project_id': task.project_id,
            'project_name': task.project.name,
            'title': task.title,
            'description': task.description,
            'priority': task.priority,
            'state': task.state,
            'due_date': task.due_date.isoformat() if task.due_date else None,
            'created_by': task.created_by,
            'creator_email': task.creator.email if task.creator else None,
            'created_at': task.created_at.isoformat(),
            'updated_at': task.updated_at.isoformat(),
            'assignments': assignments,
            'comments': comments,
            'attachments': attachments
        }
    }), 200


@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update a task"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    data = request.get_json()
    
    try:
        if 'title' in data:
            task.title = data['title']
        if 'description' in data:
            task.description = data['description']
        if 'priority' in data:
            task.priority = data['priority']
        if 'state' in data:
            task.state = data['state']
        if 'due_date' in data:
            task.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d').date() if data['due_date'] else None
        
        task.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Task updated successfully',
            'task': {
                'id': task.id,
                'title': task.title,
                'state': task.state,
                'priority': task.priority
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    try:
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': 'Task deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/users/<int:user_id>/tasks', methods=['GET'])
def get_user_tasks(user_id):
    """Get all tasks assigned to a user"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    assigned_tasks = [{
        'id': a.task.id,
        'title': a.task.title,
        'description': a.task.description,
        'priority': a.task.priority,
        'state': a.task.state,
        'due_date': a.task.due_date.isoformat() if a.task.due_date else None,
        'project_id': a.task.project_id,
        'project_name': a.task.project.name,
        'assigned_at': a.assigned_at.isoformat()
    } for a in user.task_assignments]
    
    return jsonify({
        'user_id': user_id,
        'email': user.email,
        'assigned_tasks': assigned_tasks,
        'total_tasks': len(assigned_tasks)
    }), 200


# ==================== TASK ASSIGNMENTS ROUTES ====================

@app.route('/tasks/<int:task_id>/assignments', methods=['POST'])
def assign_task(task_id):
    """Assign a task to a user"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    data = request.get_json()
    
    if not data or not data.get('user_id'):
        return jsonify({'error': 'User ID is required'}), 400
    
    user = User.query.get(data['user_id'])
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Check if already assigned
    existing = TaskAssignment.query.filter_by(task_id=task_id, user_id=data['user_id']).first()
    if existing:
        return jsonify({'error': 'Task already assigned to this user'}), 409
    
    try:
        assignment = TaskAssignment(
            task_id=task_id,
            user_id=data['user_id']
        )
        
        db.session.add(assignment)
        db.session.commit()
        
        return jsonify({
            'message': 'Task assigned successfully',
            'assignment': {
                'id': assignment.id,
                'task_id': assignment.task_id,
                'user_id': assignment.user_id,
                'user_email': assignment.user.email,
                'assigned_at': assignment.assigned_at.isoformat()
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/tasks/<int:task_id>/assignments/<int:assignment_id>', methods=['DELETE'])
def unassign_task(task_id, assignment_id):
    """Remove a task assignment"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    assignment = TaskAssignment.query.filter_by(id=assignment_id, task_id=task_id).first()
    if not assignment:
        return jsonify({'error': 'Assignment not found'}), 404
    
    try:
        db.session.delete(assignment)
        db.session.commit()
        return jsonify({'message': 'Assignment removed successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ==================== TASK COMMENTS ROUTES ====================

@app.route('/tasks/<int:task_id>/comments', methods=['POST'])
def add_task_comment(task_id):
    """Add a comment to a task"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    data = request.get_json()
    
    if not data or not data.get('comment'):
        return jsonify({'error': 'Comment is required'}), 400
    
    try:
        comment = TaskComment(
            task_id=task_id,
            user_id=session['user_id'],
            comment=data['comment']
        )
        
        db.session.add(comment)
        db.session.commit()
        
        return jsonify({
            'message': 'Comment added successfully',
            'comment': {
                'id': comment.id,
                'task_id': comment.task_id,
                'user_id': comment.user_id,
                'user_email': comment.user.email if comment.user else None,
                'comment': comment.comment,
                'created_at': comment.created_at.isoformat()
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/tasks/<int:task_id>/comments', methods=['GET'])
def get_task_comments(task_id):
    """Get all comments for a task"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    comments = TaskComment.query.filter_by(task_id=task_id).order_by(TaskComment.created_at.desc()).all()
    
    return jsonify({
        'task_id': task_id,
        'comments': [{
            'id': c.id,
            'user_id': c.user_id,
            'user_email': c.user.email if c.user else None,
            'comment': c.comment,
            'created_at': c.created_at.isoformat()
        } for c in comments]
    }), 200


@app.route('/tasks/<int:task_id>/comments/<int:comment_id>', methods=['DELETE'])
def delete_task_comment(task_id, comment_id):
    """Delete a task comment"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    comment = TaskComment.query.filter_by(id=comment_id, task_id=task_id).first()
    if not comment:
        return jsonify({'error': 'Comment not found'}), 404
    
    # Only allow the comment owner or admin to delete
    if comment.user_id != session['user_id']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        db.session.delete(comment)
        db.session.commit()
        return jsonify({'message': 'Comment deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ==================== TASK ATTACHMENTS ROUTES ====================

@app.route('/tasks/<int:task_id>/attachments', methods=['POST'])
def add_task_attachment(task_id):
    """Add an attachment to a task"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    data = request.get_json()
    
    if not data or not data.get('file_name') or not data.get('file_url'):
        return jsonify({'error': 'File name and URL are required'}), 400
    
    try:
        attachment = TaskAttachment(
            task_id=task_id,
            uploaded_by=session['user_id'],
            file_name=data['file_name'],
            file_url=data['file_url']
        )
        
        db.session.add(attachment)
        db.session.commit()
        
        return jsonify({
            'message': 'Attachment added successfully',
            'attachment': {
                'id': attachment.id,
                'task_id': attachment.task_id,
                'file_name': attachment.file_name,
                'file_url': attachment.file_url,
                'uploaded_by': attachment.uploaded_by,
                'created_at': attachment.created_at.isoformat()
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/tasks/<int:task_id>/attachments/<int:attachment_id>', methods=['DELETE'])
def delete_task_attachment(task_id, attachment_id):
    """Delete a task attachment"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    attachment = TaskAttachment.query.filter_by(id=attachment_id, task_id=task_id).first()
    if not attachment:
        return jsonify({'error': 'Attachment not found'}), 404
    
    try:
        db.session.delete(attachment)
        db.session.commit()
        return jsonify({'message': 'Attachment deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ==================== EXPENSE MANAGEMENT ROUTES ====================

@app.route('/projects/<int:project_id>/expenses', methods=['POST'])
def create_expense(project_id):
    """Create a new expense"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    project = Project.query.get(project_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    
    data = request.get_json()
    
    if not data or not data.get('description') or not data.get('amount') or not data.get('expense_date'):
        return jsonify({'error': 'Description, amount, and expense date are required'}), 400
    
    try:
        expense = Expense(
            project_id=project_id,
            task_id=data.get('task_id'),
            submitted_by=session['user_id'],
            expense_date=datetime.strptime(data['expense_date'], '%Y-%m-%d').date(),
            description=data['description'],
            amount=data['amount'],
            billable=data.get('billable', True),
            status=data.get('status', 'pending'),
            receipt_url=data.get('receipt_url')
        )
        
        db.session.add(expense)
        db.session.commit()
        
        return jsonify({
            'message': 'Expense created successfully',
            'expense': {
                'id': expense.id,
                'project_id': expense.project_id,
                'task_id': expense.task_id,
                'submitted_by': expense.submitted_by,
                'expense_date': expense.expense_date.isoformat(),
                'description': expense.description,
                'amount': expense.amount,
                'billable': expense.billable,
                'status': expense.status
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/projects/<int:project_id>/expenses', methods=['GET'])
def get_project_expenses(project_id):
    """Get all expenses for a project"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    project = Project.query.get(project_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    
    expenses = Expense.query.filter_by(project_id=project_id).all()
    
    return jsonify({
        'project_id': project_id,
        'expenses': [{
            'id': e.id,
            'task_id': e.task_id,
            'task_title': e.task.title if e.task else None,
            'submitted_by': e.submitted_by,
            'submitter_email': e.submitter.email if e.submitter else None,
            'approved_by': e.approved_by,
            'approver_email': e.approver.email if e.approver else None,
            'expense_date': e.expense_date.isoformat(),
            'description': e.description,
            'amount': e.amount,
            'billable': e.billable,
            'status': e.status,
            'receipt_url': e.receipt_url
        } for e in expenses],
        'total_amount': sum(e.amount for e in expenses)
    }), 200


@app.route('/expenses/<int:expense_id>', methods=['GET'])
def get_expense(expense_id):
    """Get a specific expense"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    expense = Expense.query.get(expense_id)
    if not expense:
        return jsonify({'error': 'Expense not found'}), 404
    
    return jsonify({
        'expense': {
            'id': expense.id,
            'project_id': expense.project_id,
            'project_name': expense.project.name,
            'task_id': expense.task_id,
            'task_title': expense.task.title if expense.task else None,
            'submitted_by': expense.submitted_by,
            'submitter_email': expense.submitter.email if expense.submitter else None,
            'approved_by': expense.approved_by,
            'approver_email': expense.approver.email if expense.approver else None,
            'expense_date': expense.expense_date.isoformat(),
            'description': expense.description,
            'amount': expense.amount,
            'billable': expense.billable,
            'status': expense.status,
            'receipt_url': expense.receipt_url
        }
    }), 200


@app.route('/expenses/<int:expense_id>', methods=['PUT'])
def update_expense(expense_id):
    """Update an expense"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    expense = Expense.query.get(expense_id)
    if not expense:
        return jsonify({'error': 'Expense not found'}), 404
    
    data = request.get_json()
    
    try:
        if 'description' in data:
            expense.description = data['description']
        if 'amount' in data:
            expense.amount = data['amount']
        if 'expense_date' in data:
            expense.expense_date = datetime.strptime(data['expense_date'], '%Y-%m-%d').date()
        if 'billable' in data:
            expense.billable = data['billable']
        if 'status' in data:
            expense.status = data['status']
        if 'approved_by' in data:
            expense.approved_by = data['approved_by']
        if 'receipt_url' in data:
            expense.receipt_url = data['receipt_url']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Expense updated successfully',
            'expense': {
                'id': expense.id,
                'description': expense.description,
                'amount': expense.amount,
                'status': expense.status
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/expenses/<int:expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    """Delete an expense"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    expense = Expense.query.get(expense_id)
    if not expense:
        return jsonify({'error': 'Expense not found'}), 404
    
    try:
        db.session.delete(expense)
        db.session.commit()
        return jsonify({'message': 'Expense deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/users/<int:user_id>/expenses', methods=['GET'])
def get_user_expenses(user_id):
    """Get all expenses submitted by a user"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    expenses = [{
        'id': e.id,
        'project_id': e.project_id,
        'project_name': e.project.name,
        'task_id': e.task_id,
        'task_title': e.task.title if e.task else None,
        'expense_date': e.expense_date.isoformat(),
        'description': e.description,
        'amount': e.amount,
        'billable': e.billable,
        'status': e.status,
        'approved_by': e.approved_by,
        'approver_email': e.approver.email if e.approver else None
    } for e in user.submitted_expenses]
    
    return jsonify({
        'user_id': user_id,
        'email': user.email,
        'expenses': expenses,
        'total_expenses': len(expenses),
        'total_amount': sum(e.amount for e in user.submitted_expenses)
    }), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
