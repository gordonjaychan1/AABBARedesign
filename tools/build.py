#!/usr/bin/env python3
"""Generates the static pages in the repo root. Run: python3 tools/build.py"""
import datetime
import hashlib
import html
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

NAME = "All American Black Belt Academy"
ADDRESS = "21001 San Ramon Valley Blvd, A7, San Ramon, CA 94583"
MAPS = "https://www.google.com/maps/search/?api=1&query=" + ADDRESS.replace(" ", "+")
EMAIL = "Laura.aabba@icloud.com"
PHONE_DISPLAY = "(925)-829-4265"
PHONE_TEL = "+19258294265"
# (name, link, square logo icon used on the old site)
SOCIAL = [
    ("Yelp", "https://www.yelp.com/biz/all-american-black-belt-academy-san-ramon", "263c6eefe13c431681f9363e2e92ddb7.png"),
    ("Instagram", "https://www.instagram.com/aabba.karate/", "8d6893330740455c96d218258a458aa4.png"),
    ("Facebook", "https://www.facebook.com/Shitorkaratedo/", "e316f544f9094143b9eac01f1f19e697.png"),
]


def wix(media_id, w, h=None, name="photo.jpg"):
    """Wix CDN resize URL, so each image is served at the size it is shown."""
    mode = "fill" if h else "fit"
    size = f"w_{w},h_{h or w * 2}"  # fit needs both bounds; the tall box leaves width as the limit
    return f"https://static.wixstatic.com/media/{media_id}/v1/{mode}/{size},al_c,q_75/{name}"


HERO = "82efacf67509447eb89b898a3ff6e3cd.jpg"  # belts photo used behind the intro text on the old site
LOGO_FLAG = "5df506_41dbd700c0724e0cbffbe98cc6886d88~mv2.jpg"
LOGO_FIST = "5df506_f9aea610ff0846b0b7c227760e09cf70~mv2.jpg"
DAY_PHOTOS = {
    "Mon": "4f0023_9cb74c4ca46d4424bddfc6e50283a875~mv2.jpeg",
    "Tue": "5df506_2f3d7d8dc1434443a4136c236e908e1a~mv2.jpg",
    "Wed": "5df506_b32a4c3c86814845888485ac26ddc93b~mv2_d_2025_1679_s_2.jpg",
    "Thu": "5df506_15eb2b3537f844a7972cf61d4deba43d~mv2_d_6557_2440_s_4_2.jpg",
    "Fri": "5df506_5ecf972506da450492e46b24177c4fb9~mv2_d_4579_3265_s_4_2.jpeg",
    "Sat": "5df506_b45cb5e8c4a145f18d7a30c63482a300~mv2_d_4898_3265_s_4_2.jpg",
}
SHIHAN = [
    "In 1966 Shihan began his karate training in Philadelphia, PA with the JKA Shotokan master, Sensei T. Okazaki. While living in Lubbock, TX in 1971 he earned a brown belt in Allen Steen\u2019s Tae Kwon Do school. After moving to San Diego, CA Shihan joined Shihan Minobu Miki\u2019s dojo and began his long journey in Hayashi ha Shitoryu Kai by earning his black belt in 1975. He is currently the only Hayashi ha Shitoryu California dojo registered with the Japan Headquarters.",
    "Shihan Hultin has a business administration degree and had a career in corporate management. In 1979 Shihan moved to the San Francisco Bay Area and in 1980 opened his karate school in Dublin. Subsequently he developed karate programs with the local YMCA and San Ramon City Recreation Department.",
    "Shihan used his dojo and competition experience to become a World Karate Federation judge at the World Championship in Masstricht, Netherlands in 1984. He continued as an official in fifteen other international events all over the world. When the USA National Karate Federation was established in 1994, he was elected the first Western Regional Vice President and a member on the Referee Council.",
    "Shihan Hultin established the United Karate Federation of California in 1990. The UKFC is a California non-profit corporation to benefit the Dublin elementary school children with low cost karate/martial art classes and give financial aid to karate athletes in Northern California. Shihan has developed a more holistic and healthy approach to his karate training to help his students maintain a healthy balance and superior physical fitness level. He is a National Strength and Conditioning Association Certified Personal Trainer.",
]

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

