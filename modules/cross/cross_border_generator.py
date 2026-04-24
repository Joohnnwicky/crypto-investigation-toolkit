"""Cross-border investigation coordination template generator module"""

import logging
from datetime import datetime
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

# Required fields per D-15 to D-18
REQUIRED_FIELDS = [
    'case_number',     # 案件编号 (D-15)
    'agency',          # 调查机构 (D-15)
    'contact_person',  # 联系人 (D-15)
    'contact_method',  # 联系方式 (D-15)
    'suspicious_behavior',  # 可疑行为描述 (D-17)
    'request_type',    # 请求类型 (D-18)
    'expected_response'  # 期望回复时间 (D-18)
]


def validate_template_fields(fields: Dict[str, Any]) -> Dict[str, Any]:
    """Validate template input fields.

    Args:
        fields: Dict with template field values

    Returns:
        Dict with valid: bool, missing: list of missing required fields
    """
    missing = []
    for field in REQUIRED_FIELDS:
        value = fields.get(field, '')
        if not value or (isinstance(value, str) and not value.strip()):
            missing.append(field)

    return {
        'valid': len(missing) == 0,
        'missing': missing
    }


def generate_plain_text(fields: Dict[str, Any]) -> str:
    """Generate plain text version for clipboard copy (per D-13).

    Args:
        fields: Dict with all template fields

    Returns:
        Plain text template string
    """
    # Format address list
    addresses = fields.get('addresses', [])
    chain_types = fields.get('chain_types', [])
    address_list_formatted = ""
    for i, addr in enumerate(addresses):
        chain = chain_types[i] if i < len(chain_types) else 'unknown'
        address_list_formatted += f"  {addr} ({chain})\n"

    # Format tx hashes
    tx_hashes = fields.get('tx_hashes', [])
    tx_list_formatted = ""
    for tx in tx_hashes:
        tx_list_formatted += f"  {tx}\n"

    template = f"""
跨境虚拟货币调查协查请求

案件编号: {fields.get('case_number', '')}
调查机构: {fields.get('agency', '')}
联系人: {fields.get('contact_person', '')}
联系方式: {fields.get('contact_method', '')}

涉案地址:
{address_list_formatted if addresses else '  无'}

金额汇总: {fields.get('total_amount', '未知')}
交易哈希:
{tx_list_formatted if tx_hashes else '  无'}

可疑行为描述: {fields.get('suspicious_behavior', '')}
资金流向简述: {fields.get('fund_flow', '')}
调查背景: {fields.get('investigation_context', '')}

请求类型: {fields.get('request_type', '')}
期望回复时间: {fields.get('expected_response', '')}

---
本协查请求由虚拟币犯罪调查工具集生成，仅供合规调查使用。
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    return template.strip()


def generate_template_web(fields: Dict[str, Any]) -> Dict[str, Any]:
    """Generate cross-border coordination template (per D-14 to D-18).

    Args:
        fields: Dict with case_info, address_info, background, request

    Returns:
        Dict with success, template_data, plain_text
    """
    # Validate required fields
    validation = validate_template_fields(fields)
    if not validation['valid']:
        missing_str = ', '.join(validation['missing'])
        return {
            'success': False,
            'error': f'缺少必填字段: {missing_str}'
        }

    # Build structured template data for frontend rendering
    template_data = {
        'case_info': {
            'case_number': fields.get('case_number', ''),
            'agency': fields.get('agency', ''),
            'contact_person': fields.get('contact_person', ''),
            'contact_method': fields.get('contact_method', '')
        },
        'address_info': {
            'addresses': fields.get('addresses', []),
            'chain_types': fields.get('chain_types', []),
            'total_amount': fields.get('total_amount', '未知'),
            'tx_hashes': fields.get('tx_hashes', [])
        },
        'background': {
            'suspicious_behavior': fields.get('suspicious_behavior', ''),
            'fund_flow': fields.get('fund_flow', ''),
            'investigation_context': fields.get('investigation_context', '')
        },
        'request': {
            'request_type': fields.get('request_type', ''),
            'expected_response': fields.get('expected_response', '')
        },
        'generated_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    # Generate plain text version for copy
    plain_text = generate_plain_text(fields)

    return {
        'success': True,
        'template_data': template_data,
        'plain_text': plain_text
    }