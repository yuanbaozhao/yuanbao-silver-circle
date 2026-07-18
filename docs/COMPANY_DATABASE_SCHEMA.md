# 企业数据库数据规范

> 本规范用于“元宝的银发圈”企业数据库。目标不是制作企业黄页，而是建立来源可追溯、可持续更新、可与百科、人物、政策、产品和案例关联的银发经济企业知识库。

## 一、企业档案状态

- `Candidate`：已进入研究清单，尚未完成基本核验。
- `Draft`：已建立档案，部分字段仍待补充。
- `Reviewed`：企业主体、业务范围和关键事实已通过公开来源审校。
- `Verified`：关键事实完成多源交叉验证，可供研究报告与 AI 稳定调用。
- `Archived`：企业已停止相关业务、注销或档案不再维护，但保留历史记录。

## 二、核心字段

### 1. 身份信息

- `company_id`：唯一编号，如 `CO-CN-0001`
- `name_cn`：企业或品牌中文名
- `legal_name`：工商主体全称
- `name_en`：英文名（如有）
- `aliases`：曾用名、品牌名或常见简称
- `website`：官方网站
- `logo`：Logo 文件路径及版权来源
- `founded_at`：成立日期
- `headquarters`：总部城市
- `operating_regions`：主要经营地区
- `status`：经营状态

### 2. 分类与定位

- `primary_category`：一级分类
- `secondary_categories`：二级分类，可多选
- `business_model`：机构运营、平台、产品销售、订阅、保险支付、政府采购等
- `customer_segments`：个人、家庭、养老机构、医疗机构、政府、保险机构等
- `service_scenarios`：居家、社区、机构、医院、旅居地、线上等

### 3. 业务信息

- `summary`：一句话简介
- `description`：企业简介
- `core_businesses`：核心业务
- `products_services`：主要产品和服务
- `revenue_logic`：收入来源与付费方
- `delivery_model`：服务交付方式
- `scale_indicators`：公开披露的门店、床位、用户、城市、收入等数据

### 4. 组织与资本

- `founders`：创始人
- `key_people`：关键管理者
- `ownership`：股权或集团归属
- `financing`：融资事件
- `listing_status`：上市状态
- `investors`：公开投资方

### 5. 知识关联

- `wiki_entries`：关联 Silver Wiki 词条
- `people`：关联人物档案
- `policies`：关联政策
- `products`：关联产品
- `cases`：关联项目或案例
- `news`：关联资讯
- `competitors`：可比企业
- `partners`：公开合作伙伴

### 6. 元宝 AI 分析

- `problem_solved`：真正解决的问题
- `growth_logic`：成长逻辑
- `moat`：竞争壁垒
- `replicability`：模式可复制性
- `risks`：主要风险
- `industry_insight`：对行业的启发

### 7. 来源与版本

- `sources`：来源标题、发布机构、日期、URL、访问日期
- `fact_as_of`：事实有效日期
- `last_reviewed_at`：最近审校日期
- `reviewer`：审校者
- `change_log`：版本变更记录

## 三、一级分类

1. 养老服务
2. 医疗健康与照护
3. 智慧养老与 AI
4. 康复辅具与适老产品
5. 银发消费与生活方式
6. 银发旅居与文旅
7. 老年教育与文娱
8. 养老金融与保险
9. 人生后服务
10. 基础设施与产业服务

## 四、发布规则

- 没有明确来源的数字不进入正式档案。
- 品牌名称与工商主体必须区分。
- 集团业务与子品牌业务不得混写。
- 企业自述、媒体报道和监管披露应标明来源性质。
- 动态数据必须记录“截至日期”。
- “头部、领先、第一”等表述必须有可核验口径，否则不使用。
- 元宝 AI 分析必须与事实层分开呈现，并明确属于研究判断。

## 五、URL 规则

企业库入口：

`companies.html`

企业详情页：

`company-{slug}.html`

示例：

`company-example.html`
