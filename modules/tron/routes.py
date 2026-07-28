"""Flask Blueprint routes for TRON analysis tools"""

from flask import Blueprint, jsonify, request, Response, render_template
from .suspicious_analyzer import analyze_address_web, is_valid_tron_address
from .behavior_analyzer import analyze_behavior_web
from modules.core.exporter import export_json, export_csv, get_export_filename

tron_bp = Blueprint('tron', __name__, url_prefix='/tron')

@tron_bp.route('/api/analyze', methods=['POST'])
def analyze():
    """API endpoint for TRON address suspicious feature analysis.

    Request JSON body: {"address": "TRON_ADDRESS"}
    Response JSON: {
        "success": bool,
        "address": str,
        "basic_info": dict,
        "alerts": {"red": [], "yellow": [], "green": [], "score": int}
    }
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'success': False, 'error': '请提供JSON数据'}), 400

    address = data.get('address', '')
    if not address:
        return jsonify({'success': False, 'error': '请提供TRON地址'}), 400

    result = analyze_address_web(address)

    if result['success']:
        return jsonify(result)
    else:
        return jsonify(result), 400

@tron_bp.route('/api/sample')
def get_sample():
    """Return sample TRON address for user input format demonstration.

    Response JSON: {"address": str, "description": str}
    """
    return jsonify({
        'address': 'TUtPdo7L45ey2KrpibdNcjNL3ujqXo1NNw',
        'description': '示例TRON地址，点击"加载样本"按钮填充'
    })

@tron_bp.route('/api/export/json', methods=['POST'])
def export_json_endpoint():
    """Export analysis result as JSON file download.

    Request JSON body: {"result": analysis_result_dict}
    Response: JSON file download with Content-Disposition header
    """
    data = request.get_json(silent=True)
    if not data or 'result' not in data:
        return jsonify({'error': '请提供分析结果数据'}), 400

    result = data['result']
    address = result.get('address', 'unknown')

    json_content = export_json(result)
    filename = get_export_filename(address, 'json')

    response = Response(
        json_content,
        mimetype='application/json',
        headers={'Content-Disposition': f'attachment; filename="{filename}"'}
    )
    return response

@tron_bp.route('/api/export/csv', methods=['POST'])
def export_csv_endpoint():
    """Export analysis alerts as CSV file download.

    Request JSON body: {"result": analysis_result_dict}
    Response: CSV file download with Content-Disposition header
    """
    data = request.get_json(silent=True)
    if not data or 'result' not in data:
        return jsonify({'error': '请提供分析结果数据'}), 400

    result = data['result']
    address = result.get('address', 'unknown')

    csv_content = export_csv(result)

    filename = get_export_filename(address, 'csv')

    response = Response(
        csv_content,
        mimetype='text/csv',
        headers={'Content-Disposition': f'attachment; filename="{filename}"'}
    )
    return response

# ============== Behavior Analyzer Routes ==============

@tron_bp.route('/behavior-analyzer')
def behavior_analyzer_page():
    """Render TRON address behavior analysis tool page.

    Returns:
        HTML template for behavior analyzer with 4 Summary Cards
    """
    return render_template('tron/behavior_analyzer.html')

@tron_bp.route('/api/behavior', methods=['POST'])
def analyze_behavior():
    """API endpoint for TRON address behavior analysis.

    Request JSON body: {"address": "TRON_ADDRESS"}
    Response JSON: {
        "success": bool,
        "address": str,
        "behaviors": {
            "funding_source": dict,
            "transfer_patterns": dict,
            "relationships": dict,
            "timeline": dict
        }
    }
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'success': False, 'error': '请提供JSON数据'}), 400

    address = data.get('address', '')
    if not address:
        return jsonify({'success': False, 'error': '请提供TRON地址'}), 400

    result = analyze_behavior_web(address)

    if result['success']:
        return jsonify(result)
    else:
        return jsonify(result), 400

@tron_bp.route('/api/export/behavior/json', methods=['POST'])
def export_behavior_json():
    """Export behavior analysis result as JSON file download.

    Request JSON body: {"result": behavior_analysis_result_dict}
    Response: JSON file download with Content-Disposition header
    """
    data = request.get_json(silent=True)
    if not data or 'result' not in data:
        return jsonify({'error': '请提供分析结果数据'}), 400

    result = data['result']
    address = result.get('address', 'unknown')

    json_content = export_json(result)

    filename = get_export_filename(address, 'json', analysis_type='behavior')

    response = Response(
        json_content,
        mimetype='application/json',
        headers={'Content-Disposition': f'attachment; filename="{filename}"'}
    )
    return response

