/* Review Risk Agent -- shared core.
   Used by the homepage section (#agent) and the full tool page
   (work/fintech-review-insights/). Keep the dataset shape, the tool
   definitions and the system prompt in ONE place: both pages must
   answer from the same rules, and a change to either has to reach both.
   The page supplies its own elements, labels and styling. */
window.RA = (function () {
  "use strict";

  var APP = {momo:"MoMo", zalopay:"ZaloPay", shopeepay:"ShopeePay", viettelmoney:"Viettel Money"};
  var APPS = Object.keys(APP);
  var CAT = {TXN_FAILURE:"Transaction failure", AUTH_ACCESS:"Login & access", ONBOARD_EKYC:"Sign-up & identity",
    FRAUD_SECURITY:"Fraud & security", FEES_LIMITS:"Fees & limits", SUPPORT:"Customer support",
    PROMO_REWARDS:"Promotions", APP_EXPERIENCE:"App experience", NON_ISSUE:"Not an issue"};
  var FLOW = {transfer:"Transfer", payment:"Payment", topup_withdraw:"Top-up / withdraw / link",
    credit_bnpl:"Pay later", unknown:"Unclear"};
  var S1T = {unauthorized_debit:"Charged without agreeing", failed_txn_money_lost:"Transaction failed, money taken",
    refund_delay:"Refund never arrived", account_frozen:"Account frozen", account_takeover:"Account taken over",
    scam:"Tricked into paying", other:"Other"};
  var SEVN = {S1:"Money lost or at risk", S2:"Can't do a core job", S3:"Annoying but usable", S4:"Minor"};

  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c];
    });
  }
  function fold(s) {
    return String(s || "").toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "").replace(/\u0111/g, "d");
  }
  /* Keep only the filter keys a tool understands, as strings. The model
     can pass anything; everything else is dropped rather than trusted. */
  function clean(q) {
    var o = {}, ks = ["app","category","severity","flow","s1_type","keyword"];
    for (var i = 0; i < ks.length; i++) { if (q && q[ks[i]]) o[ks[i]] = String(q[ks[i]]); }
    return o;
  }
  function matcher(q) {
    var kw = q.keyword ? fold(q.keyword) : null;
    return function (r) {
      return (!q.app || r.app === q.app) && (!q.category || r.cat === q.category) &&
             (!q.severity || r.sev === q.severity) && (!q.flow || r.flow === q.flow) &&
             (!q.s1_type || r.s1 === q.s1_type) && (!kw || fold(r.text).indexOf(kw) >= 0);
    };
  }
  /* Weighted share with a Wilson interval on Kish's effective sample size:
     the corpus is a stratified sample, so an unweighted count would
     over-represent the low-star strata we deliberately oversampled. */
  function weighted(rs, pred) {
    var sw = rs.reduce(function (s, r) { return s + r.w; }, 0);
    var sw2 = rs.reduce(function (s, r) { return s + r.w * r.w; }, 0);
    if (!sw) return {share: null, n_base: 0};
    var p = rs.filter(pred).reduce(function (s, r) { return s + r.w; }, 0) / sw;
    var ne = sw * sw / sw2, z = 1.96, d = 1 + z * z / ne;
    var c = (p + z * z / (2 * ne)) / d;
    var h = z * Math.sqrt(p * (1 - p) / ne + z * z / (4 * ne * ne)) / d;
    return {share: +p.toFixed(3), ci95: [+Math.max(0, c - h).toFixed(3), +Math.min(1, c + h).toFixed(3)],
      n_matching: rs.filter(pred).length, n_base: rs.length};
  }

  function tools(D) {
    return [
      {name: "get_overview",
       description: "Headline numbers for all four wallets: complaint counts, the share of each problem type, how money is lost in S1 reviews, reply rate, reply speed, how much of the replies are boilerplate, and top priorities. Call this first for any broad question.",
       execute: function () {
         var S = D.summary, o = {period: D.period, findings: D.findings.items.map(function (f) { return f.title + " " + f.body; }), apps: {}};
         APPS.forEach(function (a) {
           var x = S.apps[a];
           o.apps[a] = {name: APP[a], complaints_in_sample: x.n_complaints,
             category_share: Object.keys(x.category_share).reduce(function (m, k) { m[k] = +x.category_share[k][0].toFixed(3); return m; }, {}),
             s1_mechanism_share: x.s1_type_share ? Object.keys(x.s1_type_share).reduce(function (m, k) { m[k] = +x.s1_type_share[k][0].toFixed(3); return m; }, {}) : null,
             reply_rate_all: x.reply_rate_all ? +x.reply_rate_all[0].toFixed(3) : null,
             reply_rate_S1: x.reply_rate_S1 ? +x.reply_rate_S1[0].toFixed(3) : null,
             reply_hours_median: x.reply_hours_all, boilerplate_share: x.reply_template_share,
             top_priorities: Object.keys(x.priority || {}).slice(0, 3)};
         });
         return o;
       }},
      {name: "compare_wallets",
       description: "For a filter, return each wallet's weighted share of complaints matching it, with a 95% confidence interval. Use this for any 'which wallet has more X' question.",
       inputSchema: {type: "object", properties: {
         category: {type: "string", enum: Object.keys(CAT)},
         severity: {type: "string", enum: ["S1","S2","S3","S4"]},
         flow: {type: "string", enum: Object.keys(FLOW)},
         s1_type: {type: "string", enum: Object.keys(S1T)},
         keyword: {type: "string", description: "Text to look for inside the review, diacritics-insensitive"}}},
       execute: function (q) {
         var f = clean(q), m = matcher(f), o = {filter: f, base: "complaints per wallet", apps: {}};
         APPS.forEach(function (a) {
           o.apps[a] = weighted(D.reviews.filter(function (r) { return r.app === a && r.cat !== "NON_ISSUE"; }), m);
         });
         return o;
       }},
      {name: "search_reviews",
       description: "Find individual reviews matching a filter. Returns up to `limit` (default 6, max 10) with id, wallet, date, stars, problem type, severity and text, plus how many matched in total. Use it to quote examples.",
       inputSchema: {type: "object", properties: {
         app: {type: "string", enum: APPS}, category: {type: "string", enum: Object.keys(CAT)},
         severity: {type: "string", enum: ["S1","S2","S3","S4"]}, flow: {type: "string", enum: Object.keys(FLOW)},
         s1_type: {type: "string", enum: Object.keys(S1T)}, keyword: {type: "string"},
         limit: {type: "integer", minimum: 1, maximum: 10}}},
       execute: function (q) {
         var f = clean(q), rs = D.reviews.filter(matcher(f));
         var lim = Math.min(10, Math.max(1, parseInt(q && q.limit, 10) || 6));
         var pick = rs.slice().sort(function (a, b) {
           return (b.sev === "S1") - (a.sev === "S1") || b.text.length - a.text.length;
         }).slice(0, lim);
         return {filter: f, total_matching: rs.length,
           sample_note: "This corpus holds every S1 review plus a sample of the rest, so use compare_wallets for shares, not these counts.",
           reviews: pick.map(function (r) {
             return {id: r.id, app: r.app, date: r.date, stars: r.stars, category: r.cat,
               severity: r.sev, s1_type: r.s1, text: r.text};
           })};
       }}
    ];
  }

  function sys(D, maxWords) {
    return 'You are the analyst for a dataset of Vietnamese e-wallet app reviews (momo, zalopay, shopeepay, viettelmoney) from ' + D.period + '. 2,339 reviews were classified by problem type, by severity (S1 money lost or at risk, S2 cannot do a core job, S3 annoying, S4 minor), and for S1 reviews by how the money was lost.\n' +
      'Rules:\n' +
      '- Always call a tool before stating any number. Never estimate or recall figures.\n' +
      '- Shares are weighted and computed WITHIN each wallet\'s complaints, never over all reviews.\n' +
      '- Cite individual reviews by id in square brackets exactly as the tool returns them, e.g. [gp_momo_00123].\n' +
      '- If fewer than about 20 reviews match, or the confidence interval is wide, say the result is uncertain.\n' +
      '- Never rank wallets overall as best or worst; speak only about specific problems. Never speculate about a company\'s internal reasons.\n' +
      '- If the data cannot answer (user numbers, revenue, market share, anything outside these reviews), say so plainly instead of guessing.\n' +
      '- Answer in at most ' + (maxWords || 120) + ' words, in the language the question was asked in. Use bullets for lists.';
  }

  /* Minimal markdown: bold, bullets, paragraphs. Review ids become buttons
     only when that id is actually in the loaded corpus, so a hallucinated
     citation stays visible as plain text instead of looking clickable. */
  function render(s, byId) {
    function inline(t) {
      return t.replace(/\*\*(.+?)\*\*/g, "<b>$1</b>")
        .replace(/\[(gp_[a-z]+_\d{5})\]/g, function (m, id) {
          return byId && byId[id] ? '<button type="button" class="cite" data-id="' + id + '">' + id + '</button>' : m;
        });
    }
    var out = [], ul = false;
    esc(s).split("\n").forEach(function (ln) {
      var li = ln.match(/^\s*[-*\u2022]\s+(.*)/);
      if (li) { if (!ul) { out.push("<ul>"); ul = true; } out.push("<li>" + inline(li[1]) + "</li>"); return; }
      if (ul) { out.push("</ul>"); ul = false; }
      if (ln.trim()) out.push("<p>" + inline(ln) + "</p>");
    });
    if (ul) out.push("</ul>");
    return out.join("");
  }

  var dataPromise = null;
  function load(url) {
    if (!dataPromise) {
      dataPromise = fetch(url).then(function (r) {
        if (!r.ok) throw new Error("http " + r.status);
        return r.json();
      });
    }
    return dataPromise;
  }

  var OFF_CODES = ["not_granted","sampling_disabled","capability_disabled","not_declared","tools_unavailable"];
  var ERRS = {cancelled: "Stopped.", rate_limited: "Too many requests \u2014 try again shortly.",
    session_expired: "Your Claude session expired; sign in again.",
    prompt_too_large: "This conversation got too long \u2014 reload the page."};

  /* Wire a chat onto a page's own elements.
     o: {els:{form,input,send,log,chips}, getSample, getData, getById,
         modelTier, maxWords, offMessage, onOff} */
  function chat(o) {
    var els = o.els, turns = [], ctl = null;

    function addMsg(role, html) {
      var d = document.createElement("div");
      d.className = "msg " + role;
      d.innerHTML = html;
      els.log.append(d);
      d.scrollIntoView({block: "nearest", behavior: "smooth"});
      return d;
    }
    function busy(b) {
      if (els.send) els.send.disabled = b;
      if (els.input) els.input.disabled = b;
      if (els.chips) els.chips.querySelectorAll(".chip").forEach(function (c) { c.disabled = b; });
    }
    function off(msg) {
      els.log.innerHTML = '<div class="off">' + esc(msg) + "</div>";
      if (els.form) els.form.hidden = true;
      if (els.chips) els.chips.hidden = true;
      if (o.onOff) o.onOff(msg);
    }

    async function ask(question) {
      var sample = o.getSample(), D = o.getData();
      if (!sample || !D || !question.trim()) return;
      var byId = o.getById ? o.getById() : {};
      addMsg("user", esc(question));
      var bot = addMsg("bot", "<p>Thinking\u2026</p>");
      var det = document.createElement("details");
      det.className = "calls";
      var sum = document.createElement("summary"), pre = document.createElement("pre");
      det.append(sum, pre);
      var nCalls = 0;
      turns.push({role: "user", content: question});
      var recent = turns.slice(-7);
      if (recent[0].role !== "user") recent.shift();
      ctl = new AbortController();
      busy(true);
      /* Wrap each tool so the page can show what the agent actually called --
         the claim "it answers from the data" is only checkable if the calls
         are on screen. */
      var traced = tools(D).map(function (t) {
        return {name: t.name, description: t.description, inputSchema: t.inputSchema,
          execute: function (inp, c) {
            nCalls++;
            pre.textContent += t.name + "(" + JSON.stringify(clean(inp)) + ")\n";
            sum.textContent = nCalls + (nCalls === 1 ? " tool call" : " tool calls");
            if (!det.isConnected) bot.append(det);
            return t.execute(inp, c);
          }};
      });
      try {
        var r = await sample([{role: "user", content: sys(D, o.maxWords)}].concat(recent), {
          tools: traced, signal: ctl.signal, modelTier: o.modelTier || "quick",
          onText: function (u) { bot.innerHTML = render(u.text, byId); if (nCalls) bot.append(det); }
        });
        bot.innerHTML = render(r.text, byId);
        if (nCalls) bot.append(det);
        turns.push({role: "assistant", content: r.text});
      } catch (e) {
        var code = e && e.code;
        if (OFF_CODES.indexOf(code) >= 0) {
          bot.remove();
          off(o.offMessage || "This agent runs on your own Claude account, which isn\u2019t available in this view.");
        } else {
          bot.innerHTML = (e && e.text ? render(e.text, byId) : "") +
            '<p class="err">' + esc(ERRS[code] || "Connection problem. Try asking again.") + "</p>";
        }
        turns.pop();
      } finally { busy(false); }
    }

    return {ask: ask, off: off, busy: busy};
  }

  return {APP: APP, APPS: APPS, CAT: CAT, FLOW: FLOW, S1T: S1T, SEVN: SEVN,
    esc: esc, fold: fold, clean: clean, matcher: matcher, weighted: weighted,
    tools: tools, sys: sys, render: render, load: load, chat: chat};
})();
