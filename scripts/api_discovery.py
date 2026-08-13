#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API自动发现脚本
从目标网站自动提取所有API端点
"""

import re
import json
import requests
from urllib.parse import urljoin, urlparse
from typing import Set, List, Dict

class APIDiscovery:
    def __init__(self, base_url: str, session: requests.Session = None):
        self.base_url = base_url.rstrip('/')
        self.session = session or requests.Session()
        self.apis: Set[str] = set()
        self.visited: Set[str] = set()
        
    def discover(self, max_depth: int = 2) -> List[str]:
        """
        发现API端点
        Args:
            max_depth: 递归爬取深度
        Returns:
            API端点列表
        """
        self._crawl(self.base_url, depth=0, max_depth=max_depth)
        return list(self.apis)
    
    def _crawl(self, url: str, depth: int, max_depth: int):
        """递归爬取页面"""
        if depth > max_depth or url in self.visited:
            return
        
        self.visited.add(url)
        
        try:
            response = self.session.get(url, timeout=10)
            html = response.text
            
            # 提取API调用
            self._extract_apis_from_html(html)
            
            # 提取链接继续爬取
            links = self._extract_links(html)
            for link in links:
                full_url = urljoin(url, link)
                if self._is_same_domain(full_url):
                    self._crawl(full_url, depth + 1, max_depth)
                    
        except Exception as e:
            print(f"爬取失败: {url} - {e}")
    
    def _extract_apis_from_html(self, html: str):
        """从HTML提取API调用"""
        patterns = [
            r'["\'](/api/[^"\']+)["\']',
            r'["\'](/rest/[^"\']+)["\']',
            r'["\'](/v\d+/[^"\']+)["\']',
            r'url\s*:\s*["\']([^"\']+)["\']',
            r'fetch\s*\(\s*["\']([^"\']+)["\']',
            r'axios\.(get|post|put|delete|patch)\s*\(\s*["\']([^"\']+)["\']',
            r'\$\s*\.\s*(get|post|put|delete)\s*\(\s*["\']([^"\']+)["\']',
            r'\.get\s*\(\s*["\']([^"\']+)["\']'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    api_path = match[-1]
                else:
                    api_path = match
                
                if api_path.startswith('/'):
                    full_api = urljoin(self.base_url, api_path)
                    self.apis.add(full_api)
    
    def _extract_links(self, html: str) -> List[str]:
        """提取页面中的链接"""
        pattern = r'href\s*=\s*["\']([^"\']+)["\']'
        matches = re.findall(pattern, html, re.IGNORECASE)
        return [m for m in matches if not m.startswith('#') and not m.startswith('javascript:')]
    
    def _is_same_domain(self, url: str) -> bool:
        """检查是否同域名"""
        try:
            parsed_base = urlparse(self.base_url)
            parsed_url = urlparse(url)
            return parsed_base.netloc == parsed_url.netloc
        except:
            return False
    
    def export_to_file(self, filename: str = "discovered_apis.json"):
        """导出到文件"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(list(self.apis), f, indent=2, ensure_ascii=False)
        print(f"已导出 {len(self.apis)} 个API到 {filename}")

# 使用示例
if __name__ == "__main__":
    # 从Swagger文档发现API
    import requests
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    
    # 发现API
    discoverer = APIDiscovery('https://api.example.com', session)
    apis = discoverer.discover(max_depth=2)
    
    print(f"发现 {len(apis)} 个API端点")
    for api in apis[:10]:
        print(f"  - {api}")
