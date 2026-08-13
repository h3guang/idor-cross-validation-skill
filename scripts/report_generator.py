#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
报告生成器
生成Markdown、HTML、JSON格式的渗透测试报告
"""

import json
from datetime import datetime
from typing import Dict, List, Any, Optional

class ReportGenerator:
    """报告生成器"""
    
    def __init__(self):
        self.now = datetime.now()
    
    def generate_markdown(self, results: Dict[str, Any]) -> str:
        """
        生成Markdown格式报告
        Args:
            results: 包含漏洞信息的字典
        Returns:
            Markdown报告字符串
        """
        vulns = results.get('vulnerabilities', [])
        summary = results.get('summary', {})
        
        report = f"""# 🔐 越权渗透测试报告

## 📊 扫描概况
| 项目 | 数值 |
|------|------|
| 目标 | {results.get('target', 'N/A')} |
| 时间 | {self.now.strftime('%Y-%m-%d %H:%M:%S')} |
| 扫描接口数 | {results.get('scanned_apis', 0)} |
| 发现漏洞 | {len(vulns)} |

### 严重程度分布
| 级别 | 数量 |
|------|------|
| Critical | {summary.get('critical', 0)} |
| High | {summary.get('high', 0)} |
| Medium | {summary.get('medium', 0)} |
| Low | {summary.get('low', 0)} |

## 🚨 漏洞详情

"""
        
        if not vulns:
            report += "✅ 未发现越权漏洞，系统安全！\n"
        else:
            for idx, vuln in enumerate(vulns, 1):
                severity = vuln.get('severity', 'Unknown')
                emoji = {'Critical': '🔴', 'High': '🟠', 'Medium': '🟡', 'Low': '🟢'}.get(severity, '⚪')
                
                report += f"""
### {emoji} 漏洞 #{idx}: {vuln.get('type', 'Unknown')}

- **端点**: {vuln.get('endpoint', 'N/A')}
- **方法**: {vuln.get('method', 'GET')}
- **严重性**: **{severity}**
- **置信度**: {vuln.get('confidence', 0) * 100}%

**分析**:
{vuln.get('analysis', vuln.get('business_analysis', vuln.get('technical_analysis', 'N/A')))}

**修复建议**:
{vuln.get('fix_suggestion', '建议添加权限校验')}

---
"""
        
        return report
    
    def generate_json(self, results: Dict[str, Any]) -> str:
        """
        生成JSON格式报告
        Args:
            results: 包含漏洞信息的字典
        Returns:
            JSON字符串
        """
        report = {
            'report_time': self.now.isoformat(),
            'target': results.get('target', 'N/A'),
            'scanned_apis': results.get('scanned_apis', 0),
            'total_vulnerabilities': len(results.get('vulnerabilities', [])),
            'summary': results.get('summary', {}),
            'vulnerabilities': results.get('vulnerabilities', [])
        }
        return json.dumps(report, indent=2, ensure_ascii=False)
    
    def generate_html(self, results: Dict[str, Any]) -> str:
        """
        生成HTML格式报告
        Args:
            results: 包含漏洞信息的字典
        Returns:
            HTML字符串
        """
        vulns = results.get('vulnerabilities', [])
        
        vuln_rows = ''
        for vuln in vulns:
            severity = vuln.get('severity', 'Unknown')
            color = {'Critical': 'red', 'High': 'orange', 'Medium': 'gold', 'Low': 'green'}.get(severity, 'gray')
            vuln_rows += f"""
            <tr>
                <td>{vuln.get('id', 'N/A')}</td>
                <td>{vuln.get('type', 'N/A')}</td>
                <td><code>{vuln.get('endpoint', 'N/A')}</code></td>
                <td style="color:{color};font-weight:bold">{severity}</td>
                <td>{vuln.get('confidence', 0) * 100}%</td>
            </tr>"""
        
        return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>越权渗透测试报告</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #333; border-bottom: 3px solid #007bff; padding-bottom: 10px; }}
        h2 {{ color: #555; margin-top: 30px; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
        th {{ background-color: #007bff; color: white; }}
        tr:nth-child(even) {{ background-color: #f9f9f9; }}
        .stats {{ display: flex; gap: 20px; flex-wrap: wrap; }}
        .stat-card {{ background: #f0f0f0; padding: 15px 25px; border-radius: 8px; flex: 1; min-width: 100px; text-align: center; }}
        .stat-card .number {{ font-size: 28px; font-weight: bold; color: #007bff; }}
        .stat-card .label {{ color: #666; }}
        .critical {{ color: #dc3545; }}
        .high {{ color: #fd7e14; }}
        .medium {{ color: #ffc107; }}
        .low {{ color: #28a745; }}
        code {{ background: #f4f4f4; padding: 2px 6px; border-radius: 3px; }}
    </style>
</head>
<body>
<div class="container">
    <h1>🔐 越权渗透测试报告</h1>
    
    <h2>📊 扫描概况</h2>
    <div class="stats">
        <div class="stat-card"><div class="number">{results.get('scanned_apis', 0)}</div><div class="label">扫描接口</div></div>
        <div class="stat-card"><div class="number">{len(vulns)}</div><div class="label">发现漏洞</div></div>
        <div class="stat-card"><div class="number">{results.get('summary', {}).get('critical', 0)}</div><div class="label">严重漏洞</div></div>
        <div class="stat-card"><div class="number">{results.get('summary', {}).get('high', 0)}</div><div class="label">高危漏洞</div></div>
    </div>
    
    <h2>📋 漏洞列表</h2>
    <table>
        <tr><th>ID</th><th>类型</th><th>端点</th><th>严重性</th><th>置信度</th></tr>
        {vuln_rows if vuln_rows else '<tr><td colspan="5" style="text-align:center;">✅ 未发现越权漏洞</td></tr>'}
    </table>
    
    <p style="margin-top:30px;color:#999;font-size:12px;">
        报告生成时间: {self.now.strftime('%Y-%m-%d %H:%M:%S')}
    </p>
</div>
</body>
</html>"""
    
    def save_report(self, results: Dict[str, Any], format: str = 'markdown', filename: str = None):
        """
        保存报告到文件
        Args:
            results: 漏洞结果
            format: 报告格式 (markdown/html/json)
            filename: 文件名（可选）
        """
        generators = {
            'markdown': self.generate_markdown,
            'html': self.generate_html,
            'json': self.generate_json
        }
        
        generator = generators.get(format)
        if not generator:
            raise ValueError(f"不支持的格式: {format}")
        
        content = generator(results)
        ext = {'markdown': 'md', 'html': 'html', 'json': 'json'}.get(format, 'txt')
        filename = filename or f"report_{self.now.strftime('%Y%m%d_%H%M%S')}.{ext}"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"报告已保存: {filename}")
        return filename

# 使用示例
if __name__ == "__main__":
    # 模拟结果
    sample_results = {
        'target': 'https://api.example.com',
        'scanned_apis': 45,
        'summary': {'critical': 2, 'high': 3, 'medium': 1, 'low': 0},
        'vulnerabilities': [
            {
                'id': 'VULN-001',
                'type': 'horizontal_escalation',
                'endpoint': 'GET /api/users/{userId}',
                'method': 'GET',
                'severity': 'Critical',
                'confidence': 0.95,
                'analysis': '用户可以访问其他用户的资料',
                'fix_suggestion': '添加所有权校验'
            }
        ]
    }
    
    generator = ReportGenerator()
    generator.save_report(sample_results, 'markdown')
    generator.save_report(sample_results, 'html')
    generator.save_report(sample_results, 'json')
