# 更新记录

## 2026-07-18

### Project OS
- 在仓库建立 `docs/PROJECT.md`，作为项目唯一入口。
- 建立 `docs/SILVER_WIKI_SCHEMA.md`，统一百科词条结构、审核状态和 URL 规则。
- 建立并持续更新 `docs/ROADMAP.md`。
- 将企业数据库和知识图谱制度文件接入 Project OS。

### Silver Wiki
- 新增 `wiki.html`，上线 Silver Wiki 银发百科入口页 V1。
- 建立 12 个基础词条框架及搜索、分类和审核机制。
- 完成银发经济、陪诊服务、银发旅居、居家养老、社区养老、长期护理保险 6 个 Reviewed 词条。
- 长护险词条接入 2026 年国家制度文件来源，并明确地区政策差异和持续更新要求。

### 企业数据库 V1
- 建立 `docs/COMPANY_DATABASE_SCHEMA.md`，统一企业身份、业务、资本、关联、AI 分析、来源和版本字段。
- 建立 Candidate、Draft、Reviewed、Verified、Archived 五级企业档案状态。
- 新增 `companies.html`，上线企业关键词搜索、行业分类、地区和审核状态筛选。
- 新增 `company-template.html` 和 `docs/COMPANY_RESEARCH_LIST.md`。
- 完成泰康之家、福寿康、九如城三家 Reviewed 标杆案例。
- 三家案例统一增加发展时间轴、商业模式、价值链、规模口径、SWOT、国内外对标、AI 重构空间和《宝总点评》。
- 将 `companies.html` 从模板研究队列升级为三家真实案例入口。

### Knowledge Graph V1
- 新增 `docs/KNOWLEDGE_GRAPH.md`，统一节点类型、关系代码、证据等级、置信度、时间范围和审核状态。
- 新增 `data/knowledge-graph-v1.json`，形成机器可读图谱文件。
- 将六个 Reviewed 百科词条及泰康之家、福寿康、九如城登记为图谱节点。
- 录入首批企业—百科—政策与服务模式关系。
- 新增 `knowledge-graph.html`，上线可点击、可筛选的交互式知识图谱 V1。

### 部署检查
- 主域名 `zhaoyuanbao.com` 可正常访问，现有首页加载 Vercel Analytics，表明网站使用 Vercel 托管或分析链路。
- GitHub 仓库未发现 GitHub Actions 部署工作流，提交也未返回 GitHub 状态检查；线上发布依赖现有 Vercel 与 GitHub 主分支的自动部署配置。
- 新增页面已提交至 `main` 分支，待通过线上 URL 继续核验自动部署结果。
- 2026-07-18 再次提交部署触发记录，用于重新触发生产环境自动部署。

### 下一步
- 将银发百科、企业库和知识图谱入口正式接入首页主导航及首页内容区。
- 统一所有二级页面导航。
- 开始第二批企业案例：椿萱茂、亲和源、乐成养老等。
