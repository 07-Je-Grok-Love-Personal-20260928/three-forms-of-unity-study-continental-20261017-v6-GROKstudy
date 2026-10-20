# -*- coding: utf-8 -*-
"""v8/v11 笔记标记系统（两站共用，构建后处理）。
只处理“讲解/深读”文字；不碰：CCI 逐字原文（原文库页、背诵行、引号内文字）、链接、标题、SVG、表头、脚注、目录。
标记：
  mk-k  关键术语：加粗 + 按教义领域着色（d-god 神/父 · d-chr 基督 · d-sp 圣灵 · d-sal 救恩 · d-cov 圣约 · d-ch 教会圣礼）
  mk-hl 必背：荧光底（CSS 加在“核心一句”“本页一眼·核心”“宣信必背”上）
  mk-u  重点：实线下划线（“而是……”的正面陈述、重点框里的加粗）
  mk-x  难点/易错：波浪下划线（“不是……”的否定陈述、异端名、难点框里的加粗）
  mk-ref 经文：独立颜色
  定义框 mkdefs、应用侧栏 mk-app、记忆钉 ①②③（CSS 计数器）
全部可由图例里的开关关闭（html.mkoff），设置存于本机浏览器。"""
import re, json, os, html as H

BOOKS = "创 出 利 民 申 书 士 得 撒上 撒下 王上 王下 代上 代下 拉 尼 斯 伯 诗 箴 传 歌 赛 耶 哀 结 但 何 珥 摩 俄 拿 弥 鸿 哈 番 该 亚 玛 太 可 路 约 徒 罗 林前 林后 加 弗 腓 西 帖前 帖后 提前 提后 多 门 来 雅 彼前 彼后 约壹 约贰 约叁 犹 启".split()
BOOKS.sort(key=len, reverse=True)
REF = re.compile(r'(?<![\u4e00-\u9fff])(?:' + "|".join(BOOKS) + r')\s?\d{1,3}[:：]\d{1,3}(?:[\-–—]\d{1,3})?(?:[,，、]\s?\d{1,3}(?:[\-–]\d{1,3})?)*')

# 术语 → 领域；定义为本站用语（非引文）
G = [
 ("三位一体","d-god","独一的神，在本质上为一，在位格上为三：父、子、圣灵同等、同永恒。"),
 ("同质","d-god","子与父同一本质（homoousios），不是相似，也不是受造。尼西亚的关键词。"),
 ("位格","d-god","父、子、圣灵各自的“谁”；三个位格共享一个神的本质，彼此不混淆。"),
 ("护理","d-god","神以全能维持并管理万有，使万事都在祂的旨意之下；信徒因此可以安心。"),
 ("创造","d-god","父借着子、在圣灵里从无中造出万有；受造界本为美善。"),
 ("道成肉身","d-chr","永恒的子取了真人性，成为一位有神性也有人性的基督，为要作中保。"),
 ("二性一位","d-chr","基督是一个位格，有完全的神性与完全的人性；二性不混合、不改变、不分开、不离散。"),
 ("中保","d-chr","站在神与人之间、使两方和好的那一位；唯有既是真神又是真人的基督能当。"),
 ("代赎","d-chr","基督替选民承受罪的刑罚，满足神的公义；救恩的法律根基。"),
 ("降在阴间","d-chr","改革宗读法（HC 44）：基督在十字架上承受了地狱般的痛苦与被弃；不是到地狱再传一次福音。"),
 ("圣灵","d-sp","三一第三位格，与父子同受敬拜；把基督的一切好处实际地给到我们。"),
 ("重生","d-sp","圣灵使死在罪中的人得着新生命，是信心的源头，人无法自己发动。"),
 ("成圣","d-sp","圣灵一生持续更新信徒，使其越来越像基督；与称义相连而不相混。"),
 ("称义","d-sal","神因基督的义（不是因我们的行为）宣告罪人为义；唯独借着信心领受。"),
 ("拣选","d-sal","神在创世以前，在基督里、出于白白的恩典，定意拯救一群特定的人。"),
 ("弃绝","d-sal","神按公义任凭其余的人留在自己所选的罪中并为罪受罚；罪责在人。"),
 ("全然败坏","d-sal","堕落影响人的每一部分，人凭自己既不愿也不能转向神；不是说人坏到极点。"),
 ("原罪","d-sal","因亚当的堕落，全人类与生俱来带着罪债与败坏的本性。"),
 ("恩典","d-sal","神白白赐下、人不配得的好处；救恩从头到尾都是恩典。"),
 ("唯独信心","d-sal","信心是领受基督的手，不是挣得救恩的功劳。"),
 ("安慰","d-sal","HC 的主轴：我不属于自己，而属于基督——生死都有的确据，不是一种情绪。"),
 ("感恩","d-sal","HC 第三部：得救的人以顺服、祷告与好行为回应神；好行为是果子，不是根。"),
 ("圣徒蒙保守","d-sal","神必保守真信徒到底；他们会跌倒，但不会全然、最终地失落救恩。"),
 ("恩典之约","d-cov","神在基督里与信徒及其儿女所立的约：神应许作他们的神，并要求信心与顺服。"),
 ("行为之约","d-cov","改革宗传统对神与亚当在堕落前关系的概括（后世用语，CCI 三项联合信条只在 Dort 2 错谬中提到一次）。"),
 ("圣约","d-cov","神主动与人建立的关系，带着应许、要求与记号；串起整本圣经的主线。"),
 ("教会","d-ch","神从全人类中召聚、保守的信徒群体；以纯正讲道、圣礼与劝惩为标志。"),
 ("圣礼","d-ch","神设立的可见记号与印记，把福音的应许印在信徒身上：洗礼与圣餐。"),
 ("洗礼","d-ch","进入恩典之约的记号与印记；改革宗也给信徒的儿女施洗。"),
 ("圣餐","d-ch","基督吩咐的纪念与喂养：借着圣灵，信徒真实地与基督相交。"),
 ("大公","d-ch","普世的、历代的：不限于一时一地的基督教会，并非指罗马天主教。"),
 ("律法","d-ch","神的诫命：先照出罪（引到基督），再作感恩生活的规范。"),
]
TERM = {t: c for t, c, _ in G}; DEF = {t: d for t, _, d in G}
TERM_RE = re.compile("|".join(sorted(map(re.escape, TERM), key=len, reverse=True)))
HERESY = ["阿里乌派","阿里乌","撒伯里乌","撒伯流","聂斯脱利","欧迪奇","伯拉纠主义","伯拉纠","半伯拉纠","抗辩派","阿民念派","次位论","嗣子论","形态论"]
HER_RE = re.compile("|".join(sorted(map(re.escape, HERESY), key=len, reverse=True)))
NEG = re.compile(r'((?:不是|并非|不在于|不靠|不凭)[^，。；！？“”<>（）\s]{2,22})([，,；]\s?)((?:而是|乃是|而在于|而靠|是)[^，。；！？“”<>（）]{2,26})')

