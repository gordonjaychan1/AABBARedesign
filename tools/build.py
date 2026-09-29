#!/usr/bin/env python3
"""Generates the static pages in the repo root. Run: python3 tools/build.py"""
import datetime
import html
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

NAME = "All American Black Belt Academy"
ADDRESS = "21001 San Ramon Valley Blvd, A7, San Ramon, CA 94583"
MAPS = "https://www.google.com/maps/search/?api=1&query=" + ADDRESS.replace(" ", "+")
EMAIL = "Laura.aabba@icloud.com"
PHONE_DISPLAY = "(925) 829-4265"
PHONE_TEL = "+19258294265"
SOCIAL = [
    ("Instagram", "https://www.instagram.com/aabba.karate/"),
    ("Facebook", "https://www.facebook.com/Shitorkaratedo/"),
    ("Yelp", "https://www.yelp.com/biz/all-american-black-belt-academy-san-ramon"),
]


def wix(media_id, w, h=None, name="photo.jpg"):
    """Wix CDN resize URL, so each image is served at the size it is shown."""
    mode = "fill" if h else "fit"
    size = f"w_{w},h_{h or w * 2}"  # fit needs both bounds; the tall box leaves width as the limit
    return f"https://static.wixstatic.com/media/{media_id}/v1/{mode}/{size},al_c,q_75/{name}"


HERO = "5df506_b8bfdcba534349ae95456bb6e8f8b18e~mv2_d_4898_1859_s_2.jpeg"

INSTRUCTORS = [
    ("Master Instructor", "Carl Hultin", "5df506_42faa1f6913e4f999ac68db641080ab6~mv2.jpg", [
        "7th Degree Black Belt, Hayashi-ha Shitoryu Karate-do",
        "3rd Degree Black Belt Kenshin Ryu",
        "2nd Degree Black Belt Yamanni Ryu Kobudo",
        "Vice President, USA National Karate Federation; Member, Referee Council",
        "World Karate Federation Judge",
        "Certified Personal Trainer"]),
    ("Chief Instructor", "Eric Sevilla", "5df506_e34af537edcb429a8396e0f010005024~mv2_d_3464_4618_s_4_2.jpg", [
        "5th Degree Black Belt; 2nd Degree Black Belt Weapons",
        "8-Time National Kata Champion",
        "7-Time National Kumite Champion",
        "USNKF Certified Referee and Coach",
        "Cross-training in Jujitsu",
        "Elite Team Coach",
        "CDC HEADS UP certified in concussion training"]),
    ("Senior Instructor", "Yong Hultin", "5df506_8e3d4574100e49869b3017c63ecc653e~mv2_d_3463_4618_s_4_2.jpg", [
        "4th Degree Black Belt",
        "1st Degree Black Belt in Kenshin Ryu Kobudo",
        "Five-Time National Kata Champion"]),
    ("Senior Instructor", "Jonathan Chin", "5df506_c6a8a306e56449c9a99b4b4d6706555b~mv2_d_3464_4618_s_4_2.jpg", [
        "4th Degree Black Belt; 1st Degree Black Belt Weapons",
        "Elite Team Coach",
        "Instructor, City of San Ramon Karate Program"]),
    ("Senior Instructor", "William Fuentes", "5df506_299863601e2a48d88aec62d89945ca4d~mv2_d_3464_4618_s_4_2.jpg", [
        "5th Degree Black Belt",
        "1st Degree Black Belt in Kenshin Ryu Kobudo",
        "USNKF Certified Judge",
        "Instructor, City of Pleasant Hill Karate Program"]),
    ("Instructor", "Johanna Abello", "4f0023_488d0ef656de44bc859e0c3666e0c7d8~mv2.jpg", [
        "3rd Degree Black Belt; 1st Degree Black Belt Weapons",
        "US Open Kata Champion",
        "NASM Certified Personal Trainer with multiple specializations",
        "Instructor, City of San Ramon Karate Program"]),
    ("Instructor", "Laura Abello", "4f0023_21fd679683184b25b4506c53bb2c43e7~mv2.jpeg", [
        "2nd Degree Black Belt",
        "Certified USA NKF Judge",
        "Academy Administrator"]),
]

