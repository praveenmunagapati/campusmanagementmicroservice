from datetime import datetime
from .. import db
from sqlalchemy.dialects.postgresql import JSONB

class Report(db.Model):
    """Model for analytics reports"""
    __tablename__ = 'reports'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    report_type = db.Column(db.String(50))  # academic, financial, enrollment, etc.
    data_source = db.Column(db.String(100))  # Source of the data
    query = db.Column(db.Text)  # SQL or other query used
    parameters = db.Column(JSONB)  # Report parameters
    format = db.Column(db.String(50))  # pdf, excel, csv, etc.
    schedule = db.Column(JSONB)  # Scheduling information
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    last_run = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='active')  # active, inactive
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    metadata = db.Column(JSONB)  # Additional report data

    # Relationships
    creator = db.relationship('User', backref='created_reports')
    dashboards = db.relationship('DashboardReport', backref='report', lazy=True)

    def __repr__(self):
        return f'<Report {self.title}>'

class ReportExecution(db.Model):
    __tablename__ = 'report_executions'
    
    id = db.Column(db.Integer, primary_key=True)
    report_id = db.Column(db.Integer, db.ForeignKey('reports.id'), nullable=False)
    execution_date = db.Column(db.DateTime, nullable=False)
    parameters_used = db.Column(db.Text)  # JSON string of parameters used
    status = db.Column(db.String(20), nullable=False)  # success, failed, in_progress
    error_message = db.Column(db.Text)
    result_path = db.Column(db.String(255))  # Path to the generated report file
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    report = db.relationship('Report', backref=db.backref('executions', lazy=True))

class Dashboard(db.Model):
    """Model for analytics dashboards"""
    __tablename__ = 'dashboards'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    layout = db.Column(JSONB)  # Dashboard layout configuration
    theme = db.Column(db.String(50))  # Dashboard theme
    refresh_rate = db.Column(db.Integer)  # Refresh rate in minutes
    is_public = db.Column(db.Boolean, default=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='active')  # active, inactive
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    metadata = db.Column(JSONB)  # Additional dashboard data

    # Relationships
    creator = db.relationship('User', backref='created_dashboards')
    reports = db.relationship('DashboardReport', backref='dashboard', lazy=True)
    access_controls = db.relationship('DashboardAccess', backref='dashboard', lazy=True)

    def __repr__(self):
        return f'<Dashboard {self.title}>'

class DashboardReport(db.Model):
    """Model for reports included in dashboards"""
    __tablename__ = 'dashboard_reports'

    id = db.Column(db.Integer, primary_key=True)
    dashboard_id = db.Column(db.Integer, db.ForeignKey('dashboards.id'), nullable=False)
    report_id = db.Column(db.Integer, db.ForeignKey('reports.id'), nullable=False)
    position = db.Column(JSONB)  # Position in dashboard layout
    size = db.Column(JSONB)  # Size configuration
    refresh_rate = db.Column(db.Integer)  # Individual refresh rate
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<DashboardReport {self.id}>'

