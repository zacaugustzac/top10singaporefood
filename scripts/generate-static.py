#!/usr/bin/env python3
"""Generates one static HTML file per dish into dishes/. Run: python scripts/generate-static.py"""

import json, os, urllib.request, urllib.error, datetime

SUPABASE_URL = 'https://xlbgijjtxbflhkjftene.supabase.co'
SUPABASE_KEY = 'sb_publishable_1tTdNWd1N0n9w3ElrCynNw_ia1JWbc6'
BASE_URL     = 'https://top10singaporefood.com'
HEADERS      = {'apikey': SUPABASE_KEY, 'Authorization': f'Bearer {SUPABASE_KEY}'}


def api(endpoint):
    url = f'{SUPABASE_URL}/rest/v1/{endpoint}'
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())


def esc(s):
    return str(s or '').replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('"','&quot;')


DESCRIPTIONS = {
    'char-kway-teow': "Char kway teow is a beloved Singapore hawker dish of flat rice noodles stir-fried over intense high heat in a wok with dark soy sauce, Chinese sausage (lap cheong), cockles, eggs, beansprouts, and chives. The hallmark of a great char kway teow is wok hei — the smoky, caramelised breath of the wok — achieved only by a skilled hawker cooking in small batches over blazing flames. Originating from Fujian and Chaozhou immigrants who brought the dish to Singapore in the 19th century, it was historically a cheap, filling meal for labourers. Today it remains one of the most iconic Singapore street foods, with the best versions found at old-school hawker stalls that have been perfecting the dish for decades.",
    'bak-chor-mee': "Bak chor mee, literally \"minced pork noodles\" in Hokkien, is a quintessential Singapore hawker dish featuring springy egg noodles tossed in a robust sauce of vinegar, chilli, lard, and dark soy sauce, topped with minced pork, braised mushrooms, pork liver slices, and crispy fried sole fish. The dish is typically served dry (tossed), though a soup version with clear broth is also available. Each hawker has their own signature ratio of vinegar to chilli, making finding your preferred stall a personal quest for many Singaporeans. It is most associated with Teochew culinary traditions and is a staple breakfast or supper choice at hawker centres across the island.",
    'lor-mee': "Lor mee is a Hokkien-origin noodle dish beloved in Singapore for its thick, starchy brown gravy made from braised pork stock thickened with tapioca starch and eggs. Served over flat yellow noodles or bee hoon, the dish is typically topped with braised pork belly, ngoh hiang (five-spice pork rolls), hard-boiled eggs, fish cake slices, and crispy fried fritters, finished with a generous splash of black vinegar and a dollop of sambal chilli. The glutinous, umami-rich gravy is lor mee's defining feature — it clings to every noodle strand and intensifies with each spoonful. A comforting, hearty dish with deep Chinese immigrant roots, lor mee is best enjoyed at traditional hawker stalls that slow-braise their gravy for hours.",
    'hokkien-mee': "Singapore hokkien mee is a dish of thick yellow egg noodles and thin rice vermicelli stir-fried together in a rich prawn and pork stock, topped with prawns, squid, egg, and pork belly, then served with sambal chilli and calamansi lime on the side. Unlike its Malaysian counterpart which is darker and drier, Singapore's version is wet-style — the noodles absorb the deeply flavourful prawn broth and are finished with a squeeze of lime that cuts through the richness. The prawn shell broth is the soul of the dish; the best hawkers boil it for hours to extract maximum sweetness and depth. Originating from Fujian immigrants, hokkien mee became a fixture of Singapore's hawker culture and is widely regarded as one of the city-state's most satisfying after-dark supper dishes.",
    'laksa': "Singapore laksa is a spicy, coconut-milk-based noodle soup that is one of the most iconic dishes of Peranakan (Straits Chinese) cuisine, combining Chinese noodles with a rich Malay-style coconut curry broth fragrant with lemongrass, galangal, turmeric, and dried shrimp. The most famous variant is Katong laksa from the east of Singapore, served with thick rice vermicelli cut into short segments so the whole dish can be eaten with a spoon, topped with cockles, prawns, fish cake, and a generous ladle of the creamy, orange-hued broth. Singapore laksa should not be confused with Penang's asam laksa, which is tamarind-based and fish-forward; Singapore's version is coconut-rich, mildly spicy, and deeply aromatic. It is consistently ranked among the world's greatest noodle soups and is considered a national treasure of Singapore's culinary heritage.",
    'carrot-cake': "Despite the name, Singapore carrot cake contains no carrots — it is made from white radish (daikon) steamed with rice flour into a firm cake, then chopped and wok-fried with eggs, preserved radish (chai poh), garlic, and spring onions. It comes in two versions: white (fried without dark soy sauce, resulting in a pale, crispy egg crust) and black (tossed with dark soy sauce for a sweeter, caramelised flavour). Known locally as chai tow kway in Hokkien, the dish is a Teochew staple brought to Singapore by immigrants from the Chaoshan region of Guangdong. Whether enjoyed as a hawker breakfast, lunch, or supper, carrot cake's crispy exterior and soft, eggy interior make it one of Singapore's most comforting and well-loved street foods.",
    'prawn-noodles': "Singapore prawn noodles (hae mee) is a soul-warming dish centred on a deeply flavourful broth made by boiling prawn heads and shells for hours until the stock turns a vivid reddish-orange, intensely sweet and savoury with the essence of the sea. Served over yellow egg noodles or bee hoon (or both), the dish is topped with fresh prawns, pork ribs or pork slices, halved hard-boiled eggs, beansprouts, kangkong (water spinach), and crispy fried shallots, accompanied by sambal chilli on the side. The prawn stock — which may also incorporate pork bones for added depth — is the linchpin of a great bowl; the best hawkers guard their broth recipes closely. A staple of Singapore's hawker culture with roots in Hokkien and Teochew communities, prawn noodles is equally beloved as a morning breakfast or a late-night supper.",
    'ice-kacang': "Ice kacang is Singapore's iconic shaved ice dessert, featuring a mound of finely shaved ice drenched in brightly coloured syrups — typically rose (pink), pandan (green), and sarsi (brown) — over a base of sweet toppings including red azuki beans, attap seeds (palm fruit), grass jelly, cubed agar jelly, sweetcorn, and condensed milk. A scoop of vanilla ice cream or a drizzle of coconut milk is often added for extra richness. The name \"kacang\" means \"bean\" in Malay, referencing the red beans that are a traditional core ingredient. Originally a simple, affordable treat sold by street hawkers to beat Singapore's year-round tropical heat, ice kacang has evolved into a beloved dessert at hawker centres and dessert shops across the island, offering endless customisation and a refreshing contrast of textures and flavours.",
    'popiah': "Popiah is a fresh (unfried) spring roll of Teochew and Hokkien origin that is a beloved fixture of Singapore's hawker culture, consisting of a thin, delicate wheat flour crepe filled with a moist, flavourful stew of jicama (bangkuang) and carrot slow-braised with dried shrimp, pork, and tofu. The crepe is spread with hoisin sauce and a touch of sambal chilli before being layered with the braised filling, then topped with crushed peanuts, shredded omelette, lettuce, beansprouts, and fried shallots — each component adding texture and flavour. Eaten immediately after rolling to keep the crepe from becoming soggy, popiah is both an assembly art and a communal meal — many Singaporean families still make popiah from scratch for festive gatherings. Its light, wholesome character sets it apart from its deep-fried counterpart, the spring roll, and makes it a perennial hawker favourite.",
    'bak-kut-teh': "Bak kut teh, literally \"meat bone tea\" in Hokkien, is a hearty pork rib soup simmered for hours in a broth of garlic, pepper, and various Chinese herbs and spices, served with steamed white rice, braised tofu, mushrooms, and you tiao (Chinese dough fritters) for dipping. Singapore's version is characterised by its pale, peppery, garlic-forward broth — distinct from the darker, more herbal Malaysian Klang-style — where white and black pepper are the dominant flavours, delivering a warming, slightly spicy heat with each sip. The name \"tea\" refers not to tea in the broth but to the tradition of drinking strong Chinese tea alongside the dish to cut through the richness of the pork. Originally a fortifying meal for dock workers and coolies along the Singapore River, bak kut teh is now a beloved breakfast institution enjoyed by locals of all backgrounds.",
    'oyster-omelette': "Singapore oyster omelette (orh luak or oh chien) is a beloved hawker dish of fresh oysters folded into a mixture of beaten eggs and starchy sweet potato flour batter, pan-fried in lard until the edges turn golden and crispy while the centre remains soft and slightly chewy, finished with a tangy-spicy chilli sauce on the side. The combination of crispy, eggy fringe and the gooey, starchy interior is the hallmark of a great orh luak — and the use of lard rather than vegetable oil is non-negotiable for flavour at traditional hawker stalls. Originating from Fujian's Chaoshan coast where oysters are a prized ingredient, the dish was brought to Singapore by Teochew and Hokkien immigrants. Fresh, plump oysters and an extremely hot wok are essential for the best version — a truth known to every local who has lined up at a legendary orh luak stall.",
    'satay': "Singapore satay consists of marinated meat — chicken, beef, or mutton — threaded onto bamboo skewers and grilled over charcoal until lightly charred, smoky, and caramelised, served with a rich, sweet-savoury peanut dipping sauce, compressed rice cakes (ketupat), and a fresh salad of raw onion and cucumber. The meat is typically marinated with lemongrass, turmeric, coriander, galangal, and sugar, giving each skewer a fragrant, slightly sweet crust from the caramelisation over live coals. While satay has roots in Javanese and Malay culinary traditions, Singapore's version has been shaped by Malay, Javanese, and Chinese hawker influences over generations. Satay Club at Lau Pa Sat and the hawker stalls of East Coast Lagoon are legendary gathering spots where locals fan satay smoke and share skewers late into the night — a ritual that is quintessentially Singaporean.",
    'chilli-crab': "Chilli crab is Singapore's most celebrated dish and a national culinary icon, featuring fresh, meaty mud crabs wok-fried in a rich, tangy, and mildly spicy tomato-based chilli sauce thickened with egg and cornflour, served with steamed or deep-fried mantou buns to soak up the deeply flavourful sauce. Created in the 1950s by Cher Yam Tian along Singapore's beachfront, the dish catapulted to international fame and has been named one of the world's most delicious foods by CNN Travel. Despite the name, chilli crab's sauce is more sweet and savoury than fiery — the balance of chilli, garlic, ginger, tomato, and egg creates a complex, addictive gravy that is arguably more celebrated than the crab itself. It is a must-eat experience for any visitor to Singapore, best enjoyed at a seafood restaurant with sleeves rolled up and fingers ready.",
    'nasi-briyani': "Singapore nasi briyani (also spelled biryani) is an aromatic, layered rice dish of South Asian origin made with long-grain basmati rice cooked with whole spices — cardamom, cinnamon, cloves, star anise, bay leaves — and chicken, mutton, fish, or vegetables, slow-cooked by the dum method where the pot is sealed and the rice steams in the fragrant meat juices. Singapore's version, introduced by Indian Muslim immigrants from South India and the Malay Archipelago, is distinguished by its golden-hued, richly spiced rice served with a raita (yoghurt sauce), achar (pickled vegetables), and a curry gravy on the side. The dish is a beloved fixture at Indian Muslim hawker stalls and restaurants across Singapore, particularly in the Kampong Glam and Little India districts. Nasi briyani is central to festive celebrations in Singapore's Muslim community and is considered one of the most flavour-layered and technique-intensive dishes in the local culinary canon.",
    'chicken-rice': "Hainanese chicken rice is Singapore's de facto national dish — poached or roasted chicken served over fragrant rice cooked in chicken stock and pandan leaves, accompanied by chilli sauce, ginger paste, and dark soy sauce. The chicken is traditionally poached in a whole pot of seasoned stock at a controlled temperature, then shocked in ice water to achieve silky, tender meat and translucent, gelatinous skin — a technique brought to Singapore by Hainanese immigrants from China's Hainan Island in the early 20th century. The rice, cooked by frying raw grains in rendered chicken fat before simmering in rich stock, is as integral to the dish as the chicken itself. Singapore chicken rice stalls can inspire lifelong loyalty among locals, with debates over preferred condiment ratios and the merits of white-poached versus roasted chicken a constant feature of any food conversation on the island.",
    'bbq-stingray': "BBQ stingray is a uniquely Singaporean hawker speciality in which a whole stingray wing is marinated in a robust sambal paste of chilli, shrimp paste (belacan), lemongrass, garlic, and onion, then grilled over charcoal or gas flame atop a banana leaf until the flesh is cooked through and the sambal is caramelised and fragrant, served with more sambal and a squeeze of calamansi lime. The banana leaf imparts a subtle grassy aroma to the fish while protecting it from direct flame, and the flesh of the stingray — firm, sweet, and cartilage-free — absorbs the smoky, spicy sambal beautifully. A staple of open-air hawker centres and seafood stalls, BBQ stingray is most famously associated with the East Coast Lagoon Food Village, where the sea breeze and the scent of charcoal grilling have drawn seafood lovers for decades. It is a dish that exemplifies Singapore's fusion of Malay, Chinese, and Peranakan culinary traditions.",
    'nasi-lemak': "Nasi lemak is Singapore's beloved rice dish with deep Malay roots, consisting of fragrant rice cooked in rich coconut milk and pandan leaves, served with a complex sambal chilli sauce, fried anchovies (ikan bilis), roasted peanuts, sliced cucumber, and a hard-boiled or fried egg — with optional accompaniments of fried chicken, otah (fish cake), or curry. The rice's coconut richness is the centrepiece of the dish — creamy, aromatic, and mildly sweet — while the sambal, which varies by stall in its balance of heat, sweetness, and shrimp paste intensity, is often the marker by which nasi lemak connoisseurs judge a stall. While nasi lemak is considered Malaysia's national dish, it has been deeply adopted into Singapore's multicultural hawker culture and is enjoyed by Singaporeans of all ethnicities for breakfast, lunch, and dinner. It is a dish that embodies the warmth and complexity of Southeast Asian cuisine.",
    'wonton-mee': "Singapore wonton mee is a Cantonese noodle dish of thin, springy egg noodles served either dry (tossed in a soy-lard sauce with a dash of chilli) or in a light, clean chicken or pork broth, topped with boiled wontons filled with seasoned minced pork and prawn, char siu (barbecued pork), and a garnish of leafy greens. The dry version — the more popular choice — features noodles tossed in a savoury, slightly sweet sauce with a glossy sheen from lard, balanced by the sweetness of char siu and the delicate skin of the wontons. Originating from Hong Kong and Guangdong culinary traditions, Singapore's wonton mee has evolved its own character — often with a darker, slightly spicier sauce, chilli-pickled green chillies on the side, and a strong preference for the wiry, al-dente noodle texture that locals call \"springy.\" A hawker staple eaten at all hours, wonton mee is one of Singapore's most enduring comfort foods.",
    'duck-rice': "Singapore braised duck rice (lor ark png in Hokkien) features slow-braised duck in a deeply aromatic master stock of soy sauce, dark soy, five-spice powder, galangal, cinnamon, star anise, cloves, and rock sugar, served over steamed white rice with braised tofu, hard-boiled eggs, and preserved vegetables (kiam chye), all drizzled with the rich, amber braising sauce. The duck is braised low and slow until the meat is meltingly tender and has fully absorbed the complex, sweet-savoury flavours of the stock — a process that takes hours and rewards patience. Originating from Teochew communities in Singapore, braised duck rice is distinct from Peking duck in both technique and flavour profile, favouring depth and umami over crispiness. The best braised duck rice stalls maintain a perpetual master stock, adding to it over years so the braising liquid deepens in complexity with every batch — a form of culinary continuity unique to hawker culture.",
    'roti-prata': "Roti prata is Singapore's most beloved Indian flatbread — a flaky, buttery dough of flour, ghee, egg, and water hand-stretched and folded repeatedly to create thin, laminated layers, then cooked on a flat griddle until crispy on the outside and soft and chewy within, served with a bowl of fish or mutton curry for dipping. Brought to Singapore by South Indian Tamil immigrants, roti prata has been adapted into a uniquely Singaporean institution with dozens of variations — plain (kosong), egg (telur), cheese, onion, and even banana or chocolate prata for the sweet-toothed. The skill of the prata master in flipping and stretching the dough thin without tearing it is the mark of a great stall, and the crisp golden layers that result from this technique are what make prata exceptional. It is a deeply multicultural icon of Singapore's food scene, enjoyed at mamak stalls by Singaporeans of all backgrounds at breakfast, lunch, and supper.",
    'claypot-rice': "Claypot rice (wa bao fan) is a traditional Chinese dish where uncooked rice is placed in a sand clay pot with seasoned ingredients — typically salted fish, Chinese sausage (lap cheong), chicken marinated in soy and oyster sauce, and dark soy sauce — then cooked directly over a charcoal or gas flame until the rice at the bottom forms a crispy, golden crust called fan jiao, which is considered the most prized part of the dish. As the lid is removed tableside, a dramatic plume of steam rises carrying the mingled aromas of soy, caramelised sausage, and smoky clay, and the diner stirs everything together before eating. The cooking process in a clay pot — which distributes heat slowly and evenly — produces a depth of flavour impossible to replicate in a regular pot or rice cooker. Singapore's claypot rice stalls, some operating for 50 years or more, are a dying art form that locals treasure as an irreplaceable part of their culinary heritage.",
    'rojak': "Singapore rojak (from the Malay word meaning \"eclectic mix\") is a vibrant sweet-savoury-tangy salad of fresh and fried ingredients — typically cucumber, pineapple, bangkuang (jicama), green mango, taupok (puffed fried tofu), you char kway (dough fritters), and cuttlefish — tossed in a thick, pungent dressing of fermented prawn paste (hay ko), chilli, palm sugar, tamarind juice, and ground toasted peanuts. The resulting dish is a riot of contrasting textures (crunchy, chewy, soggy) and flavours (sweet, salty, sour, pungent), with the hay ko dressing — dark, sticky, and deeply savoury — as the defining element that makes Singapore rojak utterly distinctive. It is a uniquely Southeast Asian dish with roots in Chinese and Malay culinary traditions, and Singapore's version is distinct from the Indonesian gado-gado and the Penang rojak in its specific combination of ingredients and the predominance of the prawn paste dressing. Often described as \"the taste of Singapore in one plate,\" rojak celebrates the multicultural character of the city's food culture.",
    'yong-tau-foo': "Yong tau foo (酿豆腐) is a versatile Hakka-origin dish in which a selection of tofu, vegetables, and fish paste-stuffed items — including bitter gourd, chilli, eggplant, okra, fish balls, and various tofu varieties — are either boiled in clear broth or served dry with sauces, allowing each diner to customise their own bowl from the available ingredients. The stuffed items are filled with a seasoned mixture of minced fish paste and sometimes pork, giving each piece a bouncy, seafood-flavoured interior encased in the host ingredient's texture. Diners pick their desired items, which are then cooked to order, and choose between a clear, light soup or a dry bowl with sweet sauce, chilli sauce, and sesame paste. Yong tau foo stalls at Singapore hawker centres typically offer 30 to 50 different items, making it one of the most flexible and personalised dishes in the local food repertoire — a beloved weekday lunch among office workers and hawker centre regulars alike.",
    'fish-head-curry': "Singapore fish head curry is a spectacular dish born from the cultural confluence of South Indian and Chinese culinary traditions, featuring a large fish head — typically red snapper or sea bass — simmered in a richly spiced curry gravy of tamarind, coconut milk, chilli, mustard seeds, curry leaves, and a complex array of spices, with eggplant, lady's fingers (okra), and tomatoes cooked in the pot. The fish head is prized for its gelatinous flesh around the cheeks and collar, its rich, fatty brain matter, and the eye — considered a delicacy by many — all of which absorb the deeply flavoured curry beautifully. The dish was legendarily created in the 1950s by M.J. Gomez, an Indian cook who adapted a traditional South Indian fish curry recipe for Chinese clients in Singapore's Serangoon Road, and has since become a beloved cross-cultural icon. Served with steamed rice and eaten communally, fish head curry is a dish that embodies Singapore's unique identity as a melting pot of cultures and flavours.",
}


