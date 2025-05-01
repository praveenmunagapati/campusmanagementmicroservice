from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import AnalyticsData, Report, Dashboard, DashboardReport, DashboardAccess, DataSource, AnalyticsJob, AnalyticsLog
from .. import db
from datetime import datetime
from utils import role_required, validate_request, format_response, log_activity, handle_exception

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/analytics/data', methods=['GET'])
@jwt_required()
@role_required(['admin', 'analyst', 'faculty'])
def get_analytics_data():
    """Get all analytics data with optional filters"""
    try:
        data_type = request.args.get('type')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = AnalyticsData.query
        
        if data_type:
            query = query.filter_by(data_type=data_type)
        if start_date:
            query = query.filter(AnalyticsData.created_at >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(AnalyticsData.created_at <= datetime.fromisoformat(end_date))
        
        data = query.all()
        return format_response([item.to_dict() for item in data])
    except Exception as e:
        return handle_exception(e)

@analytics_bp.route('/analytics/data/<int:id>', methods=['GET'])
def get_analytics_data_by_id(id):
    """Get specific analytics data by ID"""
    data = AnalyticsData.query.get_or_404(id)
    return jsonify(data.to_dict())

@analytics_bp.route('/analytics/data', methods=['POST'])
def create_analytics_data():
    """Create new analytics data"""
    data = request.get_json()
    new_data = AnalyticsData(**data)
    db.session.add(new_data)
    db.session.commit()
    return jsonify(new_data.to_dict()), 201

@analytics_bp.route('/reports', methods=['GET'])
@jwt_required()
@role_required(['admin', 'analyst', 'faculty'])
def get_reports():
    """Get all reports with optional filters"""
    try:
        report_type = request.args.get('type')
        status = request.args.get('status')
        
        query = Report.query
        
        if report_type:
            query = query.filter_by(report_type=report_type)
        if status:
            query = query.filter_by(status=status)
        
        reports = query.all()
        return format_response([report.to_dict() for report in reports])
    except Exception as e:
        return handle_exception(e)

@analytics_bp.route('/analytics/reports/<int:id>', methods=['GET'])
def get_report_by_id(id):
    """Get specific report by ID"""
    report = Report.query.get_or_404(id)
    return jsonify(report.to_dict())

@analytics_bp.route('/dashboards', methods=['GET'])
@jwt_required()
@role_required(['admin', 'analyst', 'faculty'])
def get_dashboards():
    """Get all dashboards with optional filters"""
    try:
        user_id = get_jwt_identity()['id']
        query = Dashboard.query.join(DashboardAccess).filter(
            DashboardAccess.user_id == user_id
        )
        
        dashboards = query.all()
        return format_response([dashboard.to_dict() for dashboard in dashboards])
    except Exception as e:
        return handle_exception(e)

@analytics_bp.route('/analytics/dashboards/<int:id>', methods=['GET'])
def get_dashboard_by_id(id):
    """Get specific dashboard by ID"""
    dashboard = Dashboard.query.get_or_404(id)
    return jsonify(dashboard.to_dict())

@analytics_bp.route('/data-sources', methods=['GET'])
@jwt_required()
@role_required(['admin', 'analyst'])
def get_data_sources():
    """Get all data sources"""
    try:
        sources = DataSource.query.all()
        return format_response([source.to_dict() for source in sources])
    except Exception as e:
        return handle_exception(e)

@analytics_bp.route('/jobs', methods=['GET'])
@jwt_required()
@role_required(['admin', 'analyst'])
def get_analytics_jobs():
    """Get all analytics jobs with optional filters"""
    try:
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = AnalyticsJob.query
        
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(AnalyticsJob.created_at >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(AnalyticsJob.created_at <= datetime.fromisoformat(end_date))
        
        jobs = query.all()
        return format_response([job.to_dict() for job in jobs])
    except Exception as e:
        return handle_exception(e)

@analytics_bp.route('/logs', methods=['GET'])
@jwt_required()
@role_required(['admin', 'analyst'])
def get_analytics_logs():
    """Get analytics logs with optional filters"""
    try:
        job_id = request.args.get('job_id')
        level = request.args.get('level')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = AnalyticsLog.query
        
        if job_id:
            query = query.filter_by(job_id=job_id)
        if level:
            query = query.filter_by(level=level)
        if start_date:
            query = query.filter(AnalyticsLog.created_at >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(AnalyticsLog.created_at <= datetime.fromisoformat(end_date))
        
        logs = query.all()
        return format_response([log.to_dict() for log in logs])
    except Exception as e:
        return handle_exception(e)

@analytics_bp.route('/analytics/student-performance', methods=['GET'])
def get_student_performance():
    """Get student performance analytics"""
    # Implementation for student performance analytics
    return jsonify({"message": "Student performance analytics endpoint"})

@analytics_bp.route('/analytics/course-performance', methods=['GET'])
def get_course_performance():
    """Get course performance analytics"""
    # Implementation for course performance analytics
    return jsonify({"message": "Course performance analytics endpoint"})

@analytics_bp.route('/analytics/financial', methods=['GET'])
def get_financial_analytics():
    """Get financial analytics"""
    # Implementation for financial analytics
    return jsonify({"message": "Financial analytics endpoint"}) 