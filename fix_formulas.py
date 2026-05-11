#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from pathlib import Path

def wrap_formulas_in_file(file_path):
    """
    为单个文件中所有未被包裹的公式添加 {% raw %} 和 {% endraw %} 标签
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # 按行处理，更清楚地处理多行公式
    lines = content.split('\n')
    result_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # 如果这行不包含 $$，直接添加
        if '$$' not in line:
            result_lines.append(line)
            i += 1
            continue
        
        # 计算这行中 $$ 的数量
        dollar_count = line.count('$$')
        
        # 情况1: 这行有两个或以上的 $$（完整的单行公式）
        if dollar_count >= 2:
            # 检查是否已被包裹
            if '{% raw %}' in line or '{% endraw %}' in line:
                # 已有标签，直接添加
                result_lines.append(line)
            else:
                # 检查前一行是否已有 {% raw %}
                has_raw_before = (result_lines and '{% raw %}' in result_lines[-1])
                
                if not has_raw_before:
                    result_lines.append('{% raw %}')
                
                result_lines.append(line)
                result_lines.append('{% endraw %}')
            i += 1
        
        # 情况2: 这行有一个 $$（公式开始或结束）
        elif dollar_count == 1:
            # 检查这行是否已有 raw/endraw 标签
            if '{% raw %}' in line or '{% endraw %}' in line:
                # 已有标签，直接添加
                result_lines.append(line)
                i += 1
                continue
            
            # 检查是否是公式开始（前面没有 {% raw %}）
            has_raw_before = (result_lines and '{% raw %}' in result_lines[-1])
            has_endraw_before = (result_lines and '{% endraw %}' in result_lines[-1])
            
            # 如果是新公式的开始（既没有前置 raw，也没有前置 endraw，说明是新公式）
            if not has_raw_before or (has_raw_before and has_endraw_before):
                # 这是多行公式的开始
                result_lines.append('{% raw %}')
                result_lines.append(line)
                
                # 继续添加后续行直到找到结束的 $$
                i += 1
                found_end = False
                while i < len(lines):
                    next_line = lines[i]
                    result_lines.append(next_line)
                    
                    if '$$' in next_line:
                        # 找到了结束
                        if '{% endraw %}' not in next_line:
                            result_lines.append('{% endraw %}')
                        found_end = True
                        i += 1
                        break
                    i += 1
                
                # 如果没有找到结束（不应该发生），记录警告
                if not found_end:
                    result_lines.append('{% endraw %}')
            else:
                # 这是多行公式的继续或结束，直接添加
                result_lines.append(line)
                if '$$' in line and '{% endraw %}' not in line and '{% endraw %}' not in result_lines[-1]:
                    result_lines.append('{% endraw %}')
                i += 1
        else:
            result_lines.append(line)
            i += 1
    
    # 重新组合内容
    new_content = '\n'.join(result_lines)
    
    # 如果内容有改变，保存文件
    if new_content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
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
    
    print(f"找到 {len(md_files)} 个 Markdown 文件")
    print("=" * 60)
    
    modified_count = 0
    error_count = 0
    
    for md_file in md_files:
        try:
            relative_path = md_file.relative_to(posts_dir)
            if wrap_formulas_in_file(str(md_file)):
                print(f"✓ 已修改: {relative_path}")
                modified_count += 1
            else:
                print(f"✓ 无需修改: {relative_path}")
        except Exception as e:
            print(f"✗ 错误 {md_file}: {e}")
            error_count += 1
    
    print("=" * 60)
    print(f"处理完成!")
    print(f"  修改文件: {modified_count}")
    print(f"  错误: {error_count}")
    print(f"  总计: {len(md_files)}")


if __name__ == '__main__':
    process_all_markdown_files()
