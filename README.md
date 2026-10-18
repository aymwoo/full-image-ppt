# full-image-ppt · 全图演示文稿生成器

一个智能体 Skill（SKILL.md 格式）：把教案、讲义、文章、讲稿等文档转成“全图式”演示文稿。每一页都是一张 1920×1080（16:9）的整页插图，文字融入画面，不用传统文本框排版。

## 它做什么

按“先对齐、再生产”的流程逐步进行：

1. 分析文档，输出内容速览（主题、结构、关键意象、受众）。
2. 询问使用场合与时长。
3. 按时长对照表建议页数，由你确认。
4. 推荐并让你选定视觉风格。内置三种：乐高积木风格、彩色手绘风格、泥塑定格动画风格。选之前会先扫描本机已安装的风格类 skill，把它们提供的风格也加进候选，并标明来源。
5. 生成一份 Markdown 分页生图提示词文档，可复制给任意生图大模型。
6. 环境有生图能力时逐页生图（`page_01.png` …）；没有时由你用其他模型生图后放回目录。
7. 用 `scripts/build_deck.py` 把图片组装成 `全图演示文稿.pptx` 和 `全图演示文稿.pdf`。

触发词示例：“全图PPT”“全图演示文稿”“把文档做成全图幻灯片”“分页生图提示词”。

## 目录结构

```
SKILL.md                       # 技能主文件
references/styles.md           # 风格库（3 种内置风格的提示词片段与推荐逻辑）
references/page_plan.md        # 时长→页数对照表与分页结构建议
references/prompt_template.md  # Markdown 提示词文档模板
scripts/build_deck.py          # 由图片批量生成 pptx 与 pdf
scripts/scan_style_skills.py   # 扫描本机已安装的风格类 skill（只读）
```

## 安装

任选一种：

```bash
# 用 Skills CLI 安装
npx skills add aymwoo/full-image-ppt

# 或手动复制到 Claude Code 的技能目录
git clone https://github.com/aymwoo/full-image-ppt ~/.claude/skills/full-image-ppt

# 或放进项目的 .agents/skills 目录
git clone https://github.com/aymwoo/full-image-ppt .agents/skills/full-image-ppt
```

组装 pptx/pdf 需要 Python 依赖：

```bash
pip install python-pptx Pillow
python scripts/build_deck.py --input <图片目录> --output <输出目录> --name 全图演示文稿
```

## 使用本地风格类 skill

选风格时，本技能会运行 `scripts/scan_style_skills.py`，在 `~/.claude/skills`、`~/.agents/skills`、`~/.cursor/skills`、`~/.codex/skills` 和项目里的 `.claude/skills`、`.agents/skills` 等目录中查找提供画风的 skill，并读取它们的风格描述。它只读文字，不会执行这些 skill 里的脚本或 hooks。也可以自己先跑一遍看看：

```bash
python scripts/scan_style_skills.py --format md
python scripts/scan_style_skills.py --extra-dir /path/to/other/skills
```

## 更新记录

- **v1.1.1**
  - 提示词模板的参数总览表增加"风格来源 skill"和"风格来源路径"两行。
  - 每页提示词放进单独的代码块，页名只留在小标题里，避免被画成图上的标题；只画"核心信息"里列出的文字。
  - 生图后逐张检查，文字乱码、构图崩坏或多出 ✕/✓ 等符号的页面重新生成（每页最多 2 次），仍有问题的页面告诉用户。
  - `build_deck.py`：不是 16:9 的图片居中裁切后缩放到 1920×1080，不再拉伸；PDF 页面改为与 pptx 相同的 13.333″×7.5″，新增 `--pdf-quality`（默认 95），文字更清晰。
  - 工作流不再写死 AskUserQuestion、present_files 等特定工具名，换成通用说法。
- **v1.1.0**：选风格前扫描本机已安装的风格类 skill，把它们的风格加入候选。

## 来源

本技能同时发布在 SkillHub：<https://skillhub.cn/skills/user_37fa416d/full-image-ppt>
