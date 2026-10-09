"""
Single source of truth for every Threat-Intel challenge's questions.

Each question is (text, [accepted answers...], "where the answer is").
Matching is case-insensitive and ignores URL noise, defanging, quotes and trailing dots
(see engine.go.tmpl), so only list answers that differ in substance or spelling.

After editing, run:  python3 tools/gen.py
That regenerates every <name>_asker.go and WALKTHROUGH.md.
"""

CHALLENGES = [
    dict(
        dir="applejeus", gofile="applejeus_asker.go",
        banner="Hello future Threat Hunter. Someone at a crypto exchange downloaded 'trading software'. Look in the right places.",
        sources={
            "S1": ("Kaspersky GReAT - Operation AppleJeus (Aug 2018)", "https://securelist.com/operation-applejeus/87553/"),
            "S2": ("Kaspersky GReAT - Operation AppleJeus Sequel (Jan 2020)", "https://securelist.com/operation-applejeus-sequel/95596/"),
            "S3": ("US-CERT/CISA - HIDDEN COBRA: FALLCHILL (TA17-318A, Nov 2017)", "https://www.cisa.gov/news-events/cybersecurity-advisories/aa17-318a"),
            "S4": ("MITRE ATT&CK - Lazarus Group (G0032)", "https://attack.mitre.org/groups/G0032/"),
        },
        solution=(
            "The description (crypto exchange, trojanized all-in-one trading app, valid signature, Kaspersky GReAT) "
            "leads to *Operation AppleJeus* on Securelist (S1). S1 answers most questions. It mentions US-CERT's "
            "reporting on Fallchill, which leads to the government alert (S3). The Telegram question requires the "
            "2020 follow-up (S2), because APT reporting is often a series, not a single article.\n\n"
            "Changes from the first draft: removed 'TA0011 = Command and Control' (generic ATT&CK trivia, not about "
            "this operation) and 'what was the goal: Cryptocurrency' (answerable from the description alone). "
            "Added the alternate spellings the reports themselves use."
        ),
        questions=[
            ("Kaspersky published a report on this operation. What is the full link to that report?",
             ["https://securelist.com/operation-applejeus/87553/"], "S1 URL (scheme, www and trailing slash optional)"),
            ("What name did Kaspersky give to this operation? (without the word 'Operation')",
             ["AppleJeus"], "S1 - title"),
            ("Which APT group is behind this operation? (one word)",
             ["Lazarus"], "S1 - title / Overview"),
            ("What country is this APT group believed to originate from?",
             ["North Korea", "DPRK", "Democratic People's Republic of Korea"], "S4 (S1 does not name the country)"),
            ("What is the name of the fake company that distributed the trojanized cryptocurrency trading application?",
             ["Celas Limited", "Celas LLC", "Celas"], "S1 - 'Celas Trade Pro from Celas Limited' / 'Celas LLC'"),
            ("What was the name of the trojanized all-in-one trading application itself?",
             ["Celas Trade Pro", "CelasTradePro"], "S1 - 'Trojanized trading application for Windows'"),
            ("What previously-known Lazarus malware family was delivered as the final payload?",
             ["Fallchill"], "S1 - Overview / 'Fallchill backdoor loader'"),
            ("In what year did Kaspersky first publish its report on Operation AppleJeus?",
             ["2018"], "S1 - dated 23 Aug 2018"),
            ("Which other security agency published about Fallchill? (format: XX-XXXX)",
             ["US-CERT"], "S1 - 'including one from US-CERT'; S3"),
            ("In what year did that agency publish its report on Fallchill?",
             ["2017"], "S3 - November 2017"),
            ("This was the first time Kaspersky observed Lazarus distributing malware for which operating system?",
             ["macOS", "mac os", "OS X", "osx"], "S1 - Overview"),
            ("What is the MITRE ATT&CK Group ID assigned to Lazarus Group?",
             ["G0032"], "S4"),
            ("In the 2019/2020 'sequel' AppleJeus operation, what messaging app did Lazarus start abusing as a delivery vector?",
             ["Telegram"], "S2 - 'Windows version of UnionCryptoTrader'"),
            ("On the Windows side, what file name did the FallChill-delivering payload use inside C:\\Recovery\\ ?",
             ["msn.exe"], "S1 - 'Downloaded payload' (Known file name: C:\\Recovery\\msn.exe)"),
        ],
    ),

    dict(
        dir="slingshot", gofile="slingshot_asker.go",
        banner="Hello future Threat Hunter. Your network admin found something weird living inside a router. Look in the right places.",
        sources={
            "S1": ("Kaspersky - The Slingshot APT FAQ (9 Mar 2018)", "https://securelist.com/apt-slingshot/84312/"),
        },
        solution=(
            "The description paraphrases the first sentence of Kaspersky's *Slingshot APT FAQ* (S1): suspected "
            "keylogger, virtual file system, routers. Every answer is in S1. Players need to separate the infection "
            "vector (MikroTik router -> Winbox Loader -> ipv4.dll) from the implant architecture (Cahnadr/Canhadr "
            "kernel module + GollumApp).\n\n"
            "Changes from the first draft: removed the ChimayRed question. S1 says the router exploitation method "
            "'is not yet clear', so that answer was speculation no source supports. 'Yemen' is now accepted alongside "
            "'Kenya' (S1: 'Kenya and the Yemen account for most of the victims'). The kernel module's alternate spellings "
            "are accepted because S1 itself uses both 'Cahnadr' and 'Canhadr' (aka NDriver). The 'Security Analyst Summit' "
            "wording was removed from the year question because S1 doesn't mention SAS."
        ),
        questions=[
            ("Which router manufacturer's devices were abused as the initial infection vector?",
             ["MikroTik"], "S1 - intro"),
            ("What is the name of the malicious DLL planted on the router that acted as a downloader for the rest of the toolset?",
             ["ipv4.dll"], "S1 - 'How exactly does infection happen?'"),
            ("What legitimate MikroTik management software unknowingly downloads and loads this DLL onto the victim's computer?",
             ["Winbox Loader", "Winbox", "WinboxLoader"], "S1 - 'How exactly does infection happen?'"),
            ("What is the name of Slingshot's kernel-mode module?",
             ["Cahnadr", "Canhadr", "NDriver"], "S1 - 'How exactly does infection happen?' (both spellings used)"),
            ("What is the name of Slingshot's user-mode module, which alone contains nearly 1,500 functions?",
             ["GollumApp", "Gollum App"], "S1 - same section"),
            ("In what year did Kaspersky publicly reveal the Slingshot campaign?",
             ["2018"], "S1 - dated 09 Mar 2018"),
            ("Name one of the two African/Middle Eastern countries where most Slingshot victims were found.",
             ["Kenya", "Yemen", "the Yemen"], "S1 - 'What is the victim profile and target geography?'"),
            ("According to Kaspersky's analysis, in what year was the very first Slingshot sample detected - years before the campaign was publicly disclosed?",
             ["2012"], "S1 - 'When was Slingshot active?' (earliest sample compiled in 2012)"),
        ],
    ),

    dict(
        dir="zebrocy", gofile="zebrocy_asker.go",
        banner="Hello future Threat Hunter. Someone keeps rewriting the same malware in a different language every year. Look in the right places.",
        sources={
            "S1": ("Kaspersky GReAT - A Zebrocy Go Downloader (Jan 2019)", "https://securelist.com/a-zebrocy-go-downloader/89419/"),
            "S2": ("Kaspersky GReAT - Zebrocy's Multilanguage Malware Salad (Jun 2019)", "https://securelist.com/zebrocys-multilanguage-malware-salad/90680/"),
        },
        solution=(
            "Searching Kaspersky + Delphi/AutoIt malware + diplomatic targets leads to Zebrocy. Two Securelist posts "
            "carry the challenge: the Go downloader post (S1), which also states where 'Masha and these Bears' was "
            "presented (SAS2018, Cancun), and the 'Multilanguage Malware Salad' (S2) for the lineage questions.\n\n"
            "Changes from the first draft:\n"
            "- Removed the Unit 42 question. Its premise was backwards: S1 does not credit Unit 42 with first spotting the "
            "Go variant. It says Unit 42 dated its first detection to 2018-10-11, while Kaspersky had already documented the "
            "same downloader with a first deployment on 2018-05-10.\n"
            "- Fixed the BlackEnergy question. The bootkit that shares kernel code with BlackEnergy belongs to *Delphocy* (S2), "
            "not to Zebrocy.\n"
            "- Removed 'what is the title of the report' (it tests copy-paste, not reading).\n"
            "- The managed-language question now accepts every language S2 lists (Python, C#, Go)."
        ),
        questions=[
            ("Zebrocy is described as a sub-cluster/subgroup of which larger, well-known Russian-speaking APT actor?",
             ["Sofacy", "APT28", "Fancy Bear"], "S1 - 'Attribution' ('a known subset of Sofacy activity')"),
            ("In what year was Zebrocy first introduced as a Sofacy backdoor package?",
             ["2015"], "S1 - first paragraph"),
            ("Kaspersky first publicly discussed Zebrocy at their Security Analyst Summit, in a talk titled 'Masha and these Bears'. In which city was that summit held?",
             ["Cancun", "Cancún"], "S1 - first paragraph ('SAS2018 in Cancun, Mexico')"),
            ("Name the earlier Delphi-based malware family (active 2013-2015) that shares lineage and code artifacts with Zebrocy's own Delphi backdoor.",
             ["Delphocy"], "S2 - 'Zebrocy Delphi backdoor shared artefacts rooted in Delphocy and BlackEnergy'"),
            ("Delphocy's bootkit loader shares unique kernel code with which other well-known malware family?",
             ["BlackEnergy", "Black Energy"], "S2 - same section"),
            ("Besides Delphi and AutoIt, name one of the newer 'managed' programming languages Zebrocy expanded into.",
             ["Go", "Golang", "C#", "CSharp", "C Sharp", "Python"], "S2 - 'new managed languages like Python, C#, and Go'"),
        ],
    ),

    dict(
        dir="bluenoroff", gofile="bluenoroff_asker.go",
        banner="Hello future Threat Hunter. A VC-backed crypto startup just lost its hot wallet. Look in the right places.",
        sources={
            "S1": ("Kaspersky - BlueNoroff introduces new methods bypassing MoTW (Dec 2022)", "https://securelist.com/bluenoroff-methods-bypass-motw/108383/"),
            "S2": ("Kaspersky - The BlueNoroff cryptocurrency hunt is still on (Jan 2022)", "https://securelist.com/the-bluenoroff-cryptocurrency-hunt-is-still-on/105488/"),
            "S3": ("MITRE ATT&CK - APT38 (G0082)", "https://attack.mitre.org/groups/G0082/"),
        },
        solution=(
            "The description's 'no downloaded-from-the-internet warning' points to the December 2022 report on "
            "Mark-of-the-Web bypasses (S1). The group's background (Lazarus link, Bangladesh Bank origin) is in the "
            "intro of the January 2022 SnatchCrypto report (S2), which also tells the 'drained wallet' story from the "
            "description. MITRE (S3) maps BlueNoroff to APT38 and its other vendor names.\n\n"
            "Changes from the first draft: the 'name one impersonated institution' question now accepts every company in "
            "S1's lookalike-domain table instead of only Mitsubishi UFJ. The disk-image question accepts both formats "
            "with or without the dot. The alias question accepts every associated group MITRE lists."
        ),
        questions=[
            ("BlueNoroff is described by Kaspersky as a sub-cluster of which larger threat actor?",
             ["Lazarus", "Lazarus Group"], "S2 - intro ('a unit within a larger formation of Lazarus attackers')"),
            ("BlueNoroff is also tracked under another name by other vendors - name it.",
             ["APT38", "Stardust Chollima", "Nickel Gladstone", "BeagleBoyz", "Sapphire Sleet", "COPERNICIUM"], "S3 - Associated Groups"),
            ("What Windows security feature (usually referred to by a 4-letter abbreviation) did BlueNoroff's new late-2022 delivery techniques bypass?",
             ["MOTW", "Mark-of-the-Web", "Mark of the Web"], "S1 - intro"),
            ("Name one of the two container/disk-image file formats BlueNoroff adopted to evade this protection.",
             ["ISO", ".ISO", "VHD", ".VHD"], "S1 - intro ('.iso' and '.vhd')"),
            ("BlueNoroff's fake domains mostly impersonated venture capital companies and banks located in which country?",
             ["Japan"], "S1 - intro / 'Infrastructure'"),
            ("Historically, BlueNoroff has been linked to a major cyber-heist against a national bank conducted via the SWIFT network. Which bank?",
             ["Bangladesh Bank", "Bangladesh Central Bank", "Central Bank of Bangladesh", "Bank of Bangladesh"], "S2 - intro; S3"),
            ("Name one legitimate financial institution whose name/branding BlueNoroff's fake domains impersonated.",
             ["Mitsubishi UFJ Financial Group", "MUFG", "Sumitomo Mitsui Banking Corporation", "SMBC",
              "Mizuho Financial Group", "Mizuho", "Bank of America", "Beyond Next Ventures", "ANOBAKA",
              "Z Venture Capital", "ABF Capital", "Angel Bridge", "Trans-Pacific Technology Fund"],
             "S1 - 'Infrastructure' table (Genuine company column)"),
        ],
    ),

    dict(
        dir="moonbounce", gofile="moonbounce_asker.go",
        banner="Hello future Threat Hunter. IT reformatted the laptop. It's STILL beaconing. Look in the right places.",
        sources={
            "S1": ("Kaspersky - MoonBounce: the dark side of UEFI firmware (Jan 2022)", "https://securelist.com/moonbounce-the-dark-side-of-uefi-firmware/105468/"),
        },
        solution=(
            "'Survives a disk wipe' + 'Kaspersky Firmware Scanner' leads to MoonBounce (S1), which answers every "
            "question: the implant lives in CORE_DXE on the SPI flash, hooks EFI Boot Services, and injects into "
            "svchost.exe once Windows boots.\n\n"
            "Changes from the first draft: the Boot Services question listed all three functions and then accepted only "
            "AllocatePool. It now lists none and accepts all three. The 'earlier bootkits' question now accepts "
            "MosaicRegressor as well as LoJax. Removed the 'Spring 2021' question because S1 contradicts itself "
            "('detected in spring 2021' vs 'made aware... at the end of 2021'), so no answer is unambiguous."
        ),
        questions=[
            ("What type of firmware does this implant infect (4-letter acronym)?",
             ["UEFI"], "S1 - title / 'What happened?'"),
            ("Name the specific firmware component the implant modifies, which is invoked early in the UEFI boot sequence.",
             ["CORE_DXE", "CORE DXE", "DXE Foundation"], "S1 - 'Our discovery'"),
            ("On what physical storage location on the motherboard is the implant actually written?",
             ["SPI flash", "SPI", "SPI flash memory"], "S1 - 'What happened?'"),
            ("Which Kaspersky product feature/component first detected this implant's activity?",
             ["Firmware Scanner", "Kaspersky Firmware Scanner"], "S1 - 'What happened?'"),
            ("Name one of the three EFI Boot Services functions the implant hooks.",
             ["AllocatePool", "CreateEventEx", "ExitBootServices"], "S1 - 'Our discovery'"),
            ("Into which legitimate Windows process does the implant inject its user-mode payload during boot?",
             ["svchost.exe", "svchost"], "S1 - 'Our discovery'"),
            ("This was the third known UEFI firmware implant found in the wild. Name one of the two earlier ones.",
             ["LoJax", "MosaicRegressor"], "S1 - 'Revisiting the current state of the art'"),
            ("Kaspersky attributed this implant with considerable confidence to which Chinese-speaking threat actor?",
             ["APT41", "APT 41"], "S1 - 'Who is behind the MoonBounce attack?'"),
        ],
    ),

    dict(
        dir="triangulation", gofile="triangulation_asker.go",
        banner="Hello future Threat Hunter. Kaspersky found this one on their own phones. Look in the right places.",
        sources={
            "S1": ("Kaspersky - Operation Triangulation: iOS devices targeted with previously unknown malware (Jun 2023)", "https://securelist.com/operation-triangulation/109842/"),
            "S2": ("Kaspersky - Dissecting TriangleDB, a Triangulation spyware implant (Jun 2023)", "https://securelist.com/triangledb-triangulation-implant/110050/"),
            "S3": ("Kaspersky - Two more Triangulation pieces: validators and modules (Oct 2023)", "https://securelist.com/triangulation-validators-modules/110847/"),
            "S4": ("Kaspersky - Operation Triangulation: The last (hardware) mystery (Dec 2023)", "https://securelist.com/operation-triangulation-the-last-hardware-mystery/111669/"),
        },
        solution=(
            "This challenge spans a series of Securelist articles (all tagged 'Operation Triangulation'). The first "
            "article (S1) covers the discovery via KUMA, iMessage delivery, the 2019 start date and the 2023 disclosure. "
            "The implant write-up (S2) covers TriangleDB. The validators article (S3) is where the yellow-triangle canvas "
            "fingerprint, and therefore the campaign's name, is explained. The 37C3 write-up (S4) lists the full exploit "
            "chain with its CVEs and the MMIO hardware feature.\n\n"
            "Changes from the first draft: the old walkthrough said KUMA and the canvas fingerprint were in the 'last "
            "hardware mystery' article. KUMA is in S1, and the canvas fingerprint is only in S3, which the old challenge "
            "never pointed to. The INDEX now lists S3 instead of the 'catching a wild triangle' article, which none of "
            "the answers need."
        ),
        questions=[
            ("What internal Kaspersky monitoring platform first flagged the anomalous traffic on their own corporate Wi-Fi network? (spell out the acronym or give the acronym)",
             ["KUMA", "Kaspersky Unified Monitoring and Analysis Platform"], "S1 - attack overview"),
            ("What is the name of the core backdoor/implant deployed in this campaign?",
             ["TriangleDB"], "S2"),
            ("What Apple messaging application delivered the invisible, zero-click initial exploit attachment?",
             ["iMessage"], "S1 - attack overview"),
            ("What CVE number covers the remote code execution vulnerability in Apple's undocumented ADJUST TrueType font instruction?",
             ["CVE-2023-41990"], "S4 - attack chain rundown"),
            ("What web-based fingerprinting technique, which draws a specific shape on the page to uniquely identify victims and gave the whole campaign its name, was used?",
             ["Canvas fingerprinting", "Canvas"], "S3 - 'JavaScript Validator'"),
            ("Since what year has this campaign reportedly been active, according to Kaspersky's investigation?",
             ["2019"], "S1 - 'The oldest traces of infection that we discovered happened in 2019'"),
            ("In what year was this campaign publicly disclosed by Kaspersky?",
             ["2023"], "S1 - dated June 2023"),
            ("What 4-letter acronym describes the type of undocumented hardware feature (memory-mapped I/O registers) in Apple's chips that the attackers abused to bypass hardware memory protections?",
             ["MMIO"], "S4 - attack chain rundown"),
            ("What CVE number is the kernel vulnerability used to escalate to root privileges?",
             ["CVE-2023-32434"], "S4 - attack chain rundown"),
        ],
    ),

    dict(
        dir="sunburst", gofile="sunburst_asker.go",
        banner="Hello future Threat Hunter. A routine software update turned out to be anything but routine. Look in the right places.",
        sources={
            "S1": ("Mandiant/FireEye - Highly Evasive Attacker Leverages SolarWinds Supply Chain to Compromise Multiple Global Victims With SUNBURST Backdoor (13 Dec 2020)", "https://cloud.google.com/blog/topics/threat-intelligence/evasive-attacker-leverages-solarwinds-supply-chain-compromises-with-sunburst-backdoor"),
            "S2": ("Mandiant - Assembling the Russian Nesting Doll: UNC2452 Merged into APT29 (Apr 2022)", "https://cloud.google.com/blog/topics/threat-intelligence/unc2452-merged-into-apt29"),
        },
        solution=(
            "IT monitoring platform + signed update + 'the company that discovered it got breached itself' leads to "
            "SolarWinds Orion / SUNBURST and FireEye's original post (S1). The UPDATE banner at the very top of S1 says "
            "UNC2452 was merged into APT29 (detailed in S2), which is easy to miss if you skip straight to the body.\n\n"
            "Changes from the first draft: the FireEye question is now first. In the old order, two earlier questions "
            "already said 'FireEye', which gave the answer away. The dormancy question accepts '12-14' and 'two weeks' "
            "too, because S1 says 'up to two weeks' and 'at least 12 to 14 days... selected randomly from an interval'."
        ),
        questions=[
            ("Which cybersecurity company discovered this campaign while investigating the theft of its own internal (red team) tools, disclosed on December 8, 2020?",
             ["FireEye", "Mandiant"], "S1 - authorship / Executive Summary"),
            ("What is the exact file name of the trojanized SolarWinds Orion DLL that contained the backdoor?",
             ["SolarWinds.Orion.Core.BusinessLayer.dll"], "S1 - 'SUNBURST Backdoor'"),
            ("What did FireEye/Mandiant name this trojanized backdoor?",
             ["SUNBURST"], "S1 - Executive Summary"),
            ("What tracking designator did FireEye initially assign to the threat actor behind this campaign?",
             ["UNC2452"], "S1 - Executive Summary"),
            ("In a May 2022 update to their original blog post, Mandiant merged this tracking designator into which well-known, previously-identified APT group?",
             ["APT29"], "S1 - UPDATE (May 2022) banner; S2"),
            ("What is the C2 domain used by the backdoor, resolved via a domain generation algorithm?",
             ["avsvmcloud.com"], "S1 - 'DGA and Blocklists'"),
            ("For roughly how many days did the backdoor lie dormant before it would start retrieving and executing commands?",
             ["14", "12-14", "12 to 14", "two weeks", "2 weeks"], "S1 - 'up to two weeks'; 'Initialization' (12 to 14 days)"),
            ("What is the name of the memory-only second-stage dropper Mandiant documented, used to deploy a Cobalt Strike Beacon?",
             ["TEARDROP"], "S1 - 'TEARDROP and BEACON Malware Used'"),
        ],
    ),

    dict(
        dir="triton", gofile="triton_asker.go",
        banner="Hello future Threat Hunter. This isn't about stolen data. This is about the systems that stop a plant from exploding. Look in the right places.",
        sources={
            "S1": ("Mandiant/FireEye - Attackers Deploy New ICS Attack Framework 'TRITON' (14 Dec 2017)", "https://cloud.google.com/blog/topics/threat-intelligence/attackers-deploy-new-ics-attack-framework-triton"),
            "S2": ("Mandiant/FireEye - TRITON Attribution: Russian Government-Owned Lab Most Likely Built Custom Intrusion Tools (Oct 2018)", "https://cloud.google.com/blog/topics/threat-intelligence/triton-attribution-russian-government-owned-lab-most-likely-built-tools"),
            "S3": ("MITRE ATT&CK - Triton (S1009) and TEMP.Veles (G0088)", "https://attack.mitre.org/software/S1009/"),
            "S4": ("US DOJ - Four Russian Government Employees Charged in Two Historical Hacking Campaigns Targeting Critical Infrastructure (Mar 2022)", "https://www.justice.gov/archives/opa/pr/four-russian-government-employees-charged-two-historical-hacking-campaigns-targeting-critical"),
        },
        solution=(
            "This challenge is about how attribution evolves. Mandiant's original December 2017 report (S1) describes the "
            "malware, the target (Schneider Electric Triconex SIS), the TriStation protocol and the intrusion via an SIS "
            "engineering workstation, but it does *not* attribute the attack to anyone. In October 2018 Mandiant named the "
            "activity TEMP.Veles and tied it to a Russian government-owned institute (S2). MITRE (S3) lists the other names "
            "(TRISIS, HatMan) and Dragos's XENOTIME. The 2022 DOJ release (S4) names the indicted programmer, Gladkikh.\n\n"
            "Author note: no primary source (Mandiant, MITRE, DOJ) names the victim country. DOJ only says 'a foreign "
            "refinery'. 'Saudi Arabia' comes from widespread press coverage and the UK government statement, so players "
            "will find it, but it is the one answer here not backed by a vendor/government report."
        ),
        questions=[
            ("Which vendor's Safety Instrumented System (SIS) did this malware specifically target?",
             ["Schneider Electric", "Schneider"], "S1; S4"),
            ("Name the specific Schneider Electric SIS product line that was targeted.",
             ["Triconex"], "S1 - Introduction"),
            ("What undocumented, proprietary engineering protocol did the attackers have to reverse-engineer in order to talk to the SIS controllers?",
             ["TriStation"], "S1 - 'Attribution' / 'Technical Analysis'"),
            ("In what year did the first publicly known attack using this malware take place?",
             ["2017"], "S1; S4 ('between May and September 2017')"),
            ("In which country did this first publicly known attack take place?",
             ["Saudi Arabia", "KSA"], "Press coverage / UK government statement (not in S1-S4, see note)"),
            ("Besides TRITON and TRISIS, what other name is this malware also known by in ICS security circles?",
             ["HatMan"], "S3 - Associated Software"),
            ("What tracking name does Dragos use for the threat group behind this malware?",
             ["XENOTIME"], "S3 - TEMP.Veles Associated Groups"),
            ("What tracking name does Mandiant/FireEye use for this same threat group?",
             ["TEMP.Veles", "TEMP Veles"], "S2 - Overview"),
            ("Where did the attacker gain the remote access they used to deploy the attack framework and reprogram the SIS controllers?",
             ["SIS engineering workstation", "an SIS engineering workstation", "engineering workstation", "the SIS engineering workstation"],
             "S1 - 'Incident Summary'"),
            ("The US Department of Justice indicted a Russian national linked to the development of this malware. What is his surname?",
             ["Gladkikh"], "S4"),
        ],
    ),

    dict(
        dir="sea-turtle", gofile="seaturtle_asker.go",
        banner="Hello future Threat Hunter. Your server never moved. Your visitors did. Look in the right places.",
        sources={
            "S1": ("Cisco Talos - DNS Hijacking Abuses Trust In Core Internet Service (Apr 2019)", "https://blog.talosintelligence.com/seaturtle/"),
            "S2": ("Cisco Talos - Sea Turtle keeps on swimming (Jul 2019)", "https://blog.talosintelligence.com/sea-turtle-keeps-on-swimming/"),
        },
        solution=(
            "Talos's original Sea Turtle post (S1) answers every question. The follow-up (S2) shows the actor continuing "
            "after disclosure. Note that the URL in the old INDEX (`/dns-hijacking-abuses-trust-in-core-internet-service/`) "
            "is a 404. The post lives at `/seaturtle/`.\n\n"
            "Changes from the first draft: removed 'what infrastructure did it target? DNS' (answered by the description) "
            "and 'exact title of the blog post' (copy-paste, and fragile to match). The CVE question accepts all seven "
            "CVEs Talos lists. The region and registry answers accept natural variants (MENA, 'domain registry' without "
            "'a'). The registry question is still precise about registry vs registrar, which is the point of it."
        ),
        questions=[
            ("Approximately how many organizations did Talos say were compromised during this campaign? Just give the number.",
             ["40"], "S1 - Executive Summary"),
            ("Since what year had this campaign reportedly been active before its public disclosure?",
             ["2017"], "S1 - 'likely began as early as January 2017'"),
            ("Name the Swedish DNS provider that Talos confirmed was compromised as part of this campaign.",
             ["Netnod"], "S1 - 'Credential harvesting with compromised SSL certificates'"),
            ("What region of the world was primarily targeted by this campaign (governments, ministries, energy firms)?",
             ["Middle East and North Africa", "MENA", "Middle East & North Africa", "the Middle East and North Africa"], "S1 - Executive Summary"),
            ("This was the first known case of attackers compromising what type of organization - the entity that manages an entire top-level domain - for cyber-espionage purposes?",
             ["a domain registry", "domain registry", "registry", "a registry", "domain name registry", "a domain name registry"],
             "S1 - 'How is this tradecraft different?'"),
            ("Name one CVE number the actors exploited to initially breach their victims' infrastructure.",
             ["CVE-2009-1151", "CVE-2014-6271", "CVE-2017-3881", "CVE-2017-6736", "CVE-2017-12617", "CVE-2018-0296", "CVE-2018-7600"],
             "S1 - 'Initial access'"),
        ],
    ),

    dict(
        dir="arcanedoor", gofile="arcanedoor_asker.go",
        banner="Hello future Threat Hunter. Even the firewall vendor gets hacked sometimes. Look in the right places.",
        sources={
            "S1": ("Cisco Talos - ArcaneDoor: New espionage-focused campaign found targeting perimeter network devices (Apr 2024, updated Sep 2025)", "https://blog.talosintelligence.com/arcanedoor-new-espionage-focused-campaign-found-targeting-perimeter-network-devices/"),
            "S2": ("Cisco PSIRT - Event Response: Attacks Against Cisco Firewall Platforms", "https://sec.cloudapps.cisco.com/security/center/resources/asa_ftd_attacks_event_response"),
        },
        solution=(
            "Talos's ArcaneDoor post (S1) covers the actor names, both implants and the two CVEs that were used: "
            "CVE-2024-20353 (DoS used to force a reboot) and CVE-2024-20359 (persistent local code execution that loads "
            "Line Runner). The third CVE in the last question is *not* in the Talos post. It comes from Cisco's PSIRT "
            "event-response page (S2), which lists three advisories and says only 20353 and 20359 were used, so players "
            "have to check the vendor advisory page as well as the blog.\n\n"
            "Changes from the first draft: the Line Runner question no longer says 'Lua-based', which gave away a later "
            "answer. The last question no longer claims Talos identified the third CVE. The product question accepts FTD too "
            "(S2: ASA and Firepower Threat Defense).\n\n"
            "Re-verify before the event: S1 got an update on 2025-09-25 about new activity by the same actor "
            "(CVE-2025-20333, CVE-2025-20362, CVE-2025-20363). None of the current answers changed."
        ),
        questions=[
            ("What tracking designator did Cisco Talos assign to the threat actor behind this campaign?",
             ["UAT4356", "UAT-4356"], "S1 - intro"),
            ("What tracking designator did Microsoft Threat Intelligence Center assign to this same actor?",
             ["STORM-1849", "Storm 1849"], "S1 - intro"),
            ("Name one of the two Cisco product lines targeted in this campaign (give the abbreviation).",
             ["ASA", "FTD"], "S1; S2 ('Cisco ASA ... or Cisco Firepower Threat Defense (FTD)')"),
            ("What is the name of the memory-resident, in-memory shellcode-interpreter backdoor used by the actor?",
             ["Line Dancer", "LineDancer"], "S1 - 'Line Dancer: In-Memory Implant Technical Details'"),
            ("What is the name of the persistent backdoor that survives reboots and software upgrades?",
             ["Line Runner", "LineRunner"], "S1 - 'Line Runner: Persistence Mechanism'"),
            ("What CVE number is the denial-of-service vulnerability the actor abused to force a device reboot and trigger the persistent backdoor's installation?",
             ["CVE-2024-20353"], "S1 - 'Line Runner: Persistence Mechanism'"),
            ("What CVE number covers the persistent local code execution flaw abused to install the persistent backdoor?",
             ["CVE-2024-20359"], "S1 - same section"),
            ("The persistent backdoor abuses a legacy capability on the ASA originally meant for pre-loading what type of client software?",
             ["VPN clients", "VPN client", "VPN", "VPN clients and plugins"], "S1 - same section"),
            ("What scripting language does the persistent backdoor's malicious payload get written to and executed in?",
             ["Lua"], "S1 - same section (csco_config.lua, 'HTTP-based Lua backdoor')"),
            ("Cisco's ArcaneDoor event-response page lists a third, related vulnerability that was NOT actually used in this specific campaign. What is its CVE number?",
             ["CVE-2024-20358"], "S2 - advisory table (only 20353 and 20359 'were used')"),
        ],
    ),
]

# Challenge order = difficulty order (easiest first). Ports in docker-compose.yml follow it: 5010, 5011, ...
ORDER = ["sea-turtle", "zebrocy", "slingshot", "moonbounce", "sunburst",
         "bluenoroff", "arcanedoor", "applejeus", "triton", "triangulation"]
CHALLENGES.sort(key=lambda c: ORDER.index(c["dir"]))