NEG2 = re.compile(r'(?:(?<=[。；：，、])|^)([^，。；：！？“”<>（）\s]{2,18})([，,]\s?)((?:不是|而不是|并非)[^，。；！？“”<>（）]{2,18})')

VOID = {"br","img","input","meta","link","hr","wbr","source","col","area","base","embed","param","track"}
PROT_TAG = {"a","svg","script","style","h1","h2","h3","h4","h5","h6","button","summary","th","code","select","option","label","q","textarea","b","strong","sup","small","nav","title","i"}
PROT_CLS = re.compile(r'\b(rls|rart|rt|cl|verses|zh|refs2|rf1|kw|cwcs|cwc|own|ptabs|l3m|pager|foot|mklegend|mkdefs|pdfq|pdfsrc|lb|tg|chip|kchip|hchip|ychip|pch|qr|n3|readchip|secbar|stats|hero|fnh|nb|xq|cciq|cq|quote|vq|lbl|tw-no)\b')

def _segs(t, st):
    segs = []; cur = ""; q = st["q"]
    for ch in t:
        if not q and ch == "“": segs.append((cur, False)); cur = ch; q = True
        elif q and ch == "”": segs.append((cur + ch, True)); cur = ""; q = False
        else: cur += ch
    segs.append((cur, q)); st["q"] = q
    return segs

def _mark_plain(seg, st):
    s = NEG.sub(lambda m: (st.__setitem__("nneg", st["nneg"]+1) or f'<span class="mk-x">{m.group(1)}</span>{m.group(2)}<span class="mk-u">{m.group(3)}</span>'), seg) if st["neg"] else seg
    if st["neg"]:
        s = NEG2.sub(lambda m: (st.__setitem__("nneg", st["nneg"]+1) or f'<span class="mk-u">{m.group(1)}</span>{m.group(2)}<span class="mk-x">{m.group(3)}</span>') if 'mk-' not in m.group(0) else m.group(0), s)
    res = []
    for p in re.split(r'(<[^>]+>)', s):
        if p.startswith("<"): res.append(p); continue
        def ref(m):
            st["nref"] += 1; return f'<span class="mk-ref">{m.group(0)}</span>'
        p = REF.sub(ref, p)
        def term(m):
            w = m.group(0)
            if w in st["seen"]: return w
            st["seen"].add(w); st["nk"] += 1
            return f'<b class="mk-k {TERM[w]}">{w}</b>'
        def her(m):
            w = m.group(0)
            if ("h:" + w) in st["seen"]: return w
            st["seen"].add("h:" + w); st["nx"] += 1
            return f'<span class="mk-x">{w}</span>'
        sub = re.split(r'(<span class="mk-ref">[^<]*</span>)', p)
        res.append("".join(x if x.startswith("<") else HER_RE.sub(her, TERM_RE.sub(term, x)) for x in sub))
    return "".join(res)

