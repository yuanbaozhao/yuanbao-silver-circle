#!/bin/bash
# deploy.sh — 保存更改 + 部署到 Vercel（生产环境）
# 用法: ./deploy.sh [提交说明]
set -e

cd /Users/zhaoyuanbao/.easyclaw/workspace/silver-circle

MSG="${1:-update}"
echo "📦 提交: $MSG"

git add -A
git commit -m "$MSG" 2>/dev/null || {
  echo "⚠️  没有新更改，跳过提交"
  echo "🚀 开始部署..."
}

echo "🚀 部署到 Vercel 生产环境..."
npx vercel --prod 2>&1

echo ""
echo "✅ 完成！访问 https://zhaoyuanbao.com"