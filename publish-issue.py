#!/usr/bin/env python3
"""
publish-issue.py — 发布新一期银发资讯的自动化脚本
用法: python3 publish-issue.py <日期 YYYY-MM-DD> [期号]
  例如: python3 publish-issue.py 2026-07-01
        python3 publish-issue.py 2026-07-01 17

作用：
  1. 自动在 news.html 列表页最前面插入新卡片
  2. 自动在 index.html 首页资讯区最前面插入新卡片
  3. 自动在 index.html sitemap 最前面插入新条目
  4. 自动更新 news-data.json
  5. git add + commit（不自动 push，留给你确认）

前提：
  news/<日期>.html 内容页已经存在
"""
import re
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent
NEWS_FILE = ROOT / "news.html"
INDEX_FILE = ROOT / "index.html"
DATA_FILE = ROOT / "news-data.json"
NEWS_DIR = ROOT / "news"


def fail(msg):
    print(f"❌ {msg}")
    sys.exit(1)


def get_issue_number(date_str: str) -> int:
    """从 news-data.json 推断下一期期号 = max(已有) + 1"""
    data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    max_issue = max(item.get("issue", 0) for item in data)
    return max_issue + 1


def check_duplicates(date_str: str, issue: int) -> None:
    """
    去重检查：如果 news-data.json 里已经有这个期号或这个日期，提示用户。
    """
    data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    for item in data:
        if item.get("issue") == issue:
            fail(f"news-data.json 里已经存在第{issue}期，不能重复发布")
        if item.get("filename") == f"{date_str}.html":
            fail(f"news-data.json 里已经存在日期为 {date_str} 的期（文件名 {date_str}.html）")
    # 同时检查 news.html 里是否已包含该日期
    raw = NEWS_FILE.read_text(encoding="utf-8")
    if f"news/{date_str}.html" in raw:
        fail(f"news.html 列表里已经包含 news/{date_str}.html，不能重复发布")
    print(f"   ✅ 去重检查通过")


def extract_title_and_summary(html_path: Path) -> tuple[str, str]:
    """
    从 <title> 和首段正文提取标题和摘要。
    摘要 = 前 100 个中文字符 + 标点
    """
    raw = html_path.read_text(encoding="utf-8")
    # 标题
    m = re.search(r'<title>(.*?)</title>', raw, re.DOTALL)
    title = m.group(1).strip() if m else html_path.stem
    # 摘要：从 <body> 之后抓前 120 个有效字符
    body = re.sub(r'<[^>]+>', '', raw)  # 去 HTML 标签
    body = re.sub(r'\s+', ' ', body).strip()
    # 找第一个有意义的句子（去掉"银发资讯第X期"这种标题句）
    sentences = re.split(r'[。！？]', body)
    summary = ""
    for s in sentences:
        s = s.strip()
        if len(s) >= 30 and "银发资讯" not in s and "第" not in s[:3]:
            summary = s[:120] + ("..." if len(s) > 120 else "")
            break
    if not summary:
        summary = body[:120] + ("..." if len(body) > 120 else "")
    return title, summary


def insert_to_news_html(date_str: str, issue: int, title: str, summary: str, filename: str):
    """在 news.html 的 <div class="index-list"> 后面插入新卡片"""
    raw = NEWS_FILE.read_text(encoding="utf-8")
    # 提取 date 的人性化显示：2026-06-24 -> 2026年6月24日
    y, m, d = date_str.split("-")
    date_cn = f"{y}年{int(m)}月{int(d)}日"
    new_card = f'''        <a class="index-item" href="news/{filename}">
          <div class="index-no">第{issue}期</div>
          <div class="index-title"><b>{date_cn}</b><span>政策 / 产业 / 趋势 / 技术</span></div>
          <div class="index-desc">{summary}</div>
          <div class="index-link">{date_str}</div>
        </a>
'''
    # 找到 <div class="index-list">\n 的下一行开始插入
    marker = '<div class="index-list">\n'
    idx = raw.find(marker)
    if idx < 0:
        fail("news.html 里找不到 <div class=\"index-list\">")
    insert_pos = idx + len(marker)
    new_raw = raw[:insert_pos] + new_card + raw[insert_pos:]
    NEWS_FILE.write_text(new_raw, encoding="utf-8")
    print(f"   ✅ news.html 列表页已插入第{issue}期")