# (name, belts, {day: [times]}, photo shown on the block on the old Classes page)
CLASSES = [
    ("Kids Beginners", "White to Orange Stripe Belt", {
        "Mon": ["6:00 – 6:45 PM"], "Tue": ["4:00 – 4:45 PM"],
        "Wed": ["4:00 – 4:45 PM", "6:00 – 6:45 PM"], "Thu": ["4:00 – 4:45 PM"], "Fri": ["4:00 – 4:45 PM"]},
     "4f0023_faed16fd04b049038638d8ab0aa770c6~mv2.jpg"),
    ("Kids Novice", "Blue to Purple Belt", {
        "Mon": ["4:00 – 4:45 PM"], "Tue": ["6:00 – 6:45 PM"], "Wed": ["5:00 – 5:45 PM"],
        "Thu": ["5:00 – 5:45 PM"], "Fri": ["5:00 – 5:45 PM"]},
     "4f0023_2f0d375192dd4fae93770bd32607adc7~mv2.jpg"),
    ("Kids Intermediate", "Purple Stripe to Red Belt", {
        "Mon": ["5:00 – 5:45 PM"], "Tue": ["6:00 – 6:45 PM"], "Thu": ["5:00 – 5:45 PM"], "Fri": ["5:00 – 5:45 PM"]},
     "4f0023_808280f8d2f14b598703bf8bcbbb1ab9~mv2.jpeg"),
    ("Advanced Class", "Red, Brown, and Black Belt", {
        "Tue": ["7:00 – 8:00 PM"], "Wed": ["7:00 – 8:00 PM"], "Thu": ["7:00 – 8:00 PM"]},
     "4f0023_1fbca9b442764e30828e1c1630265101~mv2.jpg"),
    ("All Members Karate", "Blue Belts and Above", {
        "Mon": ["7:00 – 8:00 PM"], "Fri": ["6:00 – 7:00 PM"]},
     "4f0023_ebda3d8b7f7f42be9029b20939732cf2~mv2.jpg"),
    ("Competition Team Practice", "", {"Fri": ["7:00 – 9:15 PM"]},
     "4f0023_94e399641ccc4382be8ef01aa5e93e7f~mv2.jpg"),
    ("Weapons Class", "", {"Thu": ["6:00 – 6:45 PM"]},
     "4f0023_6b0d422afcf1462cac92c5e5ce1ea5cb~mv2.jpg"),
    ("Kumite Class", "Purple Belts and Above", {"Tue": ["5:00 – 5:45 PM"]},
     "4f0023_ff513c1a7a9c4a1798e85ecdbadb8a67~mv2.jpg"),
]
# Wide photos from the slideshow at the top of the old Classes page, in its order
SLIDESHOW = [
    "4f0023_40d8149e1c264fbb8a22d32f32ee1a43~mv2.jpeg",
    "4f0023_908364a7309d4af7b87e13291f7ce3b2~mv2_d_4898_2423_s_4_2.jpeg",
    "5df506_373f7befc11e44438d4aeaba9162975a~mv2_d_6285_2545_s_4_2.jpg",
    "5df506_12dbff89fd8747cd97f8d59a250a6bd7~mv2_d_7217_2217_s_2.jpg",
]
DAYS = [("Mon", "Monday"), ("Tue", "Tuesday"), ("Wed", "Wednesday"), ("Thu", "Thursday"), ("Fri", "Friday")]

# Posts copied from the old News & Updates page: date, category, title, text paragraphs
NEWS = json.loads((ROOT / "data" / "news.json").read_text(encoding="utf-8"))
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

# Kata from the old Media page. Add a YouTube video ID as the second value to show a player.
KATA = [(k, "") for k in [
    "Kihon Kata Ichi", "Kihon Kata Ni", "Kihon Kata San", "Kihon Kata Yon", "Kihon Kata Go",
    "Heian Shodan", "Heian Nidan", "Heian Sandan", "Heian Yodan", "Heian Godan", "Ten No Kata",
    "Chino Kata", "Jiin", "Jion", "Jitte", "Matsukaze", "Bassai Dai", "Rohai", "Kosokun Dai",
    "Seienchin", "Jyuroku", "Shinsei"]]

