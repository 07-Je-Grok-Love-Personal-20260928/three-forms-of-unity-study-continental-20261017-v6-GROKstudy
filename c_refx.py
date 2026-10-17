# -*- coding: utf-8 -*-
"""参考站互证（第二轮）：每个主要部分一个“参考站互证”小节。
规则：① “逐字”行的引文必须是 data/ref/*.txt（抓取副本，空白归一后）的子串，构建时断言；② “转述”行明确标注，并附原页链接；
③ 抓不到的站（opc.org 从箱子超时、prca.org 429）只用 WebFetch／搜索摘录，已在 data/ref/MANIFEST_x.json 与来源页注明。"""
import re,json,html as H,urllib.parse
from core import *
from c_common import *
_MAN=json.load(open("data/ref/MANIFEST_x.json",encoding="utf-8"))
OLD={"ccreformed":("ccreformed.org","https://www.ccreformed.org/our-belief/"),"canrc":("canrc.org","https://canrc.org/beliefs"),"urcna":("urcna.org","https://www.urcna.org/creeds"),
 "heritagereformed":("heritagereformed.com","https://heritagereformed.com/about-the-hrc/doctrinal-standards-and-worship/"),"reformedbeginner":("reformedbeginner.net","https://www.reformedbeginner.net/ecumenical-creeds/"),
 "wts":("wts.edu","https://www.wts.edu/about/mission-values"),"crts":("crts.edu","https://crts.edu/en/intro/")}
SITELAB={"cc":"ccreformed.org","rb":"reformedbeginner.net","urcna":"urcna.org","canrc":"canrc.org","hrc":"heritagereformed.com","crts":"canadianreformedseminary.ca","wts":"wts.edu","opc":"opc.org","prca":"prca.org"}
SCOL={"ccreformed.org":"#d4af37","reformedbeginner.net":"#5aa9e6","urcna.org":"#81b29a","canrc.org":"#e07a5f","heritagereformed.com":"#c9a0dc","canadianreformedseminary.ca":"#6bb8d6","wts.edu":"#f3d98b","crts.edu":"#9fd3c7","opc.org":"#ffb86b","prca.org":"#b0a8d8"}
_T={}
def _txt(k):
    if k not in _T: _T[k]=re.sub(r"\s+"," ",open(f"data/ref/{k}.txt",encoding="utf-8").read())
    return _T[k]
def site_of(k):
    if k in OLD: return OLD[k][0]
    return _MAN[k]["site"]
def url_of(k):
    u=OLD[k][1] if k in OLD else _MAN[k]["url"]
    return urllib.parse.quote(u,safe=":/?=&#%")
def src_a(k): 
    s=site_of(k); return f'<a class="xs" href="{url_of(k)}" target="_blank" rel="noopener" style="--c:{SCOL[s]}">{s}</a>'
def XQ(k,phrase,lang="zh",tr=None):
    assert phrase in _txt(k),f"XQ 未找到：{k}｜{phrase}"
    return f'<q class="xq" lang="{lang}">{H.escape(phrase,quote=False)}</q>'+(f'<small class="tr">{tr}</small>' if tr else "")
def row(kind,k,body,use,lang="zh",tr=None):
    """kind: q 逐字 / p 转述。q：body=原文片段（逐字）；p：body=转述（本站语言，须附原页）。"""
    if kind=="q": cell=f'<i class="tg q">逐字</i>'+XQ(k,body,lang,tr)
    else:
        assert _txt(k)
        cell=f'<i class="tg p">转述</i><span class="pp">{body}</span>'
    return [src_a(k),cell,use]
def corro(id,title,intro,rows,tail=""):
    cnt={}
    for r in rows: cnt[re.search(r'>([^<]+)</a>',r[0]).group(1)]=cnt.get(re.search(r'>([^<]+)</a>',r[0]).group(1),0)+1
    chips="".join(f'<span class="xch" style="--c:{SCOL[s]}"><i></i>{s}<b>×{n}</b></span>' for s,n in cnt.items())
    nq=sum(1 for r in rows if 'class="tg q"' in r[1])
    t=table(["来源（点开原页）","原话（逐字）／转述","本站怎么用"],rows,"cmp xqt xrt")
    return L2(id,"?",title,f'<p>{intro}</p><div class="xchips reveal" aria-label="本节引用来源">{chips}<span class="xch tot"><i></i>共 {len(rows)} 条 · 逐字 {nq} · 转述 {len(rows)-nq}</span></div>'+t+tail)

