from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import (
    Book, Author, Publisher, Category, Loan, Reservation,
    Fine, LibraryCard, LibraryStaff, LibraryEvent,
    LibraryResource, LibraryReport, LibraryPolicy,
    LibraryFeedback, LibraryInventory, LibraryLocation
)
from . import db
from datetime import datetime
from utils import role_required, validate_request, format_response, log_activity, handle_exception

library_bp = Blueprint('library', __name__)

@library_bp.route('/books', methods=['GET'])
@jwt_required()
@role_required(['admin', 'library_staff'])
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
            query = query.join(Author).filter(Author.name.ilike(f'%{author}%'))
        if category:
            query = query.join(Category).filter(Category.name == category)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(Book.publication_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Book.publication_date <= datetime.fromisoformat(end_date))
        
        books = query.all()
        return format_response([book.to_dict() for book in books])
    except Exception as e:
        return handle_exception(e)

@library_bp.route('/authors', methods=['GET'])
@jwt_required()
@role_required(['admin', 'library_staff'])
def get_authors():
    """Get all authors with optional filters"""
    try:
        name = request.args.get('name')
        nationality = request.args.get('nationality')
        status = request.args.get('status')
        
        query = Author.query
        
        if name:
            query = query.filter(Author.name.ilike(f'%{name}%'))
        if nationality:
            query = query.filter_by(nationality=nationality)
        if status:
            query = query.filter_by(status=status)
        
        authors = query.all()
        return format_response([author.to_dict() for author in authors])
    except Exception as e:
        return handle_exception(e)

@library_bp.route('/publishers', methods=['GET'])
@jwt_required()
@role_required(['admin', 'library_staff'])
def get_publishers():
    """Get all publishers with optional filters"""
    try:
        name = request.args.get('name')
        country = request.args.get('country')
        status = request.args.get('status')
        
        query = Publisher.query
        
        if name:
            query = query.filter(Publisher.name.ilike(f'%{name}%'))
        if country:
            query = query.filter_by(country=country)
        if status:
            query = query.filter_by(status=status)
        
        publishers = query.all()
        return format_response([publisher.to_dict() for publisher in publishers])
    except Exception as e:
        return handle_exception(e)

@library_bp.route('/categories', methods=['GET'])
@jwt_required()
@role_required(['admin', 'library_staff'])
def get_categories():
    """Get all categories with optional filters"""
    try:
        name = request.args.get('name')
        parent = request.args.get('parent')
        status = request.args.get('status')
        
        query = Category.query
        
        if name:
            query = query.filter(Category.name.ilike(f'%{name}%'))
        if parent:
            query = query.filter_by(parent_id=parent)
        if status:
            query = query.filter_by(status=status)
        
        categories = query.all()
        return format_response([category.to_dict() for category in categories])
    except Exception as e:
        return handle_exception(e)

@library_bp.route('/loans', methods=['GET'])
@jwt_required()
@role_required(['admin', 'library_staff'])
def get_loans():
    """Get all loans with optional filters"""
    try:
        book_id = request.args.get('book_id')
        user_id = request.args.get('user_id')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Loan.query
        
        if book_id:
            query = query.filter_by(book_id=book_id)
        if user_id:
            query = query.filter_by(user_id=user_id)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(Loan.loan_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Loan.loan_date <= datetime.fromisoformat(end_date))
        
        loans = query.all()
        return format_response([loan.to_dict() for loan in loans])
    except Exception as e:
        return handle_exception(e)

@library_bp.route('/reservations', methods=['GET'])
@jwt_required()
@role_required(['admin', 'library_staff'])
def get_reservations():
    """Get all reservations with optional filters"""
    try:
        book_id = request.args.get('book_id')
        user_id = request.args.get('user_id')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Reservation.query
        
        if book_id:
            query = query.filter_by(book_id=book_id)
        if user_id:
            query = query.filter_by(user_id=user_id)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(Reservation.reservation_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Reservation.reservation_date <= datetime.fromisoformat(end_date))
        
        reservations = query.all()
        return format_response([reservation.to_dict() for reservation in reservations])
    except Exception as e:
        return handle_exception(e)

@library_bp.route('/fines', methods=['GET'])
@jwt_required()
@role_required(['admin', 'library_staff'])
def get_fines():
    """Get all fines with optional filters"""
    try:
        user_id = request.args.get('user_id')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Fine.query
        
        if user_id:
            query = query.filter_by(user_id=user_id)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(Fine.issue_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Fine.issue_date <= datetime.fromisoformat(end_date))
        
        fines = query.all()
        return format_response([fine.to_dict() for fine in fines])
    except Exception as e:
        return handle_exception(e)

