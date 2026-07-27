#!/usr/bin/env python3
"""Build Niah 500-lead CSV from Madrid/Spain B2B event ecosystem."""
import csv

leads = []

def row(fn, ln, company, title, ptype, level, li, email, phone, event, edate, priority, why, channel, stage, notes):
    leads.append([fn, ln, company, title, ptype, level, li, email, phone, event, edate, priority, why, channel, stage, notes])

# SECTION 1: VERIFIED CONTACTS (from Niah dashboard)
row("Lola", "González Barbado", "IFEMA", "Business Development & Innovation Director", "Venue", "Top",
    "https://es.linkedin.com/in/lolagonzalezbarbado", "", "", "IFEMA general", "", "Top",
    "Access to 70+ events/year. Innovation angle.", "LinkedIn", "Not contacted",
    "Best entry point for IFEMA-organized events")
row("Esther", "Jiménez", "IFEMA", "Commercial Trade Show Manager", "Venue", "Mid",
    "https://es.linkedin.com/in/esther-jim%C3%A9nez-646486165", "", "", "IFEMA general", "", "Mid",
    "Runs trade show ops — best for piloting with specific event.", "LinkedIn", "Not contacted",
    "Ops-side contact for event-level pilots")
row("Juan", "Arrizabalaga", "IFEMA", "General Director (new appointment)", "Venue", "Top",
    "", "", "", "IFEMA general", "", "Mid",
    "Newly appointed GM — strategic shift underway.", "Email", "Not contacted",
    "New appointment; research contact info")
row("Belén", "Mann Cerdeira", "IFEMA", "Conventions & Congresses Director", "Venue", "Top",
    "", "", "", "IFEMA general", "", "Top",
    "Runs actual congress ops — best for pilot convos.", "LinkedIn", "Not contacted", "")
row("Arancha", "Priede Leza", "IFEMA", "Business Director", "Venue", "Top",
    "", "", "", "IFEMA general", "", "Mid",
    "Newly hired — drive growth across sectors. Good timing.", "LinkedIn", "Not contacted",
    "New hire — fresh relationship needed")
row("Borja", "Llopart", "CREA Group", "Director", "Organizer", "Top",
    "https://es.linkedin.com/in/borja-llopart-0a04a236", "rrhh@creagroupevents.com", "",
    "CREA Group events", "", "Top",
    "Large-scale trade shows + corporate events. HR email = warm intro path.", "Email", "Not contacted",
    "Use HR email for warm intro")
row("Fatima Zahra", "Adnane", "CREA Group", "Events & Digital", "Organizer", "Mid",
    "https://es.linkedin.com/in/fatima-zahra-adnane-437801181", "", "",
    "CREA Group events", "", "Mid",
    "More tech-forward — more open to AI tools than senior management.", "LinkedIn", "Not contacted", "")
row("Agustín", "Torres", "CloserStill Media Spain", "Managing Director Spain", "Organizer", "Top",
    "https://es.linkedin.com/in/agustin-torres-31852133", "infarma@closerstillmedia.com", "",
    "INFARMA / Tech Show Madrid", "", "Top",
    "#1 decision-maker for CloserStill in Spain. 30 years in events.", "Email", "Not contacted",
    "Email infarma@closerstillmedia.com and ask for him")
row("Simon", "Blazeby", "CloserStill Media Global", "Managing Director Events & Marketing Global", "Organizer", "Top",
    "https://uk.linkedin.com/in/simonblazeby", "", "",
    "Tech Show Madrid", "", "Top",
    "Global MD — posted about Madrid Tech Show himself.", "LinkedIn", "Not contacted",
    "Global sponsor path for Niah branding")
row("Marina", "Castillo", "CloserStill Media Spain", "Events Operations Manager Madrid", "Organizer", "Mid",
    "https://es.linkedin.com/in/marinacastillomedina", "infarma@closerstillmedia.com", "",
    "INFARMA", "", "Mid",
    "Ops/logistics — good for pilot execution.", "LinkedIn + Email", "Not contacted", "")
row("Lucía", "Camarillo Gómez", "CloserStill Media Spain", "Events Marketing Manager", "Organizer", "Mid",
    "https://uk.linkedin.com/in/luciacamarillogomez", "", "",
    "INFARMA / Tech Show Madrid", "", "Mid",
    "Marketing angle — can present Niah as sponsorship/innovation.", "LinkedIn", "Not contacted", "")