# (name, belts, {day: [times]})
CLASSES = [
    ("Kids Beginners", "White to Orange Stripe Belt", {
        "Mon": ["6:00 – 6:45 PM"], "Tue": ["4:00 – 4:45 PM"],
        "Wed": ["4:00 – 4:45 PM", "6:00 – 6:45 PM"], "Thu": ["4:00 – 4:45 PM"], "Fri": ["4:00 – 4:45 PM"]}),
    ("Kids Novice", "Blue to Purple Belt", {
        "Mon": ["4:00 – 4:45 PM"], "Tue": ["6:00 – 6:45 PM"], "Wed": ["5:00 – 5:45 PM"],
        "Thu": ["5:00 – 5:45 PM"], "Fri": ["5:00 – 5:45 PM"]}),
    ("Kids Intermediate", "Purple Stripe to Red Belt", {
        "Mon": ["5:00 – 5:45 PM"], "Tue": ["6:00 – 6:45 PM"], "Thu": ["5:00 – 5:45 PM"], "Fri": ["5:00 – 5:45 PM"]}),
    ("Advanced", "Red, Brown and Black Belt", {
        "Tue": ["7:00 – 8:00 PM"], "Wed": ["7:00 – 8:00 PM"], "Thu": ["7:00 – 8:00 PM"]}),
    ("All Members Karate", "Blue Belts and above", {
        "Mon": ["7:00 – 8:00 PM"], "Fri": ["6:00 – 7:00 PM"]}),
    ("Kumite", "Purple Belts and above", {"Tue": ["5:00 – 5:45 PM"]}),
    ("Weapons", "All ranks", {"Thu": ["6:00 – 6:45 PM"]}),
    ("Competition Team Practice", "Team members", {"Fri": ["7:00 – 9:15 PM"]}),
]
DAYS = [("Mon", "Monday"), ("Tue", "Tuesday"), ("Wed", "Wednesday"), ("Thu", "Thursday"), ("Fri", "Friday")]

CLASS_PHOTOS = [
    ("4f0023_faed16fd04b049038638d8ab0aa770c6~mv2.jpg", "Students training in the dojo"),
    ("4f0023_1fbca9b442764e30828e1c1630265101~mv2.jpg", "Class in session"),
    ("4f0023_6b0d422afcf1462cac92c5e5ce1ea5cb~mv2.jpg", "Students practicing kata"),
    ("4f0023_2f0d375192dd4fae93770bd32607adc7~mv2.jpg", "Group training"),
    ("4f0023_ebda3d8b7f7f42be9029b20939732cf2~mv2.jpg", "Kumite practice"),
    ("4f0023_ff513c1a7a9c4a1798e85ecdbadb8a67~mv2.jpg", "Students at the academy"),
    ("4f0023_808280f8d2f14b598703bf8bcbbb1ab9~mv2.jpeg", "Karate class"),
    ("4f0023_94e399641ccc4382be8ef01aa5e93e7f~mv2.jpg", "Dojo training"),
]

