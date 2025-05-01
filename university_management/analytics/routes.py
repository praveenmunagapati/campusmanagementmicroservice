from flask import Blueprint, jsonify, request
from .models import AnalyticsData, Report, Dashboard
from .. import db

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/analytics/data', methods=['GET'])
def get_analytics_data():
    """Get all analytics data"""
    data = AnalyticsData.query.all()
    return jsonify([item.to_dict() for item in data])

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

@analytics_bp.route('/analytics/reports', methods=['GET'])
def get_reports():
    """Get all reports"""
    reports = Report.query.all()
    return jsonify([report.to_dict() for report in reports])

@analytics_bp.route('/analytics/reports/<int:id>', methods=['GET'])
def get_report_by_id(id):
    """Get specific report by ID"""
    report = Report.query.get_or_404(id)
    return jsonify(report.to_dict())

@analytics_bp.route('/analytics/dashboards', methods=['GET'])
def get_dashboards():
    """Get all dashboards"""
    dashboards = Dashboard.query.all()
    return jsonify([dashboard.to_dict() for dashboard in dashboards])

@analytics_bp.route('/analytics/dashboards/<int:id>', methods=['GET'])
def get_dashboard_by_id(id):
    """Get specific dashboard by ID"""
    dashboard = Dashboard.query.get_or_404(id)
    return jsonify(dashboard.to_dict())

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