import re

def replace_odd_lines(text, pairs):
    lines = text.split('\n')
    for i in range(0, len(lines), 2):
        if i < len(pairs):
            odd_line = pairs[i].strip()
            even_line = pairs[i+1].strip()
            text = text.replace(odd_line, even_line)
    return text

# 读取 pairs.txt 文件
with open('pairs.txt', 'r', encoding='utf-8') as f:
    pairs = f.readlines()

# 读取 index.md 文件
with open('index_draft.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 替换奇数行文本为对应的偶数行文本
new_content = replace_odd_lines(content, pairs)

# 将所有图片 `![](assets/...)` 后面增加 size 属性
new_content = re.sub(r'!\[\]\(assets/.*?\)', r'\g<0>{: width="20px"}', new_content)

# 写入替换后的内容到 index.md 文件
with open('index.md', 'w', encoding='utf-8') as f:
    f.write(new_content)
