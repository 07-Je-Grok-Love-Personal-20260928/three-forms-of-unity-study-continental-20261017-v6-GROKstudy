# -*- coding: utf-8 -*-
"""第六部分：与威斯敏斯特标准的次要对照。英文只摘极短关键语，均取自 OPC 网页（opc.org/wcf.html、lc.html、sc.html）本次阅读的文本；欧陆一侧的引文经 Q() 校验为 CCI 原文。"""
from core import *
from c_common import *
OPC="https://opc.org"
def ql(s): return f'<q class="en" lang="en">{s}</q>'
def oa(path,label): return f'<a href="{OPC}/{path}" target="_blank" rel="noopener">{label}</a>'
def part_westminster():
    b = L2("wm-why","6.1","为什么做这个对照：次要比较，不是替换",
      '<p>本站的主轴是<b>欧陆改革宗</b>：三大信经＋三项联合信条。<b>威斯敏斯特标准</b>（信条 WCF、大要理问答 WLC、小要理问答 WSC，1640 年代英国）是英语世界长老会传统的主要文件。两者同属改革宗，大方向一致；本页回答三个问题：<b>哪里实质相同？哪里措辞或体裁不同？哪里是真正的强调差异？</b></p>'
      + flow([("欧陆","BC 1561 · HC 1563 · Dort 1618–19","#5aa9e6"),("古代信经","325/381 · 6世纪上半叶","#d4af37"),("英语圈","WCF · WLC · WSC（威斯敏斯特大会 1643–1653 约）","#81b29a")])
      + cards([("📚","只引已读文本","英文取自 OPC 网页：WCF 全部章节、WSC 全部、WLC 全部；英文只摘极短关键语，供核对术语，中文为本站转述，不是官方译文。","#5aa9e6"),
               ("🔗","不虚构关联","没在页面上看到的“某教会承认某文件”，一概不写；机构立场见 6.8。","#d4af37"),
               ("⚖️","判断三级","“实质同”“措辞异”“强调异”；后两者不等于对立。判断为本站的阅读，标“本站判断”。","#81b29a")],"g3")
      + note("<b>版本提示：</b>OPC 网页所载 WCF 第23章第3节是美国修订本（对“民事官长与教会”的措辞与 1647 年原本不同，原本差异本站未逐字核对，约）。引用时请以这一点为前提。<b>来源：</b>"+oa("wcf.html","WCF")+"、"+oa("lc.html","WLC")+"、"+oa("sc.html","WSC")+"。"))
    rows=[
     ["圣经：充分与最高权威",
      "BC 7："+Q("BC 7","我们相信，圣经中包含了神全部的旨意")+"；"+Q("BC 7","我们不可认为出自人手的任何著作与圣经具有同等价值")+"；BC 5：圣灵在我们心中作见证（"+bl(5)+"）",
      "WCF 1.6："+ql("expressly set down in Scripture, or by good and necessary consequence may be deduced from Scripture")+"；1.5："+ql("the inward work of the Holy Spirit bearing witness by and with the Word")+"；1.10：最高审判者是“在圣经中说话的圣灵”；WSC 2：圣经是"+ql("the only rule")+"",
      "<b>实质同。</b>WCF 1.6 明说“必然推论”并承认敬拜与治理里有“人类情境”可凭自然之光与基督徒审慎安排；BC 7 与 32 更直接地强调“不可加添”与不束缚良心（本站判断）。"],
     ["三位一体与基督论","BC 8–11、18–19；HC 24–25、35（姊妹站已逐句对读）","WCF 2.3、8.2；WLC 9–11、36–40；WSC 6、21–22","<b>实质同。</b>详细对读见姊妹站与本站第五部分。"],
     ["预定与拣选",
      "Dort 1.7："+Q("DORT 1.7","在创立世界以先，神就根据他的主权和美意，在基督里，从全人类")+"…拣选了特定数量的人；Dort 1.15 弃绝；BC 16",
      "WCF 3.5："+ql("without any foresight of faith, or good works")+"；3.4：选民之数"+ql("cannot be either increased or diminished")+"；3.7："+ql("to pass by")+"其余的人；3.8 须“审慎与关怀”；WSC 7、WLC 12–13",
      "<b>实质同。</b>WCF 3 是“神的永恒预旨”总纲（连同创造、护理），Dort 1 是针对争论的“拣选与弃绝”专论；WCF 3.8 与 Dort 1.12–1.14 在“牧养地讲预定”上同向。"],
     ["基督的死与有效",
      "Dort 2.8："+Q("DORT 2.8","将称义的信心唯独赐给他们")+"；BC 21；HC 37–44",
      "WCF 8.5、8.8；3.6："+ql("Neither are any other redeemed by Christ")+"…"+ql("but the elect only")+"；WLC 59",
      "<b>实质同。</b>Dort 2.5 另强调福音应当“不加分别地对万国万民”宣讲（"+dl("2",5)+"）；WCF 对应处在 7.3 与 10 章的“白白提供、使人愿意”。"],
     ["人的败坏与意志",
      "BC 14："+Q("BC 14","我们弃绝一切与圣经相悖的有关人自由意志的教导")+"；Dort 3-4.3："+Q("DORT 3-4.3","若没有圣灵使人重生的恩典，人既没有意愿，也没有能力转向神并改邪归正")+"；HC 8",
      "WCF 9.3："+ql("wholly lost all ability of will to any spiritual good accompanying salvation")+"；10.2：人"+ql("altogether passive")+"；WLC 25",
      "<b>实质同。</b>用语不同，结构相同：先失去能力，再因恩典被更新，然后“自愿地”顺服。"],
     ["圣约的框架",
      "BC 34、HC 74、Dort 1.17、2.8 使用“恩典之约”（"+Q("DORT 1.17","信徒的儿女是圣洁的，不是因为他们的本性圣洁，而是因为他们与父母共同承受恩典之约")+"）；三项联合信条没有专章讲约",
      "WCF 7.2："+ql("a covenant of works")+"；7.3："+ql("a second, commonly called the covenant of grace")+"；7.6："+ql("not therefore two covenants of grace, differing in substance")+"；WLC 31："+ql("made with Christ as the second Adam")+"；WSC 12、20",
      "<b>强调异。</b>威斯敏斯特把“行为之约／恩典之约”写成教义条文；三项联合信条只用恩典之约的语言，“行为之约”一词只在 Dort 2.10 的错谬二里出现一次（见 6.3）。"],
     ["信心与确信",
      "HC 21："+Q("HC 21","同时，真信心也是一种确信，坚信神完全是出于他的恩典")+"；Dort 5.9："+Q("DORT 5.9","信徒自己能够对选民蒙保守得救恩和真信徒能持守信仰有十足的把握")+"；5.11 争战中的怀疑",
      "WCF 18.3："+ql("doth not so belong to the essence of faith")+"，真信徒“可能等候许久”；14.3："+ql("growing up in many to the attainment of a full assurance")+"；WLC 81",
      "<b>措辞异（本站判断）。</b>HC 21 把“确信”写进信心的定义；WCF 18.3 把“确信”与“信心的本质”分开，但同样要求人勤勉使呼召与拣选坚定。两边都承认确信会动摇（Dort 5.11；WCF 18.4）。"],
     ["称义",
      "HC 60–61："+Q("HC 61","不是因为我的信心有什么价值，而是唯独因着基督的顺服、义和圣洁")+"；BC 22–23；Dort 3-4.14",
      "WCF 11.1："+ql("not by imputing faith itself")+"；11.2："+ql("the alone instrument of justification")+"，"+ql("yet is it not alone in the person justified")+"；WSC 33；WLC 70–73",
      "<b>实质同。</b>HC 64（真信心不可能不结感恩的果子）≈ WCF 11.2 的“信心不是孤立的”。"],
     ["善行与律法",
      "HC 86（三用之一：感恩、确信、赢得邻舍）；BC 24–25；HC 92–115（十诫在“感恩”部分）",
      "WCF 16.2："+ql("fruits and evidences of a true and lively faith")+"；19.6、19.7 律法对信徒的用处；WLC 94–97",
      "<b>结构异，实质同。</b>HC 把十诫放在“感恩”部分；WCF 把律法放在恩典与称义“之后”的第19章，同样强调律法是生活的规则（本站判断）。"],
     ["教会的标志与性质",
      "BC 29："+Q("BC 29","她宣讲纯正的福音；她按照基督当初设立圣礼的样式施行圣礼；她为纠正错误、刑罚罪恶而执行教会纪律")+"；BC 27–28；HC 54",
      "WCF 25.1–25.2：有形与无形的教会；25.4："+ql("more or less pure")+"取决于福音教义、圣礼与公共敬拜是否纯正；25.2：信徒"+ql("and of their children")+"；WLC 62–64",
      "<b>实质同。</b>BC 29 把“三标志”写成鉴别真假教会的明确清单；WCF 25.4 用“纯正程度”的语言给出同类标准（本站判断）。"],
     ["圣礼与婴孩洗礼",
      "BC 33–35；HC 66："+Q("HC 66","圣礼是圣洁的、可见的标志和印记")+"；HC 74；BC 34 取代割礼",
      "WCF 27.1："+ql("holy signs and seals of the covenant of grace")+"；28.4："+ql("the infants of one, or both, believing parents")+"；29.7 属灵的真实同在；WSC 94–96；WLC 166",
      "<b>实质同。</b>细节：WCF 28.3 明说浇水或洒水皆可；BC 34 也提到水“浇在或洒在身上”（见该条原文）。"],
     ["敬拜与安息日",
      "HC 103（"+hq(103)+"）："+Q("HC 103","特别在安息日，我当积极去神的教会聆听神的话语，参加圣礼")+"；教会规章 52",
      "WCF 21.7："+ql("one day in seven")+"，"+ql("the Christian Sabbath")+"；21.8 全日圣洁休息；WSC 58–60；WLC 116–117",
      "<b>强调异。</b>HC 103 用“聆听、圣礼、祈祷、周济”描述安息日，并指向“永恒的安息”；WSC/WLC 明确“整整一日”与休息的规条。欧陆教会内部对此的看法不一，本站不做断言（约）。"],
     ["政府与教会",
      "BC 36："+Q("BC 36","他们抑恶扬善的责任不限于维护公共秩序，也用于保护教会及其传道工作")+"；CCI 注：1905 年有一句被删除",
      "WCF 23.3（OPC 所载修订本）：官长不得"+ql("interfere in matters of faith")+"，但要如"+ql("nursing fathers")+"保护教会；WCF 30–31 教会治理有别于官长",
      "<b>强调异，且有版本史。</b>BC 36 保护福音传讲的语句，后来被一些教会改动（CCI 注）；WCF 23.3 也有美国修订。比较时须分清“原本”和“修订本”（约）。"],
     ["会议与信经的权威",
      "BC 32："+Q("BC 32","我们弃绝一切出于人，又束缚和控制人的良心")+"；教会规章（CCI）；签署书",
      "WCF 31.3："+ql("may err; and many have erred")+"；31.2 会议决议若与圣经相合，当“敬畏顺服”；1.10",
      "<b>实质同。</b>两边都说：会议可能犯错，圣经是最后的标准；欧陆多一层“签署书”的制度。"],
     ["末后的事",
      "BC 37；HC 57–58；Dort 5.14–5.15（保守的安慰）",
      "WCF 32–33；WSC 37–38；WLC 86–90",
      "<b>实质同。</b>都强调“灵魂立即归神”“身体复活”“审判的安慰与警醒”。"]]
    b += L2("wm-table","6.2","对照总表：十五个主题",
      table(["主题","欧陆（CCI 原文）","威斯敏斯特（OPC 网页）","判断"],rows,"wmt")
      + key("<b>一句话：</b>两个传统在“救恩如何全然出于神”这条主线上高度一致；差别在体裁、教义组织与几处强调（圣约的框架、确信的定义、安息日、政府与教会）。")
      + hard("英文只摘极短关键语；需要整段英文请直接读 OPC 页面。中文为本站转述。"))
    b += L2("wm-cov","6.3","圣约：威斯敏斯特的“条文”与欧陆的“语言”",
      '<p>这是读者最常问到的差异。先说<b>文本事实</b>（经脚本检索 CCI 三份文件）：</p>'
      + table(["术语","三项联合信条（CCI）","威斯敏斯特（OPC）"],[
        ["恩典之约","出现：BC 34、HC 74、Dort 1.17、2.8 等","WCF 7.3；WSC 20；WLC 30–32"],
        ["行为之约","只出现一次，在 Dort 2.10 错谬二里："+Q("DORT 2.10","无论是恩典之约还是行为之约"),"WCF 7.2、19.1；WSC 12；WLC 30"],
        ["救赎之约（圣父与圣子之间）","<b>不出现</b>","WCF 也<b>未使用这一名称</b>；但 8.1 写到神“在永恒的旨意中”拣选基督，并"+ql("from all eternity give a people")+"给他；WLC 31 说恩典之约"+ql("made with Christ as the second Adam")]],"cmp")
      + key("<b>结论（本站判断）：</b>“行为之约／恩典之约／救赎之约”三分法是后来改革宗正统神学的整理（约），威斯敏斯特写出了前两者的框架并带有第三者的内容；三项联合信条使用的是<b>圣经语言</b>“恩典之约”，没有立专章。这不等于欧陆教会不教这三者；它们在教义学与讲道里广泛使用，但“三份文件本身”没有出现这些术语。")
      + cards([("🌱","行为之约","WCF 7.2 与 WSC 12：生命应许亚当，条件是完全的个人顺服。三项联合信条在 BC 14、HC 6–9 处讲创造与堕落，但不称之为“约”（见第二、三部分）。","#e07a5f"),
               ("🕊️","恩典之约","BC 34、HC 74、Dort 1.17、2.8：把儿女、洗礼与基督的血与“约”连在一起（见第二、三、四部分）。WCF 7.6：旧约与新约是"+ql("one and the same, under various dispensations")+"。","#5aa9e6"),
               ("🧭","救赎之约","在永恒中父、子、灵的计划：三项联合信条只说拣选“在基督里”（Dort 1.7）、基督是“中保与元首”（Dort 1.7）；术语本身是后来的概括（约）。","#d4af37")],"g3")
      + note("<b>关于“荷兰人的恩典之约观”：</b>HC 74 与 BC 34（CCI 原文）对“约”与婴孩洗礼的论述，可以看出欧陆文本的重心：<b>约的应许临到信徒与他们的儿女</b>（HC 74；Dort 1.17），而<b>应许要以信心领受</b>（HC 66）。这与 WCF 28.4、WLC 166 同向。至于欧陆教会在 20 世纪内部关于约与重生的争论，CCI 页面没有涉及，本站不展开。"))
    b += L2("wm-assure","6.4","确信：HC 21 与 WCF 18.3 怎样读",
      '<p>两句话常被并置：</p>'
      + '<div class="wmcols"><div class="wmc" style="--c:#5aa9e6"><h5>HC 21（CCI）</h5><p>'+Q("HC 21","真信心也是一种确信，坚信神完全是出于他的恩典")+'</p><p class="src">'+hq(21,"HC 21 全文")+'</p></div>'
      + '<div class="wmc" style="--c:#d4af37"><h5>WCF 18.3（OPC）</h5><p>'+ql("This infallible assurance doth not so belong to the essence of faith, but that a true believer may wait long")+'</p><p class="src">'+oa("wcf.html","WCF 第18章")+'</p></div></div>'
      + key("<b>怎么读：</b>HC 21 说的是“真信心”的<b>性质</b>（含有“知道”与“信靠”两面，包括“也赐给了我”）；WCF 18.3 说的是“<b>完全确信</b>”的时间与途径（信徒可能要等候）。两者回答的不是同一个问题（本站判断）。Dort 5.11 同样承认信徒会在争战中感觉不到确信，却相信神必使他们“再次确信”。"))
    b += L2("wm-church","6.5","教会、治理与会议",
      table(["问题","欧陆","威斯敏斯特"],[
        ["谁是教会的头","BC 31 与 BC 29：基督是唯一的头（见这几条）","WCF 25.6："+ql("no other head of the church but the Lord Jesus Christ")],
        ["治理结构","BC 30–32 讲职分与治理；教会规章第44条（CCI）：相邻教会各派牧师与长老参加地方会议，至少每三个月一次（"+mu("co44","原文")+"）","WCF 30 教会的治理“有别于官长”；31 会议的权限"],
        ["信条的位置","签署书：宣告三份文件“完全符合圣经”（第五部分）","WCF 31.3 会议“可能犯错”，不可作信仰的准则，只作帮助"]],"wmt")
      + note("CCI 的教会规章介绍说，规章 1563 年起在多地会议里逐步成形，1618–19 年多特会议修订（见第四部分 4.9）；本站对威斯敏斯特的治理规条（如 1645 年的相关文件）没有逐字阅读，故不展开。"))
    b += L2("wm-sab","6.6","安息日：一个“强调差异”的例子",
      '<p>HC 103 与威斯敏斯特有以下可检验的对照：</p>'
      + table(["","HC 103（CCI）","WCF 21.7–8；WSC 58–60"],[
        ["对象","“第四条诫命”","同"],
        ["内容","<b>坚持宣讲福音、办学；特别在安息日去教会</b>聆听神的话语、参加圣礼、祈祷、周济穷人；平生不作恶，让圣灵在今生开始“永恒的安息”","明说"+ql("one day in seven")+"，现在是"+ql("the first day of the week")+"；全日"+ql("an holy rest")+"，除必要与怜悯的事外全部时间用于敬拜"],
        ["语气","牧养的、目标式","规条式的"]],"wmt")
      + hard("不要误读：这不是“欧陆不守主日”。CCI 教会规章第52条要求每主日讲 HC（"+mu("co52","原文")+"）。两边的差异在于<b>文本如何组织与要求有多细</b>；欧陆教会内部对安息日规条的具体看法不一，本站不替任何教会下结论（约）。"))
    b += L2("wm-time","6.7","时间线：从古代信经到威斯敏斯特",
      timeline([("325 / 381","尼西亚 / 君士坦丁堡","尼西亚—君士坦丁堡信经（CCI 导言）。","#e07a5f"),
                ("6世纪上半叶","亚他那修信经","CCI：最早出现于6世纪上半叶，作者不详。","#5aa9e6"),
                ("1561","比利时信条","德布利主笔（CCI：1567 年殉道）。","#d4af37"),
                ("1563","海德堡要理问答","乌尔西努与俄利维亚努，应选帝侯腓德烈三世之请（CCI 导言）。","#81b29a"),
                ("1618–1619","多特大会","多特信经；三项联合信条完成（CCI 导言）。","#a78bfa"),
                ("1643–1653 约","威斯敏斯特大会","Heritage Reformed 网站概述：英国议会召集，写成于英国内战背景下（页面所述时段）。","#6bb8d6")])
      + note("日期取自 CCI 与 Heritage Reformed 页面自述；“约”表示出处本身存在不确定。"))
    b += L2("wm-inst","6.8","机构立场（各自网站的说法）",
      table(["机构","页面所述（转述）","链接"],[
       ["加拿大归正教会 CanRC","采用三大信经与三项联合信条；强调“作为人的文件只有人的权威，唯有神的话语有神圣权威”","<a href='https://canrc.org/beliefs' target='_blank' rel='noopener'>canrc.org/beliefs</a>"],
       ["北美联合改革宗 URCNA","在“信条”栏同列三大信经与三项联合信条；各信经页附脚注，如“大公”指普世，并交叉引用 BC 27、HC 54","<a href='https://www.urcna.org/creeds' target='_blank' rel='noopener'>urcna.org/creeds</a>"],
       ["Heritage Reformed Churches","自述使用三大古代信经与三项联合信条；并另行<b>也采纳</b>威斯敏斯特标准（页面明说）","<a href='https://heritagereformed.com/about-the-hrc/doctrinal-standards-and-worship/' target='_blank' rel='noopener'>heritagereformed.com</a>"],
       ["正统长老会 OPC","标准为威斯敏斯特信条与大小要理问答（opc.org 提供全文）","<a href='https://opc.org/standards.html' target='_blank' rel='noopener'>opc.org/standards.html</a>"],
       ["新教改革宗教会 PRCA","三项联合信条为教义标准；另有三大信经，并加上迦克墩信条（页面说明：因其教义体现于 BC 19）。<i>该站对自动抓取显示验证页，此行取自搜索结果所摘页面文字。</i>","<a href='https://www.prca.org/about/official-standards/creeds' target='_blank' rel='noopener'>prca.org</a>"],
       ["加拿大改革宗神学院","“持守无谬的圣经，如大公信经与比利时信条、海德堡要理问答、多特信经所总结”（页面意思）","<a href='https://canadianreformedseminary.ca/about/discover-crts/' target='_blank' rel='noopener'>canadianreformedseminary.ca</a>"],
       ["西敏神学院 WTS","核心信念：以威斯敏斯特标准所含教义体系为主，“其次”也参照其他改革宗信条","<a href='https://www.wts.edu/about/mission-values' target='_blank' rel='noopener'>wts.edu</a>"],
       ["改革宗神学院 CRTS（台北）","学院信仰：全球改革宗教会的信条，其中列有使徒信经、海德堡要理问答、威斯敏斯特信条及大小要理问答","<a href='https://crts.edu/en/intro/' target='_blank' rel='noopener'>crts.edu/en/intro</a>"],
       ["洛杉矶恩约教会 CCRC","宣告古代信经与三项联合信条为教义准则，并提供三联合信条中英对照版与王一牧师讲解的链接","<a href='https://www.ccreformed.org/our-belief/' target='_blank' rel='noopener'>ccreformed.org/our-belief</a>"],
       ["改革宗初学者","“大公信经”栏含使徒信经、尼西亚信经、亚他那修信经与迦克墩定义；另有“威敏斯特准则”栏","<a href='https://www.reformedbeginner.net/ecumenical-creeds/' target='_blank' rel='noopener'>reformedbeginner.net</a>"]],"wmt")
      + note("<b>关于网站之间的关系：</b>本站只陈述每个页面自己说了什么；页面上没看到的隶属、合作或背书关系一概不写。各机构完整立场以其官方文件为准。"))
    b += L2("wm-diff","6.9","小结：怎样读这两条线",
      cards([("🧭","相同的骨架","一位神三位格；基督真神真人；唯独恩典、唯独信心；圣经为最高权威；教会有标志与治理；圣礼为标志与印记。","#d4af37"),
             ("🗣️","不同的语气","HC：“你唯一的安慰是什么？”；WSC：“人的首要目的是什么？”；开篇问题就决定了整本书的气质。","#5aa9e6"),
             ("📖","不同的组织","三项联合信条：三份文件各司其职；威斯敏斯特：一套信条＋两套要理问答。","#81b29a"),
             ("⚖️","几处强调","圣约的条文化、确信的定义、安息日、官长与教会、是否点名三大信经。","#e07a5f")],"g4")
      + app("读书建议：想懂欧陆，从第七–九部分的原文库出发；想对照英语圈，随手打开 WCF 3、7、18、21 与 WSC 12、20、58–60。")
      + note("WCF、WLC、WSC 的检索说明：本站另检索了 OPC 所载三份英文文本，没有“creed”一词；因此“是否点名三信经”是文本事实，不是对该传统立场的结论（见 6.8 的机构说明）。"))
    return L1("westminster","六","与威斯敏斯特标准对照（次要比较）","scale","圣经、预定、圣约、确信、教会、圣礼、安息日、政府：同一信仰在两个传统里的表述。", b)
