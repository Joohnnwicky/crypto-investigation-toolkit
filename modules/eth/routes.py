"""Flask Blueprint routes for ETH transaction query tool"""

from flask import Blueprint, jsonify, request, Response, render_template
from .eth_analyzer import query_eth_transactions_web, is_valid_eth_address
from modules.core.exporter import export_json, export_csv, get_export_filename

eth_bp = Blueprint('eth', __name__, url_prefix='/eth')


@eth_bp.route('/api/query', methods=['POST'])
def query():
    """API endpoint for ETH transaction query with Stargate detection.

    Request JSON body: {"address": "ETH_ADDRESS", "api_key": "ETHERSCAN_API_KEY"}
    Response JSON: {
        "success": bool,
        "address": str,
        "transactions": {"normal": [], "erc20": [], "total_count": int},
        "stargate_events": []
    }

    Note: API key is passed per-request per ADDR-05, never stored.
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

    result = query_eth_transactions_web(address, api_key)

    if result['success']:
        return jsonify(result)
    else:
        return jsonify(result), 400


@eth_bp.route('/transaction-query')
def transaction_query_page():
    """Page route for ETH transaction query tool.

    Returns:
        Rendered HTML template at templates/eth/transaction_query.html
    """
    return render_template('eth/transaction_query.html')


@eth_bp.route('/api/export/json', methods=['POST'])
def export_json_endpoint():
    """Export ETH transaction result as JSON file download.

    Request JSON body: {"result": analysis_result_dict}
    Response: JSON file download with Content-Disposition header
    """
    data = request.get_json()
    if not data or 'result' not in data:
        return jsonify({'error': '请提供查询结果数据'}), 400

    result = data['result']
    address = result.get('address', 'unknown')

    json_content = export_json(result)

    # Generate filename for ETH export
    date_str = __import__('datetime').datetime.now().strftime('%Y%m%d')
    addr_short = address[:8] + address[-4:] if len(address) > 12 else address
    filename = f"eth_query_{addr_short}_{date_str}.json"

    response = Response(
        json_content,
        mimetype='application/json',
        headers={'Content-Disposition': f'attachment; filename="{filename}"'}
    )
    return response


@eth_bp.route('/api/export/csv', methods=['POST'])
def export_csv_endpoint():
    """Export ETH transactions and Stargate events as CSV file download.

    Request JSON body: {"result": analysis_result_dict}
    Response: CSV file download with Content-Disposition header
    """
    data = request.get_json()
    if not data or 'result' not in data:
        return jsonify({'error': '请提供查询结果数据'}), 400

    result = data['result']
    address = result.get('address', 'unknown')

    # Export ETH-specific CSV format (transactions + stargate events)
    csv_content = export_eth_csv(result)

    # Generate filename for ETH export
    date_str = __import__('datetime').datetime.now().strftime('%Y%m%d')
    addr_short = address[:8] + address[-4:] if len(address) > 12 else address
    filename = f"eth_query_{addr_short}_{date_str}.csv"

    response = Response(
        csv_content,
        mimetype='text/csv',
        headers={'Content-Disposition': f'attachment; filename="{filename}"'}
    )
    return response


def export_eth_csv(data: dict) -> str:
    """Convert ETH query result to CSV format.

    Args:
        data: Result dict with transactions and stargate_events

    Returns:
        CSV string with transaction details and Stargate events
    """
    import csv
    from io import StringIO

    output = StringIO()
    writer = csv.writer(output)

    # Header row
    writer.writerow(['类型', '交易哈希', '时间戳', '发送方', '接收方', '金额/代币', '合约类型'])

    # Write normal transactions
    transactions = data.get('transactions', {})
    normal_txs = transactions.get('normal', [])
    erc20_txs = transactions.get('erc20', [])

    for tx in normal_txs:
        writer.writerow([
            'ETH转账',
            tx.get('hash', ''),
            tx.get('timeStamp', ''),
            tx.get('from', ''),
            tx.get('to', ''),
            tx.get('value', '0'),
            ''
        ])

    for tx in erc20_txs:
        writer.writerow([
            'ERC20转账',
            tx.get('hash', ''),
            tx.get('timeStamp', ''),
            tx.get('from', ''),
            tx.get('to', ''),
            f"{tx.get('value', '0')} {tx.get('tokenSymbol', '')}",
            ''
        ])

    # Write Stargate events
    stargate_events = data.get('stargate_events', [])
    for event in stargate_events:
        writer.writerow([
            'Stargate跨链',
            event.get('tx_hash', ''),
            event.get('timestamp', ''),
            event.get('from_address', ''),
            event.get('to_address', ''),
            event.get('value', '0'),
            event.get('contract_type', '')
        ])

    return output.getvalue()