def insert_to_index_news_grid(date_str: str, issue: int, summary: str):
    """在 index.html 的 .news-grid 内插入新卡片（限制 3 个，超出替换最旧的）"""
    raw = INDEX_FILE.read_text(encoding="utf-8")
    y, m, d = date_str.split("-")
    date_cn = f"{y}年{int(m)}月{int(d)}日"
    # 提取标题
    title_line = summary.split("，")[0].split("。")[0].split("；")[0]
    if len(title_line) > 30:
        title_line = title_line[:30] + "..."

    new_card = f'''        <article class="news-card">
          <time>{date_cn} · 第{issue}期</time>
          <div>
            <h3>{title_line}</h3>
            <p>{summary[:60]}{"..." if len(summary) > 60 else ""}</p>
          </div>
        </article>
'''
    # 找到 <div class="news-grid"> 后第一个 <article> 之前插入
    marker = '<div class="news-grid">\n'
    idx = raw.find(marker)
    if idx < 0:
        fail("index.html 里找不到 <div class=\"news-grid\">")
    insert_pos = idx + len(marker)
    new_raw = raw[:insert_pos] + new_card + raw[insert_pos:]

    # 限制最多 3 个 article，删掉多余的
    article_pattern = re.compile(
        r'        <article class="news-card">\n.*?\n        </article>\n',
        re.DOTALL
    )
    articles = list(article_pattern.finditer(new_raw))
    if len(articles) > 3:
        # 保留前 3 个，删掉后面的
        for m in articles[3:]:
            new_raw = new_raw.replace(m.group(0), "", 1)
        print(f"   ✅ index.html 资讯区已插入第{issue}期（并移除最旧 1 个，保持 3 个上限）")
    else:
        print(f"   ✅ index.html 资讯区已插入第{issue}期")

    INDEX_FILE.write_text(new_raw, encoding="utf-8")


def insert_to_index_sitemap(date_str: str, issue: int):
    """在 index.html 的资讯存档 sitemap 顶部插入新条目"""
    raw = INDEX_FILE.read_text(encoding="utf-8")
    y, m, d = date_str.split("-")
    new_item = f'            <li><a href="news/{date_str}.html">第{issue}期 · {date_str}</a></li>\n'

    # 找 <h3>资讯存档</h3> 后的 <ul> 位置
    marker = '<h3>资讯存档</h3>\n          <ul>\n'
    idx = raw.find(marker)
    if idx < 0:
        fail("index.html 里找不到资讯存档区块")
    insert_pos = idx + len(marker)
    new_raw = raw[:insert_pos] + new_item + raw[insert_pos:]
    INDEX_FILE.write_text(new_raw, encoding="utf-8")
    print(f"   ✅ index.html sitemap 已插入第{issue}期")


def update_news_data_json(date_str: str, issue: int, title: str, summary: str, filename: str):
    """在 news-data.json 数组最前面插入新条目"""
    y, m, d = date_str.split("-")
    date_cn = f"{y}年{int(m)}月{int(d)}日"
    data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    new_item = {
        "issue": issue,
        "date": date_cn,
        "title": title,
        "summary": summary,
        "tags": ["政策", "产业", "趋势", "技术"],
        "filename": filename
    }
    data.insert(0, new_item)
    DATA_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8"
    )
    print(f"   ✅ news-data.json 已插入第{issue}期")


def git_commit(date_str: str, issue: int):
    """自动 commit，但不 push（让你 review 后再 push）"""
    msg = f"feat: 发布第{issue}期银发资讯 ({date_str})"
    subprocess.run(["git", "add", "-A"], cwd=ROOT, check=True)
    result = subprocess.run(
        ["git", "commit", "-m", msg],
        cwd=ROOT, capture_output=True, text=True
    )
    if result.returncode == 0:
        print(f"   ✅ 已 commit: {msg}")
    else:
        print(f"   ⚠️  commit 返回码 {result.returncode}（可能没新内容）")


def main():
    if len(sys.argv) < 2:
        fail("用法: python3 publish-issue.py <日期 YYYY-MM-DD> [期号]\n  例如: python3 publish-issue.py 2026-07-01 17")

    date_str = sys.argv[1]
    # 校验日期格式
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        fail(f"日期格式不对: {date_str}（应为 YYYY-MM-DD）")

    # 检查内容页是否存在
    content_path = NEWS_DIR / f"{date_str}.html"
    if not content_path.exists():
        fail(f"找不到内容页: {content_path}\n  请先把 {date_str}.html 放到 news/ 目录下")

    # 推断期号
    if len(sys.argv) >= 3:
        issue = int(sys.argv[2])
    else:
        issue = get_issue_number(date_str)
        print(f"   💡 推断期号: 第{issue}期（基于 news-data.json 现有最大值）")

    # 去重检查
    check_duplicates(date_str, issue)

    # 提取标题和摘要
    print(f"\n📰 准备发布第{issue}期 ({date_str})")
    title, summary = extract_title_and_summary(content_path)
    print(f"   标题: {title}")
    print(f"   摘要: {summary[:60]}...")

    # 依次更新 4 个文件
    print(f"\n🔧 开始更新文件...")
    filename = f"{date_str}.html"
    insert_to_news_html(date_str, issue, title, summary, filename)
    insert_to_index_news_grid(date_str, issue, summary)
    insert_to_index_sitemap(date_str, issue)
    update_news_data_json(date_str, issue, title, summary, filename)

    # 自动 commit
    print(f"\n📦 Git 操作...")
    git_commit(date_str, issue)

    print(f"\n🎉 完成！接下来你只需要:")
    print(f"   git push origin main")
    print(f"\n   30 秒后 GitHub Actions 会自动部署到 https://zhaoyuanbao.com")


if __name__ == "__main__":
    sys.exit(main())
