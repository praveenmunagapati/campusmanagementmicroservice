from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import Book, Author, Publisher, Category, Loan, Reservation, LibraryCard, Fine, Resource, LibraryResource, LibraryMember, LibrarySection, LibraryStaff, LibraryEvent
from . import db
from datetime import datetime
from utils import role_required, validate_request, format_response, log_activity, handle_exception

library_bp = Blueprint('library', __name__)

# Book Routes
@library_bp.route('/books', methods=['GET'])
@jwt_required()
def get_books():
    """Get all books with optional filters"""
    try:
        title = request.args.get('title')
        author = request.args.get('author')
        category = request.args.get('category')
        status = request.args.get('status')
        
        query = Book.query
        
        if title:
            query = query.filter(Book.title.ilike(f'%{title}%'))
        if author:
            query = query.filter(Book.author.ilike(f'%{author}%'))
        if category:
            query = query.filter_by(category=category)
        if status:
            query = query.filter_by(status=status)
        
        books = query.all()
        return format_response([book.to_dict() for book in books])
    except Exception as e:
        return handle_exception(e)

@library_bp.route('/books', methods=['POST'])
@jwt_required()
@role_required(['admin', 'librarian'])
def create_book():
    """Create a new book"""
    try:
        data = request.get_json()
        new_book = Book(**data)
        db.session.add(new_book)
        db.session.commit()
        return format_response(new_book.to_dict(), 201)
    except Exception as e:
        db.session.rollback()
        return handle_exception(e)

# Author Routes
@library_bp.route('/authors', methods=['GET'])
@jwt_required()
def get_authors():
    authors = Author.query.all()
    return jsonify([{
        'id': a.id,
        'name': a.name,
        'biography': a.biography,
        'status': a.status
    } for a in authors])

@library_bp.route('/authors', methods=['POST'])
@jwt_required()
@role_required(['admin', 'librarian'])
def create_author():
    data = request.get_json()
    author = Author(
        name=data['name'],
        biography=data.get('biography'),
        status=data.get('status', 'active')
    )
    db.session.add(author)
    db.session.commit()
    return jsonify({'message': 'Author created successfully', 'id': author.id}), 201

# Publisher Routes
@library_bp.route('/publishers', methods=['GET'])
@jwt_required()
def get_publishers():
    publishers = Publisher.query.all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'address': p.address,
        'contact_info': p.contact_info,
        'status': p.status
    } for p in publishers])

@library_bp.route('/publishers', methods=['POST'])
@jwt_required()
@role_required(['admin', 'librarian'])
def create_publisher():
    data = request.get_json()
    publisher = Publisher(
        name=data['name'],
        address=data.get('address'),
        contact_info=data.get('contact_info'),
        status=data.get('status', 'active')
    )
    db.session.add(publisher)
    db.session.commit()
    return jsonify({'message': 'Publisher created successfully', 'id': publisher.id}), 201

# Category Routes
@library_bp.route('/categories', methods=['GET'])
@jwt_required()
def get_categories():
    categories = Category.query.all()
    return jsonify([{
        'id': c.id,
        'name': c.name,
        'description': c.description,
        'status': c.status
    } for c in categories])

@library_bp.route('/categories', methods=['POST'])
@jwt_required()
@role_required(['admin', 'librarian'])
def create_category():
    data = request.get_json()
    category = Category(
        name=data['name'],
        description=data.get('description'),
        status=data.get('status', 'active')
    )
    db.session.add(category)
    db.session.commit()
    return jsonify({'message': 'Category created successfully', 'id': category.id}), 201

# Loan Routes
@library_bp.route('/loans', methods=['GET'])
@jwt_required()
@role_required(['admin', 'librarian'])
def get_loans():
    """Get all loans with optional filters"""
    try:
        book_id = request.args.get('book_id')
        member_id = request.args.get('member_id')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Loan.query
        
        if book_id:
            query = query.filter_by(book_id=book_id)
        if member_id:
            query = query.filter_by(member_id=member_id)
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

