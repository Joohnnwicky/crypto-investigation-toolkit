"""Export utilities for analysis results - JSON, CSV and PDF formats"""

import json
import csv
from io import StringIO
from typing import Dict, Any

def export_json(data: Dict[str, Any]) -> str:
    """Convert analysis result to JSON string for download.

    Args:
        data: Analysis result dict (basic_info, alerts, etc.)

    Returns:
        JSON string with Chinese characters preserved (ensure_ascii=False)
    """
    return json.dumps(data, ensure_ascii=False, indent=2)

def export_csv(data: Dict[str, Any]) -> str:
    """Convert analysis alerts to CSV format.

    Expected data structure:
        data['alerts'] = {
            'red': [{'feature': str, 'detail': str, 'meaning': str}],
            'yellow': [...],
            'green': [...],
            'score': int
        }

    Args:
        data: Analysis result with alerts

    Returns:
        CSV string with columns: 级别, 特征, 详情, 意义
    """
    output = StringIO()
    writer = csv.writer(output)

    # Header row
    writer.writerow(['级别', '特征', '详情', '意义'])

    alerts = data.get('alerts', {})

    # Red alerts
    for alert in alerts.get('red', []):
        if isinstance(alert, dict):
            writer.writerow([
                '红色',
                alert.get('feature', ''),
                alert.get('detail', ''),
                alert.get('meaning', '')
            ])

    # Yellow alerts
    for alert in alerts.get('yellow', []):
        if isinstance(alert, dict):
            writer.writerow([
                '黄色',
                alert.get('feature', ''),
                alert.get('detail', ''),
                alert.get('meaning', '')
            ])

    # Green alerts
    for alert in alerts.get('green', []):
        if isinstance(alert, dict):
            writer.writerow([
                '绿色',
                alert.get('feature', ''),
                alert.get('detail', ''),
                alert.get('meaning', '')
            ])

    # Add score row
    writer.writerow(['评分', '', '', f"{alerts.get('score', 0)}/100"])

    return output.getvalue()

def build_export_filename(prefix: str, identifier: str = '', format_type: str = 'json') -> str:
    """Generate a date-stamped export filename.

    Args:
        prefix: Filename prefix, e.g. 'eth_query', 'uniswap_trace', 'tron_analysis'
        identifier: Address or tx hash (optional). Shortened to first 8 + last 4 chars.
        format_type: File extension, e.g. 'json' or 'csv'

    Returns:
        Filename like "eth_query_TUtP...NNw_20240115.json" or "mixer_trace_20240115.json"
    """
    from datetime import datetime
    date_str = datetime.now().strftime('%Y%m%d')
    if identifier and len(identifier) > 12:
        ident_short = identifier[:8] + identifier[-4:]
    elif identifier:
        ident_short = identifier
    else:
        ident_short = ''
    if ident_short:
        return f"{prefix}_{ident_short}_{date_str}.{format_type}"
    return f"{prefix}_{date_str}.{format_type}"

def get_export_filename(address: str, format_type: str, analysis_type: str = 'analysis') -> str:
    """Generate filename for TRON export download.

    Thin wrapper around build_export_filename preserving the tron_<analysis_type>
    prefix used by TRON routes.

    Args:
        address: TRON address being analyzed
        format_type: "json" or "csv"
        analysis_type: Type of analysis ("analysis", "behavior", etc.)

    Returns:
        Filename like "tron_behavior_TUtP...NNw_20240115.json"
    """
    return build_export_filename(f"tron_{analysis_type}", address, format_type)

def get_pdf_filename(address: str, tool_type: str) -> str:
    """Generate filename for PDF export download.

    Args:
        address: Address being analyzed
        tool_type: Tool type identifier (e.g., 'tron_suspicious', 'eth_query')

    Returns:
        Filename like "tron_suspicious_TUtP...NNw_20240115.pdf"
    """
    return build_export_filename(tool_type, address, 'pdf')