def _mark_text(t, st):
    # 引号内（多为 CCI 原文）保持原样；引号状态跨文本节点延续，块级元素结束时复位
    return "".join(seg if prot else _mark_plain(seg, st) for seg, prot in _segs(t, st) if seg)

def mark(h, neg=True):
    """对 <main> 内的讲解文字加标记。返回 (html, stats)。"""
    i = h.find('<main'); j = h.rfind('</main>')
    if i < 0: return h, {}
    head, body, tail = h[:i], h[i:j], h[j:]
    st = {"seen": set(), "nk": 0, "nx": 0, "nref": 0, "nneg": 0, "q": False, "neg": neg}
    stack = []; prot = 0; out = []
    for tok in re.split(r'(<[^>]+>)', body):
        if not tok: continue
        if tok.startswith("<"):
            m = re.match(r'<(/?)([a-zA-Z0-9]+)([^>]*)>', tok)
            if not m: out.append(tok); continue
            close, tag, attrs = m.group(1), m.group(2).lower(), m.group(3)
            if close:
                if tag in ("p","li","div","td","dd","section","blockquote"): st["q"] = False
                while stack:
                    t, p = stack.pop()
                    if p: prot -= 1
                    if t == tag: break
            elif tag not in VOID and not attrs.rstrip().endswith("/"):
                cls = re.search(r'class="([^"]*)"', attrs)
                p = tag in PROT_TAG or bool(cls and PROT_CLS.search(cls.group(1)))
                if tag == "section": st["seen"] = set()
                stack.append((tag, p)); prot += p
            out.append(tok)
        else:
            out.append(tok if prot else _mark_text(tok, st))
    body = "".join(out)
    # 应用侧栏：<p class="k"><i class="lb">应用</i> 与 call app
    body = re.sub(r'<p class="([^"]*)"><i class="lb">应用</i>', lambda m: f'<p class="{m.group(1)} mk-app"><i class="lb">应用</i>', body)
    return head + body + tail, {k: v for k, v in st.items() if k in ("nk", "nx", "nref", "nneg")}

def defs(h, n=6):
    t = re.sub(r'<[^>]+>', '', h)
    cnt = sorted(((t.count(w), w) for w in TERM if t.count(w) >= 2), reverse=True)[:n]
    if not cnt: return ""
    items = "".join(f'<div class="mkdef {TERM[w]}"><dt>{w}</dt><dd>{DEF[w]}</dd></div>' for _, w in cnt)
    return f'<details class="mkdefs" open><summary>📘 本页关键词定义 <small>本站用语 · 按本页出现次数排序</small></summary><dl class="mkdl">{items}</dl></details>'

LEGEND = ('<div class="mklegend" role="note" aria-label="笔记标记图例"><b class="mkl-t">🖍 标记图例</b>'
 '<span class="mk-k d-chr">关键术语</span><span class="mk-hl">必背</span><span class="mk-u">重点（正面陈述）</span>'
 '<span class="mk-x">难点·易错·异端</span><span class="mk-ref">罗3:24</span><span class="lg lg-def">定义框</span><span class="lg lg-app">应用侧栏</span><span class="lg lg-peg"><i>1</i>记忆钉</span>'
 '<span class="lgc"><i class="d-god">神/父</i><i class="d-chr">基督</i><i class="d-sp">圣灵</i><i class="d-sal">救恩</i><i class="d-cov">圣约</i><i class="d-ch">教会</i></span>'
 '<button type="button" class="btn ghost mktog" data-mktog aria-pressed="true">标记：开</button></div>')