# (iso date, category, title, summary, (gold, silver, bronze) or None)
NEWS = [
    ("2026-02-28", "event", "Annual Dojo Tournament", "Held at a new venue, Ultimate Fieldhouse. We are proud of all of our students for performing their best and showcasing their hard work.", None),
    ("2024-11-02", "tournament", "23rd Annual Ryukyukan International Karate and Kobudo Tournament", "Forty-four athletes competed in Dixon, CA.", (29, 19, 15)),
    ("2024-10-06", "tournament", "2024 Fall Classic", "Thirty-two competitors took part in Yuba City.", (19, 13, 9)),
    ("2024-09-15", "tournament", "Fiestas 51st Annual International Karate Championship", "The competition team traveled to Los Angeles and came home with 8 first-place and 1 second-place trophies.", None),
    ("2024-04-28", "tournament", "2024 NCKF Karate Championships", "", (20, 10, 12)),
    ("2024-04-13", "event", "2024 Dojo Tournament", "Students showed their skills in kata and kumite.", None),
    ("2024-02-17", "tournament", "2024 AAU Pacific Southwest District Championship", "Twelve elite students traveled to San Diego.", (7, 3, 7)),
    ("2024-02-06", "tournament", "2024 West Coast Championship", "Yuba City.", (18, 7, 13)),
    ("2024-01-11", "training", "2024 Shugyo Class", "Our annual, challenging training class to start the year.", None),
    ("2023-09-17", "tournament", "2023 Fiestas Invitational Karate Championship", "Team members competed in Los Angeles and brought home 5 second-place and 3 third-place trophies.", None),
    ("2023-07-15", "tournament", "2023 USA Karate National Championships", "Elite competitors traveled to Richmond, Virginia.", (5, 1, 1)),
    ("2023-04-09", "tournament", "2023 JIC / US Open", "Las Vegas.", (14, 6, 12)),
    ("2023-02-18", "event", "2023 Dojo Tournament", "Students competed in kata and team kata divisions.", None),
    ("2023-02-05", "tournament", "2023 West Coast Championships", "Yuba City.", (18, 12, 9)),
    ("2023-01-12", "training", "2023 Shugyo", "Annual New Year training class featuring advanced students.", None),
    ("2022-10-02", "tournament", "2022 Fall Classic Tournament", "Yuba City, elite team.", (15, 11, 10)),
    ("2022-07-05", "tournament", "2022 USA National Championships", "Spokane, Washington. Four national champions.", None),
    ("2022-05-14", "promotion", "May 2022 Black Belt Promotion", "“I am very pleased to see that students are improving thanks to their hard work.”", None),
    ("2022-04-17", "tournament", "2022 USOPEN and Junior International Cup", "Las Vegas. Multiple medal winners.", None),
    ("2022-03-27", "tournament", "2022 NCKF Championship", "Our young competitors did us proud.", (11, 3, 7)),
    ("2022-03-12", "event", "2022 Dojo Tournament (Fundraiser)", "Supported athletes competing in national tournaments.", None),
    ("2022-01-30", "tournament", "2022 West Coast Championships", "Yuba City.", (7, 8, 5)),
    ("2022-01-24", "training", "Train with Sandra Sanchez, Olympic Gold Medalist", "Our students had the opportunity to train with an Olympic champion.", None),
    ("2022-01-13", "training", "2022 Shugyo", "Brown and black belts took part in the annual New Year training.", None),
    ("2021-12-20", "tournament", "2021 USA Open and Junior International Cup", "Las Vegas. Kyle won silver at JIC and gold at the US Open; Adrianna won gold at both events.", None),
    ("2021-11-13", "promotion", "November 2021 Black Belt Promotion", "A new fitness test was introduced for black belt candidates.", None),
    ("2021-11-06", "tournament", "Ryukyukan Championships", "Dixon.", (7, 3, 5)),
    ("2021-10-03", "tournament", "Fall Classic Championships", "Our first tournament after the pandemic; nine athletes competed.", (5, 3, 0)),
    ("2021-09-02", "tournament", "2021 National Championships", "Chicago.", (3, 0, 1)),
    ("2021-05-15", "promotion", "2021 Black Belt Promotion", "Congratulations to our new black belts, who trained through lockdown.", None),
    ("2020-02-22", "event", "2020 Dojo Tournament (Fundraiser)", "Over 170 competitors, raising funds for the US Open and National Championship.", None),
    ("2020-02-09", "tournament", "2020 West Coast Championship", "Our 38-member team performed well.", None),
    ("2020-01-08", "training", "2020 Shugyo", "Annual New Year training class with challenging drills.", None),
    ("2019-11-16", "promotion", "Brown & Black Belt Promotion", "Brown and black belt examination and promotion.", None),
    ("2019-10-06", "tournament", "Fall Classic Championships", "A 45-member team competed in Yuba City.", None),
    ("2019-09-15", "tournament", "International Karate Championship", "Father and son John and Kyle Crose both took first-place trophies.", None),
    ("2019-09-01", "event", "Upcoming Tournaments", "Schedule of tournaments from October 2019 through July 2020.", None),
    ("2019-07-11", "tournament", "2019 National Championships", "Chicago, July 11–14. Seven medalists, including Adrianna Villesis, gold in Advanced Kata.", None),
    ("2019-05-04", "tournament", "Okaigan & AJKL Tournament", "More than 30 elite team members competed.", None),
    ("2019-04-19", "tournament", "2019 USA OPEN & Jr. International Cup", "Sixteen elite team members competed in Las Vegas.", None),
    ("2019-03-31", "tournament", "National Qualifier", "The elite team earned the right to compete at the USA National Championship in Chicago.", None),
    ("2019-02-24", "event", "2019 Dojo Tournament", "Over 170 athletes competed in kata and kumite.", None),
]
CHIP_LABEL = {"tournament": "Tournaments", "promotion": "Promotions", "training": "Training", "event": "Events"}
CAT_LABEL = {"tournament": "Tournament", "promotion": "Promotion", "training": "Training", "event": "Event"}

