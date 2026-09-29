#!/usr/bin/env python3
"""Generates the static pages in the repo root. Run: python3 tools/build.py"""
import datetime
import hashlib
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


def ver(path):
    """Content hash appended to asset URLs so browsers fetch the new file after each change."""
    return hashlib.md5((ROOT / path).read_bytes()).hexdigest()[:8]


def day_cards():
    cards = []
    for a, full in DAYS:
        rows = []
        for name, belts, sched in CLASSES:
            for t in sched.get(a, []):
                rows.append((t, name, belts))
        rows.sort(key=lambda r: (int(r[0].split(":")[0]) % 12 + (12 if "PM" in r[0] else 0), r[0]))
        lis = "".join(f"<li><b>{t}</b> {e(n)} <span>({e(b)})</span></li>" for t, n, b in rows)
        cards.append(f'<article class="daycard"><h3>{full}</h3><ul>{lis}</ul>'
                     f'<img src="{wix(DAY_PHOTOS[a], 480, 330, a + ".jpg")}" alt="" loading="lazy" width="480" height="330"></article>')
    cards.append(f'<article class="daycard"><h3>Saturday</h3><ul><li><b>10:00 AM &ndash; 2:00 PM</b> Reserved for Promotions / Seminars / Private Lessons</li></ul>'
                 f'<img src="{wix(DAY_PHOTOS["Sat"], 480, 330, "Sat.jpg")}" alt="" loading="lazy" width="480" height="330"></article>')
    return '<div class="daygrid">' + "".join(cards) + "</div>"


def contact_buttons():
    return f"""<div class="contact-row">
  <a class="cbtn gray" href="mailto:{EMAIL}">{ICONS['mail']}<span>{EMAIL}</span></a>
  <a class="cbtn red" href="tel:{PHONE_TEL}">{ICONS['phone']}<span>925 829 4265</span></a>
</div>"""


def free_class():
    return f"""<section class="free"><div class="wrap">
  <hr class="gold">
  <h2>Drop in for a free, introductory class</h2>
  <p class="addr"><a href="{MAPS}" target="_blank" rel="noopener">{e(ADDRESS)}</a></p>
  {contact_buttons()}
</div></section>"""


def page(fname, title, body, description, extra_body=""):
    cur = ' aria-current="page"'
    nav = "".join(f'<li><a href="{f}"{cur if f == fname else ""}>{e(t)}</a></li>' for f, t in PAGES)
    social = "".join(f'<a href="{u}" target="_blank" rel="noopener">{n}</a>' for n, u in SOCIAL)
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
    <a class="brand" href="index.html"><span class="title">{NAME}</span><span class="motto">Excellence Through Efforts</span></a>
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
    <p class="social">{social}</p>
    <p class="copy">{NAME} &middot; {e(ADDRESS)} &middot; Unofficial redesign concept</p>
  </div>
</footer>
<script src="js/main.js?v={ver('js/main.js')}"></script>
{extra_body}
</body>
</html>
"""


def title_block(h1, lead=""):
    logos = f'<img class="logo" src="{wix(LOGO_FLAG, 240, 186, "logo.jpg")}" alt="" width="120" height="93">'
    fist = f'<img class="logo" src="{wix(LOGO_FIST, 192, 208, "fist.jpg")}" alt="" width="96" height="104">'
    return f"""<section class="pagehead"><div class="wrap narrow"><div class="headrow">{logos}<h1>{h1}</h1>{fist}</div><hr class="gold">{f'<p class="lead">{lead}</p>' if lead else ''}</div></section>"""


def build_index():
    bio = "".join(f"<li>{e(t)}</li>" for t in SHIHAN)
    body = f"""<section class="hero">
  <img class="hero-bg" src="{wix(HERO, 1600, 700, 'belts.jpg')}" alt="" fetchpriority="high">
  <div class="wrap"><div class="panel">
    <p>The All American Black Belt Academy believes in and teaches Martial arts with traditional values of respect, self-discipline, humility and dedication to excellence.</p>
    <p>AABBA is well known for its high-level instruction and world-class athletes, but most notably, for its holistic methods to teach skills with an emphasis on health and fitness wellness.</p>
    <p>Shihan Hultin has had a positive impact on students&rsquo; lives while developing lasting relationships that will be remembered for years to come.</p>
  </div></div>
</section>
{title_block("Classes and Courses")}
<section class="section"><div class="wrap narrow">{day_cards()}
  <p class="note">Check the <a href="calendar.html">monthly calendar</a> for holidays and special events.</p></div></section>
<section class="section shihan"><div class="wrap narrow">
  <h2>Shihan Hultin &amp; his dojo</h2>
  <ul>{bio}</ul>
</div></section>
{free_class()}"""
    return page("index.html", "Welcome", body, "Traditional Shitoryu karate for kids and adults in San Ramon, CA. Drop in for a free introductory class.")


def build_instructors():
    cards = []
    for role, name, img, items in INSTRUCTORS:
        lis = "".join(f"<li>{e(x)}</li>" for x in items)
        cards.append(f"""<article class="person"><img src="{wix(img, 300, 400, name.lower().replace(' ', '-') + '.jpg')}" alt="{name}" loading="lazy" width="300" height="400">
