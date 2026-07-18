# 更新记录

## 2026-07-18

### Project OS
- 在仓库建立 `docs/PROJECT.md`，作为项目唯一入口。
- 建立 `docs/SILVER_WIKI_SCHEMA.md`，统一百科词条结构、审核状态和 URL 规则。
- 建立并持续更新 `docs/ROADMAP.md`。
- 将企业数据库和知识图谱制度文件接入 Project OS。

### Silver Wiki 第一阶段
- 新增 `wiki.html`，上线 Silver Wiki 银发百科入口页 V1。
- 首批建立 12 个基础词条框架。
- 增加关键词搜索、分类筛选和 Draft、Reviewed、Verified 三级审核机制。

### Silver Wiki 第二阶段
- 建立统一的独立词条页面结构。
- 新增 `wiki-silver-economy.html`，完成“银发经济”Reviewed 词条。
- 新增 `wiki-escort-care.html`，完成“陪诊服务”Reviewed 词条。
- 新增 `wiki-silver-travel.html`，完成“银发旅居”Reviewed 词条。

### Silver Wiki 第三阶段
- 新增 `wiki-home-care.html`，完成“居家养老”Reviewed 词条。
- 新增 `wiki-community-care.html`，完成“社区养老”Reviewed 词条。
- 新增 `wiki-ltc-insurance.html`，完成“长期护理保险”Reviewed 动态政策词条。
- 长护险词条接入 2026 年国家制度文件来源，并明确地区政策差异和持续更新要求。
- 更新 `wiki.html`，正式详情页由 3 个增加至 6 个。
- 在百科体系导航中增加稳定的“银发百科”入口。

### 企业数据库 V1
- 建立 `docs/COMPANY_DATABASE_SCHEMA.md`，统一企业身份、业务、资本、关联、AI 分析、来源和版本字段。
- 建立 Candidate、Draft、Reviewed、Verified、Archived 五级企业档案状态。
- 新增 `companies.html`，上线银发企业数据库 V1 入口页。
- 增加企业关键词搜索、行业分类、地区和审核状态筛选框架。
- 建立养老服务、医疗健康、智慧养老与 AI、康复辅具、银发旅居、金融保险和人生后服务等分类入口。
- 明确未经核验的企业数据只进入研究队列，不直接作为正式企业档案发布。
- 新增 `company-template.html`，建立统一企业详情页模板。
- 模板形成企业概览、业务产品、商业模式、规模资本、元宝 AI 分析、知识图谱、来源版本七个标准模块。
- 模板明确区分已核验事实、待核验字段和研究判断。
- 新增 `docs/COMPANY_RESEARCH_LIST.md`，建立首批 30 个研究对象及升级任务卡。
- 确定泰康之家、福寿康、九如城为首批 Reviewed 档案候选。

### Knowledge Graph V1
- 新增 `docs/KNOWLEDGE_GRAPH.md`，统一节点类型、关系代码、证据等级、置信度、时间范围和审核状态。
- 明确事实关系与 AI 分析分层管理，禁止将推断写入事实关系。
- 建立企业、人物、政策、产品、案例、资讯、活动、地区和机构等节点模型。
- 建立创立、任职、赛道归属、产品提供、政策影响、合作、投资、竞争、报道和案例等关系模型。
- 新增 `data/knowledge-graph-v1.json`，形成首个机器可读图谱文件。
- 将银发经济、居家养老、社区养老、长期护理保险、陪诊服务和银发旅居登记为首批 Reviewed 图谱节点。
- 初始图谱暂不录入未经来源审校的企业关系。

### 下一步
- 对泰康之家、福寿康、九如城开展官方来源与多源事实审校。
- 完成首批 3 家 Reviewed 企业档案。
- 将真实企业档案接入 `companies.html`。
- 录入首批企业—百科—政策—人物关系，并保存证据与有效时间。
