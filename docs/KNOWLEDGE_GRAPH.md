# 元宝的银发圈 Knowledge Graph V1

> 本文件定义 Silver Wiki、企业、人物、政策、产品、案例、活动与资讯之间的统一关联规则。所有关系必须可追溯、可解释、可更新；不得把推测包装为事实。

## 一、建设目标

知识图谱不是单独的可视化页面，而是全站数据之间的底层连接协议，用于：

1. 支持用户从一个词条继续探索企业、人物、政策和案例；
2. 支持企业档案展示所属赛道、关键人物、政策环境与竞争关系；
3. 为搜索、推荐、研究报告和 AI 问答提供结构化上下文；
4. 保留每条关系的证据来源、时间范围和审核状态。

## 二、节点类型（Node Types）

| 类型代码 | 中文名称 | 示例 | 推荐 ID 前缀 |
|---|---|---|---|
| WIKI | 百科词条 | 居家养老、长期护理保险 | wiki_ |
| COMPANY | 企业 | 养老服务企业、科技企业 | company_ |
| PERSON | 人物 | 创始人、管理者、专家 | person_ |
| POLICY | 政策 | 国家意见、地方实施办法 | policy_ |
| PRODUCT | 产品或服务 | 陪诊服务、智能设备 | product_ |
| CASE | 案例 | 社区养老项目、适老化案例 | case_ |
| NEWS | 资讯 | 企业动态、政策新闻 | news_ |
| EVENT | 活动 | 展会、论坛、赛事 | event_ |
| REGION | 地区 | 国家、省、市、区县 | region_ |
| ORGANIZATION | 机构 | 协会、院校、研究机构 | org_ |
| INVESTMENT | 投融资事件 | 融资、并购、战略投资 | investment_ |

每个节点至少包含：

```json
{
  "id": "company_example",
  "type": "COMPANY",
  "name": "示例企业",
  "url": "company-example.html",
  "status": "Draft",
  "updated_at": "2026-07-18"
}
```

## 三、关系类型（Edge Types）

### 1. 人物与组织关系

| 关系代码 | 中文含义 | 方向示例 |
|---|---|---|
| FOUNDED_BY | 由某人创立 | 企业 → 人物 |
| MANAGED_BY | 由某人管理 | 企业 → 人物 |
| WORKS_FOR | 任职于 | 人物 → 企业或机构 |
| ADVISED_BY | 获得顾问支持 | 企业 → 人物 |

### 2. 行业与业务关系

| 关系代码 | 中文含义 | 方向示例 |
|---|---|---|
| BELONGS_TO | 属于某赛道或概念 | 企业 → 百科词条 |
| PROVIDES | 提供产品或服务 | 企业 → 产品 |
| SERVES | 服务某类人群或场景 | 企业或产品 → 百科词条 |
| OPERATES_IN | 在某地区运营 | 企业或项目 → 地区 |
| APPLIES_TO | 适用于 | 政策或产品 → 人群、场景或地区 |

### 3. 政策与证据关系

| 关系代码 | 中文含义 | 方向示例 |
|---|---|---|
| GOVERNED_BY | 受某政策规范 | 企业、产品或服务 → 政策 |
| SUPPORTS | 政策支持某领域 | 政策 → 百科词条或产业 |
| RESTRICTS | 政策限制或设置边界 | 政策 → 企业、产品或行为 |
| REFERENCES | 引用或提及 | 页面或研究 → 来源节点 |
| EVIDENCED_BY | 由某来源证明 | 关系或判断 → 新闻、政策、公告 |

### 4. 市场关系

| 关系代码 | 中文含义 | 方向示例 |
|---|---|---|
| PARTNERS_WITH | 合作关系 | 企业 ↔ 企业或机构 |
| INVESTED_IN | 投资关系 | 企业或机构 → 企业 |
| ACQUIRED | 并购关系 | 企业 → 企业 |
| COMPETES_WITH | 竞争关系 | 企业 ↔ 企业 |
| SUPPLIES_TO | 供应关系 | 企业 → 企业或项目 |
| CUSTOMER_OF | 客户关系 | 企业或机构 → 企业 |

### 5. 内容与知识关系

| 关系代码 | 中文含义 | 方向示例 |
|---|---|---|
| RELATED_TO | 一般关联 | 任意节点 ↔ 任意节点 |
| EXPLAINS | 内容解释某对象 | 百科词条或报告 → 节点 |
| REPORTS_ON | 资讯报道某对象 | 资讯 → 企业、人物、政策 |
| PARTICIPATED_IN | 参与活动 | 企业或人物 → 活动 |
| CASE_OF | 是某概念的案例 | 案例 → 百科词条 |
| PRECEDES | 时间上先于 | 政策、事件或版本 → 后续节点 |