CALENDAR = [
    ("September 2026", "4f0023_6450845fdbd8415e931ef1b149b6e097~mv2.png"),
    ("October 2026", "4f0023_8769817bfb934f51b31b68f3c8c1f17c~mv2.png"),
    ("November 2026", "4f0023_215559630d134b24b128a8478f29744a~mv2.png"),
    ("December 2026", "4f0023_7bedf86dde7e42568d2283137e82e6ec~mv2.png"),
    ("January 2027", "4f0023_d01ffc2c73a046e9aaf1ba264ec22f89~mv2.png"),
    ("February 2027", "4f0023_90a41f5587154c13b30d157c3951ef9f~mv2.png"),
]

KATA = ["Kihon Kata Ichi", "Kihon Kata Ni", "Kihon Kata San", "Kihon Kata Yon", "Kihon Kata Go",
        "Heian Shodan", "Heian Nidan", "Heian Sandan", "Heian Yodan", "Heian Godan", "Ten No Kata",
        "Chino Kata", "Jiin", "Jion", "Jitte", "Matsukaze", "Bassai Dai", "Rohai", "Kosokun Dai",
        "Seienchin", "Jyuroku", "Shinsei"]

ICONS = {
    "pin": '<svg viewBox="0 0 24 24"><path d="M12 22s7-6.2 7-12a7 7 0 1 0-14 0c0 5.8 7 12 7 12z"/><circle cx="12" cy="10" r="2.5"/></svg>',
    "phone": '<svg viewBox="0 0 24 24"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/></svg>',
    "mail": '<svg viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg>',
}

PAGES = [("index.html", "Welcome"), ("instructors.html", "Instructors"), ("classes.html", "Classes"),
         ("news.html", "News & Updates"), ("media.html", "Media"), ("calendar.html", "Calendar")]

e = html.escape


def contact_list():
    return f"""<ul class="contact-list">
  <li><span class="ico">{ICONS['pin']}</span><span class="txt"><small>Address</small><a href="{MAPS}" target="_blank" rel="noopener">{e(ADDRESS)}</a></span></li>
  <li><span class="ico">{ICONS['phone']}</span><span class="txt"><small>Phone</small><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></span></li>
  <li><span class="ico">{ICONS['mail']}</span><span class="txt"><small>Email</small><a href="mailto:{EMAIL}">{EMAIL}</a></span></li>
</ul>"""


def page(fname, title, body, description, extra_body=""):
    cur = ' aria-current="page"'
    nav = "".join(
        f'<li><a href="{f}"{cur if f == fname else ""}>{e(t)}</a></li>' for f, t in PAGES)
    social = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{n}</a></li>' for n, u in SOCIAL)
    year = datetime.date.today().year
    full_title = NAME + " | San Ramon Karate" if fname == "index.html" else f"{title} | AABBA"
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(full_title)}</title>
<meta name="description" content="{e(description)}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://static.wixstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Shippori+Mincho:wght@600;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/styles.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap header-inner">
    <a class="brand" href="index.html"><strong>{NAME}</strong><span>Excellence Through Efforts</span></a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="nav">Menu</button>
    <nav class="nav" id="nav" aria-label="Main"><ul>{nav}</ul></nav>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer">
  <div class="wrap footer-grid">
    <div>
      <h4>{NAME}</h4>
      <p>Traditional Shitoryu karate in San Ramon. Respect, self-discipline, humility and dedication to excellence.</p>
      <p>Affiliated with Japan Karatedo Hayashi-ha Shitoryukai, <a href="http://www.usankf.org/" target="_blank" rel="noopener">USA NKF</a> and <a href="http://www.wkf.net" target="_blank" rel="noopener">WKF</a>.</p>
    </div>
    <div><h4>Visit</h4>
      <p><a href="{MAPS}" target="_blank" rel="noopener">{e(ADDRESS)}</a></p>
      <p><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></p>
    </div>
    <div><h4>Follow</h4><ul>{social}</ul></div>
  </div>
  <div class="wrap copy">&copy; {year} {NAME}. Unofficial redesign concept.</div>
