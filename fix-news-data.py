#!/usr/bin/env python3
"""
fix-news-data.py — 修复 news-data.json 里的未转义双引号
原理：手工解析每一行，对于 "summary": "..." 这样的字段，
      把值内部的裸双引号替换成中文双引号。
"""
import json
import re
import sys
from pathlib import Path

FILE = Path(__file__).parent / "news-data.json"


def fix_value_quotes(s: str) -> str:
    """
    把字符串内部的裸双引号替换成中文双引号（"→"，"→"）。
    用法：每对 "..." 配对地改成 "..."/"..."。
    """
    result = []
    in_quote = False
    for ch in s:
        if ch == '"':
            if not in_quote:
                result.append('\u201c')  # "
                in_quote = True
            else:
                result.append('\u201d')  # "
                in_quote = False
        else:
            result.append(ch)
    return ''.join(result)


def manual_fix(text: str) -> str:
    """
    手工状态机修复:
    1. 找到每一行的 "key": " ... " 模式
    2. 把 value 里出现的多余 " 替换成中文 ""
    """
    out_lines = []
    for line in text.split('\n'):
        # 找到第一对结构引号的位置
        # 形如:    "summary": "...."....
        m = re.match(r'^(\s*"[^"]+":\s*")(.*?)("\s*,?\s*)$', line)
        if not m:
            out_lines.append(line)
            continue
        prefix, value, suffix = m.group(1), m.group(2), m.group(3)
        # value 是值内部，把里面所有 " 替换成中文 ""
        if '"' in value:
            fixed = fix_value_quotes(value)
            line = prefix + fixed + suffix + '\n'
        out_lines.append(line)
    return '\n'.join(out_lines)


def main():
    raw = FILE.read_text(encoding='utf-8')

    # 1. 先验证原始是否真的有错
    try:
        data = json.loads(raw)
        print(f"✅ {FILE.name} 本来就 OK，无需修复")
        return 0
    except json.JSONDecodeError:
        pass

    # 2. 修复
    print(f"🔧 开始修复 {FILE.name} ...")
    fixed = manual_fix(raw)

    # 3. 再次验证
    try:
        data = json.loads(fixed)
        print(f"✅ 修复成功，共 {len(data)} 条记录")
        # 写回
        FILE.write_text(fixed, encoding='utf-8')
        print(f"✅ 已写回 {FILE}")
        return 0
    except json.JSONDecodeError as e:
        print(f"❌ 修复后仍有错误: line {e.lineno}, col {e.colno}")
        # 打印错误行
        lines = fixed.split('\n')
        for i in range(max(0, e.lineno-2), min(len(lines), e.lineno+1)):
            print(f"  {i+1}: {lines[i].rstrip()}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
