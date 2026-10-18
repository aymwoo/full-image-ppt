# 风格库（视觉风格提示词片段）

本文件存放"全图演示文稿"可用的视觉风格。每个风格包含：视觉特征（给用户看的说明）、适用场景、**完整风格提示词片段**（粘贴进每页提示词，含中文描述 + 英文标签，兼顾中文与英文生图模型）、**推荐逻辑**。

> 扩展方法：新增风格只需在本文档追加一个同名小节（包含上述四要素），并在 SKILL.md 步骤 3 中引用即可，无需改动其他文件。
>
> 本地 skill 风格：步骤 3.1 会用 `scripts/scan_style_skills.py` 扫描本机已安装的风格类 skill，把它们提供的风格按本文件的四要素整理后，与内置风格一起展示。外部风格不写入本文件；想长期固定某个外部风格时，可按上面的方法手动追加。

---

## 1. 乐高积木风格

**视觉特征**
整体画面由乐高积木（LEGO）拼搭而成：所有人物、物体、场景都是明快的塑料积木块造型，表面带有圆润的凸点（studs）质感，色彩饱和度高、对比鲜明，光线柔和并带轻微高光，呈现玩具般的可爱与模块化秩序感。

**适用场景**
面向青少年的趣味科普；结构 / 系统 / 流程 / 组成类内容（积木天然表达"模块化""搭建""拼装"）；公开课用于快速抓住注意力。

**完整风格提示词片段（每页必带）**
> 中文：整体由乐高积木（LEGO）拼搭而成，所有人物、物体、场景都是明快的塑料积木块造型，带有圆润凸点质感，色彩饱和、对比鲜明，柔和 studio 光照带轻微高光，玩具般可爱、模块化、整齐有序。
> 英文：LEGO brick style, plastic building blocks, visible round studs on surfaces, bright saturated colors, clean modular composition, soft studio lighting with subtle highlights, 3D render, playful toy aesthetic, front or slight isometric view

**推荐逻辑**
当受众是中小学生，或内容涉及"结构、组成、步骤、系统搭建、模块化"时优先推荐。

---

## 2. 彩色手绘风格

**视觉特征**
水彩与马克笔混合的彩色手绘插画，笔触轻松温暖，线条略带不规则的随性感，色彩明快柔和，背景常留白或淡彩晕染，带有纸面纹理，整体像一本精心绘制的绘本或课堂板书，亲切有温度。

**适用场景**
故事化 / 叙事性内容；人文社科；情感与价值观主题；阅读分享；教师个人风格化表达。

**完整风格提示词片段（每页必带）**
> 中文：水彩与马克笔混合的彩色手绘插画，笔触轻松温暖，线条略带不规则的随性感，色彩明快柔和，背景留白或淡彩晕染，带纸面纹理，像精心绘制的绘本或课堂板书，亲切有温度。
> 英文：colorful hand-drawn illustration, watercolor and marker mixed, loose warm brushstrokes, slightly irregular ink lines, soft pastel palette, paper texture, storybook picture-book style, gentle and friendly mood

**推荐逻辑**
当内容偏叙事、人文、情感，或受众需要"温度感"与亲和力时优先推荐。

---

## 3. 泥塑定格动画风格

**视觉特征**
黏土定格动画（claymation）质感：所有形象由彩色黏土捏塑而成，表面有手工指纹与颗粒肌理，边缘略不规整，配色饱满卡通化，光影带暖色柔光，像停格动画里会动的角色，奇趣又温暖。

**适用场景**
创意 / 想象类主题；角色驱动的故事；低龄或趣味科普；需要"童趣与手工感"的场合。

**完整风格提示词片段（每页必带）**
> 中文：黏土定格动画（claymation）质感，所有形象由彩色黏土捏塑而成，表面有手工指纹与颗粒肌理，边缘略不规整，配色饱满卡通化，暖色柔光，像会动的停格动画角色，奇趣温暖。
> 英文：claymation style, clay stop-motion, hand-sculpted clay figures, visible finger marks and grainy texture, slightly uneven edges, vibrant cartoon colors, warm soft lighting, whimsical tactile mood, miniature diorama

**推荐逻辑**
当内容需要强烈童趣、角色拟人，或"手工 / 创作"气质时优先推荐。
