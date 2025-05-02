from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import (
    Book, Journal, Magazine, Newspaper,
    EResource, LibraryUser, LibraryCard,
    LibraryLoan, LibraryReservation,
    LibraryFine, LibraryLocation,
    LibraryContact, LibraryPolicy
)
from . import db
from datetime import datetime
from utils import role_required, validate_request, format_response, log_activity, handle_exception

library_bp = Blueprint('library', __name__)

@library_bp.route('/books', methods=['GET'])
@jwt_required()
@role_required(['admin', 'librarian'])
def get_books():
    """Get all books with optional filters"""
    try:
        title = request.args.get('title')
        author = request.args.get('author')
        category = request.args.get('category')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Book.query
        
        if title:
            query = query.filter(Book.title.ilike(f'%{title}%'))
        if author:
            query = query.filter(Book.author.ilike(f'%{author}%'))
        if category:
            query = query.filter_by(category=category)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(Book.acquisition_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Book.acquisition_date <= datetime.fromisoformat(end_date))
        
        books = query.all()
        return format_response([book.to_dict() for book in books])
    except Exception as e:
        return handle_exception(e)

@library_bp.route('/journals', methods=['GET'])
@jwt_required()
@role_required(['admin', 'librarian'])
def get_journals():
    """Get all journals with optional filters"""
    try:
        title = request.args.get('title')
        publisher = request.args.get('publisher')
        category = request.args.get('category')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Journal.query
        
        if title:
            query = query.filter(Journal.title.ilike(f'%{title}%'))
        if publisher:
            query = query.filter(Journal.publisher.ilike(f'%{publisher}%'))
        if category:
            query = query.filter_by(category=category)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(Journal.acquisition_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Journal.acquisition_date <= datetime.fromisoformat(end_date))
        
        journals = query.all()
        return format_response([journal.to_dict() for journal in journals])
    except Exception as e:
        return handle_exception(e)

@library_bp.route('/magazines', methods=['GET'])
@jwt_required()
@role_required(['admin', 'librarian'])
def get_magazines():
    """Get all magazines with optional filters"""
    try:
        title = request.args.get('title')
        publisher = request.args.get('publisher')
        category = request.args.get('category')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Magazine.query
        
        if title:
            query = query.filter(Magazine.title.ilike(f'%{title}%'))
        if publisher:
            query = query.filter(Magazine.publisher.ilike(f'%{publisher}%'))
        if category:
            query = query.filter_by(category=category)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(Magazine.acquisition_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Magazine.acquisition_date <= datetime.fromisoformat(end_date))
        
        magazines = query.all()
        return format_response([magazine.to_dict() for magazine in magazines])
    except Exception as e:
        return handle_exception(e)

@library_bp.route('/newspapers', methods=['GET'])
@jwt_required()
@role_required(['admin', 'librarian'])
def get_newspapers():
    """Get all newspapers with optional filters"""
    try:
        title = request.args.get('title')
        publisher = request.args.get('publisher')
        category = request.args.get('category')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Newspaper.query
        
        if title:
            query = query.filter(Newspaper.title.ilike(f'%{title}%'))
        if publisher:
            query = query.filter(Newspaper.publisher.ilike(f'%{publisher}%'))
        if category:
            query = query.filter_by(category=category)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(Newspaper.acquisition_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Newspaper.acquisition_date <= datetime.fromisoformat(end_date))
        
        newspapers = query.all()
        return format_response([newspaper.to_dict() for newspaper in newspapers])
    except Exception as e:
        return handle_exception(e)

@library_bp.route('/eresources', methods=['GET'])
@jwt_required()
@role_required(['admin', 'librarian'])
def get_eresources():
    """Get all electronic resources with optional filters"""
    try:
        title = request.args.get('title')
        resource_type = request.args.get('resource_type')
        category = request.args.get('category')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = EResource.query
        
        if title:
            query = query.filter(EResource.title.ilike(f'%{title}%'))
        if resource_type:
            query = query.filter_by(resource_type=resource_type)
        if category:
            query = query.filter_by(category=category)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(EResource.acquisition_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(EResource.acquisition_date <= datetime.fromisoformat(end_date))
        
        eresources = query.all()
        return format_response([eresource.to_dict() for eresource in eresources])
    except Exception as e:
        return handle_exception(e)

@library_bp.route('/users', methods=['GET'])
@jwt_required()
@role_required(['admin', 'librarian'])
def get_users():
    """Get all library users with optional filters"""
    try:
        user_type = request.args.get('user_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = LibraryUser.query
        
        if user_type:
            query = query.filter_by(user_type=user_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(LibraryUser.registration_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(LibraryUser.registration_date <= datetime.fromisoformat(end_date))
        
        users = query.all()
        return format_response([user.to_dict() for user in users])
    except Exception as e:
        return handle_exception(e)

@library_bp.route('/cards', methods=['GET'])
@jwt_required()
@role_required(['admin', 'librarian'])
def get_cards():
    """Get all library cards with optional filters"""
    try:
        user_id = request.args.get('user_id')
        card_type = request.args.get('card_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = LibraryCard.query
        
        if user_id:
            query = query.filter_by(user_id=user_id)
        if card_type:
            query = query.filter_by(card_type=card_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(LibraryCard.issue_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(LibraryCard.issue_date <= datetime.fromisoformat(end_date))
        
        cards = query.all()
        return format_response([card.to_dict() for card in cards])
    except Exception as e:
        return handle_exception(e)

@library_bp.route('/loans', methods=['GET'])
@jwt_required()
@role_required(['admin', 'librarian'])
def get_loans():
    """Get all library loans with optional filters"""
    try:
        user_id = request.args.get('user_id')
        item_id = request.args.get('item_id')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = LibraryLoan.query
        
        if user_id:
            query = query.filter_by(user_id=user_id)
        if item_id:
            query = query.filter_by(item_id=item_id)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(LibraryLoan.loan_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(LibraryLoan.loan_date <= datetime.fromisoformat(end_date))
        
        loans = query.all()
        return format_response([loan.to_dict() for loan in loans])
    except Exception as e:
        return handle_exception(e)

@library_bp.route('/reservations', methods=['GET'])
@jwt_required()
@role_required(['admin', 'librarian'])
def get_reservations():
    """Get all library reservations with optional filters"""
    try:
        user_id = request.args.get('user_id')
        item_id = request.args.get('item_id')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = LibraryReservation.query
        
        if user_id:
            query = query.filter_by(user_id=user_id)
        if item_id:
            query = query.filter_by(item_id=item_id)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(LibraryReservation.reservation_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(LibraryReservation.reservation_date <= datetime.fromisoformat(end_date))
        
        reservations = query.all()
        return format_response([reservation.to_dict() for reservation in reservations])
    except Exception as e:
        return handle_exception(e)

@library_bp.route('/fines', methods=['GET'])
@jwt_required()
@role_required(['admin', 'librarian'])
def get_fines():
    """Get all library fines with optional filters"""
    try:
        user_id = request.args.get('user_id')
        fine_type = request.args.get('fine_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = LibraryFine.query
        
        if user_id:
            query = query.filter_by(user_id=user_id)
        if fine_type:
            query = query.filter_by(fine_type=fine_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(LibraryFine.issue_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(LibraryFine.issue_date <= datetime.fromisoformat(end_date))
        
        fines = query.all()
        return format_response([fine.to_dict() for fine in fines])
    except Exception as e:
        return handle_exception(e) 