@library_bp.route('/loans', methods=['POST'])
@jwt_required()
@role_required(['admin', 'library'])
def create_loan():
    data = request.get_json()
    loan = Loan(
        book_id=data['book_id'],
        member_id=data['member_id'],
        loan_date=datetime.fromisoformat(data['loan_date']),
        due_date=datetime.fromisoformat(data['due_date']),
        status=data.get('status', 'active')
    )
    db.session.add(loan)
    db.session.commit()
    return jsonify({'message': 'Loan created successfully', 'id': loan.id}), 201

# Reservation Routes
@library_bp.route('/reservations', methods=['GET'])
@jwt_required()
@role_required(['admin', 'librarian'])
def get_reservations():
    """Get all reservations with optional filters"""
    try:
        book_id = request.args.get('book_id')
        member_id = request.args.get('member_id')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Reservation.query
        
        if book_id:
            query = query.filter_by(book_id=book_id)
        if member_id:
            query = query.filter_by(member_id=member_id)
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

@library_bp.route('/reservations', methods=['POST'])
@jwt_required()
def create_reservation():
    data = request.get_json()
    reservation = Reservation(
        book_id=data['book_id'],
        user_id=data['user_id'],
        reservation_date=datetime.fromisoformat(data['reservation_date']),
        status=data.get('status', 'pending')
    )
    db.session.add(reservation)
    db.session.commit()
    return jsonify({'message': 'Reservation created successfully', 'id': reservation.id}), 201

# Library Card Routes
@library_bp.route('/library-cards', methods=['GET'])
@jwt_required()
def get_library_cards():
    cards = LibraryCard.query.all()
    return jsonify([{
        'id': c.id,
        'user_id': c.user_id,
        'card_number': c.card_number,
        'issue_date': c.issue_date.isoformat(),
        'expiry_date': c.expiry_date.isoformat(),
        'status': c.status
    } for c in cards])

@library_bp.route('/library-cards', methods=['POST'])
@jwt_required()
@role_required(['admin', 'librarian'])
def create_library_card():
    data = request.get_json()
    card = LibraryCard(
        user_id=data['user_id'],
        card_number=data['card_number'],
        issue_date=datetime.fromisoformat(data['issue_date']),
        expiry_date=datetime.fromisoformat(data['expiry_date']),
        status=data.get('status', 'active')
    )
    db.session.add(card)
    db.session.commit()
    return jsonify({'message': 'Library card created successfully', 'id': card.id}), 201

# Fine Routes
@library_bp.route('/fines', methods=['GET'])
@jwt_required()
@role_required(['admin', 'librarian'])
def get_fines():
    """Get all fines with optional filters"""
    try:
        member_id = request.args.get('member_id')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Fine.query
        
        if member_id:
            query = query.filter_by(member_id=member_id)
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

@library_bp.route('/fines', methods=['POST'])
@jwt_required()
@role_required(['admin', 'librarian'])
def create_fine():
    data = request.get_json()
    fine = Fine(
        loan_id=data['loan_id'],
        amount=data['amount'],
        currency=data['currency'],
        issue_date=datetime.fromisoformat(data['issue_date']),
        status=data.get('status', 'unpaid')
    )
    db.session.add(fine)
    db.session.commit()
    return jsonify({'message': 'Fine created successfully', 'id': fine.id}), 201

# Library Resource Routes
@library_bp.route('/resources', methods=['GET'])
@jwt_required()
def get_resources():
    """Get all library resources with optional filters"""
    try:
        resource_type = request.args.get('resource_type')
        category = request.args.get('category')
        status = request.args.get('status')
        
        query = LibraryResource.query
        
        if resource_type:
            query = query.filter_by(resource_type=resource_type)
        if category:
            query = query.filter_by(category=category)
        if status:
            query = query.filter_by(status=status)
        
        resources = query.all()
        return format_response([resource.to_dict() for resource in resources])
    except Exception as e:
        return handle_exception(e)