def export_pdf(data: Dict[str, Any], tool_type: str) -> bytes:
    """Convert analysis result to PDF bytes for download.

    Uses reportlab (pure Python, no native dependencies) so the tool stays
    zero-config and works offline. Chinese is rendered via the built-in
    STSong-Light CID font (no font file required).

    Args:
        data: Analysis result dict (basic_info, alerts, etc.)
        tool_type: Tool type identifier for title

    Returns:
        PDF bytes
    """
    from io import BytesIO
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.units import mm
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    )
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.cidfonts import UnicodeCIDFont

    # Built-in Adobe CID font supports Chinese with no font file needed
    cjk_font = 'STSong-Light'
    try:
        pdfmetrics.registerFont(UnicodeCIDFont(cjk_font))
    except Exception:
        cjk_font = 'Helvetica'  # fallback if CID font unavailable

    tool_names = {
        'tron_suspicious': 'TRON可疑特征分析',
        'tron_behavior': 'TRON地址行为分析',
        'eth_query': 'ETH交易查询',
        'uniswap': 'Uniswap追踪',
        'mixer': '混币器追踪',
        'btc': 'BTC交易分析',
        'cluster': '地址聚类',
        'cross_border': '跨境协查',
        'monitor': '多链监控',
        'obfuscation': '混淆攻击对抗',
        'asset_freeze': '资产追回冻结'
    }

    title = tool_names.get(tool_type, '链上分析报告')
    address = data.get('address', 'unknown')

    # Paragraph styles
    h1 = ParagraphStyle('H1', fontName=cjk_font, fontSize=18,
                        textColor=colors.HexColor('#1a1a1a'), spaceAfter=8)
    h2 = ParagraphStyle('H2', fontName=cjk_font, fontSize=13,
                        textColor=colors.HexColor('#4a4a4a'),
                        spaceBefore=14, spaceAfter=6)
    body = ParagraphStyle('Body', fontName=cjk_font, fontSize=10,
                          leading=15, textColor=colors.HexColor('#333333'))
    meaning_style = ParagraphStyle('Meaning', parent=body,
                                   textColor=colors.HexColor('#666666'))
    score_style = ParagraphStyle('Score', fontName=cjk_font, fontSize=14,
                                 textColor=colors.HexColor('#1a1a1a'), spaceAfter=6)
    footer_style = ParagraphStyle('Footer', fontName=cjk_font, fontSize=8,
                                  textColor=colors.HexColor('#888888'))

    story = []
    story.append(Paragraph(title, h1))
    story.append(Paragraph(f'分析地址: {address}', body))
    story.append(Spacer(1, 6))

    # Basic info
    story.append(Paragraph('基本信息', h2))
    basic_info = data.get('basic_info', {})
    info_rows = []
    if basic_info:
        for key, value in basic_info.items():
            if isinstance(value, dict):
                continue  # Skip nested dicts
            info_rows.append([Paragraph(str(key), body), Paragraph(str(value), body)])
    if info_rows:
        tbl = Table(info_rows, colWidths=[40 * mm, 120 * mm])
        tbl.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f5f5f5')),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(tbl)
    else:
        story.append(Paragraph('无基本信息', body))

    # Alerts
    story.append(Paragraph('风险提示', h2))
    alerts = data.get('alerts', {})
    if alerts:
        story.append(Paragraph(f'风险评分: {alerts.get("score", 0)}/100', score_style))

        # level -> (label, background, border color)
        alert_specs = [
            ('red', '高风险', colors.HexColor('#fee2e2'), colors.HexColor('#ef4444')),
            ('yellow', '中风险', colors.HexColor('#fef3c7'), colors.HexColor('#f59e0b')),
            ('green', '正常', colors.HexColor('#dcfce7'), colors.HexColor('#22c55e')),
        ]
        for level, label, bg, border in alert_specs:
            feature_style = ParagraphStyle('Feat', parent=body, fontSize=10.5,
                                           textColor=border)
            for alert in alerts.get(level, []):
                if not isinstance(alert, dict):
                    continue
                rows = [
                    [Paragraph(f'[{label}] {alert.get("feature", "")}', feature_style)],
                    [Paragraph(alert.get('detail', ''), body)],
                    [Paragraph(alert.get('meaning', ''), meaning_style)],
                ]
                tbl = Table(rows, colWidths=[160 * mm])
                tbl.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, -1), bg),
                    ('LINEBEFORE', (0, 0), (0, -1), 3, border),
                    ('LEFTPADDING', (0, 0), (-1, -1), 8),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                    ('TOPPADDING', (0, 0), (-1, -1), 4),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                ]))
                story.append(tbl)
                story.append(Spacer(1, 4))
    else:
        story.append(Paragraph('无风险提示', body))

    # Footer
    story.append(Spacer(1, 20))
    story.append(Paragraph('本报告仅供参考，不作为法律证据使用。', footer_style))
    story.append(Paragraph('区块猎影 BLOCKSHADE - 本地运行版', footer_style))

    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        topMargin=20 * mm, bottomMargin=20 * mm,
        leftMargin=20 * mm, rightMargin=20 * mm
    )
    doc.build(story)
    return buffer.getvalue()
