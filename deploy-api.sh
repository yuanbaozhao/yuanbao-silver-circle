#!/bin/bash
# deploy-api.sh — 纯 API 部署到 Vercel（绕过 vercel.com 主站 / 绕过 Vercel CLI）
# 用法: ./deploy-api.sh "提交说明"
# 前提: 环境变量 VERCEL_TOKEN 已设置，或 ~/.vercel-token 文件存在

set -e

cd "$(dirname "$0")"

MSG="${1:-update}"
TOKEN_FILE="$HOME/.vercel-token"
PROJECT_ID="prj_w0dywV5fmtwPdn1szJrNTnYlVtJ6"
TEAM_ID="team_cmAEIQVjDeI6hOASENgW6uKw"
PROJECT_NAME="yuanbao-silver-circle"

# 1. 读取 token
if [ -z "$VERCEL_TOKEN" ] && [ -f "$TOKEN_FILE" ]; then
  export VERCEL_TOKEN=$(cat "$TOKEN_FILE")
fi
if [ -z "$VERCEL_TOKEN" ]; then
  echo "❌ 找不到 Vercel Token"
  echo "   请先把 token 放到 $TOKEN_FILE（chmod 600）"
  echo "   或者设置环境变量 VERCEL_TOKEN"
  exit 1
fi

# 2. Git 提交（如果有改动）
echo "📦 Git 提交: $MSG"
git add -A
git commit -m "$MSG" 2>/dev/null || echo "⚠️  没有新改动，跳过提交"

# 3. 打包网站（排除 .git .vercel deploy.sh 等）
echo "📦 打包网站文件..."
TMP_ZIP=$(mktemp -t silver-circle-deploy).zip
zip -rq "$TMP_ZIP" . \
  -x ".git/*" \
  -x ".vercel/*" \
  -x "deploy.sh" \
  -x "deploy-api.sh" \
  -x "node_modules/*" \
  -x ".DS_Store"
echo "   打包大小: $(du -h "$TMP_ZIP" | awk '{print $1}')"

# 4. 把 zip 转 base64（Vercel API 接受 base64）
echo "📤 编码 + 上传到 Vercel..."
B64=$(base64 -i "$TMP_ZIP")

# 5. 调 Vercel API 创建部署
RESPONSE=$(curl -s -X POST \
  "https://api.vercel.com/v13/deployments?teamId=${TEAM_ID}" \
  -H "Authorization: Bearer ${VERCEL_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{
    \"name\": \"${PROJECT_NAME}\",
    \"project\": \"${PROJECT_ID}\",
    \"target\": \"production\",
    \"files\": [
      {
        \"file\": \"deploy.zip\",
        \"data\": \"${B64}\"
      }
    ]
  }")

# 6. 解析结果
DEPLOY_URL=$(echo "$RESPONSE" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('url') or d.get('deployment',{}).get('url') or d.get('error',{}).get('message','未知错误'))" 2>/dev/null || echo "$RESPONSE" | head -c 300)
DEPLOY_ID=$(echo "$RESPONSE" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('id',''))" 2>/dev/null || echo "")

# 清理临时文件
rm -f "$TMP_ZIP"

echo ""
if [ -n "$DEPLOY_ID" ]; then
  echo "✅ 部署已提交！"
  echo "   部署 ID: $DEPLOY_ID"
  echo "   预览 URL: https://${DEPLOY_URL}"
  echo "   正式域名: https://zhaoyuanbao.com"
  echo "   查看状态: https://vercel.com/dashboard"
else
  echo "❌ 部署失败"
  echo "$RESPONSE" | head -c 500
  exit 1
fi