# Belt tests locked by tools/encrypt_tests.py (no passwords in here)
TESTS = json.loads((ROOT / "data" / "tests.json").read_text(encoding="utf-8"))

ICONS = {
    "pin": '<svg viewBox="0 0 24 24"><path d="M12 22s7-6.2 7-12a7 7 0 1 0-14 0c0 5.8 7 12 7 12z"/><circle cx="12" cy="10" r="2.5"/></svg>',
    "phone": '<svg viewBox="0 0 24 24"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/></svg>',
    "mail": '<svg viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg>',
}

# (output file, link href, menu label). Links omit .html; GitHub Pages serves classes.html at /classes.
PAGES = [("index.html", "./", "Welcome"), ("instructors.html", "instructors", "Instructors"),
         ("classes.html", "classes", "Classes"), ("news.html", "news", "News & Updates"),
         ("gallery.html", "gallery", "Gallery"), ("kata.html", "kata", "Kata Videos"),
         ("tests.html", "tests", "Belt Tests"), ("calendar.html", "calendar", "Calendar")]

e = html.escape


def ver(path):
    """Content hash appended to asset URLs so browsers fetch the new file after each change."""
    return hashlib.md5((ROOT / path).read_bytes()).hexdigest()[:8]


def day_cards():
    cards = []
    for a, full in DAYS:
        rows = []
        for name, belts, sched, _ in CLASSES:
            for t in sched.get(a, []):
                rows.append((t, name, belts))
        rows.sort(key=lambda r: (int(r[0].split(":")[0]) % 12 + (12 if "PM" in r[0] else 0), r[0]))
        lis = "".join(f"<li><b>{t}</b> {e(n)}{f' <span>({e(b)})</span>' if b else ''}</li>" for t, n, b in rows)
        cards.append(f'<article class="daycard"><h3>{full}</h3><ul>{lis}</ul>'
                     f'<img src="{wix(DAY_PHOTOS[a], 480, 330, a + ".jpg")}" alt="" loading="lazy" width="480" height="330"></article>')
    cards.append(f'<article class="daycard"><h3>Saturday</h3><ul><li><b>10:00 AM &ndash; 2:00 PM</b> Reserved for Promotions / Seminars / Private Lessons</li></ul>'
                 f'<img src="{wix(DAY_PHOTOS["Sat"], 480, 330, "Sat.jpg")}" alt="" loading="lazy" width="480" height="330"></article>')
    return '<div class="daygrid">' + "".join(cards) + "</div>"


def contact_buttons():
    return f"""<div class="contact-row">
  <a class="cbtn gray" href="mailto:{EMAIL}">{ICONS['mail']}<span>{EMAIL}</span></a>
  <a class="cbtn red" href="tel:{PHONE_TEL}">{ICONS['phone']}<span>{PHONE_DISPLAY}</span></a>
</div>"""


def free_class():
    return f"""<section class="free" id="free-class"><div class="wrap">
  <hr class="gold">
  <h2>Drop in for a Free Introductory Class</h2>
  <p class="addr"><a href="{MAPS}" target="_blank" rel="noopener">{e(ADDRESS)}</a></p>
  {contact_buttons()}
</div></section>"""


