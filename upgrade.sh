#!/bin/bash
# ============================================================
# IDOR Cross-Validation Skill - 一键升级脚本
# 版本: V1.0
# 说明: 自动升级项目到最新版本
# ============================================================

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
print_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }

print_header() {
    echo ""
    echo "========================================"
    echo -e "${GREEN}$1${NC}"
    echo "========================================"
    echo ""
}

# 检查是否在项目目录
check_project_dir() {
    if [ ! -f "README.md" ] || [ ! -d "prompts" ]; then
        print_error "请在项目根目录下运行此脚本"
        exit 1
    fi
}

# 检查当前版本
check_current_version() {
    if [ -f ".version" ]; then
        CURRENT_VERSION=$(cat .version)
        print_info "当前版本: ${CURRENT_VERSION}"
    else
        CURRENT_VERSION="unknown"
        print_warning "未检测到版本信息"
    fi
}

# 拉取最新版本
pull_latest() {
    print_info "拉取最新版本..."
    
    # 备份当前配置
    if [ -f "config.json" ]; then
        print_info "备份配置文件..."
        cp config.json config.json.bak
    fi
    
    # 如果存在git，使用git更新
    if [ -d ".git" ] && command -v git &> /dev/null; then
        git fetch origin
        git pull origin main
        print_success "Git拉取完成"
    else
        print_warning "未检测到Git仓库，跳过"
    fi
}

# 更新依赖
update_dependencies() {
    print_info "更新依赖..."
    
    if [ -f "requirements.txt" ]; then
        pip3 install --upgrade -r requirements.txt --quiet
        print_success "依赖更新完成"
    fi
}

# 更新配置文件
update_config() {
    print_info "更新配置文件..."
    
    # 检查是否有新的配置模板
    if [ -f "config.example.json" ]; then
        # 检测配置变化
        if [ -f "config.json" ]; then
            print_info "检测到现有配置文件，保留用户配置"
        else
            cp config.example.json config.json
            print_warning "配置文件不存在，已创建默认配置"
        fi
    fi
}

# 检查版本更新
show_update_info() {
    if [ -f ".version" ]; then
        NEW_VERSION=$(cat .version 2>/dev/null || echo "unknown")
        if [ "$CURRENT_VERSION" != "$NEW_VERSION" ]; then
            print_success "升级完成！"
            echo "  旧版本: ${CURRENT_VERSION}"
            echo "  新版本: ${NEW_VERSION}"
        else
            print_info "已是最新版本: ${NEW_VERSION}"
        fi
    fi
}

# 清理备份文件
cleanup() {
    print_info "清理临时文件..."
    rm -f config.json.bak 2>/dev/null || true
    print_success "清理完成"
}

# 显示完成信息
show_completion() {
    print_header "升级完成！"
    
    echo "更新内容："
    echo ""
    echo "  ✅ 项目文件已更新"
    echo "  ✅ 依赖包已升级"
    echo "  ✅ 配置文件已保留"
    echo ""
    echo "📝 查看更新日志: cat CHANGELOG.md"
    echo "🐛 报告问题: https://github.com/your-repo/issues"
}

# ============ 主流程 ============

main() {
    print_header "IDOR Cross-Validation Skill 升级程序"
    
    check_project_dir
    check_current_version
    pull_latest
    update_dependencies
    update_config
    show_update_info
    cleanup
    show_completion
}

# 执行主函数
main
