import re
from collections import Counter

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
        ''
    ]
    stats_markdown = '\n'.join(lines)
    print(stats_markdown)
    return stats_markdown, games_count

# 读取 pairs.txt 文件
with open('pairs.txt', 'r', encoding='utf-8') as f:
    pairs = f.readlines()

# 读取 index_draft.md 文件
with open('index_draft.md', 'r', encoding='utf-8') as f:
    content = f.read()

stats_block, games_count = build_stats(content)

# 替换奇数行文本为对应的偶数行文本
new_content = replace_odd_lines(content, pairs)

# 将所有图片 `![](assets/...)` 后面增加 size 属性
new_content = re.sub(r'!\[\]\(assets/.*?\)', r'\g<0>{: width="20px"}', new_content)

# 将占位符替换为统计块
new_content = new_content.replace('<!-- STATS -->', stats_block)

# 写入替换后的内容到 index.md 文件
with open('index.md', 'w', encoding='utf-8') as f:
    f.write(new_content)
