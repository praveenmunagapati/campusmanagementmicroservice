import pytest
from university_management.security.base_security_test import BaseSecurityTest

class TestFinanceSecurity(BaseSecurityTest):
    def __init__(self):
        super().__init__('http://localhost:5000/api/finance')
        self.test_invoice = {
            'student_id': 1,
            'amount': 1000.00,
            'description': 'Tuition Fee'
        }
        self.test_payment = {
            'invoice_id': 1,
            'amount': 1000.00,
            'payment_method': 'credit_card'
        }
        self.test_financial_aid = {
            'student_id': 1,
            'amount': 5000.00,
            'aid_type': 'scholarship'
        }

    def test_invoice_endpoint_security(self):
        """Test security for invoice-related endpoints"""
        endpoint = '/invoices'
        
        # Test authentication
        self.test_unauthorized_access(endpoint)
        self.test_invalid_token(endpoint)
        self.test_expired_token(endpoint)
        
        # Test role-based access
        roles = {
            'admin': 200,
            'finance_staff': 200,
            'student': 403,
            'faculty': 403
        }
        self.test_role_based_access(endpoint, 'POST', roles)
        
        # Test for vulnerabilities
        self.test_sql_injection(endpoint, self.test_invoice)
        self.test_xss_prevention(endpoint, self.test_invoice)
        self.test_rate_limiting(endpoint)
        self.test_security_headers(endpoint)
        self.test_csrf_protection(endpoint, 'POST', self.test_invoice)
        self.run_vulnerability_scan(endpoint, self.test_invoice)

    def test_payment_endpoint_security(self):
        """Test security for payment-related endpoints"""
        endpoint = '/payments'
        
        # Test authentication
        self.test_unauthorized_access(endpoint)
        self.test_invalid_token(endpoint)
        self.test_expired_token(endpoint)
        
        # Test role-based access
        roles = {
            'admin': 200,
            'finance_staff': 200,
            'student': 200,  # Students can make payments
            'faculty': 403
        }
        self.test_role_based_access(endpoint, 'POST', roles)
        
        # Test for vulnerabilities
        self.test_sql_injection(endpoint, self.test_payment)
        self.test_xss_prevention(endpoint, self.test_payment)
        self.test_rate_limiting(endpoint)
        self.test_security_headers(endpoint)
        self.test_csrf_protection(endpoint, 'POST', self.test_payment)
        self.run_vulnerability_scan(endpoint, self.test_payment)

    def test_financial_aid_endpoint_security(self):
        """Test security for financial aid-related endpoints"""
        endpoint = '/financial-aid'
        
        # Test authentication
        self.test_unauthorized_access(endpoint)
        self.test_invalid_token(endpoint)
        self.test_expired_token(endpoint)
        
        # Test role-based access
        roles = {
            'admin': 200,
            'finance_staff': 200,
            'financial_aid_officer': 200,
            'student': 403,
            'faculty': 403
        }
        self.test_role_based_access(endpoint, 'POST', roles)
        
        # Test for vulnerabilities
        self.test_sql_injection(endpoint, self.test_financial_aid)
        self.test_xss_prevention(endpoint, self.test_financial_aid)
        self.test_rate_limiting(endpoint)
        self.test_security_headers(endpoint)
        self.test_csrf_protection(endpoint, 'POST', self.test_financial_aid)
        self.run_vulnerability_scan(endpoint, self.test_financial_aid)

    def test_sensitive_data_protection(self):
        """Test protection of sensitive financial data"""
        endpoints = ['/invoices', '/payments', '/financial-aid']
        
        for endpoint in endpoints:
            response = self.utils.create_mock_request(
                headers={'Accept': 'application/json'}
            )
            
            # Verify data encryption in transit
            assert 'https://' in self.base_url, "API must use HTTPS"
            
            # Verify sensitive data masking
            if response.json:
                data = response.json()
                if 'credit_card' in str(data):
                    assert '****' in str(data), "Credit card numbers should be masked"
                if 'ssn' in str(data):
                    assert '***-**-' in str(data), "SSN should be masked"

if __name__ == '__main__':
    pytest.main([__file__]) 