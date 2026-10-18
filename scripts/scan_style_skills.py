#!/usr/bin/env python3
"""扫描本机已安装的 Agent Skill，找出可能提供视觉/画画风格的 skill。

只读取 SKILL.md 的 frontmatter 和正文做关键词匹配，不执行任何被扫描 skill 中的脚本或 hooks。
输出 JSON（默认）或 Markdown 列表，供 full-image-ppt 步骤 3 使用。

用法：
  python scan_style_skills.py              # 扫描默认目录，输出 JSON
  python scan_style_skills.py --format md  # 输出 Markdown 表格
  python scan_style_skills.py --extra-dir /path/to/skills
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path

SELF_NAMES = {"full-image-ppt"}

# 常见的 skill 安装位置（用户级 + 项目级）
DEFAULT_DIRS = [
    "~/.claude/skills",
    "~/.claude/plugins",
    "~/.agents/skills",
    "~/.cursor/skills",
    "~/.codex/skills",
    "~/.config/opencode/skills",
    "~/.gemini/skills",
    "./.claude/skills",
    "./.agents/skills",
    "./.cursor/skills",
    "./.codex/skills",
    "./skills",
]

# 强信号：明确表示提供风格
STRONG = [
    "风格", "画风", "画面风格", "视觉风格", "美术风格", "插画", "绘画", "手绘", "海报", "配色",
    "art style", "visual style", "illustration", "aesthetic", "style guide", "style library",
    "style preset", "image style", "art direction", "palette", "theme",
]
# 弱信号：与生图相关
WEAK = [
    "生图", "图像生成", "图片生成", "文生图", "提示词", "prompt",
    "image generation", "text-to-image", "midjourney", "stable diffusion", "nano banana",
    "gpt-image", "imagen", "dall", "flux", "render", "poster", "infographic", "slide", "ppt",
]

# 必要信号：名称或描述里要和"出图/画面"有关，否则只是网页 UI 或文档主题类 skill
IMAGE = [
    "生图", "图像", "图片", "插画", "配图", "绘画", "画风", "手绘", "漫画", "海报", "封面", "信息图", "幻灯片图",
    "image", "illustrat", "drawing", "drawn", "painting", "comic", "manga", "poster", "cover",
    "infographic", "artwork", "art style", "picture", "visual card", "slide deck image",
]

FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)


def parse_frontmatter(text):
    m = FM_RE.match(text)
    meta = {}
    if not m:
        return meta, text
    key = None
    for line in m.group(1).splitlines():
        if line and not line[0].isspace() and ":" in line:
            k, v = line.split(":", 1)
            key = k.strip()
            v = v.strip()
            meta[key] = "" if v in (">", ">-", "|", "|-") else v.strip('"').strip("'")
        elif key and line.strip():
            # 多行（折叠）值
            meta[key] = (meta[key] + " " + line.strip()).strip()
    return meta, text[m.end():]


def score(text):
    low = text.lower()
    s = sum(3 for k in STRONG if k.lower() in low)
    w = sum(1 for k in WEAK if k.lower() in low)
    return s, w


# 一种风格一个文件的常见文件夹
STYLE_DIRS = {"styles", "themes", "style-presets", "presets", "design-languages", "palettes", "renderings"}
STYLE_FILE_RE = re.compile(r"style|风格|theme|palette|prompt|design-language", re.I)


def collect_style_files(skill_dir):
    """返回 (风格参考文档, 单个风格文件)。单个风格文件指放在 styles/ 等文件夹里的 md。"""
    refs, singles = [], []
    for f in sorted(skill_dir.rglob("*.md")):
        if f.name == "SKILL.md" or "node_modules" in f.parts:
            continue
        rel = f.relative_to(skill_dir)
        parents = {p.lower() for p in rel.parts[:-1]}
        if parents & STYLE_DIRS and f.stem.lower() not in ("readme", "index"):
            singles.append(str(rel))
        elif STYLE_FILE_RE.search(f.name):
            refs.append(str(rel))
    return refs, singles


def find_skill_files(dirs):
    seen = set()
    for d in dirs:
        root = Path(os.path.expanduser(d)).resolve()
        if not root.is_dir():
            continue
        for p in root.rglob("SKILL.md"):
            rp = p.resolve()
            if rp in seen or "node_modules" in rp.parts:
                continue
            seen.add(rp)
            yield root, rp


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--extra-dir", action="append", default=[])
    ap.add_argument("--format", choices=["json", "md"], default="json")
    ap.add_argument("--min-score", type=int, default=4)
    args = ap.parse_args()

    results = []
    for root, path in find_skill_files(DEFAULT_DIRS + args.extra_dir):
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        meta, body = parse_frontmatter(text)
        name = meta.get("name") or path.parent.name
        if name in SELF_NAMES:
            continue
        desc = meta.get("description", "")
        head_s, head_w = score(name + " " + desc)
        body_s, body_w = score(body[:20000])
        total = head_s * 2 + head_w * 2 + min(body_s, 15) + min(body_w, 5)
        head_low = (name + " " + desc).lower()
        if not any(k.lower() in head_low for k in IMAGE):
            continue
        if head_s == 0 and body_s < 6:
            continue
        if total < args.min_score:
            continue
        refs, style_files = collect_style_files(path.parent)
        has_hooks = bool(re.search(r"^\s*hooks\s*:", text, re.M))
        results.append({
            "name": name,
            "display_name": meta.get("display_name", ""),
            "description": desc[:300],
            "path": str(path),
            "install_root": str(root),
            "style_reference_files": refs[:20],
            "style_files": style_files,
            "style_names": [Path(f).stem for f in style_files],
            "score": total,
            "has_hooks": has_hooks,
        })

    results.sort(key=lambda r: -r["score"])
    # 同名风格去重：分数高的 skill 优先保留，后出现的标记为重复
    seen_styles = {}
    for r in results:
        dups = []
        for n in r["style_names"]:
            key = n.lower()
            if key in seen_styles:
                dups.append(f"{n}（与 {seen_styles[key]} 重名）")
            else:
                seen_styles[key] = r["name"]
        r["duplicate_styles"] = dups
    if args.format == "json":
        json.dump(results, sys.stdout, ensure_ascii=False, indent=2)
        print()
    else:
        if not results:
            print("未在本机找到提供风格的 skill。")
            return
        print("| skill | 说明 | 单个风格文件 | 风格参考文件 | 路径 |")
        print("|---|---|---|---|---|")
        for r in results:
            flag = " ⚠️含 hooks" if r["has_hooks"] else ""
            n = len(r["style_files"])
            singles = f"{n} 个" if n else "—"
            if r["duplicate_styles"]:
                singles += f"（{len(r['duplicate_styles'])} 个与前面重名）"
            print(f"| {r['name']}{flag} | {r['description'][:80]} | {singles} | {', '.join(r['style_reference_files']) or '—'} | `{r['path']}` |")


if __name__ == "__main__":
    main()