W=lambda s:s
def part_rows(part):
    R=[]; a=R.append
    if part=="bible":
        a(row("q","ccreformed","作为基督教会，我们的根基文件是圣经，是上帝默示无谬误的话语","根基是圣经、信条从属——与本站“先整本圣经，后逐条”的读法一致。"))
        a(row("q","urcna_beliefs","fully committed to the Bible in its entirety as the Word of God written, without error in all its parts","URCNA：把整本圣经当作神所写的话；三项联合信条是对它的“历史性”概括。","en","大意：完全委身于圣经的全部——它是神所写的话，各部分没有错误。（本站译）"))
        a(row("q","rb_faith","忠心总结了圣经的教义系统","改革宗初学者《认信声明》：三联合信条“忠心总结了圣经的教义系统”——“总结”二字，正是本站把三份文件放在整本圣经之后来读的理由。"))
        a(row("q","rb_sacramental","福音自《创世记》至《启示录》乃是一个","整本圣经只有一个福音：本站 1.2 的四幕、1.3 的圣约线索，都是这一句的展开。"))
        a(row("q","rb_republication","改革宗普遍认同摩西之约是恩典之约的一种施行方式","圣约的“统一与多样”：摩西之约是恩典之约的一种施行方式。该文接着说，如何描述它与行为之约的关系在改革宗内部有争议——所以本站把“三约”标为后世归纳。"))
        a(row("q","hrc_biblical","Scripture alone remains the living voice of God to the church today","传统不同、结论一致：圣经唯独。信条是回应，不是第二个启示。","en","大意：圣经单独仍是神今天向教会说话的活的声音。（本站译）"))
        a(row("q","crts_welcome","your Word is my lamp","CRTS 校训出自诗119:105；神学院的全部教学“以神无误的话为光”——整本圣经先于一切条文。","en","大意：你的话是我的灯。（本站译）"))
    elif part=="hc":
        a(row("q","rb_threeforms","《海德堡要理问答》（1563年）是有史以来最受人珍爱的要理问答之一","改革宗初学者对 HC 地位的判断；与 CCI 的“最有影响力”的说法同向。"))
        a(row("q","rb_threeforms","普法尔茨是当时德国路德宗和罗马天主教领土内少数几个信奉加尔文主义的地区之一","地理：改革宗的普法尔茨被路德宗与天主教领地包围——印证本站 2.3 的区域描述。"))
        a(row("q","rb_threeforms","传统上认为，乌尔西努和奥利维亚努是这份新要理问答的共同作者","作者归属用“传统上认为”——本站同样标“约”。该页还说奥利维亚努的作用“可能并没有早期学者所认为的那么重要”。"))
        a(row("q","rb_threeforms","这样就可以在一年的时间里，在主日的讲堂将整个要理问答讲解完毕","52 主日的用途。注意：该页此处把“主日”误写作“52问”，本站以 CCI 为准——52 个主日、129 问。"))
        a(row("q","canrc_worship","In one of the services, usually the afternoon service, the Heidelberg Catechism is used as a guideline for the preaching.","加拿大归正教会至今下午崇拜按 HC 讲道——本站 2.12。","en","大意：在其中一次崇拜（通常是下午）里，以海德堡要理问答作为讲道的指引。（本站译）"))
        a(row("q","cc_doctrinal","每个主日的一次敬拜中，牧师应照常宣讲按《三项联合信条》所总结的圣道，应着重于依主日次序教导《海德堡要理问答》","URCNA《教会章程》第40条（经恩约教会页面转载），与 CCI 所载教会规章第52条同一精神：按主日次序教 HC。"))
        a(row("q","urcna_heidelberg","How many things must you know to live and die in the joy of this comfort?","问2的英文（URCNA）：三件必知之事。这句也是整部 HC 的“目录”。","en","大意：要在这安慰中喜乐地生与死，你必须知道几件事？（本站译）"))
        a(row("q","urcna_heidelberg","That I am not my own","问1的英文关键词，可当英文记忆钩（URCNA 译本）。","en","大意：我不属于自己。（本站译）"))
        a(row("q","cc_youth","问答 1、2、21、26、27、28、60、69、75、86、116","恩约教会青少年宣信要求背诵的 HC 问答——本站在对应主日上标“宣信必背”小标签（主日1、7、9、10、23、26、28、32、45）。"))
        a(row("q","rb_justification","信心是称义的工具，并非由于信心本身有特别之功德，而是因为藉着信心，罪人的目光从自身移到基督身上，并接受基督完美之义的归算","对读主日23（问60–61）：信心是“手”，不是“功”；该页同时把 HC、BC、Dort 与威斯敏斯特的条文并列。"))
        a(row("q","rb_extra","加尔文主义分外说主张：基督既在其人性中真实地道成肉身，同时又作为圣父的永恒之道（Logos）而超越其人性","对读主日18（问47–48）：人性在天、神性无处不在——即所谓“加尔文主义分外说”（extra Calvinisticum）。"))
        a(row("q","rb_afterdeath","我们说它们拥有生命和知觉","对读主日22（问57）：死后灵魂不是“沉睡”——加尔文早年（《论灵魂的沉睡》）对重洗派说的话。"))
        a(row("q","rb_means","这种新式做法是个人的而非公共的，主观的而非客观的","对读主日25、28：圣礼是基督所设立、在教会中公共施行的“蒙恩之道”——与随己意发明的“个人圣餐”相对。"))
        a(row("q","rb_sacramental","无论在救赎历史的哪个阶段，圣礼都是上帝所设立的方式，用以确认祂救恩的应许，并藉此与祂的百姓相交","对读主日26–27：旧约割礼与新约洗礼同一“记号与印证”的功能（问74）。"))
    elif part=="bc":
        a(row("q","rb_threeforms","《比利时信条》是三联合信条里最古老的文件","时间坐标：1561 最先。"))
        a(row("q","rb_threeforms","是为了反抗这残酷的镇压，并向逼迫者证明改革宗信徒并非如被指控那样是暴徒","BC 为什么写：向逼迫者证明“我们不是暴徒”——与本站 3.5、BC 36 的写作处境一致。"))
        a(row("q","rb_threeforms","背受鞭笞，舌被刀割，嘴遭封堵，身投火海","该页引述的请愿书誓词：宁受酷刑也不否认信条的真理（1562年随信条呈给腓力二世）。"))
        a(row("q","rb_threeforms","1567年，古伊多·德·布利亲身应验了他所描述的殉道之死","作者的结局——信条是用生命签署的。"))
        a(row("q","rb_threeforms","德·布利的作品并不是加尔文作品的翻版，而是一部独立写作的作品","与法国信条的关系：借鉴而非翻版。"))
        a(row("q","prca_search","This is historically the first of our three forms of unity, having been composed in 1561.","PRCA（北美改革宗新教教会）自己的说法同样把 BC 放在三项联合信条之首。（prca.org 对箱子返回 429，此为搜索摘录，不是全文抓取。）","en","大意：这在历史上是我们三项联合信条的第一份，写于 1561 年。（本站译）"))
        a(row("q","crts_history","gave an inaugural address entitled “The Catholicity of the Belgic Confession.”","加拿大归正教会神学院 1969 年开学典礼，首任院长的演讲题目——BC 的“大公性”（catholicity）正是本站 BC 9、27 的主题。","en","大意：（首任院长 J. Faber）作了题为《比利时信条的大公性》的就职演讲。（本站译）"))
        a(row("q","canrc_history","The key confessional documents of these Reformed Churches were the Belgic Confession, first published in 1561, and the Heidelberg Catechism, first published in 1563.","加拿大归正教会的历史叙述：BC 1561，HC 1563。","en","大意：这些改革宗教会的主要信条文件，是 1561 年首次出版的比利时信条和 1563 年首次出版的海德堡要理问答。（本站译）"))
        a(row("q","cc_subscription","殷勤地教导并忠实地捍卫上述教义","《签署书》：牧师、长老、执事签署 BC 与 HC，并承诺“殷勤地教导并忠实地捍卫”——BC 不只是被读的文件，是被承诺守卫的文件。"))
        a(row("p","rb_bc","改革宗初学者站收录的 BC 中译本注明：由王一牧师依 URCNA 2018 年英译修订。","本站正文取 CCI《赞美手册》版，两个译本措辞可能不同，所以本站不混用，凡引中文都以 CCI 为准。"))
    elif part=="dort":
        a(row("q","rb_threeforms","虽然这是荷兰改革宗教会的全国总会，但它也具有国际性质，因为它还包括来自8个国家的26名代表","“国际会议”的规模：8 国、26 名外国代表（本站 4.4 的外国代表地图）。"))
        a(row("q","canrc_history","attended also by delegates from England, Scotland, Germany and Switzerland, the teachings of Arminius were refuted and the sovereignty of God’s grace was maintained","加拿大归正教会的概括：外国代表、驳斥亚米念、守住“神恩典的主权”。","en","大意：（会议）也有英格兰、苏格兰、德国与瑞士的代表出席，亚米念的教导被驳斥，神恩典的主权得以持守。（本站译）"))
        a(row("q","rb_threeforms","这些缩略的短语并没有捕捉到这些教义的长阔高深","对 TULIP 的提醒：口诀好记，却不等于信经本身——这正是本站 4.5 把 TULIP 标为“后来的说法”的理由。"))
        a(row("q","hrc_doctrine","the so-called “Five Points of Calvinism” as formulated by the Synod of Dort, now commonly known by their acronym, TULIP","Heritage Reformed 的写法：把五点与 Dort 相连并用 TULIP 概括——两种态度（善用／提醒）并存。","en","大意：所谓“加尔文主义五要点”，由多特会议拟定，现在通称缩写 TULIP。（本站译）"))
        a(row("q","prca_search","Because the Canons are an answer to the Five Points of the Remonstrance, they set forth only certain aspects of the truth rather than the whole body of the truth, as do our other confessions.","PRCA：Dort 是对五点抗辩的回答，只讲部分真理。（prca.org 429，搜索摘录。）","en","大意：因为信经是对抗辩派五点的回答，它只阐明真理的某些方面，而不像我们其他信条那样阐明全部。（本站译）"))
        a(row("q","prca_search","so that in our Canons the truth is defined negatively as well as positively","“正反两面”：每项后附“错谬反驳”，真理既正面陈述，也负面界定——对应本站 4.7。（搜索摘录。）","en","大意：这样，我们的信经里真理既被正面也被负面地界定。（本站译）"))
        a(row("q","rb_threeforms","信经也有它的局限性，因为它们并未涵盖全部的教义，而是集中在有争议的五项教义上","同一提醒：Dort 不是“全部神学”。"))
        a(row("q","rb_threeforms","上帝从来不离弃祂的选民","第五项的核心句（该页概括）：保守的主体是神。"))
        a(row("q","cc_justification","认为一个人可以因参与圣约恩典的外在施行而被历史性、条件性地选召、重生、与基督有救恩的联合、称义并被收纳为神的儿女，但却可以因缺乏圣约忠信而失去这些救恩益处","URCNA 2007 年谢勒维尔总会所驳斥的错误之一，条文注明依据“《多特信经》I、V”——Dort 在今天仍被用来界定“圣约”讲法的边界。"))
    elif part=="compare":
        a(row("q","cc_doctrinal","皆以因为（quia）信条与神的话相符为由，签署三项信条","“因为”（quia）而不是“只在……范围内”：签署的理由是信条与神的话相符。（本站补充：与之相对的拉丁词 quatenus 不在该页中。）"))
        a(row("q","cc_doctrinal","「同意本宗派信条」不同于 签署信条","区别：职员“签署”，会员“同意”。这是三项联合信条“怎样联合教会”的两个层级。"))
        a(row("q","urcna_about","they are statements of unity that show the world the biblical truths we love","三项联合信条的目的：是“合一的陈述”，不是用来分裂。","en","大意：它们是合一的宣告，向世界显明我们所爱的圣经真理。（本站译）"))
        a(row("q","urcna_about","we also fully confess and acknowledge the truths found in three documents of the Reformation, namely the Belgic Confession (1561), the Heidelberg Catechism (1563) and the Canons of Dort (1618-19)","年份与顺序与本站口诀“信条1561 · 问答1563 · 多特1618–19”一致。","en","大意：我们也完全承认三份宗教改革文件所含的真理，即比利时信条（1561）、海德堡要理问答（1563）、多特信经（1618–19）。（本站译）"))
        a(row("q","canrc_history","they did not wish to be bound by theological formulations beyond the Three Forms of Unity","加拿大归正教会的自我叙述：不愿被捆绑在三项联合信条之外的神学表述里——信条既是共同的基础，也是共同的边界。","en","大意：他们不愿被约束于三项联合信条之外的神学表述。（本站译）"))
        a(row("q","canrc_unity","Federative unity with the United Reformed Churches of North America is currently being pursued","三项联合信条的实际用处：不同联会之间谋求联合时的“共同语言”（该页所述，截至抓取日）。","en","大意：正在寻求与北美联合改革宗教会的联邦式合一。（本站译）"))
        a(row("q","rb_chalcedon","确定了“基督神人二性一位”的标准说法","reformedbeginner.net 把迦克墩定义列为第四份“大公信经”；本站“三大信经”遵循 CCI 与 BC 9，不含它，但 BC 19 的“二性一位”与此一致。"))
    elif part=="west":
        a(row("q","opc_confessions","Officers in the Orthodox Presbyterian Church take a vow to “sincerely receive and adopt” these confessional documents “as containing the system of doctrine taught in the Holy Scriptures.”","OPC 的职员誓词：接受威斯敏斯特标准为“圣经所教导的教义体系”。对照欧陆的《签署书》（5.6）：两条线都是“职员签署／起誓”，对象不同。","en","大意：OPC 职员发誓“诚心接受并采纳”这些信仰文件为“圣经所教导的教义体系”。（本站译）"))
        a(row("q","opc_confessions","(the Bible itself being the only infallible rule of faith and practice)","同样是“次要标准”的说法：圣经本身才是唯一无误的准则。","en","大意：（圣经本身是信仰与生活唯一无误的准则）。（本站译）"))
        a(row("q","rb_westminster","威敏斯特信仰告白和大、小要理问答被许多改革宗宗派和长老宗宗派采纳作为教义准则","威斯敏斯特标准在许多改革宗与长老宗宗派中是教义准则——本站只作“次要比较”。"))
        a(row("q","canrc_unity","Orthodox Presbyterian Church","加拿大归正教会的姊妹教会清单里含 OPC 与 URCNA（该页所列）——欧陆与英语长老会两条线在教会关系上有交叉。","en"))
        a(row("q","crts_who","as summarized in the ecumenical creeds and the Belgic Confession, the Heidelberg Catechism, and the Canons of Dort","神学院的基础声明：欧陆神学院以古代信经加三项联合信条为信仰基础；作对照：WTS 的基础是威斯敏斯特标准（见 6.8）。","en","大意：（CRTS 服从）古代信经与比利时信条、海德堡要理问答、多特信经所概括的无误之神的话。（本站译）"))
    elif part=="creedsx":
        a(row("q","rb_apostles","并非因为是使徒亲自所作，而是因为其简要地总结了使徒的教导","使徒信经的名字由来：不是使徒所作，而是总结使徒的教导。"))
        a(row("q","rb_apostles","今天我们手上的形式，成型时期不晚于四世纪","现行文本的成型：不晚于四世纪（该站说法）。"))
        a(row("q","rb_nicene","是初代基督教会，为抵挡以亚流主义为代表的诸多异端思想，所制定的正统信仰宣言","尼西亚信经为什么写：抵挡亚流主义。"))
        a(row("q","rb_nicene","西方教会在圣灵从父与子出来这句话中坚持保留「和子」这两个字","「和子」（filioque）之争：东西方的唯一重要分歧；CCI 文本含这一句（见 10.3 的说明）。"))
        a(row("q","rb_athanasian","信经作者不详，但目前的文本形式可追溯到不早于第六世纪","亚他那修信经：作者不详——与本站标“推测，非定论”的态度一致。"))
        a(row("q","rb_athanasian","信经由两大部分组成，第一部分阐述了正统的三位一体教义（3-28节），第二部分主要处理道成肉身和基督神人二性的教义（29-43节）","对照本站 10.4：该页分到第 43 节，CCI 正文只有 42 点，本站已在 10.4 标出编号差异，背诵版以 CCI 为准。"))
        a(row("q","urcna_apostles","See Heidelberg Catechism, Q&A 44; Canons of Dort, 2.4.","URCNA 在“降在阴间”处加的脚注：指向 HC 44 与 Dort 2.4——三项联合信条与古代信经的现成接口。","en","大意：参见海德堡要理问答问44；多特信经 2.4。（本站译）"))
        a(row("q","urcna_nicene","“Catholic” means universal; that is, there is one church across all times, places, and peoples (Belgic Confession, art. 27; Heidelberg Catechism, Q&A 54).","“公”＝普世：脚注指向 BC 27 与 HC 54。","en","大意：“大公”意即普世，也就是跨越一切时代、地方与民族的一个教会。（本站译）"))
        a(row("q","rb_chalcedon","确定了“基督神人二性一位”的标准说法","迦克墩定义（该站列为第四份）：本站附录不收，但其“二性一位”是亚他那修信经第 34–37 点的发展。"))
    elif part=="memory":
        a(row("q","cc_youth","背诵并基本理解使徒信经、主祷文、以及十诫，以及圣经书卷名称","恩约教会的青少年宣信：背诵清单——使徒信经、主祷文、十诫、书卷名；本站“背诵版”与记忆页正是为此。"))
        a(row("q","cc_youth","背诵并基本理解缩写恩典教义 TULIP 的五大要素","该教会连 TULIP 也列入背诵——本站标注：TULIP 是后来的口诀，Dort 原文才是依据。"))
        a(row("q","cc_youth","问答 1、2、21、26、27、28、60、69、75、86、116","HC 的“背诵优先级”：11 个问答——本站 11.7 与 2.8 已在对应主日标出。"))
        a(row("q","cc_sundayschool","结合相关经文，帮助学生将要理问答中的问题和答案应用到当今年轻人面临的挑战中","主日学的做法：HC 要“结合经文”并“应用到今天的挑战”——本站每个主日的“应用”行与此同向。"))
        a(row("q","cc_sundayschool","重点讲解《比利时信条》","高中班：长老重点讲 BC——说明 BC 在教会教导里仍是“青年人的护教基础”。"))
    return R
