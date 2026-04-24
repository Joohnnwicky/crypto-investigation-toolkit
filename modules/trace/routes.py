"""Flask Blueprint routes for transaction tracing tools"""

from flask import Blueprint, jsonify, request, Response, render_template
from modules.core.exporter import export_json

# Create Blueprint for transaction tracing tools
trace_bp = Blueprint('trace', __name__, url_prefix='/trace')

# Sample data constants (per D-13)
SAMPLE_ADDRESS = "0xdAC17F958D2ee523a2206206994597C13D831ec7"  # USDT contract
SAMPLE_DEPOSIT_TIME = "2024-04-10 14:32:18"
SAMPLE_BTC_TX_HASH = "a1075db55d416d3ca199f55b6084e2115b9345e16c5cf302fc80e9d5fbf5d48d"


# ===================== Uniswap Routes =====================

@trace_bp.route('/api/uniswap/query', methods=['POST'])
def uniswap_query():
    """API endpoint for Uniswap Swap tracing.

    Request JSON body: {"address": "ETH_ADDRESS", "api_key": "ETHERSCAN_API_KEY"}
    Response JSON: {"success": bool, "address": str, "swaps": list, "flow_diagram": str}
    """
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': '请提供JSON数据'}), 400

    address = data.get('address', '')
    api_key = data.get('api_key', '')

    if not address:
        return jsonify({'success': False, 'error': '请提供ETH地址'}), 400

    if not api_key:
        return jsonify({'success': False, 'error': '请提供Etherscan API密钥'}), 400

    # Import and call tracker
    from .uniswap_tracker import trace_address_swaps_web
    result = trace_address_swaps_web(address, api_key)

    if result['success']:
        return jsonify(result)
    else:
        return jsonify(result), 400


@trace_bp.route('/uniswap')
def uniswap_page():
    """Page route for Uniswap tracing tool."""
    return render_template('trace/uniswap.html')


@trace_bp.route('/api/uniswap/sample')
def uniswap_sample():
    """Sample address for demo."""
    return jsonify({"sample_address": SAMPLE_ADDRESS})


@trace_bp.route('/api/uniswap/export/json', methods=['POST'])
def uniswap_export_json():
    """Export Uniswap trace result as JSON file."""
    data = request.get_json()
    if not data or 'result' not in data:
        return jsonify({'error': '请提供查询结果数据'}), 400

    result = data['result']
    address = result.get('address', 'unknown')

    json_content = export_json(result)

    import datetime
    date_str = datetime.datetime.now().strftime('%Y%m%d')
    addr_short = address[:8] + address[-4:] if len(address) > 12 else address
    filename = f"uniswap_trace_{addr_short}_{date_str}.json"

    response = Response(
        json_content,
        mimetype='application/json',
        headers={'Content-Disposition': f'attachment; filename="{filename}"'}
    )
    return response


@trace_bp.route('/api/uniswap/export/csv', methods=['POST'])
def uniswap_export_csv():
    """Export Uniswap swaps as CSV file."""
    data = request.get_json()
    if not data or 'result' not in data:
        return jsonify({'error': '请提供查询结果数据'}), 400

    result = data['result']
    swaps = result.get('swaps', [])

    import csv
    from io import StringIO

    output = StringIO()
    writer = csv.writer(output)

    writer.writerow(['序号', '交易哈希', 'Swap类型', '输入', '输出', '时间'])

    for i, swap in enumerate(swaps):
        writer.writerow([
            i + 1,
            swap.get('hash', ''),
            swap.get('type', ''),
            swap.get('amount_in', ''),
            swap.get('amount_out', ''),
            swap.get('time', '')
        ])

    address = result.get('address', 'unknown')
    import datetime
    date_str = datetime.datetime.now().strftime('%Y%m%d')
    filename = f"uniswap_trace_{address[:8]}_{date_str}.csv"

    response = Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': f'attachment; filename="{filename}"'}
    )
    return response


# ===================== Mixer Routes =====================

