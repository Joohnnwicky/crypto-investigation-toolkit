"""Flask Blueprint routes for case handling tools"""

from flask import Blueprint, jsonify, request, Response, render_template
from modules.core.exporter import export_json
import datetime
import csv
from io import StringIO

# Create Blueprint for case handling tools
case_bp = Blueprint('case', __name__, url_prefix='/case')

# Sample data constants
SAMPLE_TRON_ADDRESS = "TUtPv8ZD7WKxMQFQ8RyD3m5yP9NhS3qLNNw"
SAMPLE_ETH_ADDRESS = "0xdAC17F958D2ee523a2206206994597C13D831ec7"
SAMPLE_BTC_ADDRESS = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"


# ===================== Monitor Routes =====================

@case_bp.route('/api/monitor/sample')
def monitor_sample():
    """Sample addresses for demo."""
    return jsonify({
        "sample_addresses": [
            SAMPLE_TRON_ADDRESS,
            SAMPLE_ETH_ADDRESS,
            SAMPLE_BTC_ADDRESS
        ]
    })


@case_bp.route('/api/monitor/query', methods=['POST'])
def monitor_query():
    """API endpoint for multi-chain address monitoring.

    Request JSON body: {"addresses": ["..."], "eth_key": "..."}
    Response JSON: {"success": bool, "addresses": [...], "status_cards": [...], "total_count": N}
    """
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': '请提供JSON数据'}), 400

    addresses = data.get('addresses', [])
    eth_key = data.get('eth_key', '')

    # Import and call monitor
    from .monitor import monitor_addresses_web
    result = monitor_addresses_web(addresses, eth_key)

    if result['success']:
        return jsonify(result)
    else:
        return jsonify(result), 400


@case_bp.route('/api/monitor/export/json', methods=['POST'])
def monitor_export_json():
    """Export monitor result as JSON file."""
    data = request.get_json()
    if not data or 'result' not in data:
        return jsonify({'error': '请提供查询结果数据'}), 400

    result = data['result']
    json_content = export_json(result)

    date_str = datetime.datetime.now().strftime('%Y%m%d')
    filename = f"monitor_result_{date_str}.json"

    response = Response(
        json_content,
        mimetype='application/json',
        headers={'Content-Disposition': f'attachment; filename="{filename}"'}
    )
    return response


@case_bp.route('/api/monitor/export/csv', methods=['POST'])
def monitor_export_csv():
    """Export monitor result as CSV file."""
    data = request.get_json()
    if not data or 'result' not in data:
        return jsonify({'error': '请提供查询结果数据'}), 400

    result = data['result']
    status_cards = result.get('status_cards', [])

    output = StringIO()
    writer = csv.writer(output)

    # Header row
    writer.writerow(['地址', '链类型', '余额', '交易数', '最后活跃时间'])

    # Write status cards
    for card in status_cards:
        writer.writerow([
            card.get('address', ''),
            card.get('chain', ''),
            card.get('balance', 0),
            card.get('tx_count', 0),
            card.get('last_active', '未知')
        ])

    date_str = datetime.datetime.now().strftime('%Y%m%d')
    filename = f"monitor_result_{date_str}.csv"

    response = Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': f'attachment; filename="{filename}"'}
    )
    return response


@case_bp.route('/monitor')
def monitor_page():
    """Page route for multi-chain address monitoring tool."""
    return render_template('case/monitor.html')


# ===================== Obfuscation Detection Routes =====================

@case_bp.route('/api/obfuscation/sample')
def obfuscation_sample():
    """Sample ETH address for demo."""
    return jsonify({
        "sample_address": SAMPLE_ETH_ADDRESS
    })


@case_bp.route('/api/obfuscation/detect', methods=['POST'])
def obfuscation_detect():
    """API endpoint for attack detection.

    Request JSON body: {"address": "...", "eth_key": "..."}
    Response JSON: {"success": bool, "address": "...", "attack_cards": [...], "message": "..."}
    """
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': '请提供JSON数据'}), 400

    address = data.get('address', '')
    eth_key = data.get('eth_key', '')

    # Import and call detector
    from .obfuscation_detector import detect_attacks_web
    result = detect_attacks_web(address, eth_key)

    if result['success']:
        return jsonify(result)
    else:
        return jsonify(result), 400


@case_bp.route('/api/obfuscation/export/json', methods=['POST'])
def obfuscation_export_json():
    """Export detection result as JSON file."""
    data = request.get_json()
    if not data or 'result' not in data:
        return jsonify({'error': '请提供查询结果数据'}), 400

    result = data['result']
    json_content = export_json(result)

    date_str = datetime.datetime.now().strftime('%Y%m%d')
    filename = f"obfuscation_result_{date_str}.json"

    response = Response(
        json_content,
        mimetype='application/json',
        headers={'Content-Disposition': f'attachment; filename="{filename}"'}
    )
    return response


@case_bp.route('/api/obfuscation/export/csv', methods=['POST'])
def obfuscation_export_csv():
    """Export detection result as CSV file."""
    data = request.get_json()
    if not data or 'result' not in data:
        return jsonify({'error': '请提供查询结果数据'}), 400

    result = data['result']
    attack_cards = result.get('attack_cards', [])

    output = StringIO()
    writer = csv.writer(output)

    # Header row
    writer.writerow(['攻击类型', '置信度', '交易哈希', '详情'])

    # Write attack cards
    for card in attack_cards:
        writer.writerow([
            card.get('type', ''),
            card.get('confidence', ''),
            card.get('tx_hash', ''),
            card.get('details', '')
        ])

    date_str = datetime.datetime.now().strftime('%Y%m%d')
    filename = f"obfuscation_result_{date_str}.csv"

    response = Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': f'attachment; filename="{filename}"'}
    )
    return response


@case_bp.route('/obfuscation')
def obfuscation_page():
    """Page route for obfuscation attack detection tool."""
    return render_template('case/obfuscation.html')


# ===================== Asset Freeze Template Routes =====================

@case_bp.route('/api/asset-freeze/generate', methods=['POST'])
def asset_freeze_generate():
    """API endpoint for freeze template generation.

    Request JSON body: {"case_number": "...", "addresses": [...], ...}
    Response JSON: {"success": bool, "template_data": {...}, "plain_text": "..."}
    """
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': '请提供JSON数据'}), 400

    # Import and call generator
    from .asset_freeze_generator import generate_freeze_template_web
    result = generate_freeze_template_web(data)

    if result['success']:
        return jsonify(result)
    else:
        return jsonify(result), 400


@case_bp.route('/asset-freeze')
def asset_freeze_page():
    """Page route for asset freeze template generator tool."""
    return render_template('case/asset_freeze.html')