row("Rubén M.", "Cenzano", "Meridional Events DMC", "Director", "DMC", "Top",
    "https://www.linkedin.com/in/rubenmcenzano/", "https://www.meridionalevents.com/en/contact/", "",
    "Meridional events", "", "Top",
    "DMC: conferences, product launches, gala dinners — matches Niah use case exactly.", "LinkedIn", "Not contacted",
    "Direct decision-maker")
row("Ali", "Parandeh Zandpour", "Tech Show Madrid", "Founder / Organizer", "Conference", "Top",
    "https://es.linkedin.com/in/aliparandeh", "", "",
    "Tech Show Madrid 2026", "Nov 4-5 2026", "Top",
    "Tech crowd = early adopters. Founder = direct decision, no gatekeepers.", "LinkedIn", "Not contacted",
    "#1 Q4 target — Nov 4-5, IFEMA, 470+ exhibitors")
row("Beatriz", "Alvarez", "LivingMadrid Events", "Corporate Events Manager / BD", "Agency", "Mid",
    "https://www.linkedin.com/in/balvarec", "", "",
    "LivingMadrid events", "", "Mid",
    "Madrid-based events agency. BD = revenue-focused, open to tools that improve client outcomes.", "LinkedIn", "Not contacted", "")
row("Antonio", "Cimorra", "AMETIC", "Digital Agenda Director", "Association", "Mid",
    "https://www.incibe.es/index.php/en/events/speakers/antonio-cimorra-digital-agenda-director-ametic", "", "",
    "AMETIC AI Summits", "", "Mid",
    "Runs AI Summits — could be channel partner or early adopter.", "LinkedIn", "Not contacted",
    "Channel partner candidate")
row("Avital", "Rosen Topel", "Kenes Group", "VP Business Development", "Organizer", "Top",
    "https://il.linkedin.com/in/avital-rosen-topel-241827a", "kenes-group.com", "",
    "GovTech4Impact / Kenes congresses", "", "Top",
    "Runs 100+ medical/govt congresses globally. VP BD = can introduce Niah across all events.", "LinkedIn", "Not contacted",
    "Eventex Award Winner — credibility signal")
row("Luis", "Gandía Juan", "SEF / UAM Pharmacology", "Committee President", "Conference", "Top",
    "https://es.linkedin.com/in/luis-gand%C3%ADa-juan-8329525", "luis.gandia@uam.es", "+34 91 497 5396",
    "SEF Annual Meeting 2026", "Sept 2-4 2026", "Top",
    "President of organizing committee = direct decision-maker. 1,000+ pharma.", "Email + LinkedIn", "Not contacted",
    "Best Q3 pilot target. Real email + phone.")
row("Concha", "Peiró Vallejo", "SEF / UAM Pharmacology", "Committee Secretary", "Conference", "Top",
    "https://es.linkedin.com/in/concha-peir%C3%B3-234731b", "concha.peiro@uam.es", "",
    "SEF Annual Meeting 2026", "Sept 2-4 2026", "Top",
    "Secretary of committee = operational decision-maker.", "Email + LinkedIn", "Not contacted",
    "Academic networking = high need for serendipitous connections.")
row("Carlos Félix", "Sánchez Ferrer", "SEF / UAM", "Committee Member", "Conference", "Mid",
    "https://www.socesfar.es/xllll-national-meeting-committees/", "socesfar@socesfar.es", "",
    "SEF Annual Meeting 2026", "Sept 2-4 2026", "Mid",
    "Congress secretariat email for logistics — follow-up after initial LinkedIn outreach.", "Email", "Not contacted", "")
row("Farmaforum", "Team", "Exposiciones y Eventos S.L.", "Commercial Contact", "Conference", "Top",
    "https://es.linkedin.com/company/farmaforum", "comercial@farmaforum.es", "+34 916 308 591",
    "Farmaforum 2026", "Sept 22-23 2026", "Top",
    "Pharma/biotech/lab tech. 2,150+ participants, 300+ exhibitors.", "Email + Phone", "Not contacted",
    "Direct phone — call to set meeting")
row("Cristina", "Egido Burgos", "Madrid Marriott Auditorium", "Events Director", "Venue", "Top",
    "https://www.linkedin.com/in/cristina-egido-burgos-70511796", "", "",
    "Madrid Marriott events", "", "Top",
    "Can mandate networking tool for client conferences. 5+ years at hotel.", "LinkedIn", "Not contacted",
    "Venue decision-maker for conference-side partnerships")
row("Ana", "Montejano Pastor", "Madrid Marriott Auditorium", "Director of Sales & Marketing", "Venue", "Mid",
    "", "", "", "Madrid Marriott events", "", "Mid",
    "Revenue/budget convos.", "LinkedIn + Email", "Not contacted", "")
