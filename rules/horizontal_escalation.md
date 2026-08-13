# 水平越权检测规则（完整版）

## 规则描述
检测同级别用户之间是否存在资源访问越权。

## 检测方法
1. 识别资源ID参数（URL路径/Query/Body）
2. 使用普通用户A访问普通用户B的资源
3. 判断是否返回了B的私有数据

## 判断标准
越权条件:
- 响应状态码 = 200
- 返回数据包含敏感字段（手机/邮箱/地址）
- 数据归属 != 当前用户
- 非公开资源

## 测试用例示例
GET /api/users/1002/profile
Cookie: session_user1

预期: 403 或 404
实际: 200 (返回user2数据) → 漏洞确认

## 修复建议
- 添加资源所有者校验: resource.userId == currentUser.id
- 使用UUID替代自增ID
- 添加 @PostAuthorize('returnObject.userId == authentication.principal.id')
- 批量操作逐项校验所有权

## 常见误报排除
- 公开数据（如公共文章、产品信息）
- 静态资源（图片、CSS、JS）
- 缓存响应（需清除缓存后测试）
