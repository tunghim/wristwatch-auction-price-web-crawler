import re
import json
import scrapy
import requests
from bs4 import BeautifulSoup
from datetime import datetime


class QuotesSpider(scrapy.Spider):
    name = "wristwatch_auction_price_web_crawler"
    start_urls = [
        'https://catalog.antiquorum.swiss/en/auctions/geneva-2011-03-27/lots?page=1',
    ]
    brands = ["A. Lange & Söhne", "ABP Paris", "AD-Chronographen", "Adidas", "Aerowatch", "Aigner", "Alain Silberstein", "Alexander Shorokhoff", "Alfred Dunhill", "Alfred Rochat & Fils", "Alpina", "Altanus", "Andersen Genève", "Angelus", "Angular Momentum", "Anonimo", "Apple", "Aquanautic", "Aquastar", "Aristo", "Armand Nicolet", "Armani", "Armin Strom", "Arnold & Son", "Artisanal", "Artya", "Askania", "Ateliers deMonaco", "Atlantic", "Audemars Piguet", "Auguste Reymond", "Auricoste", "Azimuth", "Azzaro", "B.R.M", "Ball", "Balmain", "Barington", "Barthelay", "Baume & Mercier", "Bedat & Co", "Bell & Ross", "Benrus", "Benzinger", "Bertolucci", "Beuchat", "Bifora", "Black-Out Concept", "Blacksand", "Blancier", "Blancpain", "blu", "Boegli", "Bogner Time", "Bombardier", "Bomberg", "Boucheron", "Bovet", "Breguet", "Breil", "Breitling", "Bremont", "Brior", "Bruno Söhnle", "Buben & Zörweg", "Bulgari", "Bulova", "Bunz", "Burberry", "BWC-Swiss", "C.H. Wolf", "Cabestan", "Camel Active", "Camille Fournet", "Candino", "Carl F. Bucherer", "Carlo Ferrara", "Cartier", "Casio", "Catena", "Catorex", "Cattin", "Century", "Cerruti", "Certina", "Chanel", "Charmex", "Charriol", "Chase-Durer", "Chaumet", "Chopard", "Chris Benz", "Christiaan v.d. Klaauw", "Christophe Claret", "Chronographe Suisse Cie", "Chronosport", "Chronoswiss", "Citizen", "Klein", "Claude Meylan", "Clerc", "Concord", "Condor", "Cornehl", "Cortébert", "Corum", "Creo", "Crockett & Jones", "Cuervo y Sobrinos", "Cvstos", "CWC", "Cyclos", "Cyma", "Cyrus", "D.Dornblüth & Sohn", "Damasko", "Daniel Roth", "David Yurman", "Davidoff", "Davosa", "De Bethune", "De Grisogono", "Deep Blue", "DeLaCour", "DeLaneau", "Delma", "Devon", "Dewitt", "Diesel", "Dietrich", "Dior", "Dodane", "Dolce & Gabbana", "Doxa", "Dubey & Schaldenbrand", "DuBois 1785", "DuBois et fils", "Dufeau", "Dugena", "Dürmeister", "Ebel", "Eberhard & Co.", "Edox", "Egotempo", "Eichmüller", "Election", "Elgin", "Elysee", "Engelhardt", "Enicar", "Enigma", "Ennebi", "Epos", "Ernest Borel", "Ernst Benz", "Erwin Sattler", "Esprit", "Eterna", "Eulit", "F.P.Journe", "Fabergé", "Favre-Leuba", "Fendi", "Festina", "Flik Flak", "Fluco", "Fludo", "Formex", "Fortis", "Fossil", "Franc Vila", "Franck Dubarry", "Franck Muller", "Frederique Constant", "Gaga Milano", "Gallet", "Gant", "Gardé", "Garmin", "Germano & Walter", "Gevril", "Girard-Perregaux", "Giuliano Mazzuoli", "Glashütte Original", "Glycine", "Graf", "Graham", "Greubel Forsey", "Grovana", "Gruen", "Grönefeld", "GUB Glashütte", "Gucci", "Guess", "Guy Laroche", "Gérald Genta", "Gübelin", "H.I.D. Watch", "H.Moser & Cie.", "Habring²", "Hacher", "Haemmer", "Hamilton", "Handwerk", "Hanhart", "Harry Winston", "Harwood", "Haurex", "Hautlence", "HD3", "Hebdomas", "Hebe", "Hentschel Hamburg", "Hermès", "Heuer", "Hirsch", "Huber", "Hublot", "Hugo Boss", "HYT", "Ice Watch", "Ikepod", "Illinois", "Ingersoll", "Invicta", "IWC", "J. Chevalier", "Jacob & Co.", "Jacob Jensen", "Jacques Etoile", "Jacques Lemans", "Jaeger-LeCoultre", "Jaermann & Stübi", "Japy", "Jaquet-Droz", "JB Gioacchino", "Jean d'Eve", "Jean Lassale", "Jean Marcel", "Jean Perret", "Jean-Mairet & Gillman", "JeanRichard", "Joop", "Jorg Hysek", "Jules Jürgensen", "Junghans", "Junkers", "Juvenia", "Jörg Schauer", "Kadloo", "Kelek", "KHS", "Kienzle", "Kobold", "Korloff", "Krieger", "Kronsegler", "L'Epée", "L.Leroy", "Laco", "Lacoste", "Lancaster", "Lang & Heyne", "Laurent Ferrier", "Lebeau-Courally", "Lemania", "Leonidas", "Limes", "Lindburgh + Benson", "Linde Werdelin", "Lip", "Liv Watches", "Locman", "Longines", "Longio", "Lorenz", "Lorus", "Louis Erard", "Louis Moinet", "Louis Vuitton", "Louis XVI", "Lucien Rochat", "Luminox", "Lüm-Tec", "M&M Swiss Watch", "Magellan", "Marcello C.", "Margi", "Martin Braun", "Marvin", "Maserati", "Mathey-Tissot", "Matthew Norman", "Mauboussin", "Maurice de Mauriac", "Maurice Lacroix", "Mb&f", "Meccaniche Veloci", "Meistersinger", "Mercure", "Meyers", "Michael Kors", "Michel Herbelin", "Michel Jordi", "Michele", "Mido", "Milleret", "Milus", "Minerva", "Momentum", "Momo Design", "Mondaine", "Mondia", "Montblanc", "Montega", "Morellato", "Moritz Grossmann", "Movado", "Mühle Glashütte", "N.B. Yäeger", "N.O.A", "Nautica", "Nauticfish", "Nike", "Nina Ricci", "Nivada", "Nivrel", "Nixon", "Nomos", "Nouvelle Horlogerie Calabrese (NHC)", "ODM", "Officina del Tempo", "Ollech & Wajs", "Omega", "Orator", "Orbita", "Orfina", "Orient", "Oris", "Panerai", "Parmigiani Fleurier", "Patek Philippe", "Paul Picot", "Pequignet", "Perigáum", "Perrelet", "Perseo", "Phantoms", "Philip Stein", "Philip Watch", "Piaget", "Pierre Balmain", "Pierre Cardin", "Pierre DeRoche", "Pierre Kunz", "Police", "Poljot", "Pomellato", "Porsche Design", "Prim", "Pro-Hunter", "Pryngeps", "Pulsar", "Puma", "Quinting", "Rado", "Raidillon", "Rainer Brand", "Rainer Nienaber", "Ralf Tech", "Ralph Lauren", "Raymond Weil", "Rebellion", "Ressence", "Revue Thommen", "RGM", "Richard Mille", "Rios1931", "Roamer", "Roberge", "Roger Dubuis", "Rolex", "Rolf Lang", "Romain Jerome", "Rothenschild", "ROWI", "RSW", "Ryser Kentfield", "S.Oliver", "S.T. Dupont", "Salvatore Ferragamo", "Sarcar", "Sarpaneva", "Scalfaro", "Schaumburg", "Schwarz Etienne", "Schäuble & Söhne", "Sea-God", "Sea-Gull", "Sector", "Seiko", "Sevenfriday", "Shellman", "Shinola", "Sinn", "Sjöö Sandström", "Skagen", "Snyper", "Solvil", "Sothis", "Speake-Marin", "Squale", "Starkiin", "Steelcraft", "Steiner Limited", "Steinhart", "Stowa", "Stuhrling", "Swatch", "Swiss Military", "Swiss Timer", "TAG Heuer", "Tavannes", "TB Buti", "Technomarine", "Technos", "Temption", "Tempvs Compvtare", "Tendence", "Terra Cielo Mare", "The One Binary", "The Royal Diamonds", "Theorein", "Thomas Ninchritz", "Thorr", "Tiffany", "Timberland Watches", "Timex", "Tissot", "Tommy Hilfiger", "Tonino Lamborghini", "Torrini", "Tourby", "Tourneau", "Traser", "Tudor", "Tutima", "TW Steel", "U-Boat", "Ulysse Nardin", "Unikatuhren", "Union Glashütte", "Universal", "Urban Jürgensen", "Urwerk", "Vacheron Constantin", "Valbray", "Valentino", "Van Cleef & Arpels", "Van Der Bauwede", "Vangarde", "Ventura", "Versace", "Vianney Halter", "Viceroy", "Victorinox Swiss Army", "Villemont", "Vincent Calabrese", "Vixa", "Vogard", "Volna", "Vostok", "Voutilainen", "Vulcain", "Xemex", "Xetum", "Yes Watch", "York", "Yves Saint Laurent", "Zannetti", "Zeitwinkel", "Zenith", "Zeno", "ZentRa", "Zeppelin", "Zodiac"]

    def parse(self, response):
        listing_page_res = self.listing_page(response)

        for i in listing_page_res:
            if i['lot_detail_page'] is None:
                continue
            detail_page_dom = requests.get(
                'https://catalog.antiquorum.swiss' + i['lot_detail_page']).text
            detail_page_soup = BeautifulSoup(detail_page_dom, "html.parser")
            detail_page_res = self.detail_page(detail_page_soup)
            if not detail_page_res:
                continue
            else:
                yield detail_page_res

        # Debug
        # detail_page_dom = requests.get(
        #     'https://catalog.antiquorum.swiss' + listing_page_res[12]['lot_detail_page']).text
        # detail_page_soup = BeautifulSoup(detail_page_dom, "html.parser")
        # detail_page_res = self.detail_page(detail_page_soup)
        # if not detail_page_res:
        #     yield {
        #         'error_msg': 'Not wristwatch.'
        #     }
        # else:
        #     yield detail_page_res

        # Navigate to next page.
        next_page = response.css('span.next a::attr("href")').extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def listing_page(self, response):
        res = []
        for i in response.css('div.col-md-3'):
            if i.css('div#lot_number > h2::text').extract_first() is not None:
                res.append({
                    'lot_number': i.css('div#lot_number > h2::text').extract_first(),
                    'lot_price': i.css('div.lots_price > p::text').extract_first(),
                    'lot_detail_page': i.css('div.lots_thumbail a::attr("href")').extract_first()
                })

        return res

    def detail_page(self, soup):
        # Locate the div containing all the info
        info_div = soup.select('div.col-xs-12.col-md-6')[1]

        # Skip if not wristwatch
        description = info_div.strong.p.text

        if 'wristwatch' not in description:
            return False

        # Location
        location_date_arr = info_div.findAll('p')[2].text.split(", ")
        location = location_date_arr.pop(0)

        # Date
        raw_date_str = ", ".join(location_date_arr)
        date_dt = datetime.strptime(raw_date_str, '%B %d, %Y')
        date = date_dt.strftime('%d/%m/%Y')

        # Brand
        for b in self.brands:
            if re.search(b, description.split(', ')[0]):
                brand = b
                break
            else:
                brand = 'Unsigned'

        # Model
        match = re.search('"(.+?)"', description)
        match_2 = re.search(' (.+?)"', description)
        match_3 = re.search('"(.+?)\n(.+?)"', description)
        if match:
            model = match.group(1)
        elif match_2:
            model = match_2.group(1)
        elif match_3:
            model = (match_3.group(1) + match_3.group(2)).replace('\r', ' ').replace(',', '')
        elif 'case' in description:
            description_arr = description.split(', ')

            for i in range(len(description_arr)):
                if 'case' in description_arr[i]:
                    model = description_arr[i - 1].replace('"', '')
                    break
        elif description.split(', ')[0] != brand:
            if description.split(', ')[0].upper().count(brand.upper()) == 1:
                match = re.search(brand + '(.+?)\n', description.split(', ')[0])
                match_2 = re.search(brand + '(.+?)$', description.split(', ')[0])
                match_3 = re.search('(.+?)\n', description.split(', ')[0])
                match_4 = re.search('(.+?)$', description.split(', ')[0])
                if match:
                    model = match.group(1)
                elif match_2:
                    model = match_2.group(1)
                elif match_3:
                    model = match_3.group(1)
                elif match_4:
                    model = match_4.group(1)
            else:
                model = description.split(', ')[0].replace(brand, '').replace('\n', ' ').replace(brand.upper(), '').replace('- ', '').strip()
        else:
            model = description.split(', ')[1]

        # Case no.
        match = re.search('case No. (.+?)[,.]', description)
        if match:
            case_number = match.group(1)
        else:
            case_number = 'Not Found'

        # Movement, diameter & thickness
        spec = info_div.findAll('p')[4].text

        if 'Cal.' in spec:
            match = re.search('[Mm][.] ?(.+?)[,]', spec)
        else:
            match = re.search('[Mm][.] ?(.+?)[,.]', spec)
        if match:
            movement = match.group(1)
        else:
            movement = 'Not Found'

        match = re.search('Dim.?(.+?) mm', spec)
        match_2 = re.search('Diam.?(.+?) mm', spec)
        match_3 = re.search('Dim.?(.+?)[.]', spec)
        match_4 = re.search('Diam.?(.+?)[.]', spec)
        if match:
            diameter = match.group(1)
        elif match_2:
            diameter = match_2.group(1)
        elif match_3:
            diameter = match_3.group(1)
        elif match_4:
            diameter = match_4.group(1)
        else:
            diameter = 'Not Found'

        match = re.search('Thickness[.:]? (.+?) ', spec)
        if match:
            thickness = match.group(1)
        elif re.search('Thickness ', spec):
            thickness = re.sub('[^0-9]', '', spec.split('Thickness ')[1])
        else:
            thickness = 'Not Found'

        # Sale
        if len(info_div.findAll('h4')) == 2:
            sale = info_div.findAll('h4')[1].text.split(' ')[3]
        else:
            sale = 'On Sale'

        res = {
            'location': location,
            'date': date,
            'lot_number': info_div.h3.text.strip().replace('LOT ', ''),
            'brand': brand,
            'model': model,
            'case_number': case_number,
            'movement': movement,
            'diameter': diameter,
            'thickness': thickness,
            'low_estimate': info_div.findAll('h4')[0].text.split(' ')[1],
            'high_estimate': info_div.findAll('h4')[0].text.split(' ')[3],
            'sale': sale
        }

        return res