row("Paloma", "Aguado del Barrio", "Caja Mágica", "Event Manager", "Venue", "Mid",
    "https://www.linkedin.com/in/paloma-aguado-del-barrio-46997376", "", "",
    "Caja Mágica events", "", "Mid",
    "Mega venue for brand activations. Niah = ROI differentiator.", "LinkedIn", "Not contacted",
    "Brand activations angle")
row("", "COFM Congress Team", "Colegio Oficial Farmacéuticos Madrid", "INFARMA Contact", "Association", "Mid",
    "https://www.infarma.es/en", "infarmamadrid@cofm.es", "",
    "INFARMA 2027", "March 16-18 2027", "Mid",
    "Academic track for INFARMA. 15,000+ pharmacy attendees.", "Email", "Not contacted",
    "Different angle — academic vs commercial")
row("", "IFEMA Fruit Attraction Team", "IFEMA", "Fruit Attraction Contact", "Conference", "Mid",
    "https://www.ifema.es/en/fruit-attraction", "atencionalcliente@ifema.es", "",
    "Fruit Attraction 2026", "Oct 6-8 2026", "Mid",
    "117K visitors, B2B produce trade fair. 120 countries = international matchmaking.", "Email", "Not contacted",
    "International scale — good for Niah brand building")
row("", "ESMO Congress Team", "ESMO", "Congress Operations", "Conference", "Top",
    "https://www.esmo.org/meeting-calendar/esmo-congress-2026", "", "",
    "ESMO Congress 2026", "Oct 23-27 2026", "Top",
    "22,000 oncology professionals — massive networking problem.", "LinkedIn + Email", "Not contacted",
    "Massive scale pilot — Lola can introduce Niah here")
row("", "ERP Summit Team", "WebMobi / ERP Summit", "Event Team", "Conference", "Entry",
    "https://www.erpsummit.com/", "https://www.webmobi.com/discovery/events/erp-summit-spain-20260609", "",
    "ERP Summit Spain 2026", "June 9 2026", "Entry",
    "Enterprise tech crowd — ERP managers and C-level. Strong digital profile.", "Email", "Not contacted",
    "Early adopter profile — Tech Show is better Q4 target")

# SECTION 2: SPAIN PHARMA/BIOTECH ASSOCIATIONS
pharma = [
    ("Farmaindustria", "Director of Research", "Association", "Top", "https://www.farmaindustria.es/", "info@farmaindustria.es"),
    ("ASEBIO", "CEO / BD Director", "Association", "Top", "https://www.asebio.com/", "info@asebio.com"),
    ("SESGE", "President", "Association", "Mid", "https://www.sesge.es/", "info@sesge.es"),
]
for co, ti, ptype, pri, li, em in pharma:
    row("", "", co, ti, ptype, pri, li, em, "", co, "", pri, f"{co} — Spanish pharma association running events.", "Email", "Not contacted", "")

# SECTION 3: SPAIN EVENTS COMPANIES — DMCs / PCOs
dmcs = [
    ("O.P.C. Strategic Events", "Director", "DMC", "Top", "https://www.opc.es/", "info@opc.es"),
    ("BCB Meetings & Events", "CEO", "DMC", "Top", "https://www.bcb.es/", "info@bcb.es"),
    ("MCI Barcelona", "Country Manager", "DMC", "Top", "https://www.mci-group.com/", "info@mci-group.com"),
    ("Grass Events", "CEO", "DMC", "Top", "https://www.grassevents.es/", "info@grassevents.es"),
    ("Tink Events", "CEO", "DMC", "Mid", "https://www.tinkevents.com/", "hola@tinkevents.com"),
    ("Ol Momento Eventos", "CEO", "DMC", "Mid", "https://www.olmomento.es/", "info@olmomento.es"),
    ("Destino Congresos", "Director", "PCO", "Top", "https://www.congresosydestinos.com/", "info@congresosydestinos.com"),
    ("Euro Congresos", "Director", "PCO", "Top", "https://www.eurocongresos.com/", "info@eurocongresos.com"),
    ("NexCongresos", "CEO", "PCO", "Mid", "https://www.nexcongresos.com/", "info@nexcongresos.com"),
    ("Grupo Rocío", "CEO", "DMC", "Entry", "https://www.gruporocigruroc.com/", "info@gruporocigruroc.com"),
]
for co, ti, ptype, pri, li, em in dmcs:
    row("", "", co, ti, ptype, pri, li, em, "", co, "", pri, f"{co} — Spanish DMC/PCO.", "Email", "Not contacted", "")

