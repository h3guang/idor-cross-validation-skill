#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
参数变异生成器
为越权测试生成各种ID变异值
"""

import base64
import hashlib
import random
from typing import List, Dict, Any

class ParameterFuzzer:
    """参数变异生成器"""
    
    def __init__(self):
        self.boundary_values = ['0', '1', '-1', '99999', '999999', 'null', 'undefined']
    
    def fuzz_numeric(self, original_id: str) -> List[str]:
        """
        数字ID变异
        Args:
            original_id: 原始ID
        Returns:
            变异后的ID列表
        """
        if not original_id.isdigit():
            return []
        
        base = int(original_id)
        mutations = [
            str(base + 1),
            str(base - 1),
            str(base + 10),
            str(base - 10),
            str(base + 100),
            str(base - 100),
            str(base * 2),
            str(base // 2) if base > 1 else '0',
            str(base * 3),
            str(base // 3) if base > 2 else '0',
        ]
        
        # 添加边界值
        mutations.extend(self.boundary_values[:5])
        
        # 去重并限制数量
        return list(set(mutations))[:20]
    
    def fuzz_string(self, original_id: str) -> List[str]:
        """
        字符串ID变异
        Args:
            original_id: 原始ID
        Returns:
            变异后的ID列表
        """
        mutations = [
            original_id.upper(),
            original_id.lower(),
            original_id.capitalize(),
            original_id + '1',
            original_id + 'x',
            original_id[:-1] if len(original_id) > 1 else original_id,
            original_id + original_id[-1] if original_id else original_id,
        ]
        
        # 字符替换
        if len(original_id) > 2:
            mid = len(original_id) // 2
            mutations.append(original_id[:mid] + 'x' + original_id[mid+1:])
            mutations.append(original_id[:mid] + '1' + original_id[mid+1:])
        
        # 添加边界值
        mutations.extend(self.boundary_values)
        
        return list(set(mutations))[:20]
    
    def fuzz_uuid(self, original_id: str) -> List[str]:
        """
        UUID变异
        Args:
            original_id: 原始UUID
        Returns:
            变异后的UUID列表
        """
        mutations = []
        parts = original_id.split('-')
        
        if len(parts) == 5:
            # 修改最后一段
            last_part = parts[-1]
            if last_part.isdigit():
                mutations.append('-'.join(parts[:-1] + [str(int(last_part) + 1)]))
                mutations.append('-'.join(parts[:-1] + [str(int(last_part) - 1)]))
            
            # 修改时间戳部分
            if parts[0].isdigit():
                mutations.append('-'.join([str(int(parts[0]) + 1)] + parts[1:]))
            
            # 修改版本号
            version_char = parts[2][0] if parts[2] else '0'
            new_version = chr(ord(version_char) + 1) if version_char else '1'
            mutations.append('-'.join([parts[0], parts[1], new_version + parts[2][1:]] + parts[3:]))
        
        # 添加边界值
        mutations.extend(['00000000-0000-0000-0000-000000000000', 'ffffffff-ffff-ffff-ffff-ffffffffffff'])
        
        return list(set(mutations))[:20]
    
    def fuzz_base64(self, original_id: str) -> List[str]:
        """
        Base64编码变异
        Args:
            original_id: 原始ID
        Returns:
            变异后的ID列表
        """
        try:
            decoded = base64.b64decode(original_id).decode('utf-8')
            mutations = [
                base64.b64encode((decoded + '1').encode()).decode(),
                base64.b64encode((decoded[:-1] if len(decoded) > 1 else decoded).encode()).decode(),
            ]
            return mutations
        except:
            return []
    
    def fuzz_all(self, original_id: str, id_type: str = 'auto') -> List[str]:
        """
        自动识别类型并生成变异
        Args:
            original_id: 原始ID
            id_type: 指定类型 (numeric/string/uuid/base64/auto)
        Returns:
            变异后的ID列表
        """
        if id_type == 'auto':
            if original_id.isdigit():
                id_type = 'numeric'
            elif '-' in original_id and len(original_id) == 36:
                id_type = 'uuid'
            elif re.match(r'^[A-Za-z0-9+/=]+$', original_id):
                id_type = 'base64'
            else:
                id_type = 'string'
        
        mutators = {
            'numeric': self.fuzz_numeric,
            'string': self.fuzz_string,
            'uuid': self.fuzz_uuid,
            'base64': self.fuzz_base64
        }
        
        mutator = mutators.get(id_type, self.fuzz_string)
        return mutator(original_id)

# 使用示例
if __name__ == "__main__":
    import re
    
    fuzzer = ParameterFuzzer()
    
    # 测试数字ID
    print("数字ID变异:")
    print(fuzzer.fuzz_numeric('1001'))
    
    print("\n字符串ID变异:")
    print(fuzzer.fuzz_string('order_abc'))
    
    print("\nUUID变异:")
    print(fuzzer.fuzz_uuid('550e8400-e29b-41d4-a716-446655440000'))