@library_bp.route('/resources', methods=['POST'])
@jwt_required()
@role_required(['admin', 'library'])
def create_resource():
    data = request.get_json()
    resource = LibraryResource(
        title=data['title'],
        resource_type=data['resource_type'],
        section_id=data['section_id'],
        status=data.get('status', 'available'),
        available_copies=data.get('available_copies', 1)
    )
    db.session.add(resource)
    db.session.commit()
    return jsonify({'message': 'Library resource added successfully', 'id': resource.id}), 201

# Library Member Routes
@library_bp.route('/members', methods=['GET'])
@jwt_required()
@role_required(['admin', 'librarian'])
def get_members():
    """Get all library members with optional filters"""
    try:
        member_type = request.args.get('member_type')
        status = request.args.get('status')
        
        query = LibraryMember.query
        
        if member_type:
            query = query.filter_by(member_type=member_type)
        if status:
            query = query.filter_by(status=status)
        
        members = query.all()
        return format_response([member.to_dict() for member in members])
    except Exception as e:
        return handle_exception(e)

@library_bp.route('/members', methods=['POST'])
@jwt_required()
@role_required(['admin', 'library'])
def create_member():
    data = request.get_json()
    member = LibraryMember(
        user_id=data['user_id'],
        membership_type=data['membership_type'],
        start_date=datetime.fromisoformat(data['start_date']),
        end_date=datetime.fromisoformat(data['end_date']) if data.get('end_date') else None,
        status=data.get('status', 'active')
    )
    db.session.add(member)
    db.session.commit()
    return jsonify({'message': 'Library member added successfully', 'id': member.id}), 201

# Library Section Routes
@library_bp.route('/sections', methods=['GET'])
@jwt_required()
def get_sections():
    sections = LibrarySection.query.all()
    return jsonify([{
        'id': s.id,
        'name': s.name,
        'description': s.description,
        'floor': s.floor,
        'status': s.status
    } for s in sections])

@library_bp.route('/sections', methods=['POST'])
@jwt_required()
@role_required(['admin', 'library'])
def create_section():
    data = request.get_json()
    section = LibrarySection(
        name=data['name'],
        description=data.get('description'),
        floor=data['floor'],
        status=data.get('status', 'active')
    )
    db.session.add(section)
    db.session.commit()
    return jsonify({'message': 'Library section created successfully', 'id': section.id}), 201

# Library Staff Routes
@library_bp.route('/staff', methods=['GET'])
@jwt_required()
@role_required(['admin', 'library'])
def get_staff():
    staff = LibraryStaff.query.all()
    return jsonify([{
        'id': s.id,
        'user_id': s.user_id,
        'role': s.role,
        'section_id': s.section_id,
        'status': s.status
    } for s in staff])

@library_bp.route('/staff', methods=['POST'])
@jwt_required()
@role_required(['admin', 'library'])
def create_staff():
    data = request.get_json()
    staff = LibraryStaff(
        user_id=data['user_id'],
        role=data['role'],
        section_id=data['section_id'],
        status=data.get('status', 'active')
    )
    db.session.add(staff)
    db.session.commit()
    return jsonify({'message': 'Library staff added successfully', 'id': staff.id}), 201

# Library Event Routes
@library_bp.route('/events', methods=['GET'])
@jwt_required()
def get_events():
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

@library_bp.route('/events', methods=['POST'])
@jwt_required()
@role_required(['admin', 'library'])
def create_event():
    data = request.get_json()
    event = LibraryEvent(
        title=data['title'],
        description=data['description'],
        event_date=datetime.fromisoformat(data['event_date']),
        location=data['location'],
        status=data.get('status', 'scheduled')
    )
    db.session.add(event)
    db.session.commit()
    return jsonify({'message': 'Library event created successfully', 'id': event.id}), 201 