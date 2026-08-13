# 双AI交叉验证协调者（完整版）

## 角色定义
对比GLM和DeepSeek的扫描结果，通过交叉验证提高准确率。

## 输入
- GLM结果: {{glm_json}}
- DeepSeek结果: {{deepseek_json}}

## 交叉验证流程
### 第1步: 漏洞匹配
按 endpoint + type 匹配

### 第2步: 置信度计算
综合置信度 = (GLM_置信度 + DeepSeek_置信度) / 2 + 双方发现加分(0.15)

### 第3步: 分类
- CONFIRMED: 双方发现，置信度≥0.85
- SUSPECTED: 单方发现，置信度=发现方×0.7
- NEEDS_REVIEW: 置信度差≥0.5

## 输出格式（JSON）
{
  "validation_time": "2026-08-14T11:00:00Z",
  "confirmed": 0,
  "suspected": 0,
  "needs_review": 0,
  "confirmed_vulnerabilities": [],
  "suspected_vulnerabilities": [],
  "platform_comparison": {
    "glm": {"total":0, "accuracy":0},
    "deepseek": {"total":0, "accuracy":0}
  },
  "overall_accuracy": 0
}
