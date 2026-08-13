#!/bin/bash
# ============================================================
# IDOR Cross-Validation Skill - 一键安装脚本
# 版本: V1.0
# 说明: 自动检查环境并安装项目依赖
# ============================================================

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo ""
    echo "========================================"
    echo -e "${GREEN}$1${NC}"
    echo "========================================"
    echo ""
}

# 检查操作系统
check_os() {
    print_info "检测操作系统..."
    OS="$(uname -s)"
    case "${OS}" in
        Linux*)     OS_TYPE="Linux";;
        Darwin*)    OS_TYPE="macOS";;
        CYGWIN*|MINGW*|MSYS*) OS_TYPE="Windows";;
        *)          OS_TYPE="Unknown";;
    esac
    print_success "操作系统: ${OS_TYPE}"
}

# 检查依赖命令
check_dependencies() {
    print_info "检查依赖命令..."
    
    local missing_deps=()
    
    # 检查 curl
    if ! command -v curl &> /dev/null; then
        missing_deps+=("curl")
    fi
    
    # 检查 git
    if ! command -v git &> /dev/null; then
        missing_deps+=("git")
    fi
    
    # 检查 python3
    if ! command -v python3 &> /dev/null; then
        missing_deps+=("python3")
    fi
    
    # 检查 pip
    if ! command -v pip3 &> /dev/null; then
        missing_deps+=("pip3")
    fi
    
    if [ ${#missing_deps[@]} -ne 0 ]; then
        print_warning "缺少依赖: ${missing_deps[*]}"
        print_info "请先安装以上依赖，然后重新运行此脚本"
        exit 1
    fi
    
    print_success "所有依赖已安装"
}

# 安装Python依赖
install_python_deps() {
    print_info "安装Python依赖..."
    
    # 检查是否存在 requirements.txt
    if [ -f "requirements.txt" ]; then
        pip3 install -r requirements.txt --quiet
        print_success "Python依赖安装完成"
    else
        print_warning "未找到 requirements.txt，跳过"
    fi
}

# 创建配置文件
create_config() {
    print_info "创建配置文件..."
    
    if [ ! -f "config.example.json" ]; then
        cat > config.example.json << 'EOF'
{
  "target": "https://your-target.com",
  "admin": {
    "username": "admin@example.com",
    "password": "Admin@123"
  },
  "user1": {
    "username": "user1@example.com",
    "password": "User1@123"
  },
  "user2": {
    "username": "user2@example.com",
    "password": "User2@456"
  },
  "scan_options": {
    "crawl_depth": 2,
    "rate_limit": 10,
    "max_requests": 500
  }
}
EOF
        print_success "配置文件已创建: config.example.json"
        print_info "请复制为 config.json 并填入真实信息"
    fi
}

# 设置执行权限
set_permissions() {
    print_info "设置执行权限..."
    
    chmod +x scripts/*.py 2>/dev/null || true
    print_success "权限设置完成"
}

# 显示完成信息
show_completion() {
    print_header "安装完成！"
    
    echo "下一步操作："
    echo ""
    echo "1. 复制配置文件："
    echo "   cp config.example.json config.json"
    echo ""
    echo "2. 编辑配置文件填入目标信息："
    echo "   vim config.json"
    echo ""
    echo "3. 在GLM平台执行扫描："
    echo "   使用 prompts/glm_scanner.md"
    echo ""
    echo "4. 在DeepSeek平台执行扫描："
    echo "   使用 prompts/deepseek_scanner.md"
    echo ""
    echo "5. 交叉验证："
    echo "   使用 prompts/cross_validator.md"
    echo ""
    echo "📚 查看文档: cat README.md"
    echo "🐛 报告问题: https://github.com/your-repo/issues"
}

# ============ 主流程 ============

main() {
    print_header "IDOR Cross-Validation Skill 安装程序"
    
    check_os
    check_dependencies
    install_python_deps
    create_config
    set_permissions
    show_completion
}

# 执行主函数
main