def page(fname, title, body, description, extra_body=""):
    cur = ' aria-current="page"'
    nav = "".join(f'<li><a href="{h}"{cur if f == fname else ""}>{e(t)}</a></li>' for f, h, t in PAGES)
    social = "".join(f'<a href="{u}" target="_blank" rel="noopener" aria-label="{n}" title="{n}">'
                     f'<img src="{wix(icon, 80, 80, n.lower() + ".png")}" alt="" width="40" height="40"></a>' for n, u, icon in SOCIAL)
    full_title = "Dojo | " + NAME + " | San Ramon" if fname == "index.html" else f"{title} | {NAME}"
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
<link href="https://fonts.googleapis.com/css2?family=Anton&family=Nunito+Sans:wght@300;400;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/styles.css?v={ver('css/styles.css')}">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="./"><span class="title">{NAME}</span><span class="motto">Excellence Through Efforts</span></a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="nav">Menu</button>
    <nav class="nav" id="nav" aria-label="Main"><ul>{nav}</ul></nav>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer">
  <div class="wrap">
    <p>Affiliated with <a href="http://hayashiha.jp/english/news/index.html" target="_blank" rel="noopener">Japan Karatedo Hayashi-ha Shitoryukai</a>, <a href="http://www.usankf.org/" target="_blank" rel="noopener">USA NKF</a> and <a href="http://www.wkf.net" target="_blank" rel="noopener">WKF</a>.
    Instruction is also offered through the San Ramon and Pleasant Hill community centers by Sensei Johanna Abello (3rd degree black belt) and William Fuentes (5th degree black belt).</p>
    <div class="social">{social}</div>
    <p class="copy">{NAME} &middot; {e(ADDRESS)} &middot; Unofficial redesign concept</p>
  </div>
</footer>
<script src="js/main.js?v={ver('js/main.js')}"></script>
{extra_body}
</body>
</html>
"""


def title_block(h1, lead="", anchor=""):
    logos = f'<img class="logo" src="{wix(LOGO_FLAG, 240, 186, "logo.jpg")}" alt="" width="120" height="93">'
    fist = f'<img class="logo" src="{wix(LOGO_FIST, 192, 208, "fist.jpg")}" alt="" width="96" height="104">'
    return f"""<section class="pagehead"{f' id="{anchor}"' if anchor else ''}><div class="wrap narrow"><div class="headrow">{logos}<h1>{h1}</h1>{fist}</div><hr class="gold">{f'<p class="lead">{lead}</p>' if lead else ''}</div></section>"""


def build_index():
    bio = "".join(f"<li>{e(t)}</li>" for t in SHIHAN)
    body = f"""<section class="hero">
  <img class="hero-bg" src="{wix(HERO, 1600, 700, 'belts.jpg')}" alt="" fetchpriority="high">
  <div class="wrap"><div class="panel">
    <p>The All American Black Belt Academy believes in and teaches Martial arts with traditional values of respect, self-discipline, humility and dedication to excellence.</p>
    <p>AABBA is well known for its high-level instruction and world-class athletes, but most notably, for its holistic methods to teach skills with an emphasis on health and fitness wellness.</p>
    <p>Shihan Hultin has had a positive impact on students&rsquo; lives while developing lasting relationships that will be remembered for years to come.</p>
    <div class="actions"><a class="btn red" href="#free-class">Book a Free Class</a><a class="btn outline" href="#schedule">See the Schedule</a></div>
  </div></div>
</section>
{title_block("Classes and Courses", anchor="schedule")}
<section class="section"><div class="wrap narrow">{day_cards()}
  <p class="note">Check the <a href="calendar">monthly calendar</a> for holidays and special events.</p></div></section>
<section class="section shihan"><div class="wrap narrow">
  <h2>Shihan Hultin &amp; His Dojo</h2>
  <ul>{bio}</ul>
</div></section>
{free_class()}"""
    return page("index.html", "Welcome", body, "Traditional Shitoryu karate for kids and adults in San Ramon, CA. Drop in for a free introductory class.")


def build_instructors():
    cards = []
    for role, name, img, items in INSTRUCTORS:
        lis = "".join(f"<li>{e(x)}</li>" for x in items)
        cards.append(f"""<article class="person"><img src="{wix(img, 480, name=name.lower().replace(' ', '-') + '.jpg')}" alt="{name}" loading="lazy" width="480" height="480">
