#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
置信度计算器
用于GLM和DeepSeek交叉验证的置信度计算
"""

from typing import Dict, Any, Optional

class ConfidenceCalculator:
    """综合置信度计算器"""
    
    def __init__(self):
        self.weights = {
            'glm_weight': 0.4,
            'deepseek_weight': 0.4,
            'consensus_bonus': 0.15,
            'poc_bonus': 0.10,
            'evidence_bonus': 0.10,
            'sensitive_data_bonus': 0.05
        }
    
    def calculate_combined_confidence(
        self,
        glm_conf: float,
        ds_conf: float,
        found_by_both: bool = False,
        has_poc: bool = False,
        has_evidence: bool = False,
        has_sensitive_data: bool = False
    ) -> float:
        """
        计算综合置信度
        
        Args:
            glm_conf: GLM置信度 (0-1)
            ds_conf: DeepSeek置信度 (0-1)
            found_by_both: 是否双方都发现
            has_poc: 是否有可执行POC
            has_evidence: 是否有详细证据
            has_sensitive_data: 是否涉及敏感数据
        
        Returns:
            综合置信度 (0-1)
        """
        # 基础平均
        base = (glm_conf * self.weights['glm_weight'] + 
                ds_conf * self.weights['deepseek_weight'])
        
        # 双方发现加分
        if found_by_both:
            base += self.weights['consensus_bonus']
        
        # POC加分
        if has_poc:
            base += self.weights['poc_bonus']
        
        # 证据加分
        if has_evidence:
            base += self.weights['evidence_bonus']
        
        # 敏感数据加分
        if has_sensitive_data:
            base += self.weights['sensitive_data_bonus']
        
        return round(min(base, 1.0), 2)
    
    def get_confidence_level(self, confidence: float) -> str:
        """
        获取置信度等级
        
        Args:
            confidence: 综合置信度
        
        Returns:
            置信度等级 (High/Medium/Low)
        """
        if confidence >= 0.85:
            return "High"
        elif confidence >= 0.60:
            return "Medium"
        else:
            return "Low"
    
    def get_confidence_color(self, confidence: float) -> str:
        """
        获取置信度对应的颜色
        
        Args:
            confidence: 综合置信度
        
        Returns:
            颜色代码
        """
        if confidence >= 0.85:
            return "🟢"
        elif confidence >= 0.60:
            return "🟡"
        else:
            return "🔴"
    
    def calculate_false_positive_probability(self, glm_conf: float, ds_conf: float) -> float:
        """
        计算误报概率
        
        Args:
            glm_conf: GLM置信度
            ds_conf: DeepSeek置信度
        
        Returns:
            误报概率 (0-1)
        """
        # 双方置信度都高 → 误报概率低
        if glm_conf >= 0.8 and ds_conf >= 0.8:
            return 0.05
        
        # 一方置信度低 → 误报概率高
        if glm_conf < 0.5 or ds_conf < 0.5:
            return 0.30
        
        # 中间情况
        return 0.15
    
    def get_verdict(
        self,
        glm_conf: float,
        ds_conf: float,
        found_by_both: bool
    ) -> Dict[str, Any]:
        """
        获取最终判定
        
        Args:
            glm_conf: GLM置信度
            ds_conf: DeepSeek置信度
            found_by_both: 是否双方都发现
        
        Returns:
            判定结果字典
        """
        combined = self.calculate_combined_confidence(glm_conf, ds_conf, found_by_both)
        level = self.get_confidence_level(combined)
        
        if found_by_both and combined >= 0.85:
            status = "CONFIRMED"
            priority = "HIGH"
        elif found_by_both and combined >= 0.60:
            status = "VERIFIED"
            priority = "MEDIUM"
        elif not found_by_both and combined >= 0.60:
            status = "SUSPECTED"
            priority = "MEDIUM"
        else:
            status = "NEEDS_REVIEW"
            priority = "LOW"
        
        return {
            'status': status,
            'combined_confidence': combined,
            'confidence_level': level,
            'priority': priority,
            'confidence_color': self.get_confidence_color(combined),
            'false_positive_probability': self.calculate_false_positive_probability(glm_conf, ds_conf)
        }

# 使用示例
if __name__ == "__main__":
    calc = ConfidenceCalculator()
    
    # 示例1: 双方一致
    result = calc.get_verdict(glm_conf=0.85, ds_conf=0.90, found_by_both=True)
    print("双方一致:")
    print(result)
    
    # 示例2: 单方发现
    result = calc.get_verdict(glm_conf=0.85, ds_conf=0.0, found_by_both=False)
    print("\n单方发现:")
    print(result)