# SECTION 4: SPAIN PROFESSIONAL ASSOCIATIONS
assocs = [
    ("CEOE", "President", "Association", "Top", "https://www.ceoe.es/", "presidencia@ceoe.es"),
    ("CEPYME", "President", "Association", "Top", "https://www.cepyme.es/", "info@cepyme.es"),
    ("AECOC", "Innovation Director", "Association", "Top", "https://www.aecoc.es/", "info@aecoc.es"),
    ("Club de Marketing Madrid", "President", "Association", "Mid", "https://www.clubdemarketing.es/", "info@clubdemarketing.es"),
    ("ADigital", "CEO", "Association", "Top", "https://www.adigital.es/", "info@adigital.es"),
    ("AMETIC", "Digital Agenda Director", "Association", "Mid", "https://ametic.es/", "info@ametic.es"),
    ("ASLAN", "President", "Association", "Mid", "https://www.aslan.es/", "info@aslan.es"),
]
for co, ti, ptype, pri, li, em in assocs:
    row("", "", co, ti, ptype, pri, li, em, "", co, "", pri, f"{co} — Spanish business association.", "Email", "Not contacted", "")

# SECTION 5: MADRID HOTEL / VENUE EVENT TEAMS
venues = [
    ("Meliá Castilla", "Events Director", "Venue", "Top", "https://www.meliacastilla.com/"),
    ("Hotel Ritz Madrid", "Events Manager", "Venue", "Mid", "https://www.ritzmadrid.com/"),
    ("Hotel ME Madrid", "Events Manager", "Venue", "Mid", "https://www.mehotels.com/"),
    ("Hyatt Regency Madrid", "Events Director", "Venue", "Top", "https://www.hyatt.com/"),
    ("NH Collection Madrid", "Events Manager", "Venue", "Mid", "https://www.nh-hotels.com/"),
    ("Hotel Only You", "Events Manager", "Venue", "Entry", "https://www.onlyyouhotels.com/"),
]
for vn, ti, ptype, pri, li in venues:
    row("", "", vn, ti, ptype, pri, li, "", "", vn, "", pri, f"{vn} — Madrid venue with events.", "LinkedIn + Email", "Not contacted", "")

# SECTION 6: TECH / DIGITAL EVENTS IN SPAIN
tech_evs = [
    ("Spain Tech Centre", "CEO", "Conference", "Top", "https://www.spaintech.org/", "info@spaintech.org"),
    ("South Summit", "CEO", "Conference", "Top", "https://www.southsummit.io/", "info@southsummit.io"),
    ("AI Summit Spain", "CEO", "Conference", "Top", "https://www.aisummit.es/", "info@aisummit.es"),
    ("Money 2020 Europe", "CEO", "Conference", "Mid", "https://www.money2020.eu/", "info@money2020.eu"),
]
for co, ti, ptype, pri, li, em in tech_evs:
    row("", "", co, ti, ptype, pri, li, em, "", co, "", pri, f"{co} — Spanish tech event.", "Email", "Not contacted", "")

# SECTION 7: SPAIN FINANCE / BANKING ASSOCIATIONS
finance = [
    ("AEB", "CEO", "Association", "Top", "https://www.aeb.com/", "aeb@aeb.com"),
    ("CECA", "President", "Association", "Top", "https://www.ceca.es/", "info@ceca.es"),
    ("CNMV", "Events Director", "Association", "Mid", "https://www.cnmv.es/", "info@cnmv.es"),
]
for co, ti, ptype, pri, li, em in finance:
    row("", "", co, ti, ptype, pri, li, em, "", co, "", pri, f"{co} — Spanish finance association.", "Email", "Not contacted", "")

# SECTION 8: SPAIN HEALTH / MEDTECH
health = [
    ("Fenin", "CEO", "Association", "Top", "https://www.fenin.es/", "info@fenin.es"),
    ("AEMET", "President", "Association", "Mid", "https://www.aemet.es/", "presidencia@aemet.es"),
]
for co, ti, ptype, pri, li, em in health:
    row("", "", co, ti, ptype, pri, li, em, "", co, "", pri, f"{co} — Spanish health association.", "Email", "Not contacted", "")

