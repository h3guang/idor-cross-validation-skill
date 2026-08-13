# IDOR Cross-Validation Skill

GLM + DeepSeek 双AI交叉验证越权渗透测试系统

作者: h3guang | 版本: 1.0.1


## 简介

利用 GLM（智谱）和 DeepSeek 两个AI平台的互补优势，实现高准确率的越权漏洞自动化检测。

| 对比项 | 单AI平台 | 双AI交叉验证 |
|--------|---------|-------------|
| 误报率 | 10-15% | < 3% |
| 漏报率 | 20-30% | < 10% |


## 快速开始

### 1. 克隆项目

git clone https://github.com/h3guang/idor-cross-validation-skill.git
cd idor-cross-validation-skill

### 2. 在 GLM 平台执行扫描

打开 chatglm.cn，输入：

启动越权渗透测试（业务语义优先）
目标: https://your-target.com
管理员: admin/Admin123
普通用户1: user1/Pass123
普通用户2: user2/Pass456
请输出JSON格式结果。

### 3. 在 DeepSeek 平台执行扫描

打开 chat.deepseek.com，输入：

启动越权渗透测试（技术实现优先）
目标: https://your-target.com
管理员: admin/Admin123
普通用户1: user1/Pass123
普通用户2: user2/Pass456
请输出JSON格式结果。

### 4. 交叉验证

将两份结果粘贴到任一平台，执行：

请交叉验证以下两份结果：
【GLM结果】粘贴GLM输出
【DeepSeek结果】粘贴DeepSeek输出
输出最终报告。


## 项目结构

idor-cross-validation-skill/
├── prompts/          # AI提示词（核心）
├── rules/            # 检测规则
├── schemas/          # 数据格式
├── scripts/          # 辅助脚本
├── templates/        # 报告模板
└── examples/         # 示例数据



## 漏洞覆盖

- 水平越权 / 垂直越权
- 业务逻辑（金额篡改/并发超卖/优惠券滥用）
- 流程绕过（支付跳过/注册绕过/回调伪造）
- 认证缺陷（暴力破解/用户名枚举/密码重置）
- 信息泄露（敏感数据/目录列表）


## 环境要求

- 可访问 GLM 和 DeepSeek 平台
- 至少2个测试账号（管理员+普通用户）


## 版本

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| 1.0.1 | 2026-08-14 | 首次发布 |


## 免责声明

本工具仅供授权测试使用，未经授权禁止使用。