<div><h3>{role} {name}</h3><ul>{lis}</ul></div></article>""")
    body = title_block("Instructors") + f'<section class="section"><div class="wrap narrow"><div class="people">{"".join(cards)}</div></div></section>' + free_class()
    return page("instructors.html", "Instructors", body, "Meet the black belt instructors at All American Black Belt Academy.")


def build_classes():
    cards = []
    for name, belts, sched, photo in CLASSES:
        rows = "".join(f'<li><b>{full}</b><span>{"<br>".join(sched[a])}</span></li>' for a, full in DAYS if a in sched)
        sub = f'<p class="belts">{e(belts)}</p>' if belts else ""
        cards.append(f'<article class="daycard classcard"><img src="{wix(photo, 540, 510, "class.jpg")}" alt="" loading="lazy" width="540" height="510">'
                     f'<h3>{e(name)}</h3>{sub}<ul class="times">{rows}</ul></article>')
    n = len(SLIDESHOW)
    slides = "".join(
        f'<div class="slide" role="group" aria-roledescription="slide" aria-label="Photo {i + 1} of {n}">'
        f'<img src="{wix(m, 1800, 720, "slide.jpg")}" alt="" loading="{"eager" if i == 0 else "lazy"}" width="1800" height="720"></div>'
        for i, m in enumerate(SLIDESHOW))
    body = title_block("Classes and Courses", "Monday through Friday, by belt level. Saturdays are reserved for promotions, seminars, and private lessons.") + f"""
<section class="section">
  <div class="carousel wide" data-carousel tabindex="0" aria-roledescription="carousel" aria-label="Class photos">
    <div class="track">{slides}</div>
    <button class="car-btn prev" aria-label="Previous photo">&#8249;</button>
    <button class="car-btn next" aria-label="Next photo">&#8250;</button>
  </div>
</section>
<section class="section"><div class="wrap"><div class="daygrid">{"".join(cards)}</div>
  <p class="note">Check the <a href="calendar">monthly calendar</a> for holidays and special events.</p></div></section>""" + free_class()
    return page("classes.html", "Classes", body, "Class schedule by belt level: kids, advanced, kumite, weapons and competition team.")


def build_news():
    items = sorted(NEWS, key=lambda n: n["date"], reverse=True)
    years = {}
    for it in items:
        years.setdefault(it["date"][:4], []).append(it)
    chips = '<button class="chip" data-cat="all" aria-pressed="true">All</button>' + "".join(
        f'<button class="chip" data-cat="{k}" aria-pressed="false">{v}</button>' for k, v in CHIP_LABEL.items())
    groups = []
    for y, its in years.items():
        rows = []
        for it in its:
            d, c = it["date"], it["category"]
            dt = datetime.date.fromisoformat(d)
            text = "".join(f"<p>{e(t)}</p>" for t in it["text"])
            photo = (f'<button class="news-photo" data-full="{wix(it["photo"], 1600, name="full.jpg")}" aria-label="Enlarge photo: {e(it["title"])}">'
                     f'<img src="{wix(it["photo"], 480, 354, "news.jpg")}" alt="" loading="lazy" width="480" height="354"></button>')
            rows.append(f"""<li class="news-item" data-cat="{c}"><time datetime="{d}">{dt:%b} {dt.day}</time>
<div class="news-body"><h3>{e(it["title"])}</h3><span class="tag {c}">{CAT_LABEL[c]}</span>{text}</div>{photo}</li>""")
        groups.append(f'<section class="year-group"><h2>{y}</h2><ul class="news-list">{"".join(rows)}</ul></section>')
    body = title_block("News &amp; Updates", "Tournament results, promotions, and training events.") + f"""
<section class="section"><div class="wrap narrow">
  <div class="filters" data-news-filter role="group" aria-label="Filter news">{chips}</div>
  {"".join(groups)}
