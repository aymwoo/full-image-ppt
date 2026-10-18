#!/usr/bin/env python3
"""由一组全图（page_01.png ...）生成 全图演示文稿.pptx 与 .pdf。

用法:
  python build_deck.py --input <图片目录> [--output <输出目录>] [--prefix page] [--name 全图演示文稿] [--dpi 150]

依赖: python-pptx, Pillow
  pip install python-pptx Pillow

说明:
  - pptx: 每页为一整张铺满画面的图片（16:9，13.333"×7.5"），无占位符。
  - pdf: 由同一批图片按页生成的高清 PDF。
  - 图片按前缀后的数字顺序排序（page_01.png < page_02.png ...）。
"""
import argparse
import glob
import os
import re
import sys

try:
    from pptx import Presentation
    from pptx.util import Inches
except ImportError:
    sys.exit("缺少依赖 python-pptx。请先运行: pip install python-pptx Pillow")

try:
    from PIL import Image
except ImportError:
    sys.exit("缺少依赖 Pillow。请先运行: pip install python-pptx Pillow")


def sorted_pages(input_dir, prefix):
    """按 page_01, page_02 ... 顺序返回图片路径；无数字时按文件名排序兜底。"""
    files = glob.glob(os.path.join(input_dir, f"{prefix}_*.png"))
    if not files:
        files = sorted(glob.glob(os.path.join(input_dir, "*.png")))
        return files

    def key(p):
        m = re.search(rf"{re.escape(prefix)}_(\d+)\.", os.path.basename(p))
        return int(m.group(1)) if m else 10**9

    return sorted(files, key=key)


def build_pptx(pages, out_path):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]  # 完全空白版式
    for img in pages:
        slide = prs.slides.add_slide(blank)
        # 铺满整页（拉伸以彻底无黑边；图片应为 16:9，否则按比例拉伸）
        slide.shapes.add_picture(img, 0, 0, width=prs.slide_width, height=prs.slide_height)
    prs.save(out_path)


def build_pdf(pages, out_path, dpi=150):
    imgs = []
    for p in pages:
        im = Image.open(p).convert("RGB")
        im.info["dpi"] = (dpi, dpi)
        imgs.append(im)
    if not imgs:
        sys.exit("未找到任何图片，无法生成 PDF。")
    first = imgs[0]
    first.save(
        out_path,
        "PDF",
        save_all=True,
        append_images=imgs[1:],
        resolution=dpi,
    )


def main():
    ap = argparse.ArgumentParser(description="由全图图片生成 pptx 与 pdf")
    ap.add_argument("--input", required=True, help="图片目录（含 page_01.png ...）")
    ap.add_argument("--output", default=".", help="输出目录，默认当前目录")
    ap.add_argument("--prefix", default="page", help="图片前缀，如 page_01.png 的前缀 page")
    ap.add_argument("--name", default="全图演示文稿", help="输出文件名（不含扩展名）")
    ap.add_argument("--dpi", type=int, default=150, help="PDF 分辨率，默认 150")
    args = ap.parse_args()

    pages = sorted_pages(args.input, args.prefix)
    if not pages:
        sys.exit(f"在 {args.input} 未找到 {args.prefix}_*.png 图片。")

    os.makedirs(args.output, exist_ok=True)
    pptx_path = os.path.join(args.output, args.name + ".pptx")
    pdf_path = os.path.join(args.output, args.name + ".pdf")

    build_pptx(pages, pptx_path)
    print(f"已生成 PPTX: {pptx_path}（{len(pages)} 页）")

    try:
        build_pdf(pages, pdf_path, args.dpi)
        print(f"已生成 PDF : {pdf_path}")
    except Exception as e:  # PDF 失败不应阻断 pptx 交付
        print(f"警告：PDF 生成失败（{e}）。PPTX 已正常生成。")


if __name__ == "__main__":
    main()