<div><h3>{role} {name}</h3><ul>{lis}</ul></div></article>""")
    body = title_block("Instructors") + f'<section class="section"><div class="wrap narrow"><div class="people">{"".join(cards)}</div></div></section>' + free_class()
    return page("instructors.html", "Instructors", body, "Meet the black belt instructors at All American Black Belt Academy.")


def build_classes():
    cards = []
    for name, belts, sched in CLASSES:
        rows = "".join(f'<li><b>{full}</b><span>{" &amp; ".join(sched[a])}</span></li>' for a, full in DAYS if a in sched)
        cards.append(f'<article class="daycard"><h3>{e(name)}</h3><p class="belts">{e(belts)}</p><ul class="times">{rows}</ul></article>')
    slides = "".join(
        f'<div class="slide" role="group" aria-roledescription="slide" aria-label="Photo {i + 1} of {len(CLASS_PHOTOS)}">'
        f'<img src="{wix(m, 1000, 625, "class.jpg")}" alt="{e(a)}" loading="{"eager" if i == 0 else "lazy"}" width="1000" height="625"></div>'
        for i, (m, a) in enumerate(CLASS_PHOTOS))
    thumbs = "".join(
        f'<button aria-label="Show photo {i + 1}" aria-current="false"><img src="{wix(m, 168, 116, "t.jpg")}" alt="" loading="lazy" width="84" height="58"></button>'
        for i, (m, a) in enumerate(CLASS_PHOTOS))
    body = title_block("Classes", "Monday through Friday, by belt level. Saturdays are reserved for promotions, seminars and private lessons.") + f"""
<section class="section"><div class="wrap narrow">
  <div class="carousel" data-carousel tabindex="0" aria-roledescription="carousel" aria-label="Class photos">
    <div class="track">{slides}</div>
    <button class="car-btn prev" aria-label="Previous photo">&#8249;</button>
    <button class="car-btn next" aria-label="Next photo">&#8250;</button>
    <div class="thumbs">{thumbs}</div>
    <p class="car-count" aria-live="polite"></p>
  </div>
</div></section>
<section class="section"><div class="wrap narrow"><div class="daygrid">{"".join(cards)}</div>
  <p class="note">Or see the <a href="index.html">schedule by day</a> on the welcome page.</p></div></section>""" + free_class()
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
            rows.append(f"""<li class="news-item" data-cat="{c}"><time datetime="{d}">{dt:%b} {dt.day}</time>
<div><h3>{e(t)}</h3><p><span class="tag {c}">{CAT_LABEL[c]}</span>{e(s)}</p>{med}</div></li>""")
        groups.append(f'<section class="year-group"><h2>{y}</h2><ul class="news-list">{"".join(rows)}</ul></section>')
    body = title_block("News &amp; Updates", "Tournament results, promotions and training events, newest first.") + f"""
<section class="section"><div class="wrap narrow">
  <div class="filters" data-news-filter role="group" aria-label="Filter news">{chips}</div>
  {"".join(groups)}
</div></section>""" + free_class()
    return page("news.html", "News & Updates", body, "Tournament results, black belt promotions and training events from AABBA.")


def build_media():
    photos = "".join(
        f'<button data-full="{wix(m, 1600, name="full.jpg")}" aria-label="Enlarge photo: {e(a)}"><img src="{wix(m, 480, name="thumb.jpg")}" alt="{e(a)}" loading="lazy"></button>'
        for m, a in CLASS_PHOTOS)
    kata = "".join(f"<li>{k}</li>" for k in KATA)
    body = title_block("Media", "Photos from the dojo and the kata we practice.") + f"""
<section class="section"><div class="wrap narrow"><h2>Photos</h2><div class="masonry">{photos}</div></div></section>
<section class="section"><div class="wrap narrow"><h2>Kata</h2>
  <p class="note">Video links can be added next to each kata once the academy shares them.</p>
  <ul class="kata-list">{kata}</ul></div></section>
<div class="lightbox" role="dialog" aria-modal="true" aria-label="Enlarged photo"><button class="x" aria-label="Close">&times;</button><img alt=""></div>""" + free_class()
    return page("media.html", "Media", body, "Photos and kata from All American Black Belt Academy.")


def build_calendar():
    jump = "".join(f'<a class="chip" href="#m{i}">{n}</a>' for i, (n, m) in enumerate(CALENDAR))
    tabs = "".join(
        f'<section class="section" id="m{i}"><div class="wrap narrow"><h2>{n}</h2><div class="cal-frame"><img src="{wix(m, 1200, name="cal.png")}" alt="{n} class schedule" loading="{"eager" if i == 0 else "lazy"}"></div></div></section>'
        for i, (n, m) in enumerate(CALENDAR))
    body = title_block("Calendar", "Monthly schedules, including holidays and special events.") + \
        f'<div class="wrap narrow"><div class="filters">{jump}</div></div>' + tabs + free_class()
    return page("calendar.html", "Calendar", body, "Monthly class calendar for All American Black Belt Academy.")


if __name__ == "__main__":
    for fn, builder in [("index.html", build_index), ("instructors.html", build_instructors),
                        ("classes.html", build_classes), ("news.html", build_news),
                        ("media.html", build_media), ("calendar.html", build_calendar)]:
        (ROOT / fn).write_text(builder(), encoding="utf-8")
        print("wrote", fn)