</div></section>
<div class="lightbox" role="dialog" aria-modal="true" aria-label="Enlarged photo"><button class="x" aria-label="Close">&times;</button><img alt=""></div>""" + free_class()
    return page("news.html", "News & Updates", body, "Tournament results, black belt promotions and training events from AABBA.")


def build_calendar():
    jump = "".join(f'<a class="chip" href="#m{i}">{n}</a>' for i, (n, m) in enumerate(CALENDAR))
    tabs = "".join(
        f'<section class="section" id="m{i}"><div class="wrap narrow"><div class="cal-frame"><img src="{wix(m, 1200, name="cal.png")}" alt="{n} class schedule" loading="{"eager" if i == 0 else "lazy"}"></div></div></section>'
        for i, (n, m) in enumerate(CALENDAR))
    body = title_block("Calendar", "Monthly schedules, including holidays and special events.") + \
        f'<div class="wrap narrow"><div class="filters">{jump}</div></div>' + tabs + free_class()
    return page("calendar.html", "Calendar", body, "Monthly class calendar for All American Black Belt Academy.")


def build_gallery():
    photos = list(dict.fromkeys([c[3] for c in CLASSES] + list(DAY_PHOTOS.values()) + SLIDESHOW))
    tiles = "".join(
        f'<button data-full="{wix(m, 1600, name="full.jpg")}" aria-label="Enlarge photo {i + 1}"><img src="{wix(m, 480, name="photo.jpg")}" alt="" loading="lazy"></button>'
        for i, m in enumerate(photos))
    body = title_block("Gallery", "Photos from classes, tournaments, and events at the dojo.") + f"""
<section class="section"><div class="wrap"><div class="masonry">{tiles}</div></div></section>
<div class="lightbox" role="dialog" aria-modal="true" aria-label="Enlarged photo"><button class="x" aria-label="Close">&times;</button><img alt=""></div>""" + free_class()
    return page("gallery.html", "Gallery", body, "Photos from classes, tournaments and events at All American Black Belt Academy.")


def build_kata():
    rows = []
    for name, yt in KATA:
        if yt:
            action = f'<button class="btn red small" data-yt="{e(yt)}" aria-label="Watch {e(name)}">Watch</button>'
        else:
            action = '<span class="soon">Video coming soon</span>'
        rows.append(f'<li><div class="kata-row"><span class="kata-name">{e(name)}</span>{action}</div></li>')
    body = title_block("Kata Videos", "Practice videos for each kata in our curriculum.") + f"""
<section class="section"><div class="wrap narrow"><ul class="kata-list">{"".join(rows)}</ul></div></section>""" + free_class()
    return page("kata.html", "Kata Videos", body, "Kata practice videos from All American Black Belt Academy.")


def build_tests():
    options = "".join(f'<option value="{t["id"]}" data-file="{t["file"]}" data-iterations="{t["iterations"]}">{e(t["label"])}</option>' for t in TESTS)
    body = title_block("Belt Tests", "Students: choose your belt and enter the password Sensei Eric gave you to open your written test.") + f"""
<section class="section"><div class="wrap narrow">
  <form class="test-box" id="test-form" novalidate>
    <label for="belt">Your belt</label>
    <select id="belt"><option value="">Choose your belt</option>{options}</select>
    <label for="pw">Password</label>
    <input id="pw" type="password" autocomplete="off" autocapitalize="none" spellcheck="false">
    <label class="check"><input type="checkbox" id="showpw"> Show password</label>
    <button class="btn red" type="submit">Open Test</button>
    <p id="test-msg" role="status" aria-live="polite"></p>
  </form>
  <div id="test-result" class="test-result" hidden>
    <h3></h3>
    <div class="actions"><a class="btn red open" target="_blank" rel="noopener">Open in New Tab</a><a class="btn outline download">Download</a></div>
    <iframe class="test-frame" title="Belt test"></iframe>
  </div>
  <p class="note">Don&rsquo;t have a password yet? Ask Sensei Eric when you&rsquo;re ready to test for your next belt.</p>
</div></section>""" + free_class()
    return page("tests.html", "Belt Tests", body, "Written belt tests for students of All American Black Belt Academy.",
                extra_body=f'<script src="js/tests.js?v={ver("js/tests.js")}"></script>')


if __name__ == "__main__":
    for fn, builder in [("index.html", build_index), ("instructors.html", build_instructors),
                        ("classes.html", build_classes), ("news.html", build_news),
                        ("gallery.html", build_gallery), ("kata.html", build_kata),
                        ("tests.html", build_tests), ("calendar.html", build_calendar)]:
        (ROOT / fn).write_text(builder(), encoding="utf-8")
        print("wrote", fn)
