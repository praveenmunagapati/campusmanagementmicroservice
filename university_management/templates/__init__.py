from flask import Blueprint

# Replace {service_name} with the actual service name (e.g., 'faculty', 'library', etc.)
{service_name}_bp = Blueprint('{service_name}', __name__)

from . import routes 