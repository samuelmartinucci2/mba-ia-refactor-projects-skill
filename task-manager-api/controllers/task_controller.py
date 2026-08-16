from flask import request, jsonify
from database import db
from models.task import Task
from models.user import User
from models.category import Category
from datetime import datetime, timezone
import json

def get_tasks():
    try:
        # Handle query filters
        status = request.args.get('status')
        priority = request.args.get('priority')
        user_id = request.args.get('user_id')
        category_id = request.args.get('category_id')

        query = Task.query
        if status:
            query = query.filter_by(status=status)
        if priority:
            query = query.filter_by(priority=int(priority))
        if user_id:
            query = query.filter_by(user_id=int(user_id))
        if category_id:
            query = query.filter_by(category_id=int(category_id))

        tasks = query.all()
        return jsonify([t.to_dict() for t in tasks]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_task(task_id):
    try:
        task = Task.query.get(task_id)
        if not task:
            return jsonify({'error': 'Tarefa não encontrada'}), 404
        return jsonify(task.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def create_task():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Dados inválidos'}), 400

        title = data.get('title')
        if not title:
            return jsonify({'error': 'Título é obrigatório'}), 400

        task = Task()
        task.title = title
        task.description = data.get('description', '')
        
        status = data.get('status', 'pending')
        if not task.validate_status(status):
            return jsonify({'error': 'Status inválido'}), 400
        task.status = status

        priority = data.get('priority', 3)
        if not task.validate_priority(priority):
            return jsonify({'error': 'Prioridade inválida (deve ser entre 1 e 5)'}), 400
        task.priority = priority

        user_id = data.get('user_id')
        if user_id:
            user = User.query.get(user_id)
            if not user:
                return jsonify({'error': 'Usuário associado não existe'}), 400
            task.user_id = user_id

        category_id = data.get('category_id')
        if category_id:
            category = Category.query.get(category_id)
            if not category:
                return jsonify({'error': 'Categoria associada não existe'}), 400
            task.category_id = category_id

        due_date_str = data.get('due_date')
        if due_date_str:
            try:
                task.due_date = datetime.fromisoformat(due_date_str.replace('Z', '+00:00'))
            except:
                return jsonify({'error': 'Formato de data inválido. Use ISO format (YYYY-MM-DD)'}), 400

        tags = data.get('tags', [])
        if isinstance(tags, list):
            task.tags = ','.join(tags)

        db.session.add(task)
        db.session.commit()

        # Try to trigger notification service if assigned to user
        if user_id:
            try:
                from services.notification_service import NotificationService
                ns = NotificationService()
                ns.notify_task_assigned(user, task)
            except Exception as ne:
                print(f"Erro ao disparar notificação: {str(ne)}")

        return jsonify(task.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro ao criar tarefa: {str(e)}'}), 500

def update_task(task_id):
    try:
        task = Task.query.get(task_id)
        if not task:
            return jsonify({'error': 'Tarefa não encontrada'}), 404

        data = request.get_json()
        if not data:
            return jsonify({'error': 'Dados inválidos'}), 400

        if 'title' in data:
            task.title = data['title']

        if 'description' in data:
            task.description = data['description']

        if 'status' in data:
            if not task.validate_status(data['status']):
                return jsonify({'error': 'Status inválido'}), 400
            task.status = data['status']

        if 'priority' in data:
            if not task.validate_priority(data['priority']):
                return jsonify({'error': 'Prioridade inválida'}), 400
            task.priority = data['priority']

        if 'user_id' in data:
            user_id = data['user_id']
            if user_id:
                user = User.query.get(user_id)
                if not user:
                    return jsonify({'error': 'Usuário associado não existe'}), 400
                task.user_id = user_id
            else:
                task.user_id = None

        if 'category_id' in data:
            category_id = data['category_id']
            if category_id:
                category = Category.query.get(category_id)
                if not category:
                    return jsonify({'error': 'Categoria associada não existe'}), 400
                task.category_id = category_id
            else:
                task.category_id = None

        if 'due_date' in data:
            due_date_str = data['due_date']
            if due_date_str:
                try:
                    task.due_date = datetime.fromisoformat(due_date_str.replace('Z', '+00:00'))
                except:
                    return jsonify({'error': 'Formato de data inválido'}), 400
            else:
                task.due_date = None

        if 'tags' in data:
            tags = data['tags']
            if isinstance(tags, list):
                task.tags = ','.join(tags)

        # Fix Deprecated: datetime.utcnow -> timezone-aware
        task.updated_at = datetime.now(timezone.utc)

        db.session.commit()
        return jsonify(task.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro ao atualizar tarefa: {str(e)}'}), 500

def delete_task(task_id):
    try:
        task = Task.query.get(task_id)
        if not task:
            return jsonify({'error': 'Tarefa não encontrada'}), 404

        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': 'Tarefa deletada com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro ao deletar tarefa: {str(e)}'}), 500