## 四、关系数据结构

每条关系必须独立记录，不允许只在正文中用自然语言暗示。

```json
{
  "id": "edge_company_example_belongs_to_home_care",
  "source": "company_example",
  "relation": "BELONGS_TO",
  "target": "wiki_home_care",
  "direction": "directed",
  "status": "Reviewed",
  "confidence": "high",
  "valid_from": "2025-01-01",
  "valid_to": null,
  "evidence": [
    {
      "title": "企业官网业务介绍",
      "url": "https://example.com",
      "published_at": null,
      "accessed_at": "2026-07-18"
    }
  ],
  "note": "企业官网明确将居家养老列为核心业务。",
  "updated_at": "2026-07-18"
}
```

## 五、证据与可信度

### 证据等级

- **A 级**：法律法规、政府文件、交易所公告、企业正式公告、工商或司法公开信息。
- **B 级**：企业官网、官方公众号、权威行业机构、主流媒体直接采访。
- **C 级**：研究报告、会议材料、专业媒体二手报道。
- **D 级**：自媒体、营销材料、未经独立核验的转载，仅可作为线索。

### 置信度

- **high**：至少一个 A 级来源，或两个相互独立的 B 级来源。
- **medium**：一个可靠 B 级来源，或多个一致的 C 级来源。
- **low**：仅有线索性来源，必须标注“待核验”，不得用于确定性结论。

## 六、关系审核状态

- **Candidate**：发现可能关系，尚未录入正式证据。
- **Draft**：已录入来源，但尚未完成交叉核验。
- **Reviewed**：关系定义、方向、时间和来源已审校，可在网页展示。
- **Verified**：完成多源验证，可用于研究报告、榜单和 AI 稳定调用。
- **Expired**：关系曾经成立，但已经终止或超过有效期。
- **Disputed**：可靠来源之间存在冲突，必须展示争议说明。

节点状态与关系状态分别管理。一家 Verified 企业不代表其所有关系都已 Verified。

## 七、关系时间规则

以下关系必须设置时间范围：

- 任职、管理、合作、投资、客户、供应、竞争、政策适用和运营地区；
- 企业名称变更、品牌归属和并购关系；
- 会随业务调整而改变的赛道归属。

无法确认开始日期时，可以只记录年份或设置 `date_precision`。禁止用当前关系倒推历史关系。

## 八、双向展示规则

数据库可存储单向关系，但页面必须根据关系生成合理的反向阅读：

- 企业 `BELONGS_TO` 居家养老 → 居家养老词条显示“相关企业”；
- 企业 `PROVIDES` 某产品 → 产品页显示“提供企业”；
- 企业 `FOUNDED_BY` 某人物 → 人物页显示“创立企业”；
- 企业 `GOVERNED_BY` 某政策 → 政策页显示“影响对象”；
- 资讯 `REPORTS_ON` 某企业 → 企业页显示“相关动态”。

反向文案不等于新增一条独立事实关系，避免重复维护。

## 九、页面最低关联字段

### Silver Wiki 词条

- related_companies
- related_policies
- related_products
- related_cases
- related_people
- related_news

### 企业档案

- founders_and_leaders
- industry_topics
- products_and_services
- operating_regions
- related_policies
- partners
- competitors
- investment_events
- related_news
- evidence_sources

### 政策档案

- issuing_authority
- applicable_regions
- affected_topics
- affected_companies
- implementation_cases
- related_news

## 十、编辑红线

1. 不以“行业普遍认为”代替来源。
2. 不把品牌宣传语直接转化为竞争优势结论。
3. 不把同赛道企业自动标为直接竞争对手。
4. 不把一次活动同台视为合作关系。
5. 不把媒体推测视为投资、并购或任职事实。
6. 涉及负面事件、司法、财务和经营风险时，必须保留原始来源、日期和主体回应。
7. AI 推断只能作为 `analysis` 字段，不得写入事实关系。

## 十一、V1 实施顺序

1. 为六个 Reviewed Silver Wiki 词条补充关联字段。
2. 建立企业详情页模板并嵌入关系卡片。
3. 为首批三家 Reviewed 企业录入百科、人物、政策、地区和资讯关系。
4. 建立 `data/knowledge-graph-v1.json` 作为初始机器可读文件。
5. 上线关系图谱可视化页面前，先验证移动端性能与可访问性。
6. 后续再接入人物库、政策库、产品库和 AI 检索。

## 十二、版本信息

- 版本：V1.0
- 建立日期：2026-07-18
- 维护项目：元宝的银发圈
- 适用范围：Silver Wiki、企业数据库及后续人物、政策、产品、案例与资讯数据库