TITLES={"bible":("参考站互证：整本圣经与总结性信条","本部分只用页面上<b>真实读到</b>的话；逐字引文在生成网页时断言为抓取副本（<code>data/ref/</code>）的子串。"),
 "hc":("参考站互证：HC 在各教会怎样被使用与理解","来自 ccreformed.org、reformedbeginner.net、urcna.org、canrc.org 等的原话（逐字）与转述，均附原页链接。"),
 "bc":("参考站互证：BC 的写作处境与今日使用","同上：逐字行必为抓取页面子串；转述行有标注。prca.org 对箱子返回 429，只用搜索摘录。"),
 "dort":("参考站互证：Dort 的会议、五点与口诀","同上；对 TULIP 并列“善用”与“提醒”两种态度，由读者自己判断。"),
 "compare":("参考站互证（续）：签署、同意与联合","补充 5.9：多读了 ccreformed.org 的《教义委身程度报告》与《签署书》等页面。"),
 "west":("参考站互证：OPC 与威斯敏斯特标准的页面说法","opc.org 对箱子超时（198.18.0.1），改用 WebFetch：页面正文与所选问答已存为 <code>data/ref/opc_*.txt</code>（只含所选段落，不是全文）。"),
 "creedsx":("参考站互证：三大信经的来历与注脚","来自 reformedbeginner.net 与 urcna.org 的说明与脚注。"),
 "memory":("参考站互证：教会实际要求背什么","ccreformed.org 的青少年宣信与主日学页面。")}
