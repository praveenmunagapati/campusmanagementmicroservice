import pytest
from .test_utils import SecurityTestUtils
from typing import Dict, Any, List
import requests

class BaseSecurityTest:
    """Base class for all microservice security tests"""

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.utils = SecurityTestUtils()
        self.default_headers = {
            'Content-Type': 'application/json'
        }

    def test_unauthorized_access(self, endpoint: str, method: str = 'GET') -> None:
        """Test access without authentication"""
        response = requests.request(method, f"{self.base_url}{endpoint}")
        assert response.status_code in [401, 403], f"Endpoint {endpoint} should require authentication"

    def test_invalid_token(self, endpoint: str, method: str = 'GET') -> None:
        """Test access with invalid token"""
        headers = self.default_headers.copy()
        headers['Authorization'] = 'Bearer invalid_token'
        response = requests.request(method, f"{self.base_url}{endpoint}", headers=headers)
        assert response.status_code == 401, f"Endpoint {endpoint} should reject invalid tokens"

    def test_expired_token(self, endpoint: str, method: str = 'GET') -> None:
        """Test access with expired token"""
        token = self.utils.generate_test_token(1, 'user', expired=True)
        headers = self.default_headers.copy()
        headers['Authorization'] = f'Bearer {token}'
        response = requests.request(method, f"{self.base_url}{endpoint}", headers=headers)
        assert response.status_code == 401, f"Endpoint {endpoint} should reject expired tokens"

    def test_role_based_access(self, endpoint: str, method: str, roles: Dict[str, int]) -> None:
        """Test role-based access control"""
        results = self.utils.test_role_based_access(
            f"{self.base_url}{endpoint}",
            method,
            roles.keys(),
            roles
        )
        for role, success in results.items():
            assert success, f"Incorrect access rights for role {role} on endpoint {endpoint}"

    def test_sql_injection(self, endpoint: str, payload: Dict[str, Any]) -> None:
        """Test SQL injection prevention"""
        for test_case in self.utils.sql_injection_test_cases():
            modified_payload = {k: test_case for k in payload.keys()}
            response = requests.post(f"{self.base_url}{endpoint}", json=modified_payload)
            assert response.status_code != 500, f"Potential SQL injection vulnerability with payload: {test_case}"

    def test_xss_prevention(self, endpoint: str, payload: Dict[str, Any]) -> None:
        """Test XSS prevention"""
        for test_case in self.utils.xss_test_cases():
            modified_payload = {k: test_case for k in payload.keys()}
            response = requests.post(f"{self.base_url}{endpoint}", json=modified_payload)
            assert test_case not in response.text, f"Potential XSS vulnerability with payload: {test_case}"

    def test_rate_limiting(self, endpoint: str, method: str = 'GET', requests_per_minute: int = 60) -> None:
        """Test rate limiting"""
        assert self.utils.rate_limit_test(
            f"{self.base_url}{endpoint}",
            method,
            requests_per_minute
        ), f"Rate limiting not properly implemented for endpoint {endpoint}"

    def test_security_headers(self, endpoint: str) -> None:
        """Test security headers"""
        response = requests.get(f"{self.base_url}{endpoint}")
        required_headers = [
            'X-Frame-Options',
            'X-XSS-Protection',
            'X-Content-Type-Options',
            'Strict-Transport-Security',
            'Content-Security-Policy'
        ]
        for header in required_headers:
            assert header in response.headers, f"Missing security header: {header}"

    def run_vulnerability_scan(self, endpoint: str, payload: Dict[str, Any]) -> None:
        """Run comprehensive vulnerability scan"""
        vulnerabilities = self.utils.vulnerability_scan(f"{self.base_url}{endpoint}", payload)
        for category, issues in vulnerabilities.items():
            assert len(issues) == 0, f"Security vulnerabilities found in {category}: {issues}"

    def test_csrf_protection(self, endpoint: str, method: str = 'POST', payload: Dict[str, Any] = None) -> None:
        """Test CSRF protection"""
        # First request to get CSRF token
        session = requests.Session()
        response = session.get(f"{self.base_url}{endpoint}")
        assert 'csrf-token' in response.headers, "CSRF token not provided"
        
        # Request without CSRF token
        response = requests.request(method, f"{self.base_url}{endpoint}", json=payload or {})
        assert response.status_code == 403, "Request without CSRF token should be rejected"
        
        # Request with CSRF token
        headers = self.default_headers.copy()
        headers['X-CSRF-Token'] = response.headers['csrf-token']
        response = session.request(method, f"{self.base_url}{endpoint}", headers=headers, json=payload or {})
        assert response.status_code != 403, "Request with valid CSRF token should be accepted" 