</footer>
<script src="js/main.js"></script>
{extra_body}
</body>
</html>
"""


def hero_small(eyebrow, h1, lead):
    return f"""<section class="hero small">
  <img class="hero-bg" src="{wix(HERO, 1600, 500, 'hero.jpg')}" alt="" fetchpriority="high">
  <div class="wrap"><div class="kanji">空手道</div><h1>{h1}</h1><p class="lede">{lead}</p></div>
</section>"""


def free_class_band():
    return f"""<section class="cta-band"><div class="wrap">
  <div><h2>Drop in for a free introductory class</h2><p>No experience needed. Come see what we are about.</p></div>
  <a class="btn btn-light" href="mailto:{EMAIL}?subject=Free%20introductory%20class">Book your free class</a>
</div></section>"""


def build_index():
    recent = sorted(NEWS, key=lambda n: n[0], reverse=True)[:3]
    news_html = "".join(
        f'<article class="card card-pad"><span class="tag {c}">{CAT_LABEL[c]}</span><h3>{e(t)}</h3>'
        f'<p class="muted">{datetime.date.fromisoformat(d):%B %-d, %Y}</p></article>'
        for d, c, t, s, m in recent)
    lead = INSTRUCTORS[0]
    body = f"""<section class="hero">
  <img class="hero-bg" src="{wix(HERO, 1800, 900, 'hero.jpg')}" alt="" fetchpriority="high">
  <div class="wrap">
    <div class="kanji">空手道 · SAN RAMON</div>
    <h1>Traditional karate.<br>Lasting character.</h1>
    <p class="lede">The All American Black Belt Academy teaches martial arts with traditional values of respect, self-discipline, humility and dedication to excellence.</p>
    <div class="actions">
      <a class="btn btn-red" href="mailto:{EMAIL}?subject=Free%20introductory%20class">Try a free class</a>
      <a class="btn btn-ghost" href="classes.html">See the schedule</a>
    </div>
  </div>
</section>

<section class="section"><div class="wrap grid g2" style="align-items:center;gap:48px">
  <div>
    <p class="eyebrow">About the academy</p>
    <h2>High-level instruction. World-class athletes.</h2>
    <p>AABBA is well known for its high-level instruction and world-class athletes, but most notably for its holistic methods to teach skills with an emphasis on health and fitness wellness.</p>
    <p>Shihan Hultin has had a positive impact on students&rsquo; lives while developing lasting relationships that will be remembered for years to come.</p>
  </div>
  <div class="grid g3" style="gap:20px">
    <div class="value"><h3>Respect</h3><p>Bowing in, bowing out, and treating everyone on the floor well.</p></div>
    <div class="value"><h3>Discipline</h3><p>Showing up, working hard and finishing what you start.</p></div>
    <div class="value"><h3>Humility</h3><p>Every belt is the start of the next thing to learn.</p></div>
  </div>
</div></section>

<section class="section dark"><div class="wrap">
  <p class="eyebrow">Competition record</p>
  <h2>Built on effort</h2>
  <div class="stats">
    <div class="stat"><b>170+</b><span>competitors at our annual dojo tournament</span></div>
    <div class="stat"><b>63</b><span>medals at the 2024 Ryukyukan tournament</span></div>
    <div class="stat"><b>8&times;</b><span>national kata champion on our staff</span></div>
    <div class="stat"><b>7th</b><span>degree black belt Master Instructor</span></div>
  </div>
</div></section>

<section class="section"><div class="wrap grid g2" style="align-items:center;gap:48px">
  <div class="card"><img src="{wix(lead[2], 700, 800, 'carl-hultin.jpg')}" alt="{lead[1]}" loading="lazy" width="700" height="800" style="width:100%;height:auto"></div>
  <div>
    <p class="eyebrow">Meet your instructors</p>
    <h2>{lead[1]}, {lead[0]}</h2>
    <p>7th Degree Black Belt in Hayashi-ha Shitoryu Karate-do, Vice President of the USA National Karate Federation and a World Karate Federation judge, leading a staff of champion competitors and coaches.</p>
    <div class="actions"><a class="btn btn-red" href="instructors.html">Meet the team</a></div>
  </div>
</div></section>

<section class="section alt"><div class="wrap">
  <div style="display:flex;justify-content:space-between;align-items:baseline;flex-wrap:wrap;gap:8px"><h2>Latest news</h2><a href="news.html"><b>All news &rarr;</b></a></div>
  <div class="grid g3">{news_html}</div>