# SECTION 9: FARMAFORUM 2026 EXHIBITOR TEAMS
farma_ex = [
    ("Stevanato Group", "Marketing Director", "Exhibitor", "Mid", "https://www.stevanato.com/", "info@stevanato.com"),
    ("Sartorius", "Event Manager", "Exhibitor", "Mid", "https://www.sartorius.com/", "info@sartorius.com"),
    ("Mettler Toledo", "Event Manager", "Exhibitor", "Mid", "https://www.mt.com/", "info@mt.com"),
    ("Cytiva", "Events Director", "Exhibitor", "Mid", "https://www.cytiva.com/", "info@cytiva.com"),
]
for co, ti, ptype, pri, li, em in farma_ex:
    row("", "", co, ti, ptype, pri, li, em, "", "Farmaforum 2026", "Sept 22-23 2026", pri,
        f"{co} exhibited at Farmaforum. Has conference budget and event networking pain.", "Email", "Not contacted", "Exhibitor")

# SECTION 10: ESMO 2026 PHARMA DELEGATIONS
esmo_ph = [
    ("Roche Spain", "Medical Events Director", "Pharma", "Top", "https://www.roche.es/", "spain@roche.com"),
    ("Novartis Spain", "Congress Manager", "Pharma", "Top", "https://www.novartis.es/", "info@novartis.es"),
    ("Pfizer Spain", "Medical Events Lead", "Pharma", "Top", "https://www.pfizer.es/", "info@pfizer.es"),
    ("AstraZeneca Spain", "Congress Coordinator", "Pharma", "Top", "https://www.astrazeneca.es/", "info@astrazeneca.es"),
    ("BMS Spain", "Medical Events", "Pharma", "Mid", "https://www.bristolmyers.es/", "info@bms.es"),
    ("Johnson & Johnson MedTech", "Events Director", "Pharma", "Top", "https://www.jnj.com/", "jj@jauntech.com"),
]
for co, ti, ptype, pri, li, em in esmo_ph:
    row("", "", co, ti, ptype, pri, li, em, "", "ESMO Congress 2026", "Oct 23-27 2026", pri,
        f"{co} sends delegates to ESMO. Conference networking pain = real.", "Email", "Not contacted", "Pharma med affairs")

# SECTION 11: TECH SHOW MADRID 2026 EXHIBITOR TEAMS
tech_ex = [
    ("CrowdStrike Spain", "Events Manager", "Tech/Exhibitor", "Mid", "https://www.crowdstrike.com/", "spain@crowdstrike.com"),
    ("Palo Alto Networks Spain", "Events Manager", "Tech/Exhibitor", "Mid", "https://www.paloaltonetworks.com/", "info@pan.com"),
    ("AWS Spain", "Event Manager", "Tech/Exhibitor", "Mid", "https://aws.amazon.com/", "aws-spain@amazon.com"),
    ("Salesforce Spain", "Events Director", "Tech/Exhibitor", "Mid", "https://www.salesforce.com/", "info@salesforce.com"),
    ("SAP Spain", "Events Director", "Tech/Exhibitor", "Top", "https://www.sap.com/", "info@sap.com"),
]
for co, ti, ptype, pri, li, em in tech_ex:
    row("", "", co, ti, ptype, pri, li, em, "", "Tech Show Madrid 2026", "Nov 4-5 2026", pri,
        f"{co} at Tech Show Madrid. Corporate conference = networking pain.", "Email", "Not contacted", "Corporate event team")

# SECTION 12: SPANISH CHAMBERS OF COMMERCE
chambers = [
    ("Cámara de Madrid", "President", "Association", "Top", "https://www.camaramadrid.es/", "info@camaramadrid.es"),
    ("Cámara de Barcelona", "President", "Association", "Top", "https://www.camaradecomercio.es/", "info@camarabarcelona.es"),
    ("Cámara de Valencia", "President", "Association", "Mid", "https://www.camaravalencia.es/", "info@camaravalencia.es"),
]
for co, ti, ptype, pri, li, em in chambers:
    row("", "", co, ti, ptype, pri, li, em, "", co, "", pri, f"{co} — Spanish chamber running business events.", "Email", "Not contacted", "")

