"""Flask Blueprint routes for cross-chain analysis tools"""

from flask import Blueprint, jsonify, request, Response, render_template
from modules.core.exporter import export_json
import datetime
import csv
from io import StringIO

# Create Blueprint for cross-chain analysis tools
cross_bp = Blueprint('cross', __name__, url_prefix='/cross')

# Sample data constants (per D-04)
SAMPLE_TRON_ADDRESS = "TUtPv8ZD7WKxMQFQ8RyD3m5yP9NhS3qLNNw"  # Sample TRON address
SAMPLE_ETH_ADDRESS = "0xdAC17F958D2ee523a2206206994597C13D831ec7"  # USDT contract
SAMPLE_BTC_ADDRESS = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"  # Genesis block address


# ===================== Cluster Routes =====================

@cross_bp.route('/api/cluster/query', methods=['POST'])
def cluster_query():
    """API endpoint for address clustering.

    Request JSON body: {"addresses": ["..."], "eth_key": "..."}
    Response JSON: {"success": bool, "addresses": [...], "clusters": [...], "unassociated": [...]}
    """
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': '请提供JSON数据'}), 400

    addresses = data.get('addresses', [])
    eth_key = data.get('eth_key', '')

    # Clean addresses (strip whitespace, filter empty)
    addresses = [addr.strip() for addr in addresses if addr.strip()]

    if not addresses:
        return jsonify({'success': False, 'error': '请输入至少一个地址'}), 400

    # Import and call analyzer
    from .cluster_analyzer import cluster_addresses_web
    result = cluster_addresses_web(addresses, {'eth_key': eth_key})

    if result['success']:
        return jsonify(result)
    else:
        return jsonify(result), 400


@cross_bp.route('/cluster')
def cluster_page():
    """Page route for address clustering tool."""
    return render_template('cross/cluster.html')


@cross_bp.route('/api/cluster/sample')
def cluster_sample():
    """Sample addresses for demo (per D-04)."""
    return jsonify({
        "sample_addresses": [
            SAMPLE_TRON_ADDRESS,
            SAMPLE_ETH_ADDRESS,
            SAMPLE_BTC_ADDRESS
        ]
    })


@cross_bp.route('/api/cluster/export/json', methods=['POST'])
def cluster_export_json():
    """Export cluster result as JSON file."""
    data = request.get_json()
    if not data or 'result' not in data:
        return jsonify({'error': '请提供查询结果数据'}), 400

    result = data['result']
    json_content = export_json(result)

    date_str = datetime.datetime.now().strftime('%Y%m%d')
    filename = f"cluster_result_{date_str}.json"

    response = Response(
        json_content,
        mimetype='application/json',
        headers={'Content-Disposition': f'attachment; filename="{filename}"'}
    )
    return response


@cross_bp.route('/api/cluster/export/csv', methods=['POST'])
def cluster_export_csv():
    """Export cluster result as CSV file."""
    data = request.get_json()
    if not data or 'result' not in data:
        return jsonify({'error': '请提供查询结果数据'}), 400

    result = data['result']
    clusters = result.get('clusters', [])
    unassociated = result.get('unassociated', [])

    output = StringIO()
    writer = csv.writer(output)

    # Header row
    writer.writerow(['聚类ID', '地址', '链类型', '关联原因'])

    # Write clusters
    for cluster in clusters:
        cluster_id = cluster.get('cluster_id', '')
        addresses = cluster.get('addresses', [])
        chain_types = cluster.get('chain_types', [])
        reasons = cluster.get('reasons', [])
        reasons_str = '; '.join(reasons) if reasons else ''

        for i, addr in enumerate(addresses):
            chain = chain_types[i] if i < len(chain_types) else 'unknown'
            writer.writerow([cluster_id, addr, chain, reasons_str])

    # Write unassociated addresses
    for addr in unassociated:
        writer.writerow(['无', addr, 'unknown', '无关联'])

    date_str = datetime.datetime.now().strftime('%Y%m%d')
    filename = f"cluster_result_{date_str}.csv"

    response = Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': f'attachment; filename="{filename}"'}
    )
    return response


# ===================== Cross-Border Routes =====================

@cross_bp.route('/api/cross-border/generate', methods=['POST'])
def cross_border_generate():
    """API endpoint for template generation.

    Request JSON body: {"case_number": "...", "agency": "...", ...}
    Response JSON: {"success": bool, "template_data": {...}, "plain_text": "..."}
    """
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': '请提供JSON数据'}), 400

    # Import and call generator
    from .cross_border_generator import generate_template_web
    result = generate_template_web(data)

    if result['success']:
        return jsonify(result)
    else:
        return jsonify(result), 400


@cross_bp.route('/cross-border')
def cross_border_page():
    """Page route for cross-border coordination tool."""
    return render_template('cross/cross_border.html')