@tron_bp.route('/api/export/behavior/csv', methods=['POST'])
def export_behavior_csv():
    """Export behavior analysis results as CSV file download.

    Request JSON body: {"result": behavior_analysis_result_dict}
    Response: CSV file download with Content-Disposition header
    """
    data = request.get_json(silent=True)
    if not data or 'result' not in data:
        return jsonify({'error': '请提供分析结果数据'}), 400

    result = data['result']
    address = result.get('address', 'unknown')

    # Create CSV for behavior analysis
    csv_content = export_behavior_csv_content(result)

    filename = get_export_filename(address, 'csv', analysis_type='behavior')

    response = Response(
        csv_content,
        mimetype='text/csv',
        headers={'Content-Disposition': f'attachment; filename="{filename}"'}
    )
    return response


def export_behavior_csv_content(data: dict) -> str:
    """Convert behavior analysis results to CSV format.

    Args:
        data: Behavior analysis result with behaviors dict

    Returns:
        CSV string with behavior analysis data
    """
    import csv
    from io import StringIO

    output = StringIO()
    writer = csv.writer(output)

    # Header
    writer.writerow(['分析类型', '指标', '值'])

    behaviors = data.get('behaviors', {})

    # Funding source
    funding = behaviors.get('funding_source', {})
    if funding.get('status'):
        writer.writerow(['首次资金来源', '状态', funding['status']])
    else:
        writer.writerow(['首次资金来源', '资助地址', funding.get('funder_address', '')])
        writer.writerow(['首次资金来源', '首次转入时间', funding.get('first_transfer_time_str', '')])
        writer.writerow(['首次资金来源', '首次转入金额', f"{funding.get('first_amount', '')} USDT"])
        writer.writerow(['首次资金来源', '资助方交易数', funding.get('funder_tx_count', 0)])

    # Transfer patterns
    patterns = behaviors.get('transfer_patterns', {})
    if patterns.get('status'):
        writer.writerow(['交易模式', '状态', patterns['status']])
    else:
        writer.writerow(['交易模式', '转入总额', f"{patterns.get('total_in', '0')} USDT"])
        writer.writerow(['交易模式', '转出总额', f"{patterns.get('total_out', '0')} USDT"])
        writer.writerow(['交易模式', '入出比例', patterns.get('in_out_ratio', 0)])
        writer.writerow(['交易模式', '平均转账间隔', f"{patterns.get('avg_transfer_interval_hours', 0)} 小时"])
        writer.writerow(['交易模式', '转入次数', patterns.get('transfer_count_in', 0)])
        writer.writerow(['交易模式', '转出次数', patterns.get('transfer_count_out', 0)])

    # Relationships
    relationships = behaviors.get('relationships', {})
    if relationships.get('status'):
        writer.writerow(['地址关系', '状态', relationships['status']])
    else:
        writer.writerow(['地址关系', '互动地址数', relationships.get('unique_addresses_interacted', 0)])
        for i, cp in enumerate(relationships.get('top_counterparties', [])[:5], 1):
            writer.writerow(['地址关系', f'频繁交易对象{i}', cp.get('address', '')])
            writer.writerow(['地址关系', f'互动次数{i}', cp.get('interaction_count', 0)])
            writer.writerow(['地址关系', f'交易总额{i}', f"{cp.get('total_amount', 0)} USDT"])

    # Timeline
    timeline = behaviors.get('timeline', {})
    if timeline.get('status'):
        writer.writerow(['活动时间线', '状态', timeline['status']])
    else:
        writer.writerow(['活动时间线', '首次活动', timeline.get('first_activity_str', '')])
        writer.writerow(['活动时间线', '最后活动', timeline.get('last_activity_str', '')])
        writer.writerow(['活动时间线', '活跃天数', timeline.get('active_days', 0)])
        writer.writerow(['活动时间线', '高峰期', timeline.get('peak_activity_period', {}).get('period_str', '')])
        writer.writerow(['活动时间线', '高峰期交易数', timeline.get('peak_activity_period', {}).get('count', 0)])
        writer.writerow(['活动时间线', '总交易数', timeline.get('total_transfers', 0)])

    return output.getvalue()