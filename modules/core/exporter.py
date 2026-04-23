"""Export utilities for analysis results - JSON and CSV formats"""

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
    """Convert analysis alerts to CSV format for download.

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

def get_export_filename(address: str, format_type: str) -> str:
    """Generate filename for export download.

    Args:
        address: TRON address being analyzed
        format_type: "json" or "csv"

    Returns:
        Filename like "tron_analysis_TUtP...NNw_20240115.json"
    """
    from datetime import datetime
    date_str = datetime.now().strftime('%Y%m%d')
    addr_short = address[:8] + address[-4:] if len(address) > 12 else address
    return f"tron_analysis_{addr_short}_{date_str}.{format_type}"