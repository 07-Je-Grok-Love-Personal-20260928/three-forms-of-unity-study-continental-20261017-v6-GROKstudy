# -*- coding: utf-8 -*-
import re,collections
from core import *
from c_common import *

def cci_urls(bodies):
    urls=collections.OrderedDict()
    for k,h in bodies.items():
        for u in re.findall(r'href="(https://ccifellowship\.org[^"#]*)',h):
            urls.setdefault(u,set()).add(k)
    return urls
GROUP=[("/books/book-of-praise/confessions/","原文库（逐字）"),("/books/i-belong/","《我属于》（I Belong）"),("/books/book-of-praise/forms/","签署书"),("/books/book-of-praise/liturgical-forms/","仪文"),
 ("/books/book-of-praise/prayers/","祷文"),("/books/book-of-praise/church-order/","教会规章"),("/books/book-of-praise/creeds","三大信经"),("/books/the-candlestand-statement","《烛台宣言》"),
 ("/books/the-beauty-of-church-worship","《归正教会敬拜礼仪之美》"),("/books/flame-of-truth","《真理的火焰》"),("/books/the-gift-from-heaven","《从天而来的礼物》"),("/sermons/","讲道")]
def part_src(bodies):
    D=lambda n: J(n)
    cr,bc,hc,dt=D("creeds"),D("bc"),D("hc"),D("dort")
    ndort=sum(len(h["items"]) for h in dt["heads"])
    nq=sum(1 for l in hc["lds"] for b in l["blocks"] if b["t"]=="h4")
    u=cci_urls(bodies)
    grp=collections.OrderedDict((g,[]) for _,g in GROUP); grp["其他"]=[]
    for url in u:
        path=url.replace(CCI,"")
        for p,g in GROUP:
            if path.startswith(p): grp[g].append(url); break
        else: grp["其他"].append(url)
    b = L2("src-exact","12.1","逐字收录自 CCI 的文本（可核对）",
      '<p>下列文本<b>逐字</b>取自华人改革宗《赞美手册》（基督教华人网络团契，CCI）中文版，由爬取页面的原文生成，没有改写；每条均附原页链接。本站以脚本核对（见 12.5）。</p>'
      + table(["文本","范围","CCI 原页","本站页面"],[
        ["比利时信条",f"全部 {len(bc['articles'])} 条",A(bc["url"],"the-belgic-confession"),'<a href="#bct">第八部分</a>'],
        ["海德堡要理问答",f"全部 {nq} 问（{len(hc['lds'])} 个主日），含经文脚注",A(hc["url"],"heidelberg-catechism"),'<a href="#hct">第七部分</a>'],
        ["多特信经",f"全部 {ndort} 个条目（四项教义，含各项“错谬反驳”）",A(dt["url"],"canons-of-dort"),'<a href="#dtt">第九部分</a>'],
        ["使徒信经",f"CCI 页面全文",A(cr["apostles"]["url"],"apostles-creed"),'<a href="#cr-ap">第十部分</a>'],
        ["尼西亚信经","CCI 页面全文",A(cr["nicene"]["url"],"nicene-creed"),'<a href="#cr-ni">第十部分</a>'],
        ["亚他那修信经","CCI 页面全文（编号见下）",A(cr["athanasian"]["url"],"athanasian-creed"),'<a href="#cr-at">第十部分</a>']],"cmp")
      + note("全站所有以“ ”标出的 CCI 引文，都在生成网页时由程序核对为 CCI 原文的逐字片段；不一致则网页无法生成。分组标题若非 CCI 所有，页面上标为“本站分组”。"))
    cl=""
    for g,l in grp.items():
        if not l: continue
        cl+=f'<details class="srcd"><summary>{g}（{len(l)} 个页面）</summary><ul class="refs">'+"".join(f'<li>{A(x,x.replace("https://ccifellowship.org",""))}</li>' for x in l)+'</ul></details>'
    b += L2("src-cci","12.2","CCI 其他内容：转述与短引（附链接）",
      '<p>下面是<b>本站网页里实际链接到的 CCI 页面</b>（由程序按链接自动汇总，数量以网页为准）。除原文库外，这些页面在本站<b>只转述、只做很短的引文</b>，完整内容请读原页：</p>'+cl
      + table(["CCI 内容","本站用途"],[
        ["《我属于》（I Belong）1–52 主日","每个主日的“概要”（CCI 对各课的归纳）：第二部分 52 主日的“CCI 概述”引文；全部 52 个主日均有概要（部分主日合并为一课）"],
        ["签署书（两版）","第五部分 5.6：签署书的完整中文原文与结构分解"],
        ["公开信仰告白仪文","第五部分 5.8：第一问问的是对“归纳在信条中，并在本教会宣讲的圣经教义”的相信"],
        ["教会规章（导言、第 44、52、53、58 条）","第四部分 4.9 与第五部分：规章的形成史；每主日宣讲 HC"],
        ["《烛台宣言》","第五部分：教义的价值、教会制度等条文的短引"],
        ["《归正教会敬拜礼仪之美》第 4 章","第二部分：HC 问103 与敬拜的四个“主要成分”（转述）"],
        ["Clarence Stam 的 HC 讲道","第二、三、五部分：LD52 讲道指出三份文件都以“真信徒能持守信仰”收束（转述）"],
        ["《真理的火焰》","儿童教会史读物：与三份文件的人物、事件联系（转述）"]],"cmp")
      + note("没有逐字收录 CCI 的《我属于》课文、讲道、仪文与图书全文，以免大段复制；需要时请直接阅读原页。"))
    ref=[("ccreformed.org（洛杉矶恩约教会）","信仰页：古代信经与三联合信条构成教义准则；说古代信经“把我们连结在古代基督教会上”，三联合信条“把我们连结在十六、十七世纪广大的改革宗传统中”","https://www.ccreformed.org/our-belief/"),
      ("reformedbeginner.net（改革宗初学者）","“大公信经”专页：统称使徒、尼西亚、亚他那修与迦克墩","https://www.reformedbeginner.net/ecumenical-creeds/"),
      ("canrc.org（加拿大归正教会）","Beliefs 页（英文）：采纳三大信经与三大信条；人的文件只有人的权威","https://canrc.org/beliefs"),
      ("urcna.org（北美联合改革宗）","Ecumenical Creeds 与信经页（英文）：脚注把“降在阴间”“大公”连到信条","https://www.urcna.org/creeds"),
      ("heritagereformed.com","Doctrinal Standards 页（英文）：三大古代信经、三项联合信条，并采纳威斯敏斯特标准","https://heritagereformed.com/about-the-hrc/doctrinal-standards-and-worship/"),
      ("prca.org（美国抗议宗改革宗）","<b>仅取自搜索结果摘录</b>（网站被验证页拦截，本站未能直接读取）：采纳三份信经，另加迦克墩信经","https://www.prca.org/about/official-standards/creeds"),
      ("opc.org（正统长老会）","WCF、WLC、WSC 英文原文页：本次完整读取，用于第六部分的短语对照","https://opc.org/standards.html"),
      ("canadianreformedseminary.ca","神学院使命介绍页（英文），仅作背景","https://canadianreformedseminary.ca/about/discover-crts/"),
      ("wts.edu（威斯敏斯特神学院）","使命与价值观页（英文），仅作背景","https://www.wts.edu/about/mission-values"),
      ("crts.edu（改革宗神学院，台北）","学院介绍页，仅作背景","https://crts.edu/en/intro/")]
    b += L2("src-ref","12.3","参考网站：只转述我们读到的",
      '<p>下列网站我们读了相关页面，只<b>转述并注明出处</b>；没有读到的联系，我们不假设。</p>'
      + table(["网站","本站使用的内容","链接"],[[n,w,A(x,x.split("//")[1].replace("www.","").strip("/"))] for n,w,x in ref],"cmp"))
    b += L2("src-miss","12.4","CCI 上没有找到的内容（本站不补）",
      "<ul class='refs'>"
      "<li><b>多特信经的序言与结论</b>：CCI 页面只有导言与教义条文（四项），没有原信经的序言与结语，本站不补。</li>"
      "<li><b>“TULIP”一词</b>：在本站抓取的 CCI 页面中没有出现；CCI 的多特导言用中文列出“五大点”（抗辩派五点；改革宗五点），并说第三、四项合并。TULIP 是后来的英语口诀，见第四部分。</li>"
      "<li><b>德布利 1561 年信与致国王请愿书的原文</b>：CCI 导言只作概述，我们抓取的页面里没有全文；本站只转述 CCI 导言说的内容。</li>"
      "<li><b>HC 讲道</b>：CCI 讲道库只有主日 32、43、45–52（本站抓取时），其余主日没有对应讲道。</li>"
      "<li><b>《迦克墩信经》</b>：CCI 的“普世信经”页只有三份信经；改革宗初学者与 PRCA 另加迦克墩，本站在这里只作说明，不收全文。</li>"
      "<li><b>威斯敏斯特标准</b>：CCI 没有；英文取自 OPC 网页。</li>"
      "<li><b>三项联合信条的英文文本</b>：CCI 页面为中文；英文只在与 OPC 对照时摘极短语。</li>"
      "<li><b>分组标题</b>：BC 的七群、HC 部分内的小节名等，除 CCI 目录明确给出的，均为“本站分组”。</li>"
      "<li><b>亚他那修信经编号</b>：CCI 导言写“第二部分包括第29–43点”，正文只编到42点；本站依正文42点。</li></ul>"
      + note("<b>更正：</b>姊妹站《三大公教会信经》的来源页曾写有数个主日缺“概要”；本次重新核对 CCI《我属于》页面，52 个主日（含合并课）都有“概要”，是旧版解析遗漏。"))
    b += L2("src-method","12.5","方法：怎样保证“逐字”",
      "<ul class='refs'><li>网站数据来自 CCI 页面的文本，保存为 data/*.json，不做改写。</li><li>构建时，所有 BC、HC、Dort 与 CCI 其他页面的引号引文，都经程序检查为数据的逐字子串；有一处不符，构建失败。</li><li>tools/verify_exact.py 逐条对照原库与生成网页；tools/check_links.py 检查所有站内链接与目录锚点。</li><li>历史背景（如多德雷赫特、莱顿、日内瓦、苏黎世等地理与年代）凡 CCI 页面没有说明的，页内标“约”或说明“一般历史常识”；本站没有逐条引用学术著作。</li></ul>")
    b += L2("src-ver","12.6","版本记录",
      '<ul class="refs"><li><b>v20261017-2</b>：三级/四级目录（52 主日、BC 37 条、多特各项与条、三大信经按条/按组）；信经背诵版（一行一句，原文不改）；52 主日罗盘、记忆页“已背熟”、动画与图标；排版细化。标题为本站学习标题，不是 CCI 原文。</li><li><b>v20261017-1</b>：三项联合信条深读首版：十二部分、52 主日、37 条、多特 63 条目、威斯敏斯特对照、记忆与 52 周计划。</li></ul>')
    return L1("sources","十二","来源与说明","library","哪些是逐字收录、哪些是转述、哪些在 CCI 上没有找到。", b)
