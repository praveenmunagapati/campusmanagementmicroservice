from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import Tuition, Fee, Payment, FinancialAid, Scholarship, Budget, Expense, Revenue, Invoice, Refund
from . import db
from datetime import datetime
from utils import role_required, validate_request, format_response, log_activity, handle_exception

finance_bp = Blueprint('finance', __name__)

# Tuition Routes
@finance_bp.route('/tuition', methods=['GET'])
@jwt_required()
@role_required(['admin', 'finance_staff', 'student'])
def get_tuition_rates():
    """Get tuition rates with optional filters"""
    try:
        program_id = request.args.get('program_id')
        academic_year = request.args.get('academic_year')
        term = request.args.get('term')
        status = request.args.get('status')
        
        query = Tuition.query
        
        if program_id:
            query = query.filter_by(program_id=program_id)
        if academic_year:
            query = query.filter_by(academic_year=academic_year)
        if term:
            query = query.filter_by(term=term)
        if status:
            query = query.filter_by(status=status)
        
        tuition_rates = query.all()
        return format_response([rate.to_dict() for rate in tuition_rates])
    except Exception as e:
        return handle_exception(e)

@finance_bp.route('/tuition', methods=['POST'])
@jwt_required()
@role_required(['admin', 'finance'])
def create_tuition_rate():
    data = request.get_json()
    tuition = Tuition(
        program_id=data['program_id'],
        academic_year=data['academic_year'],
        term=data['term'],
        amount=data['amount'],
        currency=data['currency'],
        status=data.get('status', 'active')
    )
    db.session.add(tuition)
    db.session.commit()
    return jsonify({'message': 'Tuition rate created successfully', 'id': tuition.id}), 201

