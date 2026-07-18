(function () {
  document.querySelectorAll("body > header, body > footer").forEach((el) => el.remove());

  const page = document.body.dataset.page || "";
  const title = document.body.dataset.title || document.title.split("｜")[0];
  const parent = document.body.dataset.parent || "";
  const updated = document.body.dataset.updated || "2026-07-18";
  const nav = [
    ["index.html", "首页", "home"],
    ["news.html", "资讯", "news"],
    ["companies.html", "企业数据库", "companies"],
    ["wiki.html", "银发百科", "wiki"],
    ["knowledge-graph.html", "知识图谱", "graph"],
    ["data-center.html", "数据中心", "data"],
    ["topic-ltc.html", "专题研究", "topics"],
    ["services.html", "合作", "services"],
  ];
  const parentUrl =
    parent === "企业数据库"
      ? "companies.html"
      : parent === "银发百科"
        ? "wiki.html"
        : parent === "知识图谱"
          ? "knowledge-graph.html"
          : parent === "数据中心"
            ? "data-center.html"
            : "index.html";

  const header = document.createElement("header");
  header.className = "yb-header yb-shell";
  header.innerHTML = `<div class="yb-header-inner"><a class="yb-brand" href="index.html"><strong>元宝的银发圈</strong><span>SILVER ECONOMY KNOWLEDGE PLATFORM</span></a><nav class="yb-nav" id="yb-nav">${nav
    .map((n) => `<a href="${n[0]}" class="${page === n[2] ? "is-active" : ""}">${n[1]}</a>`)
    .join("")}</nav><a class="yb-search" href="index.html#site-search">搜索</a><button class="yb-menu" id="yb-menu" aria-label="打开导航">☰</button></div>`;
  document.body.insertBefore(header, document.body.firstChild);

  const menu = document.getElementById("yb-menu");
  const navEl = document.getElementById("yb-nav");
  menu.onclick = () => navEl.classList.toggle("is-open");

  if (page !== "home") {
    const crumb = document.createElement("div");
    crumb.className = "yb-breadcrumb yb-shell";
    crumb.innerHTML = `<a href="index.html">首页</a><span>›</span>${parent ? `<a href="${parentUrl}">${parent}</a><span>›</span>` : ""}<b>${title}</b>`;
    header.insertAdjacentElement("afterend", crumb);
  }

  const footer = document.createElement("footer");
  footer.className = "yb-footer yb-shell";
  footer.innerHTML = `<div class="yb-footer-inner"><section><h3>元宝的银发圈</h3><p>建立中国银发经济值得信赖的知识平台，持续连接政策、企业、人物、产品、数据与商业模式。</p></section><section><h4>知识入口</h4><p><a href="companies.html">企业数据库</a><br><a href="wiki.html">银发百科</a><br><a href="knowledge-graph.html">知识图谱</a><br><a href="data-center.html">数据中心</a></p></section><section><h4>内容与专题</h4><p><a href="news.html">银发资讯</a><br><a href="interviews.html">人物专访</a><br><a href="topic-ltc.html">专题研究</a><br><a href="events.html">论坛峰会</a></p></section><section><h4>联系宝总</h4><p>微信：yuanbao0910<br>邮箱：yuanbao0910@163.com<br>公众号：神州养老研习社、银发神州</p></section></div><div class="yb-footer-bottom"><div><span>© 2026 元宝的银发圈 · zhaoyuanbao.com</span><span>最后更新：${updated}</span></div></div>`;
  document.body.appendChild(footer);
})();