def l2(part):
    t,i=TITLES[part]
    return corro("rx-"+part,t,i,part_rows(part))
# ---- HC 52 主日：宣信必背标记（来自 ccreformed.org/youth-profession）----
YOUTH_Q=[1,2,21,26,27,28,60,69,75,86,116]
assert XQ("cc_youth","问答 1、2、21、26、27、28、60、69、75、86、116")
YOUTH_LD=sorted({HCLD[q] for q in YOUTH_Q})
def youth_chip(n):
    qs=[q for q in YOUTH_Q if HCLD[q]==n]
    return f'<span class="ychip" title="恩约教会青少年宣信要求背诵：问{"、".join(map(str,qs))}（ccreformed.org/youth-profession）">📖 宣信必背·问{"、".join(map(str,qs))}</span>' if qs else ""

def manifest_l2():
    rows=[]
    for k,v in sorted(_MAN.items(),key=lambda kv:(kv[1]["site"],kv[0])):
        n=v.get("chars"); how=v["how"]
        rows.append([f'<a class="xs" href="{url_of(k)}" target="_blank" rel="noopener" style="--c:{SCOL[v["site"]]}">{v["site"]}</a>',f'<code>data/ref/{k}.txt</code>',(f"{n} 字" if n else "摘录"),how])
    t=table(["站点（点开原页）","抓取副本","大小","取得方式"],rows,"cmp xrm")
    return L2("src-refx","?","本轮新增的参考站抓取副本（共 %d 份）"%len(rows),"<p>以下文本存于仓库 <code>data/ref/</code>，页面里“逐字”引文在生成网页时必须是它们的子串（空白归一后）。“摘录”＝只保存所选段落：opc.org 对箱子超时（解析到 198.18.0.1），改用 WebFetch；prca.org 返回 429，仅有搜索摘录；不是全文抓取。</p>"+t)
