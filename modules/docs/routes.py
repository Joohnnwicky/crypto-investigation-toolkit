"""Flask Blueprint routes for Documentation and PDF export"""

from flask import Blueprint, jsonify, request, Response, render_template
from modules.core.exporter import export_pdf, get_pdf_filename

docs_bp = Blueprint('docs', __name__, url_prefix='/docs')

@docs_bp.route('/api/export/pdf', methods=['POST'])
def export_pdf_endpoint():
    """Export analysis result as PDF file download.

    Request JSON body: {"result": analysis_result_dict, "tool_type": str}
    Response: PDF file download with Content-Disposition header
    """
    data = request.get_json()
    if not data or 'result' not in data or 'tool_type' not in data:
        return jsonify({'error': '请提供分析结果和工具类型'}), 400

    result = data['result']
    tool_type = data['tool_type']
    address = result.get('address', 'unknown')

    try:
        pdf_bytes = export_pdf(result, tool_type)
        filename = get_pdf_filename(address, tool_type)

        response = Response(
            pdf_bytes,
            mimetype='application/pdf',
            headers={'Content-Disposition': f'attachment; filename="{filename}"'}
        )
        return response
    except Exception as e:
        return jsonify({'error': f'PDF生成失败: {str(e)}'}), 500


# Page routes for documentation
@docs_bp.route('/manuals')
def manuals_page():
    """Documentation manuals index page."""
    return render_template('docs/manuals.html')


@docs_bp.route('/api-guide')
def api_guide_page():
    """API key registration guide page."""
    return render_template('docs/api_guide.html')


@docs_bp.route('/manual/<tool>')
def manual_page(tool):
    """Individual tool manual page.

    Args:
        tool: Tool slug (tron-suspicious, tron-behavior, eth-query, etc.)
    """
    valid_slugs = [
        'tron-suspicious', 'tron-behavior', 'eth-query', 'uniswap',
        'mixer', 'btc', 'cluster', 'cross-border', 'monitor',
        'obfuscation', 'asset-freeze'
    ]
    if tool not in valid_slugs:
        return "Page not found", 404
    # Convert slug hyphens to underscores for template filename
    template_name = tool.replace('-', '_')
    return render_template(f'docs/manual_{template_name}.html')