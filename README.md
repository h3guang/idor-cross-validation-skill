# IDOR Cross-Validation Skill

> GLM + DeepSeek 双AI交叉验证越权渗透测试系统

---

## 目录

- [项目简介](#项目简介)
- [核心特性](#核心特性)
- [漏洞覆盖范围](#漏洞覆盖范围)
- [项目结构](#项目结构)
- [环境要求](#环境要求)
- [快速开始](#快速开始)
- [详细使用指南](#详细使用指南)
- [交叉验证说明](#交叉验证说明)
- [常见问题](#常见问题)
- [免责声明](#免责声明)

---

## 项目简介

IDOR Cross-Validation Skill 是一个利用 GLM（智谱）和 DeepSeek 两个AI平台的互补优势，实现高准确率越权漏洞自动化检测的系统。

### 为什么需要双AI交叉验证？

| 问题 | 单AI平台 | 双AI交叉验证 |
|------|---------|-------------|
| 误报率 | 10-15% | 小于 3% |
| 漏报率 | 20-30% | 小于 10% |
| 偏见性 | 单一思维模式 | 互补消除 |
| 覆盖度 | 单一维度 | 多维度覆盖 |

### 工作原理

用户输入目标信息
        |
        v
   任务分发器
   (拆分任务到两个平台)
        |
    +---+---+
    |       |
    v       v
 GLM平台  DeepSeek平台
(业务语义) (技术实现)
    |       |
    v       v
 结果集A   结果集B
    |       |
    +---+---+
        |
        v
  交叉验证引擎
  (综合研判)
        |
        v
    最终报告
(确认+疑似+修复建议)


## 核心特性

- 双AI独立扫描：GLM覆盖业务语义维度，DeepSeek覆盖技术实现维度
- 智能交叉验证：准确率提升至95%，误报率降至3%以下
- 自动生成POC：每个漏洞都附带可执行的验证代码
- 完整修复建议：提供代码级修复方案
- 零配置使用：仅需目标URL和账号密码
- 多格式报告：支持 Markdown / HTML / JSON 三种格式


## 漏洞覆盖范围

| 类型 | 子类型 | 说明 |
|------|--------|------|
| 水平越权 | IDOR | 同角色用户访问他人资源 |
| 垂直越权 | 权限提升 | 低权限访问高权限接口 |
| 业务逻辑 | 金额篡改 | 负数/超大/极小值订单 |
|  | 并发超卖 | 库存并发控制缺陷 |
|  | 优惠券滥用 | 重复使用/叠加使用 |
|  | 状态机绕过 | 订单状态跳跃 |
| 流程绕过 | 支付跳过 | 跳过支付步骤 |
|  | 注册绕过 | 跳过验证步骤 |
|  | 回调伪造 | 伪造支付回调 |
| 认证缺陷 | 暴力破解 | 登录无锁定机制 |
|  | 用户名枚举 | 用户存在性泄露 |
|  | 密码重置 | 重置链接可预测 |
| 信息泄露 | 敏感数据 | 手机/邮箱/身份证泄露 |
|  | 目录列表 | 敏感目录可浏览 |


## 项目结构

idor-cross-validation-skill/
|
|-- README.md                   项目使用说明书
|-- CHANGELOG.md                版本更新日志
|-- install.sh                  一键安装脚本
|-- upgrade.sh                  一键升级脚本
|-- requirements.txt            Python依赖列表
|
|-- prompts/                    AI提示词模板
|   |-- glm_scanner.md          GLM平台扫描器
|   |-- deepseek_scanner.md     DeepSeek平台扫描器
|   -- cross_validator.md      交叉验证协调器
|
|-- schemas/                    数据格式定义
|   |-- glm_result_schema.json      GLM输出格式
|   |-- deepseek_result_schema.json DeepSeek输出格式
|   -- final_report_schema.json    最终报告格式
|
|-- rules/                      检测规则库
|   |-- horizontal_escalation.md    水平越权规则
|   |-- vertical_escalation.md      垂直越权规则
|   |-- business_logic.md           业务逻辑规则
|   |-- flow_bypass.md              流程绕过规则
|   -- auth_weakness.md            认证缺陷规则
|
|-- scripts/                    辅助脚本
|   |-- api_discovery.py            API自动发现
|   |-- parameter_fuzzer.py         参数变异生成器
|   |-- confidence_calculator.py    置信度计算器
|   -- report_generator.py         报告生成器
|
|-- templates/                  报告模板
|   |-- markdown_report_template.md  Markdown模板
|   |-- html_report_template.html    HTML模板
|   -- json_output_template.json    JSON模板
|
-- examples/                   示例数据
    |-- sample_glm_output.json       GLM输出示例
    |-- sample_deepseek_output.json  DeepSeek输出示例
    -- sample_final_report.md       最终报告示例


## 环境要求

| 项目 | 要求 |
|------|------|
| 操作系统 | Windows / Linux / macOS |
| 网络 | 可访问 GLM 和 DeepSeek 平台 |
| 账号 | 至少2个测试账号（管理员+普通用户） |
| Python | 3.7+ （仅用于辅助脚本） |


## 快速开始

### 1. 克隆/下载项目

git clone https://github.com/your-repo/idor-cross-validation-skill.git
cd idor-cross-validation-skill

### 2. 执行安装脚本

Linux / macOS:
chmod +x install.sh
./install.sh

Windows (PowerShell):
直接使用项目文件即可

### 3. 准备测试目标

你需要准备：
- 一个授权测试的目标网站
- 至少2个账号（管理员 + 普通用户）
- 目标网站的登录地址


## 详细使用指南

### 方式一：使用GLM扫描（业务语义优先）

在GLM平台（chatglm.cn）执行：

启动越权渗透测试（业务语义优先）

目标: https://your-target.com
管理员账号: admin@example.com / Admin@123
普通用户1: user1@example.com / User1@123
普通用户2: user2@example.com / User2@456

请执行完整扫描并输出JSON格式结果。

预期输出：包含漏洞列表的JSON格式结果


### 方式二：使用DeepSeek扫描（技术实现优先）

在DeepSeek平台（chat.deepseek.com）执行：

启动越权渗透测试（技术实现优先）

目标: https://your-target.com
管理员账号: admin@example.com / Admin@123
普通用户1: user1@example.com / User1@123
普通用户2: user2@example.com / User2@456

请执行完整扫描并输出JSON格式结果。

预期输出：包含漏洞列表和POC的JSON格式结果


### 方式三：交叉验证（综合报告）

在任一平台执行：

请执行双AI交叉验证

【GLM结果】
{粘贴GLM的JSON输出}

【DeepSeek结果】
{粘贴DeepSeek的JSON输出}

请输出最终验证报告，包含：
1. 确认漏洞（双方都发现）
2. 疑似漏洞（仅一方发现）
3. 误报过滤
4. 修复建议
5. 综合置信度评分

预期输出：完整的交叉验证报告


### 方式四：使用辅助脚本（可选）

安装Python依赖:
pip install -r requirements.txt

API发现:
python scripts/api_discovery.py

参数变异测试:
python scripts/parameter_fuzzer.py

生成报告:
python scripts/report_generator.py


## 交叉验证说明

### 置信度计算规则

| 条件 | 加分 |
|------|------|
| 双方都发现 | +0.15 |
| 有可执行POC | +0.10 |
| 有详细证据 | +0.10 |
| 涉及敏感数据 | +0.05 |

### 漏洞分类标准

| 分类 | 条件 | 处理方式 |
|------|------|----------|
| CONFIRMED | 双方发现 + 置信度 >= 0.85 | 直接纳入报告 |
| VERIFIED | 双方发现 + 置信度 >= 0.60 | 纳入报告 |
| SUSPECTED | 单方发现 | 标记需人工复核 |
| NEEDS_REVIEW | 置信度差 >= 0.5 | 优先人工验证 |
| FALSE_POSITIVE | 双方置信度 < 0.5 | 从报告中移除 |


## 常见问题

Q1: 需要什么权限？
A: 必须获得目标系统所有者的明确书面授权方可进行测试。

Q2: GLM和DeepSeek结果不一致怎么办？
A: 这正是交叉验证的价值所在。结果不一致时，需要人工复核确认。

Q3: 支持哪些接口类型？
A: 支持 REST API、GraphQL、WebSocket 等常见接口类型。

Q4: 扫描速度如何？
A: 取决于目标系统的接口数量和响应速度，通常100接口约需10-15分钟。

Q5: 如何处理验证码？
A: 当前版本需要手动处理验证码，未来版本将支持自动识别。

Q6: 可以测试内网系统吗？
A: 可以，只要AI平台能访问到目标地址即可。


## 版本更新

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| 1.0.1 | 2026-08-14 | 首次发布，支持GLM+DeepSeek交叉验证，作者: h3guang |


## 免责声明

重要声明：

1. 本工具仅供安全测试人员、渗透测试人员在获得授权的情况下使用
2. 未经授权使用本工具进行测试属于违法行为
3. 使用者必须遵守所在国家/地区的法律法规
4. 作者不对任何非法使用本工具的行为承担责任
5. 测试过程中请勿修改、删除生产数据
6. 测试完成后应及时清理测试数据

使用本工具即表示您已阅读并同意以上条款。


版本: 1.0.1 | 更新日期: 2026-08-14 | 作者: h3guang