GOOGLE_ICON = '<svg width="16" height="16" viewBox="0 0 24 24" style="flex-shrink:0"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l3.66-2.84z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.47 3.99 3.47 3.99l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/></svg>'

GOOGLE_ICON = '<svg width="16" height="16" viewBox="0 0 24 24" style="flex-shrink:0"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l3.66-2.84z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/></svg>'


def render_rows(rests):
    if not rests:
        return '        <tr><td colspan="3"><div class="empty-state"><h3>No restaurants yet</h3></div></td></tr>'
    rows = []
    for r in rests:
        addr = f'<div class="addr">{esc(r["address"])}</div>' if r.get("address") else ''
        rows.append(f'''        <tr id="row-{r["id"]}">
          <td class="rest-cell">
            <div class="name">{esc(r["name"])}</div>
            {addr}
          </td>
          <td class="count-cell" id="count-{r["id"]}">{(r.get("total_votes") or 0):,}</td>
          <td class="vote-cell">
            <div class="vctrl">
              <button class="vbtn" onclick="changeVote({r["id"]},-1)" disabled>−</button>
              <span class="vnum" id="vnum-{r["id"]}">0</span>
              <button class="vbtn" onclick="changeVote({r["id"]},1)" disabled>+</button>
            </div>
          </td>
        </tr>''')
    return '\n'.join(rows)


