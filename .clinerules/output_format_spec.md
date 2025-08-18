# AceFlow 输出格式规范

## 📁 标准化输出目录

所有工作产出必须保存到 `aceflow_result/` 目录，按照以下结构组织：

```
aceflow_result/
├── current_state.json          # 项目当前状态
├── stage_progress.json         # 各阶段进度跟踪
├── user_stories.md            # 用户故事文档
├── tasks_planning.md          # 任务规划文档
├── test_design.md             # 测试设计文档
├── implementation_report.md   # 实现报告
├── test_report.md             # 测试报告
└── review_report.md           # 评审报告
```

## 📝 文档格式规范

### 标准文档头部
每个文档都必须包含：

```markdown
# 文档标题

> **项目**: 项目名称  
> **阶段**: 当前阶段名称  
> **创建时间**: YYYY-MM-DD  
> **状态**: 进行中/已完成/待审核

## 📋 概述
文档内容概述...
```

### Markdown格式要求
- 使用标准的Markdown格式
- 代码块必须指定语言类型
- 表格使用标准Markdown表格格式
- 适度使用Emoji增强可读性

## 💾 状态文件格式

### current_state.json
```json
{
  "project": {
    "name": "项目名称",
    "mode": "流程模式",
    "created_at": "ISO时间戳",
    "last_updated": "ISO时间戳"
  },
  "flow": {
    "current_stage": "当前阶段名",
    "completed_stages": ["已完成阶段列表"],
    "next_stage": "下一阶段名",
    "progress_percentage": 数字
  }
}
```

## 🏷️ 文件命名规范

- 使用小写字母和下划线
- 阶段文档使用标准命名
- 状态文件使用.json扩展名
- 避免特殊字符和空格
