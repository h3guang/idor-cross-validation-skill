# ============================================================
# 版本升级脚本 version-bump.ps1
# 用法: ./version-bump.ps1 [patch|minor|major]
# ============================================================

param(
    [ValidateSet('patch', 'minor', 'major')]
    [string]$Type = 'patch'
)

# 读取当前版本
$versionFile = "VERSION"
$currentVersion = Get-Content $versionFile -Raw
$currentVersion = $currentVersion.Trim()
$parts = $currentVersion.Split('.')

$major = [int]$parts[0]
$minor = [int]$parts[1]
$patch = [int]$parts[2]

# 根据类型升级
switch ($Type) {
    'major' {
        $major++
        $minor = 0
        $patch = 0
        $typeName = "主版本"
    }
    'minor' {
        $minor++
        $patch = 0
        $typeName = "次版本"
    }
    'patch' {
        $patch++
        $typeName = "补丁版本"
    }
}

$newVersion = "$major.$minor.$patch"

# 更新 VERSION 文件
$newVersion | Out-File -Encoding UTF8 $versionFile

# 更新 README.md 中的版本号
$readme = Get-Content README.md -Raw
$readme = $readme -replace '\d+\.\d+\.\d+', $newVersion
$readme | Set-Content README.md -Encoding UTF8

# 更新 CHANGELOG.md 中的版本号
$changelog = Get-Content CHANGELOG.md -Raw
$changelog = $changelog -replace '\[Unreleased\]', "[$newVersion] - $(Get-Date -Format 'yyyy-MM-dd')"
$changelog | Set-Content CHANGELOG.md -Encoding UTF8

Write-Host ""
Write-Host "========================================"
Write-Host "版本升级成功！"
Write-Host "========================================"
Write-Host ""
Write-Host "  $typeName : $currentVersion -> $newVersion"
Write-Host "  类型: $Type"
Write-Host ""
Write-Host "下一步:"
Write-Host "  1. 更新 CHANGELOG.md 添加本次更新内容"
Write-Host "  2. git add ."
Write-Host "  3. git commit -m `"chore: 升级版本到 $newVersion`""
Write-Host "  4. git tag -a v$newVersion -m `"Release v$newVersion`""
Write-Host "  5. git push && git push --tags"
Write-Host "========================================"