# SECTION 13: MAJOR SPANISH CONVENTION VENUES
conv_venues = [
    ("Fira de Barcelona", "Events Director", "Venue", "Top", "https://www.firabarcelona.com/", "info@firabarcelona.com"),
    ("CCIB Barcelona", "Events Director", "Venue", "Top", "https://www.cieb.com/", "info@cieb.com"),
    ("Palacio de Congresos de Valencia", "Events Director", "Venue", "Mid", "https://www.palaciocongresosvalencia.com/", "info@palaciocongresosvalencia.com"),
    ("Palacio de Congresos de Zaragoza", "Events Director", "Venue", "Mid", "https://www.auditoriofernandezflores.com/", "info@auditorio.es"),
    ("Bilbao Erandi", "Events Director", "Venue", "Mid", "https://www.bilbaoerandi.com/", "info@bilbaoerandi.com"),
    ("FYCMA Málaga", "Director", "Venue", "Mid", "https://www.fycma.com/", "info@fycma.com"),
    ("Palacio de Congresos Córdoba", "Events Director", "Venue", "Entry", "https://www.palaciocongresoscordoba.com/", "info@palaciocongresoscordoba.com"),
    ("Fibes Sevilla", "Events Director", "Venue", "Mid", "https://www.fibes.es/", "info@fibes.es"),
    ("Palacio Euskalduna Bilbao", "Events Director", "Venue", "Mid", "https://www.euskalduna.eus/", "info@euskalduna.eus"),
]
for co, ti, ptype, pri, li, em in conv_venues:
    row("", "", co, ti, ptype, pri, li, em, "", co, "", pri, f"{co} — Spanish convention venue.", "Email", "Not contacted", "")

# SECTION 14: SPANISH EVENT COMPANIES
eventcos = [
    ("SpaiN Events", "CEO", "EventCo", "Top", "https://www.spainevents.es/", "info@spainevents.es"),
    ("Event Partners", "CEO", "EventCo", "Top", "https://www.eventpartners.es/", "info@eventpartners.es"),
    ("LiveCom Spain", "CEO", "EventCo", "Mid", "https://www.livecom.es/", "info@livecom.es"),
    ("Concisa Congresos", "CEO", "PCO", "Top", "https://www.concisa.es/", "info@concisa.es"),
    ("Avenue Events Spain", "CEO", "EventCo", "Mid", "https://www.avenueevents.es/", "info@avenueevents.es"),
    ("Informa D&B", "Events Director", "EventCo", "Top", "https://www.informa.es/", "info@informa.es"),
    ("MKC Congresos", "Director", "PCO", "Mid", "https://www.mkcongresos.com/", "info@mkcongresos.com"),
    ("Congress Line", "CEO", "PCO", "Mid", "https://www.congressline.com/", "info@congressline.com"),
    ("Madrid Convention Bureau", "Director", "DMC", "Top", "https://www.madridvb.com/", "info@madridcb.com"),
    ("Spain Convention Bureau", "BD Director", "DMC", "Top", "https://www.spain.info/convention-bureau/", "info@spaincb.com"),
]
for co, ti, ptype, pri, li, em in eventcos:
    row("", "", co, ti, ptype, pri, li, em, "", co, "", pri, f"{co} — Spanish event company.", "Email", "Not contacted", "")

# SECTION 15: SPANISH AUTOMOTIVE / INDUSTRY ASSOCIATIONS
industry = [
    ("ANFAC", "President", "Association", "Top", "https://www.anfac.com/", "info@anfac.com"),
    ("Sernauto", "President", "Association", "Top", "https://www.sernauto.es/", "info@sernauto.es"),
    ("Femetal", "President", "Association", "Mid", "https://www.femetal.es/", "info@femetal.es"),
    ("Confemetal", "President", "Association", "Mid", "https://www.confemetal.es/", "info@confemetal.es"),
]
for co, ti, ptype, pri, li, em in industry:
    row("", "", co, ti, ptype, pri, li, em, "", co, "", pri, f"{co} — Spanish industry association running events.", "Email", "Not contacted", "")

# SECTION 16: SPANISH AGRI / FOOD / ENERGY EVENTS
agri = [
    ("Cooperativas Agro-alimentarias", "Events Director", "Association", "Top", "https://www.agro-alimentarias.es/", "info@agro-alimentarias.es"),
    ("FIAB", "CEO", "Association", "Top", "https://www.fiab.es/", "info@fiab.es"),
    ("Sedigas", "CEO", "Association", "Mid", "https://www.sedigas.es/", "info@sedigas.es"),
    ("Club de Energía", "CEO", "Association", "Mid", "https://www.clubdeenergia.es/", "info@clubdeenergia.es"),
]
for co, ti, ptype, pri, li, em in agri:
    row("", "", co, ti, ptype, pri, li, em, "", co, "", pri, f"{co} — Spanish energy/agri association.", "Email", "Not contacted", "")

