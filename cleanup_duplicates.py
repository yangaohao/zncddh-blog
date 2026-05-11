#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from pathlib import Path

def cleanup_duplicate_tags(file_path):
    """
    清理重复的 {% raw %} 和 {% endraw %} 标签
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # 移除连续的重复 {% raw %} 标签
    content = re.sub(r'({%\s*raw\s*%})\s*\1+', r'\1', content, flags=re.MULTILINE)
    
    # 移除连续的重复 {% endraw %} 标签
    content = re.sub(r'({%\s*endraw\s*%})\s*\1+', r'\1', content, flags=re.MULTILINE)
    
    # 处理形如 {% raw %} \n {% raw %} 的情况
    content = re.sub(r'{%\s*raw\s*%}\s*\n\s*{%\s*raw\s*%}', '{% raw %}', content)
    
    # 处理形如 {% endraw %} \n {% endraw %} 的情况
    content = re.sub(r'{%\s*endraw\s*%}\s*\n\s*{%\s*endraw\s*%}', '{% endraw %}', content)
    
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def process_all_markdown_files():
    """
    处理 _posts 文件夹中的所有 Markdown 文件
    """
    posts_dir = Path('/home/yah/docker-learn/hexo-blog/source/_posts')
    
    if not posts_dir.exists():
        print(f"错误: {posts_dir} 目录不存在")
        return
    
    # 找到所有 .md 文件
    md_files = list(posts_dir.glob('**/*.md'))
    
    print(f"开始清理 {len(md_files)} 个 Markdown 文件中的重复标签...")
    print("=" * 60)
    
    modified_count = 0
    
    for md_file in md_files:
        try:
            relative_path = md_file.relative_to(posts_dir)
            if cleanup_duplicate_tags(str(md_file)):
                print(f"✓ 已清理: {relative_path}")
                modified_count += 1
            else:
                print(f"✓ 无重复标签: {relative_path}")
        except Exception as e:
            print(f"✗ 错误 {md_file}: {e}")
    
    print("=" * 60)
    print(f"清理完成! 共修改 {modified_count} 个文件")


if __name__ == '__main__':
    process_all_markdown_files()