</div></section>

{free_class_band()}

<section class="section"><div class="wrap grid g2" style="gap:48px;align-items:center">
  <div><p class="eyebrow">Visit us</p><h2>Find the dojo</h2>{contact_list()}
    <p class="muted" style="margin-top:20px">Classes run Monday to Friday, 4&ndash;8 PM. Saturdays are reserved for promotions, seminars and private lessons. We also teach through the San Ramon and Pleasant Hill community centers.</p></div>
  <div class="card card-pad"><h3>Class times</h3><p>Kids and adult classes by belt level, plus kumite, weapons and competition team.</p><a class="btn btn-red" href="classes.html">View classes</a></div>
</div></section>"""
    return page("index.html", "Welcome", body, "Traditional Shitoryu karate for kids and adults in San Ramon, CA. Try a free introductory class.")


def build_instructors():
    cards = []
    for i, (role, name, img, items) in enumerate(INSTRUCTORS):
        lis = "".join(f"<li>{e(x)}</li>" for x in items)
        size = (600, 800) if i == 0 else (300, 400)
        cards.append(f"""<article class="card person{' lead' if i == 0 else ''}">
  <img src="{wix(img, *size, name.lower().replace(' ', '-') + '.jpg')}" alt="{name}" loading="{'eager' if i == 0 else 'lazy'}" width="{size[0]}" height="{size[1]}">
  <div><p class="role">{role}</p><h3>{name}</h3><ul>{lis}</ul></div></article>""")
    body = hero_small("", "Our instructors", "Champions, referees and coaches who teach with patience and high standards.") + \
        f'<section class="section"><div class="wrap"><div class="people">{"".join(cards)}</div></div></section>' + free_class_band()
    return page("instructors.html", "Instructors", body, "Meet the black belt instructors at All American Black Belt Academy.")


def build_classes():
    chips = '<button class="chip" data-day="all" aria-pressed="true">All days</button>' + "".join(
        f'<button class="chip" data-day="{a}" aria-pressed="false">{full}</button>' for a, full in DAYS)
    cards = []
    for name, belts, sched in CLASSES:
        rows = "".join(f'<li data-day="{a}"><b>{full}</b><span>{" &middot; ".join(sched[a])}</span></li>'
                       for a, full in DAYS if a in sched)
        cards.append(f'<article class="card class-card"><h3>{e(name)}</h3><p class="belts">{e(belts)}</p><ul class="times">{rows}</ul></article>')
    slides = "".join(
        f'<div class="slide" role="group" aria-roledescription="slide" aria-label="Photo {i + 1} of {len(CLASS_PHOTOS)}">'
        f'<img src="{wix(m, 1000, 625, "class.jpg")}" alt="{e(a)}" loading="{"eager" if i == 0 else "lazy"}" width="1000" height="625"></div>'
        for i, (m, a) in enumerate(CLASS_PHOTOS))
    thumbs = "".join(
        f'<button aria-label="Show photo {i + 1}" aria-current="false"><img src="{wix(m, 168, 116, "t.jpg")}" alt="" loading="lazy" width="84" height="58"></button>'
        for i, (m, a) in enumerate(CLASS_PHOTOS))
    body = hero_small("", "Classes &amp; schedule", "Monday to Friday, by belt level. Saturdays are reserved for promotions, seminars and private lessons.") + f"""
<section class="section"><div class="wrap">
  <div class="carousel" data-carousel tabindex="0" aria-roledescription="carousel" aria-label="Class photos">
    <div class="track">{slides}</div>
    <button class="car-btn prev" aria-label="Previous photo">&#8249;</button>
    <button class="car-btn next" aria-label="Next photo">&#8250;</button>
    <div class="thumbs">{thumbs}</div>
    <p class="car-count" aria-live="polite"></p>
  </div>
</div></section>
<section class="section alt"><div class="wrap">
  <p class="eyebrow">Weekly schedule</p><h2>Find your class</h2>
  <div class="chips" data-day-filter role="group" aria-label="Filter by day">{chips}</div>
  <div class="classes">{"".join(cards)}</div>
  <p class="muted" style="margin-top:24px">We also offer programs through the San Ramon and Pleasant Hill community centers. Check the <a href="calendar.html"><b>monthly calendar</b></a> for holidays and special events.</p>