@library_bp.route('/library-cards', methods=['GET'])
@jwt_required()
@role_required(['admin', 'library_staff'])
def get_library_cards():
    """Get all library cards with optional filters"""
    try:
        user_id = request.args.get('user_id')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = LibraryCard.query
        
        if user_id:
            query = query.filter_by(user_id=user_id)
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

@library_bp.route('/staff', methods=['GET'])
@jwt_required()
@role_required(['admin', 'library_staff'])
def get_library_staff():
    """Get all library staff with optional filters"""
    try:
        role = request.args.get('role')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = LibraryStaff.query
        
        if role:
            query = query.filter_by(role=role)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(LibraryStaff.start_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(LibraryStaff.start_date <= datetime.fromisoformat(end_date))
        
        staff = query.all()
        return format_response([member.to_dict() for member in staff])
    except Exception as e:
        return handle_exception(e)

@library_bp.route('/events', methods=['GET'])
@jwt_required()
@role_required(['admin', 'library_staff'])
def get_library_events():
    """Get all library events with optional filters"""
    try:
        event_type = request.args.get('event_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = LibraryEvent.query
        
        if event_type:
            query = query.filter_by(event_type=event_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(LibraryEvent.start_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(LibraryEvent.end_date <= datetime.fromisoformat(end_date))
        
        events = query.all()
        return format_response([event.to_dict() for event in events])
    except Exception as e:
        return handle_exception(e)

@library_bp.route('/resources', methods=['GET'])
@jwt_required()
@role_required(['admin', 'library_staff'])
def get_library_resources():
    """Get all library resources with optional filters"""
    try:
        resource_type = request.args.get('resource_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = LibraryResource.query
        
        if resource_type:
            query = query.filter_by(resource_type=resource_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(LibraryResource.acquisition_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(LibraryResource.acquisition_date <= datetime.fromisoformat(end_date))
        
        resources = query.all()
        return format_response([resource.to_dict() for resource in resources])
    except Exception as e:
        return handle_exception(e)

@library_bp.route('/reports', methods=['GET'])
@jwt_required()
@role_required(['admin', 'library_staff'])
def get_library_reports():
    """Get all library reports with optional filters"""
    try:
        report_type = request.args.get('report_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = LibraryReport.query
        
        if report_type:
            query = query.filter_by(report_type=report_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(LibraryReport.report_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(LibraryReport.report_date <= datetime.fromisoformat(end_date))
        
        reports = query.all()
        return format_response([report.to_dict() for report in reports])
    except Exception as e:
        return handle_exception(e)

@library_bp.route('/policies', methods=['GET'])
@jwt_required()
@role_required(['admin', 'library_staff'])
def get_library_policies():
    """Get all library policies with optional filters"""
    try:
        policy_type = request.args.get('policy_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = LibraryPolicy.query
        
        if policy_type:
            query = query.filter_by(policy_type=policy_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(LibraryPolicy.effective_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(LibraryPolicy.effective_date <= datetime.fromisoformat(end_date))
        
        policies = query.all()
        return format_response([policy.to_dict() for policy in policies])
    except Exception as e:
        return handle_exception(e)

@library_bp.route('/feedback', methods=['GET'])
@jwt_required()
@role_required(['admin', 'library_staff'])
def get_library_feedback():
    """Get all library feedback with optional filters"""
    try:
        feedback_type = request.args.get('feedback_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = LibraryFeedback.query
        
        if feedback_type:
            query = query.filter_by(feedback_type=feedback_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(LibraryFeedback.submission_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(LibraryFeedback.submission_date <= datetime.fromisoformat(end_date))
        
        feedback = query.all()
        return format_response([item.to_dict() for item in feedback])
    except Exception as e:
        return handle_exception(e)

@library_bp.route('/inventory', methods=['GET'])
@jwt_required()
@role_required(['admin', 'library_staff'])
def get_library_inventory():
    """Get all library inventory with optional filters"""
    try:
        item_type = request.args.get('item_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = LibraryInventory.query
        
        if item_type:
            query = query.filter_by(item_type=item_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(LibraryInventory.acquisition_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(LibraryInventory.acquisition_date <= datetime.fromisoformat(end_date))
        
        inventory = query.all()
        return format_response([item.to_dict() for item in inventory])
    except Exception as e:
        return handle_exception(e)

@library_bp.route('/locations', methods=['GET'])
@jwt_required()
@role_required(['admin', 'library_staff'])
def get_library_locations():
    """Get all library locations with optional filters"""
    try:
        location_type = request.args.get('location_type')
        status = request.args.get('status')
        
        query = LibraryLocation.query
        
        if location_type:
            query = query.filter_by(location_type=location_type)
        if status:
            query = query.filter_by(status=status)
        
        locations = query.all()
        return format_response([location.to_dict() for location in locations])
    except Exception as e:
        return handle_exception(e) 