def build_page(dish, rests):
    page_url    = f'{BASE_URL}/dishes/{dish["slug"]}'
    title       = f'Top 10 {dish["name"]} in Singapore — Voted by Community'
    desc        = f'Community-voted top 10 {dish["name"]} restaurants in Singapore. Real-time rankings updated by food lovers.'
    footer      = f'{len(rests)} restaurant{"s" if len(rests) != 1 else ""} · sorted by community votes'
    description = DESCRIPTIONS.get(dish['slug'], f'{dish["name"]} is a beloved Singapore hawker dish enjoyed by locals and visitors alike.')
    init_data   = json.dumps({"id": dish["id"], "name": dish["name"], "slug": dish["slug"], "restaurants": rests})

    breadcrumb = json.dumps({
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE_URL}/"},
            {"@type": "ListItem", "position": 2, "name": f"Top 10 {dish['name']}", "item": page_url}
        ]
    }, indent=2)

    item_list = json.dumps({
        "@context": "https://schema.org", "@type": "ItemList",
        "name": f"Top 10 {dish['name']} Restaurants in Singapore",
        "description": desc, "url": page_url,
        "itemListElement": [
            {"@type": "ListItem", "position": i+1,
             "item": {"@type": "Restaurant", "name": r["name"], "servesCuisine": dish["name"],
                      "address": {"@type": "PostalAddress", "streetAddress": r.get("address",""), "addressCountry": "SG"}}}
            for i, r in enumerate(rests)
        ]
    }, indent=2)

    schema = f'[{breadcrumb},{item_list}]'
    rows   = render_rows(rests)
    google_icon_js = GOOGLE_ICON.replace("'", "\\'")

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{page_url}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{page_url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Top 10 Singapore Food">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<script type="application/ld+json">
{schema}
</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500&display=swap" rel="stylesheet">
<script src="/supabase.min.js"></script>
<style>
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

  :root {{
    --red: #C0392B; --red-light: #fdf0ef;
    --bg: #faf9f7; --surface: #ffffff; --border: #e8e4de;
    --text: #1a1a1a; --muted: #6b6660; --hint: #a09a94;
    --info-bg: #eef4fb; --info: #1a4f8a;
  }}

  body {{ font-family: \'DM Sans\', sans-serif; background: var(--bg); color: var(--text); min-height: 100vh; }}

  header {{ background: var(--red); color: white; padding: 0 24px; }}
  .header-inner {{ max-width: 860px; margin: 0 auto; display: flex; align-items: center; justify-content: space-between; gap: 16px; min-height: 56px; }}
  .header-left {{ display: flex; align-items: center; gap: 10px; min-width: 0; }}
  .back-link {{ color: rgba(255,255,255,0.75); text-decoration: none; font-size: 18px; line-height: 1; flex-shrink: 0; transition: color 0.15s; }}
  .back-link:hover {{ color: white; }}
  header h1 {{ font-family: \'DM Sans\', sans-serif; font-size: clamp(14px,3.2vw,20px); font-weight: 500; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; letter-spacing: -0.01em; line-height: 1; }}

  .container {{ max-width: 860px; margin: 0 auto; padding: 20px 16px 90px; }}

  .search-wrap {{ margin-bottom: 12px; position: relative; }}
  .search-wrap svg {{ position: absolute; left: 12px; top: 50%; transform: translateY(-50%); color: var(--hint); pointer-events: none; }}
  .search-input {{ width: 100%; padding: 9px 12px 9px 36px; border: 1px solid var(--border); border-radius: 8px; font-family: \'DM Sans\', sans-serif; font-size: 14px; background: var(--surface); color: var(--text); outline: none; transition: border-color 0.15s, box-shadow 0.15s; }}
  .search-input::placeholder {{ color: var(--hint); }}
  .search-input:focus {{ border-color: var(--red); box-shadow: 0 0 0 3px rgba(192,57,43,0.1); }}

  .votes-bubble {{ position: fixed; bottom: 24px; left: 50%; transform: translateX(-50%); background: var(--info); color: white; padding: 10px 10px 10px 20px; border-radius: 99px; font-size: 14px; font-weight: 500; display: flex; align-items: center; gap: 12px; box-shadow: 0 4px 16px rgba(26,79,138,0.35); z-index: 90; white-space: nowrap; }}
  .votes-bubble .pips {{ display: flex; gap: 3px; }}
  .pip {{ width: 8px; height: 8px; border-radius: 50%; background: rgba(255,255,255,0.35); transition: background 0.2s; }}
  .pip.used {{ background: white; }}
  .submit-btn {{ background: white; color: var(--info); border: none; padding: 6px 16px; border-radius: 99px; font-family: \'DM Sans\', sans-serif; font-size: 13px; font-weight: 600; cursor: pointer; transition: background 0.15s, opacity 0.15s; touch-action: manipulation; }}
  .submit-btn:hover:not(:disabled) {{ background: #e8f0fe; }}
  .submit-btn:disabled {{ opacity: 0.45; cursor: not-allowed; }}

  .table-wrap {{ background: var(--surface); border: 1px solid var(--border); border-radius: 12px; overflow: hidden; }}
  table {{ width: 100%; border-collapse: collapse; table-layout: fixed; }}
  thead th {{ font-size: 10px; font-weight: 500; color: var(--hint); letter-spacing: 0.05em; text-transform: uppercase; padding: 10px 14px; border-bottom: 1px solid var(--border); text-align: left; background: #faf9f7; }}
  thead th.r {{ text-align: right; }}
  thead th.count-cell {{ font-size: 10px; color: var(--hint); }}
  tbody tr {{ border-bottom: 1px solid var(--border); transition: background 0.1s; }}
  tbody tr:last-child {{ border-bottom: none; }}
  tbody tr:hover {{ background: #faf9f7; }}
  td {{ padding: 12px 14px; vertical-align: middle; }}
  .rest-cell {{ overflow: hidden; }}
  .rest-cell .name {{ font-size: 13px; font-weight: 500; color: var(--text); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
  .rest-cell .addr {{ font-size: 12px; color: var(--hint); margin-top: 2px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
  .count-cell {{ font-size: 12px; color: var(--muted); text-align: right; white-space: nowrap; width: 70px; }}
  .vote-cell {{ text-align: right; width: 72px; }}
  .vctrl {{ display: inline-flex; align-items: center; gap: 4px; }}
  .vbtn {{ width: 22px; height: 22px; border-radius: 50%; border: 1px solid var(--border); background: var(--bg); color: var(--text); font-size: 14px; line-height: 1; cursor: pointer; display: flex; align-items: center; justify-content: center; transition: border-color 0.15s, background 0.15s; font-family: \'DM Sans\', sans-serif; touch-action: manipulation; -webkit-tap-highlight-color: transparent; }}
  .vbtn:hover:not(:disabled) {{ border-color: var(--red); background: var(--red-light); color: var(--red); }}
  .vbtn:disabled {{ opacity: 0.35; cursor: not-allowed; }}
  .vnum {{ font-size: 12px; font-weight: 500; min-width: 16px; text-align: center; color: var(--text); }}
  .vnum.active {{ color: var(--red); }}
  .voted-row td {{ background: #fefaf9; }}
  .empty-state {{ text-align: center; padding: 48px 24px; color: var(--hint); }}
  .empty-state h3 {{ font-size: 20px; font-weight: 400; margin-bottom: 8px; color: var(--muted); }}
  .footer-note {{ text-align: center; font-size: 12px; color: var(--hint); margin-top: 20px; }}
  .dish-description {{ margin-top: 32px; padding: 24px; background: var(--surface); border: 1px solid var(--border); border-radius: 12px; }}
  .dish-description h2 {{ font-size: 16px; font-weight: 500; color: var(--text); margin-bottom: 10px; }}
  .dish-description p {{ font-size: 14px; line-height: 1.7; color: var(--muted); }}
  .noscript-note {{ display: none; background: var(--info-bg); color: var(--info); padding: 10px 16px; border-radius: 8px; font-size: 13px; margin-bottom: 12px; }}
  .loading-row td {{ text-align: center; padding: 40px; color: var(--hint); font-size: 14px; }}
  .toast {{ position: fixed; bottom: 24px; left: 50%; transform: translateX(-50%) translateY(80px); background: #1a1a1a; color: white; padding: 10px 20px; border-radius: 99px; font-size: 14px; transition: transform 0.3s ease; z-index: 100; white-space: nowrap; }}
  .toast.show {{ transform: translateX(-50%) translateY(0); }}
  .auth-bar {{ display: flex; align-items: center; flex-shrink: 0; }}
  .google-btn {{ background: white; color: #3c4043; border: none; padding: 8px 16px; border-radius: 8px; font-family: \'DM Sans\', sans-serif; font-size: 13px; font-weight: 500; cursor: pointer; display: inline-flex; align-items: center; gap: 8px; transition: background 0.15s, box-shadow 0.15s; touch-action: manipulation; }}
  .google-btn:hover {{ background: #f1f3f4; box-shadow: 0 1px 4px rgba(0,0,0,0.15); }}
  .signout-btn {{ background: rgba(255,255,255,0.2); color: white; border: 1px solid rgba(255,255,255,0.3); padding: 4px 12px; border-radius: 6px; font-family: \'DM Sans\', sans-serif; font-size: 12px; cursor: pointer; transition: background 0.15s; touch-action: manipulation; }}
  .signout-btn:hover {{ background: rgba(255,255,255,0.3); }}

  @media (max-width: 600px) {{
    .votes-bubble {{ font-size: 13px; padding: 8px 8px 8px 16px; bottom: 16px; }}
    .votes-bubble .pips {{ display: none; }}
    .submit-btn {{ padding: 6px 14px; font-size: 12px; }}
    header {{ padding: 0 16px; }}
    header h1 {{ font-size: clamp(12px,3.5vw,16px); }}
    td {{ padding: 10px 6px; }}
    thead th {{ padding: 10px 6px; }}
    .vbtn {{ width: 34px; height: 34px; font-size: 17px; }}
    .vnum {{ font-size: 13px; min-width: 18px; }}
    .vote-cell {{ width: auto; }}
  }}
</style>
<noscript><style>
  .vote-cell, thead th:last-child, .votes-bubble, .auth-bar {{ display: none !important; }}
  .noscript-note {{ display: block !important; }}
</style></noscript>
</head>
<body>

<header>
  <div class="header-inner">
    <div class="header-left">
      <a class="back-link" href="/">←</a>
      <h1>Top 10 {esc(dish["name"])} Voted by Community</h1>
    </div>
    <div class="auth-bar" id="auth-bar">
      <button class="google-btn" onclick="signIn()">{GOOGLE_ICON}<span>Sign in with Google to vote</span></button>
    </div>
  </div>
</header>

<div class="container">

  <div class="noscript-note">Voting requires JavaScript. The restaurant rankings below reflect the latest community votes.</div>

  <div class="search-wrap">
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
    <input class="search-input" id="search-input" type="search" placeholder="Search restaurants…" oninput="onSearch(this.value)">
  </div>

  <div class="table-wrap">
    <table>
      <thead>
        <tr>
          <th>Restaurant</th>
          <th class="r count-cell">Total Votes</th>
          <th class="r">Your vote</th>
        </tr>
      </thead>
      <tbody id="table-body">
{rows}
      </tbody>
    </table>
  </div>

  <p class="footer-note" id="footer-note">{footer}</p>

  <section class="dish-description">
    <h2>What is {esc(dish["name"])}?</h2>
    <p>{description}</p>
  </section>
</div>

<div class="votes-bubble">
  <span>You have <strong id="votes-left">10</strong> votes left</span>
  <div class="pips" id="pips-container"></div>
  <button class="submit-btn" id="submit-btn" onclick="commitVotes()" disabled>Save</button>
</div>

<div class="toast" id="toast"></div>

<script>
  const SUPABASE_URL = 'https://xlbgijjtxbflhkjftene.supabase.co';
  const SUPABASE_KEY = 'sb_publishable_1tTdNWd1N0n9w3ElrCynNw_ia1JWbc6';
  const TOTAL_VOTES  = 10;

  const sb = window.supabase.createClient(SUPABASE_URL, SUPABASE_KEY);

  const INIT       = {init_data};
  let categoryId   = INIT.id;
  let categoryName = INIT.name;
  let slug         = INIT.slug;
  let restaurants  = INIT.restaurants;
  let currentUser  = null;
  let myVotes      = {{}};
  let savedVotes   = {{}};
  let searchQuery  = '';

  sb.auth.onAuthStateChange(async (event, session) => {{
    currentUser = session?.user || null;
    if (window.location.hash) history.replaceState(null, '', window.location.pathname);
    renderAuthBar();
    if (currentUser) {{
      savedVotes = await fetchMyVotes();
      myVotes = {{ ...savedVotes }};
    }} else {{
      savedVotes = {{}};
      myVotes = {{}};
    }}
    renderTable();
  }});

  function renderAuthBar() {{
    const bar  = document.getElementById('auth-bar');
    const icon = '{google_icon_js}';
    if (currentUser) {{
      bar.innerHTML = '<button class="signout-btn" onclick="signOut()">Sign out</button>';
    }} else {{
      bar.innerHTML = '<button class="google-btn" onclick="signIn()">' + icon + '<span>Sign in with Google to vote</span></button>';
    }}
  }}

  async function signIn() {{
    const {{ error }} = await sb.auth.signInWithOAuth({{
      provider: 'google',
      options: {{ redirectTo: window.location.origin + window.location.pathname, scopes: 'email' }}
    }});
    if (error) showToast('Sign in failed: ' + error.message);
  }}

  function signOut() {{
    myVotes = {{}}; savedVotes = {{}}; currentUser = null;
    try {{ localStorage.removeItem('sb-xlbgijjtxbflhkjftene-auth-token'); }} catch {{}}
    sb.auth.signOut({{ scope: 'local' }}).catch(() => {{}});
    renderAuthBar();
    renderTable();
  }}

  function getAuthToken() {{
    try {{
      const s = localStorage.getItem('sb-xlbgijjtxbflhkjftene-auth-token');
      return s ? JSON.parse(s)?.access_token ?? null : null;
    }} catch {{ return null; }}
  }}

  function authHeaders() {{
    const t = getAuthToken();
    return t ? {{ apikey: SUPABASE_KEY, Authorization: 'Bearer ' + t, 'Content-Type': 'application/json' }} : null;
  }}

  async function fetchMyVotes() {{
    const h = authHeaders();
    if (!h) return {{}};
    try {{
      const r = await fetch(
        SUPABASE_URL + '/rest/v1/votes?select=target_id,votes_given&user_id=eq.' + currentUser.id + '&target_type=eq.restaurant',
        {{ headers: h }}
      );
      if (!r.ok) return {{}};
      const data = await r.json();
      const map = {{}};
      data.forEach(v => {{ map[v.target_id] = v.votes_given; }});
      return map;
    }} catch {{ return {{}}; }}
  }}

  function votesUsed()      {{ return Object.values(myVotes).reduce((a, b) => a + b, 0); }}
  function votesRemaining() {{ return TOTAL_VOTES - votesUsed(); }}

  async function loadRestaurants() {{
    try {{
      const r = await fetch(
        SUPABASE_URL + '/rest/v1/restaurants_with_votes?category_id=eq.' + categoryId + '&order=total_votes.desc',
        {{ headers: {{ apikey: SUPABASE_KEY, Authorization: 'Bearer ' + SUPABASE_KEY }} }}
      );
      if (r.ok) restaurants = await r.json();
    }} catch {{}}
    if (currentUser) {{ savedVotes = await fetchMyVotes(); myVotes = {{ ...savedVotes }}; }}
    renderTable();
  }}

  function onSearch(val) {{ searchQuery = val.trim().toLowerCase(); renderTable(); }}

  function hasChanges() {{
    const ids = new Set([...Object.keys(myVotes), ...Object.keys(savedVotes)].map(Number));
    for (const id of ids) {{ if ((myVotes[id] || 0) !== (savedVotes[id] || 0)) return true; }}
    return false;
  }}

  function renderTable() {{
    const remaining = votesRemaining(), used = votesUsed();
    document.getElementById('votes-left').textContent = remaining;
    renderPips(used);
    const btn     = document.getElementById('submit-btn');
    const changed = hasChanges();
    btn.disabled  = !changed;
    btn.textContent = changed ? 'Save (' + used + ')' : (used > 0 ? 'Saved' : 'Save');

    const tbody = document.getElementById('table-body');
    if (!restaurants.length) {{
      tbody.innerHTML = '<tr><td colspan="3"><div class="empty-state"><h3>No restaurants yet</h3></div></td></tr>';
      document.getElementById('footer-note').textContent = '';
      return;
    }}

    const filtered = searchQuery
      ? restaurants.filter(r => r.name.toLowerCase().includes(searchQuery) || (r.address || '').toLowerCase().includes(searchQuery))
      : restaurants;

    if (!filtered.length) {{
      tbody.innerHTML = '<tr class="loading-row"><td colspan="3">No restaurants match "' + document.getElementById('search-input').value + '".</td></tr>';
      document.getElementById('footer-note').textContent = '';
      return;
    }}

    tbody.innerHTML = filtered.map(r => {{
      const myV = myVotes[r.id] || 0;
      return '<tr class="' + (myV > 0 ? 'voted-row' : '') + '" id="row-' + r.id + '">' +
        '<td class="rest-cell"><div class="name">' + r.name + '</div>' +
        (r.address ? '<div class="addr">' + r.address + '</div>' : '') + '</td>' +
        '<td class="count-cell" id="count-' + r.id + '">' + (r.total_votes || 0).toLocaleString() + '</td>' +
        '<td class="vote-cell"><div class="vctrl">' +
          '<button class="vbtn" onclick="changeVote(' + r.id + ',-1)"' + (!currentUser || myV <= 0 ? ' disabled' : '') + '>−</button>' +
          '<span class="vnum' + (myV > 0 ? ' active' : '') + '" id="vnum-' + r.id + '">' + myV + '</span>' +
          '<button class="vbtn" onclick="changeVote(' + r.id + ',1)"' + (!currentUser || remaining <= 0 ? ' disabled' : '') + '>+</button>' +
        '</div></td></tr>';
    }}).join('');

    document.getElementById('footer-note').textContent = searchQuery
      ? filtered.length + ' of ' + restaurants.length + ' restaurants'
      : restaurants.length + ' restaurant' + (restaurants.length !== 1 ? 's' : '') + ' · sorted by community votes';
  }}

  function renderPips(used) {{
    document.getElementById('pips-container').innerHTML =
      Array.from({{ length: TOTAL_VOTES }}, (_, i) => '<div class="pip' + (i < used ? ' used' : '') + '"></div>').join('');
  }}

  function changeVote(restId, delta) {{
    if (!currentUser) {{ showToast('Please sign in to vote'); return; }}
    const cur = myVotes[restId] || 0;
    if (delta < 0 && cur <= 0) return;
    if (delta > 0 && votesRemaining() <= 0) return;
    const nv = cur + delta;
    if (nv <= 0) delete myVotes[restId]; else myVotes[restId] = nv;
    renderTable();
  }}

  async function commitVotes() {{
    const btn = document.getElementById('submit-btn');
    btn.disabled = true; btn.textContent = 'Saving…';
    try {{
      const h = authHeaders();
      if (!h) throw new Error('not authenticated');
      const ids = new Set([...Object.keys(myVotes), ...Object.keys(savedVotes)].map(Number));
      for (const rid of ids) {{
        const nv = myVotes[rid] || 0, ov = savedVotes[rid] || 0;
        if (nv === ov) continue;
        if (nv > 0) {{
          const r = await fetch(SUPABASE_URL + '/rest/v1/votes?on_conflict=user_id,target_type,target_id',
            {{ method: 'POST', headers: {{ ...h, Prefer: 'resolution=merge-duplicates,return=minimal' }},
              body: JSON.stringify({{ user_id: currentUser.id, target_type: 'restaurant', target_id: rid, votes_given: nv }}) }});
          if (!r.ok) throw new Error('upsert failed');
        }} else {{
          const r = await fetch(SUPABASE_URL + '/rest/v1/votes?user_id=eq.' + currentUser.id + '&target_type=eq.restaurant&target_id=eq.' + rid,
            {{ method: 'DELETE', headers: h }});
          if (!r.ok) throw new Error('delete failed');
        }}
      }}
      savedVotes = {{ ...myVotes }};
      showToast('Votes saved!');
      await loadRestaurants();
    }} catch {{ showToast('Error saving votes. Please try again.'); }}
    renderTable();
  }}

  function showToast(msg) {{
    const t = document.getElementById('toast');
    t.textContent = msg; t.classList.add('show');
    setTimeout(() => t.classList.remove('show'), 2800);
  }}
</script>
</body>
</html>'''


def main():
    print('Fetching dishes from Supabase...')
    dishes = api('dishes_with_votes?select=*&order=total_votes.desc')
    print(f'Found {len(dishes)} dishes.\n')

    out_dir = os.path.join(os.path.dirname(__file__), '..', 'dishes')
    os.makedirs(out_dir, exist_ok=True)

    slugs = []
    for dish in dishes:
        print(f'  {dish["slug"]}...', end='', flush=True)
        rests = api(f'restaurants_with_votes?category_id=eq.{dish["id"]}&order=total_votes.desc')
        html  = build_page(dish, rests)
        out   = os.path.join(out_dir, f'{dish["slug"]}.html')
        with open(out, 'w', encoding='utf-8') as f:
            f.write(html)
        slugs.append(dish['slug'])
        print(f' {len(rests)} restaurants OK')

    # Regenerate sitemap
    today = datetime.date.today().isoformat()
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        f'  <url><loc>{BASE_URL}/</loc><lastmod>{today}</lastmod><changefreq>daily</changefreq><priority>1.0</priority></url>',
    ]
    for s in slugs:
        lines.append(f'  <url><loc>{BASE_URL}/dishes/{s}</loc><lastmod>{today}</lastmod><changefreq>weekly</changefreq><priority>0.8</priority></url>')
    lines.append('</urlset>')
    sitemap_path = os.path.join(os.path.dirname(__file__), '..', 'sitemap.xml')
    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')
    print(f'\nDone! {len(slugs)} pages in dishes/')
    print('sitemap.xml regenerated with clean /dishes/ URLs.')


if __name__ == '__main__':
    main()