# Fee Routes
@finance_bp.route('/fees', methods=['GET'])
@jwt_required()
@role_required(['admin', 'finance_staff', 'student'])
def get_fees():
    """Get all fees with optional filters"""
    try:
        fee_type = request.args.get('fee_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Fee.query
        
        if fee_type:
            query = query.filter_by(fee_type=fee_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(Fee.effective_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Fee.effective_date <= datetime.fromisoformat(end_date))
        
        fees = query.all()
        return format_response([fee.to_dict() for fee in fees])
    except Exception as e:
        return handle_exception(e)

@finance_bp.route('/fees', methods=['POST'])
@jwt_required()
@role_required(['admin', 'finance'])
def create_fee():
    data = request.get_json()
    fee = Fee(
        name=data['name'],
        description=data.get('description'),
        amount=data['amount'],
        currency=data['currency'],
        fee_type=data['fee_type'],
        status=data.get('status', 'active')
    )
    db.session.add(fee)
    db.session.commit()
    return jsonify({'message': 'Fee created successfully', 'id': fee.id}), 201

# Payment Routes
@finance_bp.route('/payments', methods=['GET'])
@jwt_required()
@role_required(['admin', 'finance_staff', 'student'])
def get_payments():
    """Get all payments with optional filters"""
    try:
        student_id = request.args.get('student_id')
        payment_type = request.args.get('payment_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Payment.query
        
        if student_id:
            query = query.filter_by(student_id=student_id)
        if payment_type:
            query = query.filter_by(payment_type=payment_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(Payment.payment_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Payment.payment_date <= datetime.fromisoformat(end_date))
        
        payments = query.all()
        return format_response([payment.to_dict() for payment in payments])
    except Exception as e:
        return handle_exception(e)

@finance_bp.route('/payments', methods=['POST'])
@jwt_required()
def create_payment():
    data = request.get_json()
    payment = Payment(
        student_id=data['student_id'],
        amount=data['amount'],
        currency=data['currency'],
        payment_date=datetime.fromisoformat(data['payment_date']),
        payment_method=data['payment_method'],
        transaction_id=data.get('transaction_id'),
        status=data.get('status', 'pending')
    )
    db.session.add(payment)
    db.session.commit()
    return jsonify({'message': 'Payment created successfully', 'id': payment.id}), 201

# Financial Aid Routes
@finance_bp.route('/financial-aid', methods=['GET'])
@jwt_required()
@role_required(['admin', 'finance_staff', 'student'])
def get_financial_aid():
    """Get all financial aid records with optional filters"""
    try:
        student_id = request.args.get('student_id')
        aid_type = request.args.get('aid_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = FinancialAid.query
        
        if student_id:
            query = query.filter_by(student_id=student_id)
        if aid_type:
            query = query.filter_by(aid_type=aid_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(FinancialAid.application_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(FinancialAid.application_date <= datetime.fromisoformat(end_date))
        
        aid_records = query.all()
        return format_response([record.to_dict() for record in aid_records])
    except Exception as e:
        return handle_exception(e)

@finance_bp.route('/financial-aid', methods=['POST'])
@jwt_required()
@role_required(['admin', 'finance'])
def create_financial_aid():
    data = request.get_json()
    financial_aid = FinancialAid(
        student_id=data['student_id'],
        aid_type=data['aid_type'],
        amount=data['amount'],
        currency=data['currency'],
        start_date=datetime.fromisoformat(data['start_date']),
        end_date=datetime.fromisoformat(data['end_date']),
        status=data.get('status', 'active')
    )
    db.session.add(financial_aid)
    db.session.commit()
    return jsonify({'message': 'Financial aid created successfully', 'id': financial_aid.id}), 201

# Scholarship Routes
@finance_bp.route('/scholarships', methods=['GET'])
@jwt_required()
@role_required(['admin', 'finance_staff', 'student'])
def get_scholarships():
    """Get all scholarships with optional filters"""
    try:
        scholarship_type = request.args.get('scholarship_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Scholarship.query
        
        if scholarship_type:
            query = query.filter_by(scholarship_type=scholarship_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(Scholarship.start_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Scholarship.end_date <= datetime.fromisoformat(end_date))
        
        scholarships = query.all()
        return format_response([scholarship.to_dict() for scholarship in scholarships])
    except Exception as e:
        return handle_exception(e)

@finance_bp.route('/scholarships', methods=['POST'])
@jwt_required()
@role_required(['admin', 'finance'])
def create_scholarship():
    data = request.get_json()
    scholarship = Scholarship(
        name=data['name'],
        description=data.get('description'),
        amount=data['amount'],
        currency=data['currency'],
        criteria=data['criteria'],
        status=data.get('status', 'active')
    )
    db.session.add(scholarship)
    db.session.commit()
    return jsonify({'message': 'Scholarship created successfully', 'id': scholarship.id}), 201

# Budget Routes
@finance_bp.route('/budgets', methods=['GET'])
@jwt_required()
@role_required(['admin', 'finance_staff'])
def get_budgets():
    """Get all budgets with optional filters"""
    try:
        department_id = request.args.get('department_id')
        fiscal_year = request.args.get('fiscal_year')
        status = request.args.get('status')
        
        query = Budget.query
        
        if department_id:
            query = query.filter_by(department_id=department_id)
        if fiscal_year:
            query = query.filter_by(fiscal_year=fiscal_year)
        if status:
            query = query.filter_by(status=status)
        
        budgets = query.all()
        return format_response([budget.to_dict() for budget in budgets])
    except Exception as e:
        return handle_exception(e)

@finance_bp.route('/budgets', methods=['POST'])
@jwt_required()
@role_required(['admin', 'finance'])
def create_budget():
    data = request.get_json()
    budget = Budget(
        department_id=data['department_id'],
        fiscal_year=data['fiscal_year'],
        amount=data['amount'],
        currency=data['currency'],
        status=data.get('status', 'active')
    )
    db.session.add(budget)
    db.session.commit()
    return jsonify({'message': 'Budget created successfully', 'id': budget.id}), 201

# Expense Routes
@finance_bp.route('/expenses', methods=['GET'])
@jwt_required()
@role_required(['admin', 'finance_staff'])
def get_expenses():
    """Get all expenses with optional filters"""
    try:
        department_id = request.args.get('department_id')
        expense_type = request.args.get('expense_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Expense.query
        
        if department_id:
            query = query.filter_by(department_id=department_id)
        if expense_type:
            query = query.filter_by(expense_type=expense_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(Expense.expense_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Expense.expense_date <= datetime.fromisoformat(end_date))
        
        expenses = query.all()
        return format_response([expense.to_dict() for expense in expenses])
    except Exception as e:
        return handle_exception(e)

@finance_bp.route('/expenses', methods=['POST'])
@jwt_required()
@role_required(['admin', 'finance'])
def create_expense():
    data = request.get_json()
    expense = Expense(
        department_id=data['department_id'],
        amount=data['amount'],
        currency=data['currency'],
        expense_date=datetime.fromisoformat(data['expense_date']),
        category=data['category'],
        description=data.get('description'),
        status=data.get('status', 'pending')
    )
    db.session.add(expense)
    db.session.commit()
    return jsonify({'message': 'Expense created successfully', 'id': expense.id}), 201

# Revenue Routes
@finance_bp.route('/revenue', methods=['GET'])
@jwt_required()
@role_required(['admin', 'finance_staff'])
def get_revenue():
    """Get all revenue records with optional filters"""
    try:
        revenue_type = request.args.get('revenue_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Revenue.query
        
        if revenue_type:
            query = query.filter_by(revenue_type=revenue_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(Revenue.revenue_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Revenue.revenue_date <= datetime.fromisoformat(end_date))
        
        revenue_records = query.all()
        return format_response([record.to_dict() for record in revenue_records])
    except Exception as e:
        return handle_exception(e)

@finance_bp.route('/revenues', methods=['GET'])
@jwt_required()
@role_required(['admin', 'finance'])
def get_revenues():
    revenues = Revenue.query.all()
    return jsonify([{
        'id': r.id,
        'source': r.source,
        'amount': r.amount,
        'currency': r.currency,
        'revenue_date': r.revenue_date.isoformat(),
        'category': r.category,
        'description': r.description,
        'status': r.status
    } for r in revenues])

@finance_bp.route('/revenues', methods=['POST'])
@jwt_required()
@role_required(['admin', 'finance'])
def create_revenue():
    data = request.get_json()
    revenue = Revenue(
        source=data['source'],
        amount=data['amount'],
        currency=data['currency'],
        revenue_date=datetime.fromisoformat(data['revenue_date']),
        category=data['category'],
        description=data.get('description'),
        status=data.get('status', 'pending')
    )
    db.session.add(revenue)
    db.session.commit()
    return jsonify({'message': 'Revenue created successfully', 'id': revenue.id}), 201

# Invoice Routes
@finance_bp.route('/invoices', methods=['GET'])
@jwt_required()
@role_required(['admin', 'finance_staff'])
def get_invoices():
    """Get all invoices with optional filters"""
    try:
        student_id = request.args.get('student_id')
        invoice_type = request.args.get('invoice_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Invoice.query
        
        if student_id:
            query = query.filter_by(student_id=student_id)
        if invoice_type:
            query = query.filter_by(invoice_type=invoice_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(Invoice.invoice_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Invoice.invoice_date <= datetime.fromisoformat(end_date))
        
        invoices = query.all()
        return format_response([invoice.to_dict() for invoice in invoices])
    except Exception as e:
        return handle_exception(e)

@finance_bp.route('/invoices', methods=['POST'])
@jwt_required()
@role_required(['admin', 'finance'])
def create_invoice():
    data = request.get_json()
    invoice = Invoice(
        student_id=data['student_id'],
        amount=data['amount'],
        currency=data['currency'],
        due_date=datetime.fromisoformat(data['due_date']),
        status=data.get('status', 'pending')
    )
    db.session.add(invoice)
    db.session.commit()
    return jsonify({'message': 'Invoice created successfully', 'id': invoice.id}), 201

# Refund Routes
@finance_bp.route('/refunds', methods=['GET'])
@jwt_required()
@role_required(['admin', 'finance_staff'])
def get_refunds():
    """Get all refunds with optional filters"""
    try:
        student_id = request.args.get('student_id')
        refund_type = request.args.get('refund_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Refund.query
        
        if student_id:
            query = query.filter_by(student_id=student_id)
        if refund_type:
            query = query.filter_by(refund_type=refund_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(Refund.refund_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Refund.refund_date <= datetime.fromisoformat(end_date))
        
        refunds = query.all()
        return format_response([refund.to_dict() for refund in refunds])
    except Exception as e:
        return handle_exception(e)

@finance_bp.route('/refunds', methods=['POST'])
@jwt_required()
@role_required(['admin', 'finance'])
def create_refund():
    data = request.get_json()
    refund = Refund(
        student_id=data['student_id'],
        amount=data['amount'],
        currency=data['currency'],
        refund_date=datetime.fromisoformat(data['refund_date']),
        reason=data['reason'],
        status=data.get('status', 'pending')
    )
    db.session.add(refund)
    db.session.commit()
    return jsonify({'message': 'Refund created successfully', 'id': refund.id}), 201 