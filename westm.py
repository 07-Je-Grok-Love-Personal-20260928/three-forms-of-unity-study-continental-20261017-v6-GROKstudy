# -*- coding: utf-8 -*-
"""第六部分：与威斯敏斯特标准的次要对照。只用已核对的 OPC 网页文本（WCF/WLC/WSC）与 CCI 原文；英文只作很短的关键语摘录。"""
from core import *
import quotes as Q
OPC="https://opc.org"
def ql(s): return f'<q class="en" lang="en">{s}</q>'
def oa(path,label): return f'<a href="{OPC}/{path}" target="_blank" rel="noopener">{label}</a>'
def part_westminster():
    b = L2("wm-why","6.1","为什么做这个对照：次要比较，不是替换",
      '<p>本站的主轴是<b>欧陆改革宗</b>：三大信经＋三项联合信条（比利时信条、海德堡要理问答、多特信经）。<b>威斯敏斯特标准</b>（威斯敏斯特信条 WCF、大要理问答 WLC、小要理问答 WSC）则是英语世界长老会／清教徒传统的主要文件。两者同属改革宗，教义大体同向；本页只做<b>次要对照</b>，帮你看清“同一信仰，不同语言与体裁”。</p>'
      + flow([("欧陆","BC 1561 · HC 1563 · Dort 1618–19","#5aa9e6"),("三大信经","约2–8世纪 · 325/381 · 6世纪上半叶","#d4af37"),("英语圈","WCF · WLC · WSC（威斯敏斯特大会 1643–1653）","#81b29a")])
      + cards([("📚","本页只引已核对的文本","WCF 1.10、2.3、8、31；WLC 9–11、36–44、50；WSC 6、21–28——均取自 OPC 网页（opc.org）英文原文，本站用中文转述并附很短的英文关键语。","#5aa9e6"),
               ("🔗","不虚构关联","未在页面上看到的“某教会承认某文件”，一概不写。能核对的机构立场见下方 6.6。","#d4af37"),
               ("🕯️","中文本站用语","“神”为 CCI 译文用字；英文只为核对术语。","#81b29a")],"g3")
      + note("<b>来源与版权：</b>威斯敏斯特标准英文本为公有领域文献；这里的引文极短，意在对照；全文请读 "+oa("wcf.html","WCF")+"、"+oa("lc.html","WLC")+"、"+oa("sc.html","WSC")+"。"))
    rows=[
      ["三位一体（基本表述）","BC 8：“他只有一个本质，而有三个位格”；HC 25：神在圣经里这样启示自己，三位“乃是独一、真实、永在的神”","WCF 2.3："+ql("three persons, of one substance, power, and eternity")+"；WLC 9 / WSC 6：三位“同一实质、权能与荣耀均等”","同实质。HC 用“圣经这样启示”回答，WCF/WLC 用更精炼的教义语言。"],
      ["位格的独有属性","亚他那修信经第21–23点（CCI）：父自有、非受造非受生；子独出于父，受生；圣灵从父和子而出","WCF 2.3："+ql("the Father is of none, neither begotten, nor proceeding")+"；子永远受生；圣灵永远从父和子而出。WLC 10 同","WCF 2.3 的三句，与亚他那修信经第21–23点<b>结构相同</b>（本站观察；WCF 页面未自称引用）。"],
      ["圣灵从父和子而出","BC 11：“圣灵从永恒中由父与子而出”；亚他那修信经第23点；尼西亚信经（CCI 西方本）","WCF 2.3："+ql("eternally proceeding from the Father and the Son")+"；WLC 10","<b>一致</b>：都取西方 filioque。东方教会不接受（CCI 尼西亚信经导言）。"],
      ["圣子神性与受生","BC 10：“从永恒而生，非受造亦非被造……乃与圣父同本质、同永恒”；HC 33","WCF 2.3："+ql("eternally begotten of the Father")+"；WCF 8.2 称子“真而永恒的神、与父同质”（of one substance）；WLC 11：圣经将“只属于神的名号、属性、作为和敬拜”归给子与圣灵","<b>一致</b>：同质、永恒受生是共同承重句。"],
      ["基督的两性一位","BC 19：“神人二性合于同一个位格中；这二性各有其独特的属性”；HC 16–17、35；亚他那修信经第34–37点","WCF 8.2："+ql("two whole, perfect, and distinct natures … inseparably joined together in one person, without conversion, composition, or confusion")+"；WLC 36；WSC 21","<b>一致</b>。WCF 的“without conversion, composition, or confusion”与亚他那修信经第35–36点同方向，且读起来贴近迦克墩的语感（本站判断）。"],
      ["道成肉身与童贞女","BC 18：取了“真正的人性及其诸般的软弱，只是没有罪”；HC 35–36","WCF 8.2：由圣灵大能“在童女马利亚腹中”成孕、取自她的本质；WLC 37 / WSC 22："+ql("a true body and a reasonable soul")+"（WSC 22 同）","<b>一致</b>。WLC 37 明说“真身体与理性灵魂”（针对阿波利拿里），BC 18 说“不仅取了人的身体，还取了人的灵魂”。"],
      ["为什么中保必须是神又是人","HC 16–17：必须是真人且无罪；必须是真神","WLC 38–40：中保须是神、须是人、须神人同在一位格；WCF 8.1","<b>一致</b>，论证顺序相近（先神、后人、再合一）。"],
      ["基督的名与三职","HC 31–32（CCI 答31）：先知、祭司、君王；信徒分享其受膏","WCF 8.1："+ql("Prophet, Priest, and King")+"；WLC 42–44；WSC 23–26（先知、祭司、君王的执行）","<b>一致</b>。HC 32 强调信徒分享三职；WSC/WLC 偏重基督如何执行三职（本站概括，见两处原文）。"],
      ["降在阴间","HC 44（CCI）：解为基督在十架受苦中承受地狱般的痛苦与被弃；URCNA 在使徒信经此句旁注“见海德堡问答第44问；多特信经 2.4”","WLC 50：基督死后的卑微“在于被埋葬，并在死亡的状态与权势之下直到第三日；这就是‘降在阴间’的另一种说法”；WCF 8.4 只说 "+ql("remained under the power of death")+"（未用“降在阴间”一语）","两边都不主张“到地狱传道”。HC 偏重‘受苦’，WLC 偏重‘死的状态’（本站对读，约）。"],
      ["复活、升天与再来","HC 45–52；BC 37","WCF 8.4："+ql("On the third day he arose from the dead")+"，带同一身体升天、坐在父的右边；WSC 28：升高在于复活、升天、坐右边、末日审判","<b>一致</b>。WSC 28 把三者归为“升高”，HC 逐项讲其“益处”。"],
    ]
    b += L2("wm-table","6.2","对照总表：三一、基督论与信经句",
      table(["主题","欧陆（CCI 与 URCNA 所载文本）","威斯敏斯特（OPC 网页文本）","对读结论"],rows,"wmt")
      + key("<b>一句话：</b>在三位一体与基督论上，两个传统<b>实质一致</b>，差别主要在<b>体裁</b>（问答的牧养语气 vs 条文的教义语气）与<b>是否点名三信经</b>（见 6.4）。")
      + hard("上表右列的英文只摘极短关键语。需要“一字不差”的英文请直接读 OPC 页面；这里的中文是本站转述，不是官方译文。"))
    b += L2("wm-trin","6.3","并排读：三一与基督（三条阅读路径）",
      '<div class="wmcols">'
      +'<div class="wmc" style="--c:#5aa9e6"><h5>路径甲 · 先读信经</h5><ol><li>亚他那修信经 第21–23点（起源与次序）</li><li>WCF 2.3（同一结构的精简版）</li><li>BC 8（“他只有一个本质，而有三个位格”）</li><li>HC 25（为什么说三位）</li></ol></div>'
      +'<div class="wmc" style="--c:#d4af37"><h5>路径乙 · 基督论</h5><ol><li>亚他那修信经 第29–37点</li><li>WCF 8.2 · WLC 36–40</li><li>BC 18–19</li><li>HC 16–18、35–36</li></ol></div>'
      +'<div class="wmc" style="--c:#81b29a"><h5>路径丙 · 三职与安慰</h5><ol><li>HC 31–32（受膏、三职）</li><li>WLC 42–44 · WSC 23–26</li><li>BC 21–26（基督的救赎与代求）</li><li>HC 1（唯一的安慰）</li></ol></div></div>'
      + app("对教会生活的好处：用 HC 作主日讲道的教学线，用 WSC/WLC 作逻辑对照，能让一个人同时听懂“牧养的话”和“教义的话”。（本站建议）"))
    b += L2("wm-creeds","6.4","差别一：怎样对待“信经”与“教会会议”",
      table(["问题","三项联合信条一侧","威斯敏斯特一侧"],[
       ["是否点名接受三大信经","BC 9：“我们甘愿接受《使徒信经》、《尼西亚信经》和《亚他拿修信经》”（CCI 原文）；CanRC、URCNA、PRCA 页面均照此列出三信经","在 OPC 网站所载 WCF、WLC、WSC 英文原文中，<b>检索不到</b>“creed”一词，也未点名这三份信经（本站逐页检索所得）。"],
       ["圣经与会议的关系","BC 7：圣经充分；CCI《我属于》主日7：信经始终次于圣经，信经“在教会中有权柄”，圣经有“从神而来的权柄”（转述）","WCF 1.10：断定一切宗教争议、会议决议、古代作者意见的最高审判者，只能是“在圣经中说话的圣灵”（转述）；WCF 31.3：自使徒时代以来的一切会议“可能犯错，且有许多犯过错”，不可作信仰的准则，只作帮助（转述）"],
       ["教会职分人员如何受约束","CCI《签署书》：牧师、长老、执事“在神面前”宣告比利时信条、海德堡要理问答和多特信经的全部教义“均完全符合圣经”，并承诺教导与捍卫","（本站未核对 OPC 的誓词原文，不作比较）"]],"wmt")
      + hard("<b>不要误读：</b>WCF 31.3 说的是“会议可能犯错”，<b>并没有</b>点名否定尼西亚或迦克墩；WCF 2.3 与 8.2 的内容与三信经同向。没有“creed”一词不等于不接受其内容——这是文本事实，而不是对该传统立场的结论。机构立场请看 6.6。")
      + key("<b>共同原则：</b>圣经是最高权威；信经与信条因“与圣经相合”而被接受（比较 BC 7、9；WCF 1.10）。差别在<b>是否在文本中点名</b>这三份古代文件。"))
    b += L2("wm-time","6.5","时间线：从古代信经到威斯敏斯特",
      timeline([("325 / 381","尼西亚 / 君士坦丁堡","尼西亚—君士坦丁堡信经（CCI 导言）。","#e07a5f"),
                ("6世纪上半叶","亚他那修信经","CCI：最早出现于6世纪上半叶，作者不详；亚他那修（公元293-373年）并非作者。","#5aa9e6"),
                ("1561","比利时信条","德布利主笔（CCI 导言：1567年殉道）。","#d4af37"),
                ("1563","海德堡要理问答","乌尔西努与俄利维亚努，应选帝侯腓德烈三世之请（CCI 导言）。","#81b29a"),
                ("1618–1619","多特大会","多特信经；三项联合信条完成（CCI 导言）。","#a78bfa"),
                ("1643–1653","威斯敏斯特大会","Heritage Reformed 网站概述：英国议会召集，在英国内战背景下写成（页面所述时段）。","#6bb8d6")])
      + note("日期均取自 CCI 与 Heritage Reformed 页面的自述；“约”表示出处本身存在不确定。"))
    b += L2("wm-inst","6.6","已核对的机构立场（各自网站上的说法）",
      table(["机构","页面所述（转述）","链接"],[
       ["加拿大归正教会 CanRC","采用三大信经（使徒、尼西亚、亚他那修）与三项联合信条；强调“作为人的文件，只有人的权威；唯有神的话语有神圣权威”","<a href='https://canrc.org/beliefs' target='_blank' rel='noopener'>canrc.org/beliefs</a>"],
       ["北美联合改革宗 URCNA","在网站“信条”栏同列三大信经与三项联合信条；各信经页附脚注，如“大公”指普世，并交叉引用 BC 27、HC 54","<a href='https://www.urcna.org/creeds' target='_blank' rel='noopener'>urcna.org/creeds</a>"],
       ["Heritage Reformed Churches","自述使用三大古代信经与三项联合信条；并另行<b>也采纳</b>威斯敏斯特标准（页面明说）","<a href='https://heritagereformed.com/about-the-hrc/doctrinal-standards-and-worship/' target='_blank' rel='noopener'>heritagereformed.com</a>"],
       ["正统长老会 OPC","标准为威斯敏斯特信条与大小要理问答（opc.org 提供全文）","<a href='https://opc.org/standards.html' target='_blank' rel='noopener'>opc.org/standards.html</a>"],
       ["新教改革宗教会 PRCA","三项联合信条为教义标准；另有三大信经，并加上迦克墩信条（页面说明：因其教义体现于 BC 19）。<i>该站对自动抓取显示验证页，此行取自搜索结果所摘页面文字。</i>","<a href='https://www.prca.org/about/official-standards/creeds' target='_blank' rel='noopener'>prca.org</a>"],
       ["加拿大改革宗神学院","“持守无谬的圣经，如大公信经与比利时信条、海德堡要理问答、多特信经所总结”（页面意思）","<a href='https://canadianreformedseminary.ca/about/discover-crts/' target='_blank' rel='noopener'>canadianreformedseminary.ca</a>"],
       ["西敏神学院 WTS","核心信念：以威斯敏斯特标准所含教义体系为主，“其次”也参照其他改革宗信条","<a href='https://www.wts.edu/about/mission-values' target='_blank' rel='noopener'>wts.edu</a>"],
       ["改革宗神学院 CRTS（台北）","学院信仰：全球改革宗教会的信条，其中列有使徒信经、海德堡要理问答、威斯敏斯特信条及大小要理问答","<a href='https://crts.edu/en/intro/' target='_blank' rel='noopener'>crts.edu/en/intro</a>"],
       ["洛杉矶恩约教会 CCRC","宣告古代信经与三项联合信条为教义准则，并提供三联合信条中英对照版与王一牧师讲解的链接","<a href='https://www.ccreformed.org/our-belief/' target='_blank' rel='noopener'>ccreformed.org/our-belief</a>"],
       ["改革宗初学者","“大公信经”栏含使徒信经、尼西亚信经、亚他那修信经与迦克墩定义；另有“威敏斯特准则”栏","<a href='https://www.reformedbeginner.net/ecumenical-creeds/' target='_blank' rel='noopener'>reformedbeginner.net</a>"]],"wmt")
      + note("<b>关于网站之间的关系：</b>本站只陈述每个页面自己说了什么；没有在页面上看到的隶属、合作或背书关系，一概不写。各机构完整立场以其官方文件为准。"))
    b += L2("wm-diff","6.7","小结：差异与怎样读",
      cards([("🧭","相同的骨架","一位神、三位格；基督真神真人一位格；圣灵从父和子；圣经为最高权威。","#d4af37"),
             ("🗣️","不同的语气","欧陆文本更常用“你唯一的安慰是什么？”式的牧养问答（HC）；威斯敏斯特的 WCF 条文更像教义论文，WSC 则是短问短答。","#5aa9e6"),
             ("📖","不同的组织法","HC 依“罪、救、谢”三部与52主日；WCF 依教义主题逐章（第1章圣经、第2章神、第8章中保、第31章会议）。","#81b29a"),
             ("⚖️","不同的措辞","降在阴间：HC 44 讲‘地狱般的痛苦’，WLC 50 讲‘死的状态’；是否点名三信经：BC 9 点名，OPC 所载 WCF/WLC/WSC 未点名。","#e07a5f")],"g4")
      + app("读书建议：想懂欧陆传统，从本站第八–十部分的原文库出发；想对照英语圈，随手打开 WCF 2、8 与 WLC 36–44；遇到术语差异，回到三大信经（第七部分）。"))
    return L1("westminster","六","与威斯敏斯特标准对照（次要比较）","scale","同一信仰在英语长老会传统中的表述：三一、基督论、信经与会议。", b)