QTITLE = {"own": "本站用语，不是引文", "tr": "本站译文或其他中文译本的措辞，不是 CCI 逐字原文"}
def qfix(h, table):
    """把未在 CCI/参考站/手册找到的引号短语改为带说明的虚线标注（去掉引号）。"""
    hit = {}
    def f(m):
        x = m.group(1)
        if x in table:
            a = table[x]["act"]; a = "tr" if a == "cci" else a
            hit[x] = hit.get(x, 0) + 1
            return f'<span class="own{" tr" if a=="tr" else ""}" title="{QTITLE[a]}">{x}</span>'
        return m.group(0)
    return re.sub(r'“([^”]{4,120})”', f, h), hit

def vis_text_len(h):
    h = re.sub(r'(?s)<(script|style|svg|nav)[^>]*>.*?</\1>', '', h); h = re.sub(r'<[^>]+>', '', h)
    return len(re.sub(r'\s', '', H.unescape(h)))

def apply(h, deep=True, recite=False):
    """整页后处理：深读页加标记、图例、定义框；背诵页只加纯视觉的分段着色。"""
    stats = {}
    if deep:
        h, stats = mark(h)
        m = re.search(r'<nav class="ptabs".*?</nav>', h)
        if m:
            sb = re.search(r'<div class="secbar">.*?</div>', h[m.end():m.end()+2000])
            at = m.end() + (sb.end() if sb and sb.start() < 400 else 0)
            mi = h.find('<main'); body = h[mi:]
            h = h[:at] + LEGEND + h[at:]
            dfs = defs(body)
            hm = re.search(r'<header class="l1h[^"]*">.*?</header>', h[at:], re.S)
            if dfs and hm: p = at + hm.end(); h = h[:p] + dfs + h[p:]
            elif dfs: h = h[:at + len(LEGEND)] + dfs + h[at + len(LEGEND):]
        h = re.sub(r'(<div class="cw k1"><b>[^<]*</b><span>)(.*?)(</span></div>)', lambda m: m.group(1) + '<span class="mk-hl">' + m.group(2) + '</span>' + m.group(3), h, flags=re.S)
    if recite:
        n = [0]
        def rp(mm):
            n[0] += 1; return mm.group(0).replace('class="rpart"', f'class="rpart rp{(n[0]-1)%6}"')
        h = re.sub(r'<h4 class="rpart">', rp, h)
    return h, stats

def wfreq(docs, terms):
    """docs: [(名称, CCI 原文文本)]；terms: [(词, 领域类)]。按 CCI 原文计数（构建时统计）。"""
    mx = max(sum(t.count(w) for _, t in docs) for w, _ in terms) or 1
    rows = ""
    for w, dc in terms:
        cs = [t.count(w) for _, t in docs]; tot = sum(cs)
        bars = "".join(f'<i style="width:{c/mx*100:.1f}%" title="{n}：{c}"></i>' for (n, _), c in zip(docs, cs))
        rows += f'<div class="wf {dc}"><b>{w}</b><span class="wb" role="img" aria-label="{w}：' + "，".join(f"{n} {c}" for (n, _), c in zip(docs, cs)) + f'">{bars}</span><small>' + " · ".join(f"{n} {c}" for (n, _), c in zip(docs, cs)) + f' · 合计 {tot}</small></div>'
    key = '<div class="wkey">' + "".join(f'<span><i style="background:var({v})"></i>{n}</span>' for (n, _), v in zip(docs, ["--c-god", "--c-sp", "--c-chr", "--c-cov"])) + '</div>'
    return f'<div class="wfreq reveal">{key}{rows}</div>'

MARK_TABLE = [
 ["<b class=\"mk-k d-sal\">称义</b>", "加粗 + 领域色", "关键术语（每节首次出现）", "颜色＝教义领域：蓝神/父 · 金基督 · 绿圣灵 · 珊瑚救恩 · 紫圣约 · 青教会"],
 ["<span class=\"mk-hl\">核心一句</span>", "荧光底", "必背句（🎯 核心一句）", "先背荧光句，再看其余"],
 ["<span class=\"mk-u\">而是……</span>", "金色实线", "正面陈述、重点", "实线＝要记住的“是什么”"],
 ["<span class=\"mk-x\">不是……</span>", "红色波浪线", "否定、难点、易错、异端", "波浪＝要避开的“不是什么”"],
 ["<span class=\"mk-ref\">罗3:24</span>", "琥珀色底", "经文出处", "看到琥珀色就去翻圣经"],
 ["定义框", "蓝色方框", "本页关键词定义（本站用语）", "页首先读定义，再读正文"],
 ["应用侧栏", "绿色左边条", "应用、操练", "绿条＝今天怎么活"],
 ["① ② ③", "金色圆号", "记忆钉（记忆钩、关键词）", "按序号回忆，一钉一词"],
]
