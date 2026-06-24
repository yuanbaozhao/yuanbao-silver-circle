#!/bin/bash
# health-check.sh — 网站健康检查 + 关键页面完整性监控
# 跑在 EasyClaw 服务器，不依赖宝总 Mac 网络
# Cron 任务：每 6 小时

set -e

REPO="/Users/zhaoyuanbao/.easyclaw/workspace/silver-circle"
LOG="/tmp/silver-circle-health.log"
ALERT_TO="ou_7b79f58ccf5918782242d7094b6c5428"
SITE="https://zhaoyuanbao.com"

echo "==================================" >> "$LOG"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 健康检查开始" >> "$LOG"

ERRORS=()
WARNINGS=()

# 1. 首页是否 200
HTTP_CODE=$(curl -sI -m 15 -o /dev/null -w "%{http_code}" "$SITE/?v=$RANDOM" 2>/dev/null || echo "000")
if [ "$HTTP_CODE" != "200" ]; then
  ERRORS+=("首页 HTTP 状态码异常: $HTTP_CODE（期望 200）")
fi
echo "✅ 首页 HTTP: $HTTP_CODE" >> "$LOG"

# 2. quotes.html 完整性
QUOTES_BLOCKQUOTES=$(curl -s -m 15 "$SITE/quotes.html?v=$RANDOM" | grep -o "<blockquote>" | wc -l | tr -d ' ')
if [ "$QUOTES_BLOCKQUOTES" != "28" ]; then
  ERRORS+=("quotes.html 语录数异常: $QUOTES_BLOCKQUOTES 条（期望 28 条）")
fi
echo "✅ quotes.html 语录数: $QUOTES_BLOCKQUOTES" >> "$LOG"

# 3. news.html 列表完整性（应有 news-data.json 那么多期）
NEWS_COUNT_HTML=$(curl -s -m 15 "$SITE/news.html?v=$RANDOM" | grep -c '<a class="index-item"' | tr -d ' ')
EXPECTED_COUNT=$(curl -s -m 15 "$SITE/news-data.json" | python3 -c "import json,sys; print(len(json.load(sys.stdin)))" 2>/dev/null || echo 0)
if [ "$NEWS_COUNT_HTML" != "$EXPECTED_COUNT" ]; then
  ERRORS+=("news.html 列表卡片数 $NEWS_COUNT_HTML 与 news-data.json 期数 $EXPECTED_COUNT 不一致")
fi
echo "✅ news.html 卡片数: $NEWS_COUNT_HTML (期望 $EXPECTED_COUNT)" >> "$LOG"

# 4. 4 个关键页面是否 200
for page in "index.html" "interviews.html" "quotes.html" "comic.html" "events.html"; do
  code=$(curl -sI -m 10 -o /dev/null -w "%{http_code}" "$SITE/$page?v=$RANDOM" 2>/dev/null || echo "000")
  if [ "$code" != "200" ]; then
    ERRORS+=("$page HTTP 状态码异常: $code")
  fi
  echo "✅ $page HTTP: $code" >> "$LOG"
done

# 5. 关键资源是否 200
for asset in "assets/site.css" "assets/avatar.png" "news-data.json"; do
  code=$(curl -sI -m 10 -o /dev/null -w "%{http_code}" "$SITE/$asset?v=$RANDOM" 2>/dev/null || echo "000")
  if [ "$code" != "200" ]; then
    ERRORS+=("$asset 资源不可访问: HTTP $code")
  fi
done

# 6. 首页是否包含关键模块（4 个内容卡片 + 资讯区）
HOMEPAGE=$(curl -s -m 15 "$SITE/index.html?v=$RANDOM")
for keyword in "人物专访" "银发资讯" "论坛峰会" "大咖语录" "site-counter" "wechat"; do
  if ! echo "$HOMEPAGE" | grep -q "$keyword"; then
    WARNINGS+=("首页缺少关键模块: $keyword")
  fi
done

# 报告
echo "" >> "$LOG"
if [ ${#ERRORS[@]} -gt 0 ]; then
  echo "❌ 发现 ${#ERRORS[@]} 个错误" >> "$LOG"
  for e in "${ERRORS[@]}"; do
    echo "  - $e" >> "$LOG"
  done

  # 发送飞书告警
  MSG="🚨 [网站健康检查告警] https://zhaoyuanbao.com\n\n发现 ${#ERRORS[@]} 个问题：\n"
  for e in "${ERRORS[@]}"; do
    MSG="$MSG\n• $e"
  done
  if [ ${#WARNINGS[@]} -gt 0 ]; then
    MSG="$MSG\n\n另外 ${#WARNINGS[@]} 个警告：\n"
    for w in "${WARNINGS[@]}"; do
      MSG="$MSG\n⚠️ $w"
    done
  fi
  MSG="$MSG\n\n详细日志：$LOG\n时间：$(date '+%Y-%m-%d %H:%M:%S')"

  echo "📨 告警内容: $MSG" >> "$LOG"
elif [ ${#WARNINGS[@]} -gt 0 ]; then
  echo "⚠️ 发现 ${#WARNINGS[@]} 个警告" >> "$LOG"
  for w in "${WARNINGS[@]}"; do
    echo "  - $w" >> "$LOG"
  done
else
  echo "✅ 一切正常" >> "$LOG"
fi

# 保留最近 100 行日志
tail -100 "$LOG" > "$LOG.tmp" && mv "$LOG.tmp" "$LOG"

echo "" >> "$LOG"
