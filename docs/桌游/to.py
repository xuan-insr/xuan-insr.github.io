import re
from pathlib import Path
from collections import Counter

try:
    from PIL import Image
except ImportError:
    Image = None

# 压缩参数：最大边 1200px，WebP quality 82
ASSETS_MAX_SIDE = 1200
WEBP_QUALITY = 82

def replace_odd_lines(text, pairs):
    lines = text.split('\n')
    for i in range(0, len(lines), 2):
        if i < len(pairs):
            odd_line = pairs[i].strip()
            even_line = pairs[i+1].strip()
            text = text.replace(odd_line, even_line)
    return text

# 场次行：含 | **、人局**、#expand（即「XX Y 人局」标题行）
SESSION_ROW_RE = re.compile(r'\|\s*\*\*[^*]+\*\*\s*\(([^)]+)\)')
def is_session_row(line):
    return '| **' in line and '人局**' in line and '#expand' in line

def build_stats(content):
    games_count = -2
    sessions_count = 0
    person_count = Counter()
    for line in content.split('\n'):
        if line.startswith('|') and '#expand' not in line:
            games_count += 1
        if is_session_row(line):
            sessions_count += line.count('人局')
            m = SESSION_ROW_RE.search(line)
            if m:
                for char in m.group(1):
                    if char != '等':
                        person_count[char] += 1
    lines = [
        f'??? info "统计"',
        f'    - **桌游总计**：{games_count} 款',
        f'    - **场次**：{sessions_count} 场',
        '    - **大家出场次数**：' + ' | '.join(f'{p} {n}' for p, n in person_count.most_common()) if person_count else '    - **大家出场次数**：—',
    ]
    stats_markdown = '\n'.join(lines)
    return stats_markdown, games_count

# 从内容中提取所有 assets/xxx.png 引用（去重）
ASSETS_PNG_RE = re.compile(r'assets/([^)]+\.png)')
def collect_png_refs(content):
    return list(dict.fromkeys(ASSETS_PNG_RE.findall(content)))

def compress_png_to_webp_if_needed(assets_dir, png_basename):
    """若 assets/xxx.webp 不存在，则把 assets/xxx.png 压缩为 WebP。"""
    png_path = assets_dir / png_basename
    webp_basename = png_basename[:-4] + ".webp"
    webp_path = assets_dir / webp_basename
    if webp_path.exists():
        return
    if not png_path.exists():
        return
    if Image is None:
        raise RuntimeError("Pillow 未安装，无法压缩图片。请安装：pip install Pillow")
    img = Image.open(png_path)
    if img.mode == "P":
        img = img.convert("RGBA")
    w, h = img.size
    if w > ASSETS_MAX_SIDE or h > ASSETS_MAX_SIDE:
        if w >= h:
            new_w, new_h = ASSETS_MAX_SIDE, max(1, int(h * ASSETS_MAX_SIDE / w))
        else:
            new_w, new_h = max(1, int(w * ASSETS_MAX_SIDE / h)), ASSETS_MAX_SIDE
        img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    img.save(webp_path, format="WEBP", quality=WEBP_QUALITY)

def compress_assets_and_replace_links(content, assets_dir):
    """扫描 content 中的 assets/*.png，按需压缩为 .webp，并替换链接。返回 (新内容，被引用的 png 文件名列表)。"""
    png_refs = collect_png_refs(content)
    for png_basename in png_refs:
        compress_png_to_webp_if_needed(assets_dir, png_basename)
    # 将文中所有 assets/xxx.png 替换为 assets/xxx.webp
    new_content = ASSETS_PNG_RE.sub(lambda m: f"assets/{m.group(1)[:-4]}.webp", content)
    return new_content, png_refs

def format_size(n_bytes):
    """格式化为人类可读大小（KB/MB）。"""
    if n_bytes < 1024:
        return f"{n_bytes} B"
    if n_bytes < 1024 * 1024:
        return f"{n_bytes / 1024:.1f} KB"
    return f"{n_bytes / (1024 * 1024):.1f} MB"

def referenced_webp_stats(assets_dir, png_refs):
    """统计被引用的 webp 数量与总大小（字节）。"""
    count = 0
    total = 0
    for png_basename in png_refs:
        webp_path = assets_dir / (png_basename[:-4] + ".webp")
        if webp_path.exists():
            count += 1
            total += webp_path.stat().st_size
    return count, total

# 读取 pairs.txt 文件
with open('pairs.txt', 'r', encoding='utf-8') as f:
    pairs = f.readlines()

# 读取 index_draft.md 文件
with open('index_draft.md', 'r', encoding='utf-8') as f:
    content = f.read()

stats_block, games_count = build_stats(content)

# 替换奇数行文本为对应的偶数行文本
new_content = replace_odd_lines(content, pairs)

# 按需将 assets/*.png 压缩为 .webp 并替换链接
script_dir = Path(__file__).resolve().parent
assets_dir = script_dir / "assets"
new_content, png_refs = compress_assets_and_replace_links(new_content, assets_dir)

# 被引用的 webp 数量与总大小，追加到统计块
img_count, img_bytes = referenced_webp_stats(assets_dir, png_refs)
stats_block += f'\n    - **图片数**：{img_count} 张\n    - **图片总大小**：{format_size(img_bytes)}'


# 将所有图片 `![](assets/...)` 后面增加 size 属性
new_content = re.sub(r'!\[\]\(assets/.*?\)', r'\g<0>{: width="20px"}', new_content)

# 将占位符替换为统计块
new_content = new_content.replace('<!-- STATS -->', stats_block)
print(stats_block)

# 写入替换后的内容到 index.md 文件
with open('index.md', 'w', encoding='utf-8') as f:
    f.write(new_content)
