
from decimal import Decimal

def safe_decimal(value, default='0.00'):
    """Safely convert any price value to Decimal"""
    if value is None or value == '' or str(value).lower() == 'none':
        return Decimal(default)
    try:
        # Remove any non-numeric characters except . and -
        cleaned = ''.join(c for c in str(value) if c.isdigit() or c in '.-')
        if not cleaned or cleaned == '.':
            return Decimal(default)
        return Decimal(cleaned)
    except:
        return Decimal(default)
