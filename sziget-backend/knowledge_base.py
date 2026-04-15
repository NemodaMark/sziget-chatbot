# Barni által elkészített adatbázis

data = [

    ("Idén is augusztus elején lesz a Sziget?", "festival_info",
     "Igen, a Sziget általában augusztus elején kerül megrendezésre, kb. 6 napig tart."),

    ("Ugyanúgy 6 napos lesz mint tavaly?", "festival_info",
     "Igen, a fesztivál jellemzően 6 napos programmal zajlik."),

    ("Mikor kezdődik pontosan az idei?", "festival_info",
     "A pontos dátumot minden évben külön jelentik be, de általában augusztus elején indul."),

    ("Ugyanott lesz megint az Óbudain?", "festival_info",
     "Igen, a Sziget minden évben az Óbudai-szigeten kerül megrendezésre Budapesten."),

    ("HÉV még mindig a legjobb opció kijutni?", "festival_info",
     "Igen, a HÉV az egyik leggyorsabb és legkényelmesebb mód a kijutásra."),

    ("Mikor szokták bejelenteni a fellépőket?", "festival_info",
     "A fellépőket általában hónapokkal a fesztivál előtt kezdik el bejelenteni."),

    ("Hány színpad van kb?", "festival_info",
     "Több nagy és kisebb színpad is van, különböző zenei stílusokkal."),

    ("Mikor van a Sziget 2026-ban?", "festival_info",
     "A Sziget 2026-ban is augusztus elején kerül megrendezésre az Óbudai-szigeten."),

    ("Hol van a Sziget helyszíne?", "festival_info",
     "Igen, a Sziget minden évben az Óbudai-szigeten kerül megrendezésre Budapesten."),

    ("Hogyan lehet kijutni a Szigetre?", "festival_info",
     "Igen, a HÉV az egyik leggyorsabb és legkényelmesebb mód a kijutásra."),

    ("Hány napos a fesztivál?", "festival_info",
     "Igen, a fesztivál jellemzően 6 napos programmal zajlik."),

    # --- pricing ---
    ("Drágább lett idén a bérlet?", "pricing",
     "A jegyárak évről évre változnak, de általában enyhén emelkednek."),

    ("Early bird még megéri?", "pricing",
     "Igen, az early bird jegyek általában olcsóbbak, ezért érdemes korán megvenni."),

    ("Van még valami kedvezmény?", "pricing",
     "Időszakosan lehetnek akciók, de klasszikus diák kedvezmény ritkán van."),

    ("Még mindig cashless az egész?", "pricing",
     "Igen, a Sziget jellemzően cashless rendszerben működik, kártyával fizetsz."),

    ("Lehet kártyával fizetni?", "pricing",
     "Igen, szinte mindenhol lehet bankkártyával fizetni a fesztiválon."),

    ("Mennyibe kerül egy napijegy?", "pricing",
     "A napijegyek ára változó, de általában több tíz euró körül alakul."),

    ("Drága a kaja bent?", "pricing",
     "A fesztiválon az árak általában magasabbak, mint a városban."),

    ("Drágák az ételek a Szigeten?", "pricing",
     "A fesztiválon az árak általában magasabbak, mint a városban."),

    ("Mennyibe kerül a belépő?", "pricing",
     "A napijegyek ára változó, de általában több tíz euró körül alakul."),

    # --- camping ---
    ("Alapkemping még mindig oké?", "camping",
     "Az alapkemping benne van a bérletben, de elég zsúfolt lehet."),

    ("Megéri upgrade-elni a kempinget?", "camping",
     "Ha kényelmesebb körülményeket szeretnél, akkor igen, megéri upgrade-elni."),

    ("Van zuhany a kempingben?", "camping",
     "Igen, vannak zuhanyzók, de csúcsidőben sorban kell állni."),

    ("Mennyire gáz a wc helyzet?", "camping",
     "A wc-k rendszeresen takarítottak, de a forgalmas időszakokban zsúfoltak."),

    ("Lehet áramot használni a kempingben?", "camping",
     "Egyes kempingekben van áram, de az alap kempingben általában nincs."),

    ("Mennyire hangos éjszaka?", "camping",
     "A kempingben éjszaka is lehet zaj, főleg a forgalmas részeken."),

     ("Milyen a sátorozási lehetőség a Szigeten?", "camping",
     "Az alapkemping benne van a bérletben, de elég zsúfolt lehet. Prémium kempingek is elérhetők."),

    ("Mennyire zsúfolt a kemping a Szigeten?", "camping",
     "A kemping főleg csúcsidőben lehet zsúfolt, de prémium opcióval kényelmesebb elhelyezést kaphatsz."),

    # --- rules ---
    ("Kaját még mindig lehet bevinni?", "rules",
     "Kis mennyiségű ételt általában be lehet vinni, de korlátozások lehetnek."),

    ("Szigorítottak a beengedésen?", "rules",
     "A biztonsági ellenőrzés szigorú, különösen a tiltott tárgyak miatt."),

    ("Mennyire para a lopás?", "rules",
     "Alapvetően biztonságos, de érdemes vigyázni az értékeidre."),

    ("Biztonságos mostanában?", "rules",
     "Igen, a szervezők nagy hangsúlyt fektetnek a biztonságra."),

    ("Mit nem lehet bevinni?", "rules",
     "Tiltott tárgyakat, például veszélyes eszközöket nem lehet bevinni."),

    ("Van beléptetésnél ellenőrzés?", "rules",
     "Igen, a belépésnél biztonsági ellenőrzésen kell átesni."),

    # --- general ---
    ("Megéri idén is menni?", "general",
     "Ha szereted a fesztiválhangulatot és a nemzetközi zenét, akkor igen, megéri."),

    ("Mennyire van tele mostanában?", "general",
     "A Sziget nagyon népszerű, ezért csúcsidőben kifejezetten zsúfolt lehet."),

    ("Milyen az általános hangulat?", "general",
     "Nemzetközi, sokszínű és nagyon pörgős fesztiválhangulat jellemzi."),

    ("Sok külföldi van?", "general",
     "Igen, a Sziget nagyon nemzetközi fesztivál, sok külföldi látogatóval."),

    ("Milyen a közönség általában?", "general",
     "Fiatalos, nyitott és bulizós közösség jellemzi a fesztivált."),

    ("Érdemes-e menni a Szigetre?", "general",
     "Ha szereted a fesztiválhangulatot és a nemzetközi zenét, akkor igen, megéri."),

    ("Sokan vannak a Szigeten?", "general",
     "A Sziget nagyon népszerű, ezért csúcsidőben kifejezetten zsúfolt lehet."),

    ("Ajánlod a Szigetet?", "general",
     "Ha szereted a fesztiválhangulatot és a nemzetközi zenét, akkor igen, megéri."),

    # --- lineup_schedule ---
    ("Kik lépnek fel idén a Szigeten?", "lineup_schedule",
     "A 2026-os Sziget fellépői között szerepel többek között: Twenty One Pilots, Florence + The Machine, "
     "Lewis Capaldi, Zara Larsson, Bring Me The Horizon, Skepta, Jorja Smith, Peggy Gou, Biffy Clyro, "
     "Ashnikko, bbno$, Tash Sultana, Underworld és sok más előadó."),

    ("Milyen a lineup 2026-ban?", "lineup_schedule",
     "A lineup nagyon erős nemzetközi szinten: pop, rock, elektronikus és hip-hop előadók is vannak, "
     "például Florence + The Machine, Bring Me The Horizon, Peggy Gou és Skepta."),

    ("Milyen stílusok vannak a lineupban?", "lineup_schedule",
     "A lineup nagyon változatos: pop, rock, indie, elektronikus, techno és hip-hop előadók is szerepelnek."),

    ("Van magyar fellépő is?", "lineup_schedule",
     "Igen, több magyar előadó is fellép, például Elefánt és Sisi."),

    ("Ki lép fel melyik nap?", "lineup_schedule",
     "1. nap: nagy pop headlinerek (pl. Zara Larsson) | 2. nap: alternatív/indie (pl. Florence + The Machine) | "
     "3. nap: rock/metal (pl. Bring Me The Horizon) | 4. nap: elektronikus (pl. Peggy Gou) | "
     "5. nap: vegyes headlinerek (pl. Twenty One Pilots). A pontos napi bontás a hivatalos oldalon frissül."),

    ("Milyen fellépők vannak napokra bontva?", "lineup_schedule",
     "A fellépők napokra bontva vannak beosztva, és a lista folyamatosan frissül a hivatalos oldalon."),

    ("Lesz lineup napi bontásban?", "lineup_schedule",
     "Igen, a Sziget minden évben napi bontásban közli a fellépőket."),

    ("Melyik nap lesznek a nagy headlinerek?", "lineup_schedule",
     "A headlinerek általában estére vannak időzítve minden nap. "
     "Ilyen fellépők például: Twenty One Pilots, Florence + The Machine és Lewis Capaldi."),

    ("Milyen a heti lineup?", "lineup_schedule",
     "1. nap: headliner + több nemzetközi előadó | 2. nap: elektronikus és pop | 3. nap: rock és alternatív | "
     "4. nap: vegyes lineup | 5. nap: nagy headlinerek | 6. nap: záró fellépők. "
     "A pontos lista mindig a hivatalos oldalon található."),

    ("Hol találom a fellépők listáját?", "lineup_schedule",
     "A legfrissebb lineup mindig a hivatalos Sziget weboldalon érhető el: https://szigetfestival.com/hu/program#/"),

     ("Hol nézhetem meg a menetrendet?", "lineup_schedule",
     "A legfrissebb lineup és menetrend mindig a hivatalos Sziget weboldalon érhető el: https://szigetfestival.com/hu/program#/"),

    # --- programs ---
    ("Mit lehet csinálni a koncerteken kívül?", "programs",
     "A Szigeten rengeteg extra program van: workshopok, színház, installációk és chill zónák."),

    ("Van valami érdekes program a bulin kívül?", "programs",
     "Igen, például művészeti installációk, street performance-ok és nappali programok is vannak."),

    ("Milyen programokat ajánlasz napközben?", "programs",
     "Napközben érdemes workshopokra menni, strandolni vagy felfedezni az interaktív installációkat."),

    ("Van valami nyugisabb program is?", "programs",
     "Igen, vannak chill zónák, jóga, beszélgetések és relax programok is."),

    ("Mit érdemes kipróbálni a Szigeten?", "programs",
     "Top programötletek: óriás installációk és fényshow-k, nemzetközi street food, "
     "workshopok és kreatív programok, chill zónák és nappali pihenés, kisebb színpadok felfedezése."),

    ("Vannak workshopok a fesztiválon?", "programs",
     "Igen, számos workshop és kreatív foglalkozás várja a látogatókat napközben."),

    ("Milyen szórakozási lehetőség van a Szigeten?", "programs",
     "A Szigeten rengeteg szórakozási lehetőség van: programok, installációk, workshopok, chill zónák."),

    ("Mi van a koncerteken kívül?", "programs",
     "A Szigeten rengeteg extra program van: workshopok, színház, installációk és chill zónák."),
]
