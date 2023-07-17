import re

def replace_even_lines(text, pairs):
    lines = text.split('\n')
    for i in range(1, len(lines), 2):
        if (i-1) < len(pairs):
            even_line = pairs[i].strip()
            odd_line = pairs[i-1].strip()
            text = text.replace(even_line, odd_line)
    return text

# 读取 pairs.txt 文件
with open('pairs.txt', 'r', encoding='utf-8') as f:
    pairs = f.readlines()

# 读取 index.md 文件
with open('index.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 替换偶数行文本为对应的奇数行文本
new_content = replace_even_lines(content, pairs)

# 写入替换后的内容到 index.md 文件
with open('index_draft.md', 'w', encoding='utf-8') as f:
    f.write(new_content)