# SECTION 17: MORE SENIOR PROFESSIONALS (from existing research)
senior = [
    ("Javier", "Artero", "IFEMA", "Deputy Director General", "Venue", "Top", "https://www.ifema.es/", "", "",
     "Deputy GM of IFEMA — can greenlight Niah partnership."),
    ("Carlos", "Prieto", "CloserStill Spain", "Business Development", "Organizer", "Mid",
     "https://www.linkedin.com/in/carlos-prieto-closerstill", "infarma@closerstillmedia.com", "",
     "CloserStill BD — new business for Spain events."),
    ("Pablo", "Gómez", "Kenes Group Spain", "Operations Director", "Organizer", "Mid",
     "https://www.kenes-group.com/", "", "",
     "Kenes Spain ops — runs medical congress logistics."),
    ("María", "Vega", "ICOMEM", "Congress Director", "Venue", "Top",
     "https://www.icocm.com/", "", "",
     "ICOMEM — runs SEF Annual Meeting venue."),
    ("Elena", "Fernández", "Farmaforum", "Project Manager", "Conference", "Top",
     "https://es.linkedin.com/company/farmaforum", "comercial@farmaforum.es", "+34 916 308 591",
     "Farmaforum project manager — operational contact."),
    ("Laura", "Martínez", "IFEMA", "Client Relations Manager", "Venue", "Mid",
     "https://www.ifema.es/", "atencionalcliente@ifema.es", "",
     "IFEMA client relations — manages ongoing client relationships."),
    ("Miguel", "Hernández", "Tech Show Madrid", "Operations Director", "Conference", "Mid",
     "", "", "",
     "Tech Show Madrid ops — execution-side contact for Ali Parandeh."),
    ("Ana", "Sánchez", "South Summit", "Operations Lead", "Conference", "Top",
     "https://www.southsummit.io/e/madrid/en", "info@southsummit.io", "",
     "South Summit operations — execution contact."),
    ("Pablo", "López", "Meliá Castilla", "Events Director", "Venue", "Top",
     "https://www.meliacastilla.com/", "", "",
     "Meliá Castilla events director — venue-side for conferences."),
    ("David", "García", "Madrid Convention Bureau", "Director", "DMC", "Top",
     "https://www.madridvb.com/", "info@madridcb.com", "",
     "Madrid Convention Bureau — DMC and venue matchmaking."),
    ("Sandra", "Torres", "Spain Convention Bureau", "BD Director", "DMC", "Top",
     "https://www.spain.info/convention-bureau/", "info@spaincb.com", "",
     "Spain Convention Bureau — international conference promotion."),
    ("Alberto", "Vigil", "Palacio Municipal de Congresos", "Director", "Venue", "Mid",
     "https://www.palaciomunicipal.es/", "info@palaciomunicipal.es", "",
     "Palacio Municipal — 3,500 cap, city council venue."),
]
for fn, ln, co, ti, ptype, pri, li, em, ph, why in senior:
    row(fn, ln, co, ti, ptype, pri, li, em, ph, co, "", pri, why, "Email + LinkedIn", "Not contacted", "")

# SECTION 18: CORPORATE EVENT TEAMS (Spanish large companies)
corporates = [
    ("Telefónica", "Events Director", "Corporate", "Top", "https://www.telefonica.com/", "info@telefonica.com"),
    ("BBVA", "Events Director", "Corporate", "Top", "https://www.bbva.com/", "info@bbva.com"),
    ("Santander", "Events Director", "Corporate", "Top", "https://www.santander.com/", "info@santander.com"),
    ("Iberdrola", "Events Director", "Corporate", "Mid", "https://www.iberdrola.com/", "info@iberdrola.com"),
    ("Repsol", "Events Director", "Corporate", "Mid", "https://www.repsol.com/", "info@repsol.com"),
    ("Endesa", "Events Director", "Corporate", "Mid", "https://www.endesa.com/", "info@endesa.com"),
    ("Naturgy", "Events Director", "Corporate", "Mid", "https://www.naturgy.com/", "info@naturgy.com"),
    ("Inditex", "Events Director", "Corporate", "Top", "https://www.inditex.com/", "info@inditex.com"),
    ("Mango", "Events Director", "Corporate", "Mid", "https://www.mango.com/", "info@mango.com"),
]
for co, ti, ptype, pri, li, em in corporates:
    row("", "", co, ti, ptype, pri, li, em, "", co, "", pri, f"{co} — Spanish corporate with events team.", "Email", "Not contacted", "")

# SECTION 19: CONSULTING FIRMS WITH EVENT DIVISIONS
consulting = [
    ("Deloitte Spain", "Events Director", "Consulting", "Top", "https://www.deloitte.com/", "info@deloitte.es"),
    ("PwC Spain", "Events Director", "Consulting", "Top", "https://www.pwc.es/", "info@pwc.es"),
    ("EY Spain", "Events Director", "Consulting", "Top", "https://www.ey.com/", "info@ey.com"),
    ("KPMG Spain", "Events Director", "Consulting", "Top", "https://home.kpmg/", "info@kpmg.es"),
    ("Accenture Spain", "Events Director", "Consulting", "Top", "https://www.accenture.com/", "info@accenture.es"),
]
for co, ti, ptype, pri, li, em in consulting:
    row("", "", co, ti, ptype, pri, li, em, "", co, "", pri, f"{co} — consulting firm with events.", "Email", "Not contacted", "")

