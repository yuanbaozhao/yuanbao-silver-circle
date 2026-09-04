(function () {
  document.querySelectorAll("body > header, body > footer").forEach((el) => el.remove());

  const page = document.body.dataset.page || "";
  const title = document.body.dataset.title || document.title.split("｜")[0];
  const parent = document.body.dataset.parent || "";
  const updated = document.body.dataset.updated || "2026-07-18";
  const nav = [
    ["index.html", "首页", "home"],
    ["news.html", "最新观察", "news"],
    ["reports.html", "研究资料", "reports"],
    ["companies.html", "产业案例", "companies"],
    ["services.html", "关于合作", "services"],
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
          : parent === "研究报告"
            ? "reports.html"
          : "index.html";

  const header = document.createElement("header");
  header.className = "yb-header yb-shell";
  header.innerHTML = `<div class="yb-header-inner"><a class="yb-brand" href="index.html"><strong>元宝的银发圈</strong><span>SILVER ECONOMY OBSERVATORY</span></a><nav class="yb-nav" id="yb-nav">${nav
    .map((n) => `<a href="${n[0]}" class="${page === n[2] ? "is-active" : ""}">${n[1]}</a>`)
    .join("")}</nav><a class="yb-search" href="services.html">联系</a><button class="yb-menu" id="yb-menu" aria-label="打开导航" aria-controls="yb-nav" aria-expanded="false">☰</button></div>`;
  document.body.insertBefore(header, document.body.firstChild);

  const menu = document.getElementById("yb-menu");
  const navEl = document.getElementById("yb-nav");
  menu.onclick = () => {
    const isOpen = navEl.classList.toggle("is-open");
    menu.setAttribute("aria-expanded", String(isOpen));
    menu.setAttribute("aria-label", isOpen ? "关闭导航" : "打开导航");
  };

  if (page !== "home") {
    const crumb = document.createElement("div");
    crumb.className = "yb-breadcrumb yb-shell";
    crumb.innerHTML = `<a href="index.html">首页</a><span>›</span>${parent ? `<a href="${parentUrl}">${parent}</a><span>›</span>` : ""}<b>${title}</b>`;
    header.insertAdjacentElement("afterend", crumb);
  }

  const footer = document.createElement("footer");
  footer.className = "yb-footer yb-shell";
  footer.innerHTML = `<div class="yb-footer-inner"><section><h3>元宝的银发圈</h3><p>记录变化，整理知识，连接实践。</p></section><section><h4>浏览内容</h4><p><a href="news.html">最新观察</a><br><a href="reports.html">研究资料</a><br><a href="companies.html">产业案例</a></p></section><section><h4>联系元宝</h4><p>微信：yuanbao0910<br>邮箱：yuanbao0910@163.com<br>公众号：神州养老研习社、银发神州</p></section></div><div class="yb-footer-bottom"><div><span>© 2026 元宝的银发圈 · zhaoyuanbao.com</span><span>最后更新：${updated}</span></div></div>`;
  document.body.appendChild(footer);
})();