@trace_bp.route('/api/mixer/query', methods=['POST'])
def mixer_query():
    """API endpoint for Tornado Cash mixer tracing.

    Request JSON body: {"deposit_time": "YYYY-MM-DD HH:MM:SS"}
    Response JSON: {"success": bool, "deposit_time": str, "suspicious_withdrawals": list}
    """
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': '请提供JSON数据'}), 400

    deposit_time = data.get('deposit_time', '')
    if not deposit_time:
        return jsonify({'success': False, 'error': '请提供存款时间'}), 400

    # Import and call tracker
    from .mixer_tracker import time_window_analysis_web
    result = time_window_analysis_web(deposit_time)

    if result['success']:
        return jsonify(result)
    else:
        return jsonify(result), 400


@trace_bp.route('/mixer')
def mixer_page():
    """Page route for Mixer tracing tool."""
    return render_template('trace/mixer.html')


@trace_bp.route('/api/mixer/sample')
def mixer_sample():
    """Sample deposit time for demo."""
    return jsonify({"sample_deposit_time": SAMPLE_DEPOSIT_TIME})


@trace_bp.route('/api/mixer/export/json', methods=['POST'])
def mixer_export_json():
    """Export mixer trace result as JSON file."""
    data = request.get_json()
    if not data or 'result' not in data:
        return jsonify({'error': '请提供查询结果数据'}), 400

    result = data['result']

    json_content = export_json(result)

    import datetime
    date_str = datetime.datetime.now().strftime('%Y%m%d')
    filename = f"mixer_trace_{date_str}.json"

    response = Response(
        json_content,
        mimetype='application/json',
        headers={'Content-Disposition': f'attachment; filename="{filename}"'}
    )
    return response


# ===================== BTC Routes =====================

@trace_bp.route('/api/btc/query', methods=['POST'])
def btc_query():
    """API endpoint for BTC transaction analysis.

    Request JSON body: {"tx_hash": "64_HEX_CHARS"}
    Response JSON: {"success": bool, "tx_hash": str, "transaction": dict}
    """
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': '请提供JSON数据'}), 400

    tx_hash = data.get('tx_hash', '')
    if not tx_hash:
        return jsonify({'success': False, 'error': '请提供交易哈希'}), 400

    # Import and call analyzer
    from .btc_analyzer import analyze_btc_transaction_web
    result = analyze_btc_transaction_web(tx_hash)

    if result['success']:
        return jsonify(result)
    else:
        return jsonify(result), 400


@trace_bp.route('/btc')
def btc_page():
    """Page route for BTC analysis tool."""
    return render_template('trace/btc.html')


@trace_bp.route('/api/btc/sample')
def btc_sample():
    """Sample BTC transaction hash for demo."""
    return jsonify({"sample_tx_hash": SAMPLE_BTC_TX_HASH})


@trace_bp.route('/api/btc/export/json', methods=['POST'])
def btc_export_json():
    """Export BTC analysis result as JSON file."""
    data = request.get_json()
    if not data or 'result' not in data:
        return jsonify({'error': '请提供查询结果数据'}), 400

    result = data['result']
    tx_hash = result.get('tx_hash', 'unknown')

    json_content = export_json(result)

    import datetime
    date_str = datetime.datetime.now().strftime('%Y%m%d')
    filename = f"btc_analysis_{tx_hash[:8]}_{date_str}.json"

    response = Response(
        json_content,
        mimetype='application/json',
        headers={'Content-Disposition': f'attachment; filename="{filename}"'}
    )
    return response


@trace_bp.route('/api/btc/export/csv', methods=['POST'])
def btc_export_csv():
    """Export BTC transaction details as CSV file."""
    data = request.get_json()
    if not data or 'result' not in data:
        return jsonify({'error': '请提供查询结果数据'}), 400

    result = data['result']
    tx_info = result.get('transaction', {})

    import csv
    from io import StringIO

    output = StringIO()
    writer = csv.writer(output)

    writer.writerow(['类型', '地址', '金额', '地址类型', '钱包提示'])

    # Write outputs
    for out in tx_info.get('vout', []):
        writer.writerow([
            '输出',
            out.get('address', ''),
            out.get('value', 0) / 100000000 if out.get('value') else 0,
            out.get('address_type', ''),
            out.get('wallet_hint', '')
        ])

    tx_hash = result.get('tx_hash', 'unknown')
    import datetime
    date_str = datetime.datetime.now().strftime('%Y%m%d')
    filename = f"btc_analysis_{tx_hash[:8]}_{date_str}.csv"

    response = Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': f'attachment; filename="{filename}"'}
    )
    return response