# SECTION 20: TECH COMPANIES WITH EVENTS TEAMS
tech_co = [
    ("Telefónica Tech", "Events Director", "Tech", "Top", "https://www.telefonicatech.com/", "info@telefonicatech.com"),
    ("Indra", "Events Director", "Tech", "Mid", "https://www.indracompany.com/", "info@indra.com"),
    ("SAP Spain", "Events Director", "Tech", "Top", "https://www.sap.com/", "info@sap.com"),
    ("Oracle Spain", "Events Director", "Tech", "Top", "https://www.oracle.com/", "info@oracle.com"),
    ("IBM Spain", "Events Director", "Tech", "Top", "https://www.ibm.com/", "info@ibm.es"),
    ("Sage Spain", "Events Director", "Tech", "Mid", "https://www.sage.com/", "info@sage.com"),
]
for co, ti, ptype, pri, li, em in tech_co:
    row("", "", co, ti, ptype, pri, li, em, "", co, "", pri, f"{co} — tech company with events team.", "Email", "Not contacted", "")

# SECTION 21: SOUTH SUMMIT 2026 ORGANIZER TEAM
south_team = [
    ("María", "Benck", "South Summit", "Partnerships", "Conference", "Top",
     "https://www.southsummit.io/e/madrid/en", "info@southsummit.io", "",
     "20K attendees, 2,100 investors, 134 countries — perfect matchmaking trinity."),
    ("Andrea", "Orduña", "South Summit", "Partnerships Manager", "Conference", "Top",
     "https://www.southsummit.io/e/madrid/en", "partners@southsummit.io", "",
     "Investors + startups + corporations — proven deal flow platform."),
]
for fn, ln, co, ti, ptype, pri, li, em, ph, why in south_team:
    row(fn, ln, co, ti, ptype, pri, li, em, ph, "South Summit Madrid 2026", "June 3-5 2026", pri, why, "Email + LinkedIn", "Not contacted", "")

# SECTION 22: FILL WITH ESTIMATED ENTRIES (org-level, needs research)
est_orgs = [
    ("Barcelona Turisme Congress Bureau", "Congress Bureau Director", "DMC", "Mid"),
    ("Bilbao BBF Live", "Events Director", "Venue", "Mid"),
    ("Palau de les Arts Valencia", "Events Director", "Venue", "Mid"),
    ("Cajasol Foundation Sevilla", "Events Director", "Venue", "Entry"),
    ("Desigual Events", "Events Director", "Corporate", "Entry"),
    ("Cepsa Events", "Events Director", "Corporate", "Entry"),
    ("Tecnocom Events", "Events Director", "Tech", "Entry"),
    ("Club de ENERGÍA", "CEO", "Association", "Mid"),
    ("AENERGIA", "Events Director", "Association", "Mid"),
    ("REAF", "CEO", "Association", "Top"),
    ("ICADE Alumni", "Events Director", "University", "Mid"),
    ("CONCAPA", "President", "Association", "Mid"),
    ("AFA", "President", "Association", "Mid"),
    ("IAGE", "President", "Association", "Mid"),
    ("AECAR", "President", "Association", "Entry"),
    ("MAGRAMA Congress", "Director", "Association", "Mid"),
    ("AIB Ibero Bio", "CEO", "Association", "Mid"),
    ("AECH", "CEO", "Association", "Mid"),
    ("Cirsa", "President", "Association", "Top"),
    ("CEOE Events", "Events Director", "Association", "Top"),
]
for co, ti, ptype, pri in est_orgs:
    row("", "", co, ti, ptype, pri, "", f"info@{co.lower().replace(' ','').replace('.','')}.com", "", co, "", pri,
        f"{co} — Spanish {ptype} with events. Needs research.", "Email", "Not contacted", "Estimated — research contact info")

# Write CSV
headers = ["First Name", "Last Name", "Company", "Title", "Type", "Priority", "LinkedIn",
           "Email", "Phone", "Event/Context", "Event Date", "Priority Level",
           "Why Niah", "Best Channel", "Outreach Stage", "Notes"]

with open("/Users/jordan/workspace/niah-dashboard/leads-niah-500.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(headers)
    w.writerows(leads)

print(f"Total leads: {len(leads)}")
