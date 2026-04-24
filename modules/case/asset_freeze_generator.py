"""Asset freeze request template generator module"""

import logging
from datetime import datetime
from typing import Dict, Any, List

from modules.cross.chain_detector import detect_chain_type

logger = logging.getLogger(__name__)

# Required fields per D-35, D-37
REQUIRED_FREEZE_FIELDS = [
    'case_number',       # 案件编号 (D-35)
    'agency',            # 调查机构 (D-35)
    'contact_person',    # 联系人 (D-35)
    'contact_method',    # 联系方式 (D-35)
    'suspicious_behavior',   # 可疑行为描述 (D-37)
    'freeze_necessity',  # 冻结必要性 (D-37)
]


def validate_freeze_fields(fields: Dict[str, Any]) -> Dict[str, Any]:
    """Validate freeze template input fields.

    Args:
        fields: Dict with template field values

    Returns:
        Dict with valid: bool, missing: list of missing required fields
    """
    missing = []
    for field in REQUIRED_FREEZE_FIELDS:
        value = fields.get(field, '')
        if not value or (isinstance(value, str) and not value.strip()):
            missing.append(field)

    return {
        'valid': len(missing) == 0,
        'missing': missing
    }


def detect_chain_types(addresses: List[str]) -> List[str]:
    """Detect chain types for address list.

    Args:
        addresses: List of wallet addresses

    Returns:
        List of chain type strings ('tron', 'eth', 'btc', 'unknown')
    """
    chain_types = []
    for addr in addresses:
        chain = detect_chain_type(addr)
        chain_types.append(chain)
    return chain_types


def generate_freeze_plain_text(fields: Dict[str, Any]) -> str:
    """Generate plain text version for clipboard copy (per D-40).

    Args:
        fields: Dict with all template fields

    Returns:
        Plain text template string
    """
    # Format address list (D-36)
    addresses = fields.get('addresses', [])
    chain_types = fields.get('chain_types', [])
    address_list_formatted = ""
    for i, addr in enumerate(addresses):
        chain = chain_types[i] if i < len(chain_types) else 'unknown'
        address_list_formatted += f"  {addr} ({chain})\n"

    template = f"""
虚拟货币资产冻结申请

案件编号: {fields.get('case_number', '')}
调查机构: {fields.get('agency', '')}
联系人: {fields.get('contact_person', '')}
联系方式: {fields.get('contact_method', '')}

冻结对象地址:
{address_list_formatted if addresses else '  无'}

冻结金额: {fields.get('freeze_amount', '未知')}
资产类型: {fields.get('asset_type', '未知')}

可疑行为描述: {fields.get('suspicious_behavior', '')}
资金来源说明: {fields.get('fund_source', '')}
冻结必要性: {fields.get('freeze_necessity', '')}
法律依据: {fields.get('legal_basis', '')}

冻结期限: {fields.get('freeze_duration', '')}
解除冻结条件: {fields.get('unlock_conditions', '')}
后续处理: {fields.get('follow_up', '')}

---
本冻结申请由虚拟币犯罪调查工具集生成，仅供合规调查使用。
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    return template.strip()


def generate_freeze_template_web(fields: Dict[str, Any]) -> Dict[str, Any]:
    """Generate asset freeze request template (per D-34 to D-38).

    Args:
        fields: Dict with case_info, target_info, reason_info, terms_info

    Returns:
        Dict with success, template_data, plain_text
    """
    # Detect chain types for addresses if not provided
    addresses = fields.get('addresses', [])
    chain_types = fields.get('chain_types', [])
    if addresses and not chain_types:
        chain_types = detect_chain_types(addresses)
        fields['chain_types'] = chain_types

    # Validate required fields
    validation = validate_freeze_fields(fields)
    if not validation['valid']:
        missing_str = ', '.join(validation['missing'])
        return {
            'success': False,
            'error': f'缺少必填字段: {missing_str}'
        }

    # Build structured template data with 4 sections (D-34)
    template_data = {
        'case_info': {
            'case_number': fields.get('case_number', ''),
            'agency': fields.get('agency', ''),
            'contact_person': fields.get('contact_person', ''),
            'contact_method': fields.get('contact_method', '')
        },
        'target_info': {
            'addresses': addresses,
            'chain_types': chain_types,
            'freeze_amount': fields.get('freeze_amount', '未知'),
            'asset_type': fields.get('asset_type', '未知')
        },
        'reason_info': {
            'suspicious_behavior': fields.get('suspicious_behavior', ''),
            'fund_source': fields.get('fund_source', ''),
            'freeze_necessity': fields.get('freeze_necessity', ''),
            'legal_basis': fields.get('legal_basis', '')
        },
        'terms_info': {
            'freeze_duration': fields.get('freeze_duration', ''),
            'unlock_conditions': fields.get('unlock_conditions', ''),
            'follow_up': fields.get('follow_up', '')
        },
        'generated_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    # Generate plain text version for clipboard copy (D-40)
    plain_text = generate_freeze_plain_text(fields)

    return {
        'success': True,
        'template_data': template_data,
        'plain_text': plain_text
    }