class DashboardAccess(db.Model):
    """Model for dashboard access controls"""
    __tablename__ = 'dashboard_access'

    id = db.Column(db.Integer, primary_key=True)
    dashboard_id = db.Column(db.Integer, db.ForeignKey('dashboards.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    access_level = db.Column(db.String(20))  # view, edit, admin
    granted_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    granted_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = db.relationship('User', foreign_keys=[user_id], backref='dashboard_access')
    granter = db.relationship('User', foreign_keys=[granted_by], backref='granted_access')

    def __repr__(self):
        return f'<DashboardAccess {self.id}>'

class DashboardWidget(db.Model):
    __tablename__ = 'dashboard_widgets'
    
    id = db.Column(db.Integer, primary_key=True)
    dashboard_id = db.Column(db.Integer, db.ForeignKey('dashboards.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    widget_type = db.Column(db.String(50), nullable=False)  # chart, table, metric
    data_source = db.Column(db.String(100), nullable=False)
    query = db.Column(db.Text, nullable=False)
    position = db.Column(db.Integer, nullable=False)
    size = db.Column(db.String(20))  # small, medium, large
    refresh_interval = db.Column(db.Integer)  # in minutes
    last_refresh = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    dashboard = db.relationship('Dashboard', backref=db.backref('widgets', lazy=True))

class DataSource(db.Model):
    """Model for data sources"""
    __tablename__ = 'data_sources'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    source_type = db.Column(db.String(50))  # database, api, file, etc.
    connection_details = db.Column(JSONB)  # Connection configuration
    refresh_schedule = db.Column(JSONB)  # Data refresh schedule
    last_refresh = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='active')  # active, inactive, error
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    metadata = db.Column(JSONB)  # Additional source data

    # Relationships
    creator = db.relationship('User', backref='created_data_sources')

    def __repr__(self):
        return f'<DataSource {self.name}>'

class DataSourceRefresh(db.Model):
    __tablename__ = 'data_source_refreshes'
    
    id = db.Column(db.Integer, primary_key=True)
    data_source_id = db.Column(db.Integer, db.ForeignKey('data_sources.id'), nullable=False)
    refresh_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), nullable=False)  # success, failed, in_progress
    error_message = db.Column(db.Text)
    records_processed = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    data_source = db.relationship('DataSource', backref=db.backref('refreshes', lazy=True))

class AnalyticsAlert(db.Model):
    __tablename__ = 'analytics_alerts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    alert_type = db.Column(db.String(50), nullable=False)  # threshold, anomaly, trend
    data_source = db.Column(db.String(100), nullable=False)
    query = db.Column(db.Text, nullable=False)
    condition = db.Column(db.Text)  # JSON string of alert conditions
    severity = db.Column(db.String(20), default='normal')  # low, normal, high, critical
    is_active = db.Column(db.Boolean, default=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    creator = db.relationship('User', backref=db.backref('created_alerts', lazy=True))

class AlertTrigger(db.Model):
    __tablename__ = 'alert_triggers'
    
    id = db.Column(db.Integer, primary_key=True)
    alert_id = db.Column(db.Integer, db.ForeignKey('analytics_alerts.id'), nullable=False)
    trigger_date = db.Column(db.DateTime, nullable=False)
    value = db.Column(db.Float)
    threshold = db.Column(db.Float)
    status = db.Column(db.String(20), default='active')  # active, acknowledged, resolved
    acknowledged_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    acknowledged_at = db.Column(db.DateTime)
    resolved_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    resolved_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    alert = db.relationship('AnalyticsAlert', backref=db.backref('triggers', lazy=True))
    acknowledger = db.relationship('User', foreign_keys=[acknowledged_by], backref=db.backref('acknowledged_alerts', lazy=True))
    resolver = db.relationship('User', foreign_keys=[resolved_by], backref=db.backref('resolved_alerts', lazy=True))

class AnalyticsJob(db.Model):
    """Model for analytics jobs"""
    __tablename__ = 'analytics_jobs'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    job_type = db.Column(db.String(50))  # report, data_refresh, etc.
    schedule = db.Column(JSONB)  # Job scheduling information
    parameters = db.Column(JSONB)  # Job parameters
    status = db.Column(db.String(20), default='pending')  # pending, running, completed, failed
    last_run = db.Column(db.DateTime)
    next_run = db.Column(db.DateTime)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    metadata = db.Column(JSONB)  # Additional job data

    # Relationships
    creator = db.relationship('User', backref='created_analytics_jobs')

    def __repr__(self):
        return f'<AnalyticsJob {self.name}>'

class AnalyticsLog(db.Model):
    """Model for analytics logs"""
    __tablename__ = 'analytics_logs'

    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('analytics_jobs.id'))
    event_type = db.Column(db.String(50))  # report_generated, data_refreshed, error, etc.
    message = db.Column(db.Text)
    details = db.Column(JSONB)  # Additional log details
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    job = db.relationship('AnalyticsJob', backref='logs')
    creator = db.relationship('User', backref='analytics_logs')

    def __repr__(self):
        return f'<AnalyticsLog {self.id}>' 