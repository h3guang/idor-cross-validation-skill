# ============================================================
# 一键发布脚本 release.ps1
# 用法: ./release.ps1 [patch|minor|major] "更新描述"
# ============================================================

param(
    [ValidateSet('patch', 'minor', 'major')]
    [string]$Type = 'patch',
    [string]$Message = "更新"
)

# 执行版本升级
.\version-bump.ps1 $Type

# 读取新版本
$newVersion = Get-Content VERSION -Raw
$newVersion = $newVersion.Trim()

# 添加所有变更
git add .

# 提交
git commit -m "release: $Message (v$newVersion)"

# 创建标签
git tag -a "v$newVersion" -m "Release v$newVersion"

# 推送到远程
git push
git push --tags

Write-Host ""
Write-Host "========================================"
Write-Host "发布完成！"
Write-Host "========================================"
Write-Host ""
Write-Host "  版本: v$newVersion"
Write-Host "  描述: $Message"
Write-Host ""
Write-Host "  查看发布:"
Write-Host "  https://github.com/h3guang/idor-cross-validation-skill/releases"
Write-Host "========================================"
