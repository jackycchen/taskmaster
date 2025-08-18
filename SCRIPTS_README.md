# AceFlow 项目级脚本说明 (Python版本)

本项目包含以下AceFlow工作脚本，用于项目管理和状态控制：

## 🛠️ 可用脚本

### 1. aceflow-stage.py - 阶段管理
```bash
python aceflow-stage.py status          # 查看当前阶段状态
python aceflow-stage.py next            # 推进到下一阶段
python aceflow-stage.py list            # 列出所有阶段
python aceflow-stage.py reset           # 重置项目状态
```

### 2. aceflow-validate.py - 项目验证
```bash
python aceflow-validate.py              # 标准验证
python aceflow-validate.py --mode=complete --report  # 完整验证并生成报告
python aceflow-validate.py --fix        # 自动修复问题
```

### 3. aceflow-templates.py - 模板管理
```bash
python aceflow-templates.py list        # 列出可用模板
python aceflow-templates.py apply       # 应用模板
python aceflow-templates.py validate    # 验证模板
```

## 📋 使用建议

1. **AI Agent集成**: 这些脚本被设计为与AI Agent协同工作
2. **状态管理**: 使用 `aceflow-stage.py` 管理项目进度
3. **质量保证**: 定期运行 `aceflow-validate.py` 确保合规性
4. **模板利用**: 使用 `aceflow-templates.py` 标准化工作流程

## ⚠️ 重要提醒

- 这些脚本是项目级副本，与全局安装的Python CLI配合使用
- 脚本会自动识别项目结构和配置，无需额外设置
- 如需更新脚本，重新运行初始化命令即可

## 🌍 跨平台兼容性

- **Python版本**: 支持Python 3.7+
- **操作系统**: Windows、macOS、Linux
- **依赖**: 仅使用Python标准库，无额外依赖