</div></section>""" + free_class_band()
    return page("classes.html", "Classes", body, "Class schedule by belt level: kids, advanced, kumite, weapons and competition team.")


def build_news():
    items = sorted(NEWS, key=lambda n: n[0], reverse=True)
    years = {}
    for it in items:
        years.setdefault(it[0][:4], []).append(it)
    chips = '<button class="chip" data-cat="all" aria-pressed="true">All</button>' + "".join(
        f'<button class="chip" data-cat="{k}" aria-pressed="false">{v}</button>' for k, v in CHIP_LABEL.items())
    groups = []
    for y, its in years.items():
        rows = []
        for d, c, t, s, m in its:
            dt = datetime.date.fromisoformat(d)
            med = ""
            if m:
                med = '<span class="medals" aria-label="Medals">' + "".join(
                    f'<span class="{k}">{v} {n}</span>' for k, v, n in zip("gsb", m, ["gold", "silver", "bronze"]) if v) + "</span>"
            rows.append(f"""<li class="news-item" data-cat="{c}"><time datetime="{d}"><b>{dt:%b} {dt.day}</b>{y}</time>
<div><h3>{e(t)}</h3><p><span class="tag {c}">{CAT_LABEL[c]}</span>{e(s)}</p>{med}</div></li>""")
        groups.append(f'<section class="year-group"><h2>{y} <small>{len(its)} update{"s" if len(its) != 1 else ""}</small></h2><ul class="news-list">{"".join(rows)}</ul></section>')
    body = hero_small("", "News &amp; updates", "Tournament results, promotions and training events, newest first.") + f"""
<section class="section"><div class="wrap">
  <div class="filters" data-news-filter role="group" aria-label="Filter news">{chips}</div>
  {"".join(groups)}
</div></section>"""
    return page("news.html", "News & Updates", body, "Tournament results, black belt promotions and training events from AABBA.")


def build_media():
    photos = "".join(
        f'<button data-full="{wix(m, 1600, name="full.jpg")}" aria-label="Enlarge photo: {e(a)}"><img src="{wix(m, 480, name="thumb.jpg")}" alt="{e(a)}" loading="lazy"></button>'
        for m, a in CLASS_PHOTOS)
    kata = "".join(f"<li>{k}</li>" for k in KATA)
    body = hero_small("", "Media", "Photos from the dojo and the kata we practice.") + f"""
<section class="section"><div class="wrap"><p class="eyebrow">Photos</p><h2>Life at the dojo</h2>
  <div class="masonry">{photos}</div></div></section>
<section class="section alt"><div class="wrap"><p class="eyebrow">Kata videos</p><h2>Kata curriculum</h2>
  <p class="muted">Video links can be added next to each kata once the academy shares them.</p>
  <ul class="kata-list">{kata}</ul></div></section>
<div class="lightbox" role="dialog" aria-modal="true" aria-label="Enlarged photo"><button class="x" aria-label="Close">&times;</button><img alt=""></div>"""
    return page("media.html", "Media", body, "Photos and kata videos from All American Black Belt Academy.")


def build_calendar():
    tabs = "".join(
        f'<section class="section{" alt" if i % 2 else ""}" id="m{i}"><div class="wrap"><h2>{n}</h2><div class="cal-frame"><img src="{wix(m, 1200, name="cal.png")}" alt="{n} class schedule" loading="{"eager" if i == 0 else "lazy"}"></div></div></section>'
        for i, (n, m) in enumerate(CALENDAR))
    jump = "".join(f'<a class="chip" href="#m{i}" style="text-decoration:none">{n}</a>' for i, (n, m) in enumerate(CALENDAR))
    body = hero_small("", "Calendar", "Monthly schedules, including holidays and special events.") + \
        f'<div class="wrap" style="padding-top:28px"><div class="chips">{jump}</div></div>' + tabs
    return page("calendar.html", "Calendar", body, "Monthly class calendar for All American Black Belt Academy.")


if __name__ == "__main__":
    for fn, builder in [("index.html", build_index), ("instructors.html", build_instructors),
                        ("classes.html", build_classes), ("news.html", build_news),
                        ("media.html", build_media), ("calendar.html", build_calendar)]:
        (ROOT / fn).write_text(builder(), encoding="utf-8")
        print("wrote", fn)
