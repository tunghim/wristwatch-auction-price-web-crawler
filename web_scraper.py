import re
import json
import scrapy
import requests
from bs4 import BeautifulSoup
from datetime import datetime


class QuotesSpider(scrapy.Spider):
    name = "wristwatch_auction_price_web_crawler"
    start_urls = [
        'https://catalog.antiquorum.swiss/en/auctions/monaco-2018-07-18/lots?page=1'
        # 'https://catalog.antiquorum.swiss/en/auctions/geneva-2011-03-27/lots?page=1'
    ]
    brands = ["A. Lange & Söhne", "ABP Paris", "AD-Chronographen", "Adidas", "Aerowatch", "Aigner", "Alain Silberstein", "Alexander Shorokhoff", "Alfred Dunhill", "Alfred Rochat & Fils", "Alpina", "Altanus", "Andersen Genève", "Angelus", "Angular Momentum", "Anonimo", "Apple", "Aquanautic", "Aquastar", "Aristo", "Armand Nicolet", "Armani", "Armin Strom", "Arnold & Son", "Artisanal", "Artya", "Askania", "Ateliers deMonaco", "Atlantic", "Audemars Piguet", "Auguste Reymond", "Auricoste", "Azimuth", "Azzaro", "B.R.M", "Ball", "Balmain", "Barington", "Barthelay", "Baume & Mercier", "Bedat & Co", "Bell & Ross", "Benrus", "Benzinger", "Bertolucci", "Beuchat", "Bifora", "Black-Out Concept", "Blacksand", "Blancier", "Blancpain", "blu", "Boegli", "Bogner Time", "Bombardier", "Bomberg", "Boucheron", "Bovet", "Breguet", "Breil", "Breitling", "Bremont", "Brior", "Bruno Söhnle", "Buben & Zörweg", "Bulgari", "Bulova", "Bunz", "Burberry", "BWC-Swiss", "C.H. Wolf", "Cabestan", "Camel Active", "Camille Fournet", "Candino", "Carl F. Bucherer", "Carlo Ferrara", "Cartier", "Casio", "Catena", "Catorex", "Cattin", "Century", "Cerruti", "Certina", "Chanel", "Charmex", "Charriol", "Chase-Durer", "Chaumet", "Chopard", "Chris Benz", "Christiaan v.d. Klaauw", "Christophe Claret", "Chronographe Suisse Cie", "Chronosport", "Chronoswiss", "Citizen", "Klein", "Claude Meylan", "Clerc", "Concord", "Condor", "Cornehl", "Cortébert", "Corum", "Creo", "Crockett & Jones", "Cuervo y Sobrinos", "Cvstos", "CWC", "Cyclos", "Cyma", "Cyrus", "D.Dornblüth & Sohn", "Damasko", "Daniel Roth", "David Yurman", "Davidoff", "Davosa", "De Bethune", "De Grisogono", "Deep Blue", "DeLaCour", "DeLaneau", "Delma", "Devon", "Dewitt", "Diesel", "Dietrich", "Dior", "Dodane", "Dolce & Gabbana", "Doxa", "Dubey & Schaldenbrand", "DuBois 1785", "DuBois et fils", "Dufeau", "Dugena", "Dürmeister", "Ebel", "Eberhard & Co.", "Edox", "Egotempo", "Eichmüller", "Election", "Elgin", "Elysee", "Engelhardt", "Enicar", "Enigma", "Ennebi", "Epos", "Ernest Borel", "Ernst Benz", "Erwin Sattler", "Esprit", "Eterna", "Eulit", "F.P.Journe", "Fabergé", "Favre-Leuba", "Fendi", "Festina", "Flik Flak", "Fluco", "Fludo", "Formex", "Fortis", "Fossil", "Franc Vila", "Franck Dubarry", "Franck Muller", "Frederique Constant", "Gaga Milano", "Gallet", "Gant", "Gardé", "Garmin", "Germano & Walter", "Gevril", "Girard-Perregaux", "Giuliano Mazzuoli", "Glashütte Original", "Glycine", "Graf", "Graham", "Greubel Forsey", "Grovana", "Gruen", "Grönefeld", "GUB Glashütte", "Gucci", "Guess", "Guy Laroche", "Gérald Genta", "Gübelin", "H.I.D. Watch", "H.Moser & Cie.", "Habring²", "Hacher", "Haemmer", "Hamilton", "Handwerk", "Hanhart", "Harry Winston", "Harwood", "Haurex", "Hautlence", "HD3", "Hebdomas", "Hebe", "Hentschel Hamburg", "Hermès", "Heuer", "Hirsch", "Huber", "Hublot", "Hugo Boss", "HYT", "Ice Watch", "Ikepod", "Illinois", "Ingersoll", "Invicta", "IWC", "J. Chevalier", "Jacob & Co.", "Jacob Jensen", "Jacques Etoile", "Jacques Lemans", "Jaeger-LeCoultre", "Jaermann & Stübi", "Japy", "Jaquet-Droz", "JB Gioacchino", "Jean d'Eve", "Jean Lassale", "Jean Marcel", "Jean Perret", "Jean-Mairet & Gillman", "JeanRichard", "Joop", "Jorg Hysek", "Jules Jürgensen",
              "Junghans", "Junkers", "Juvenia", "Jörg Schauer", "Kadloo", "Kelek", "KHS", "Kienzle", "Kobold", "Korloff", "Krieger", "Kronsegler", "L'Epée", "L.Leroy", "Laco", "Lacoste", "Lancaster", "Lang & Heyne", "Laurent Ferrier", "Lebeau-Courally", "LeCoultre", "Lemania", "Leonidas", "Limes", "Lindburgh + Benson", "Linde Werdelin", "Lip", "Liv Watches", "Locman", "Longines", "Longio", "Lorenz", "Lorus", "Louis Erard", "Louis Moinet", "Louis Vuitton", "Louis XVI", "Lucien Rochat", "Luminox", "Lüm-Tec", "M&M Swiss Watch", "Magellan", "Marcello C.", "Margi", "Martin Braun", "Marvin", "Maserati", "Mathey-Tissot", "Matthew Norman", "Mauboussin", "Maurice de Mauriac", "Maurice Lacroix", "Mb&f", "Meccaniche Veloci", "Meistersinger", "Mercure", "Meyers", "Michael Kors", "Michel Herbelin", "Michel Jordi", "Michele", "Mido", "Milleret", "Milus", "Minerva", "Momentum", "Momo Design", "Mondaine", "Mondia", "Montblanc", "Montega", "Morellato", "Moritz Grossmann", "Movado", "Mühle Glashütte", "N.B. Yäeger", "N.O.A", "Nautica", "Nauticfish", "Nike", "Nina Ricci", "Nivada", "Nivrel", "Nixon", "Nomos", "Nouvelle Horlogerie Calabrese (NHC)", "ODM", "Officina del Tempo", "Ollech & Wajs", "Omega", "Orator", "Orbita", "Orfina", "Orient", "Oris", "Panerai", "Parmigiani Fleurier", "Patek Philippe", "Paul Picot", "Pequignet", "Perigáum", "Perrelet", "Perseo", "Phantoms", "Philip Stein", "Philip Watch", "Piaget", "Pierre Balmain", "Pierre Cardin", "Pierre DeRoche", "Pierre Kunz", "Police", "Poljot", "Pomellato", "Porsche Design", "Prim", "Pro-Hunter", "Pryngeps", "Pulsar", "Puma", "Quinting", "Rado", "Raidillon", "Rainer Brand", "Rainer Nienaber", "Ralf Tech", "Ralph Lauren", "Raymond Weil", "Rebellion", "Ressence", "Revue Thommen", "RGM", "Richard Mille", "Rios1931", "Roamer", "Roberge", "Roger Dubuis", "Rolex", "Rolf Lang", "Romain Jerome", "Rothenschild", "ROWI", "RSW", "Ryser Kentfield", "S.Oliver", "S.T. Dupont", "Salvatore Ferragamo", "Sarcar", "Sarpaneva", "Scalfaro", "Schaumburg", "Schwarz Etienne", "Schäuble & Söhne", "Sea-God", "Sea-Gull", "Sector", "Seiko", "Sevenfriday", "Shellman", "Shinola", "Sinn", "Sjöö Sandström", "Skagen", "Snyper", "Solvil", "Sothis", "Speake-Marin", "Squale", "Starkiin", "Steelcraft", "Steiner Limited", "Steinhart", "Stowa", "Stuhrling", "Swatch", "Swiss Military", "Swiss Timer", "TAG Heuer", "Tavannes", "TB Buti", "Technomarine", "Technos", "Temption", "Tempvs Compvtare", "Tendence", "Terra Cielo Mare", "The One Binary", "The Royal Diamonds", "Theorein", "Thomas Ninchritz", "Thorr", "Tiffany", "Timberland Watches", "Timex", "Tissot", "Tommy Hilfiger", "Tonino Lamborghini", "Torrini", "Tourby", "Tourneau", "Traser", "Tudor", "Tutima", "TW Steel", "U-Boat", "Ulysse Nardin", "Unikatuhren", "Union Glashütte", "Universal", "Urban Jürgensen", "Urwerk", "Vacheron Constantin", "Valbray", "Valentino", "Van Cleef & Arpels", "Van Der Bauwede", "Vangarde", "Ventura", "Versace", "Vianney Halter", "Viceroy", "Victorinox Swiss Army", "Villemont", "Vincent Calabrese", "Vixa", "Vogard", "Volna", "Vostok", "Voutilainen", "Vulcain", "Xemex", "Xetum", "Yes Watch", "York", "Yves Saint Laurent", "Zannetti", "Zeitwinkel", "Zénith", "Zeno", "ZentRa", "Zeppelin", "Zodiac"]

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
        #     'https://catalog.antiquorum.swiss' + listing_page_res[19]['lot_detail_page']).text
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
        # Locate the div containing all the info, except grading system.
        info_div = soup.select('div.col-xs-12.col-md-6')[1]

        # Skip if not wristwatch
        description = info_div.strong.p.text

        if 'wristwatch' not in description and 'chronographe bracelet' not in description:
            return False

        # Location
        location_date_arr = info_div.findAll('p')[2].text.split(", ")
        location = location_date_arr.pop(0)

        # Date
        raw_date_str = ", ".join(location_date_arr)
        date_dt = datetime.strptime(raw_date_str, '%B %d, %Y')
        date = date_dt.strftime('%d/%m/%Y')

        # Brand
        if 'Numbers' in info_div.text:
            for p in info_div.findAll('p'):
                if 'Brand' in p.text:
                    brand = p.text.split('\u2003')[1]
        else:
            for b in self.brands:
                if re.search(b, description.split(', ')[0], re.IGNORECASE):
                    brand = b
                    break
                else:
                    brand = 'Unsigned'

        # Model
        if 'Numbers' in info_div.text:
            for p in info_div.findAll('p'):
                if 'Model' in p.text:
                    model = p.text.split('\u2003')[1]
        else:
            match = re.search('"(.+?)"', description)
            match_2 = re.search(' (.+?)"', description)
            match_3 = re.search('"(.+?)\n(.+?)"', description)
            if match:
                model = match.group(1)
            elif match_2:
                model = match_2.group(1)
            elif match_3:
                model = (match_3.group(1) + match_3.group(2)
                         ).replace('\r', ' ').replace(',', '')
            elif 'movement' in description:
                description_arr = description.split(', ')

                for i in range(len(description_arr)):
                    if 'movement' in description_arr[i]:
                        model = description_arr[i - 1].replace('"', '')
                        break
            elif 'case' in description:
                description_arr = description.split(', ')

                for i in range(len(description_arr)):
                    if 'case' in description_arr[i]:
                        model = description_arr[i - 1].replace('"', '')
                        break
            elif description.split(', ')[0] != brand:
                if description.split(', ')[0].upper().count(brand.upper()) == 1:
                    match = re.search(brand + '(.+?)\n',
                                      description.split(', ')[0])
                    match_2 = re.search(
                        brand + '(.+?)$', description.split(', ')[0])
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
                    model = description.split(', ')[0].replace(brand, '').replace(
                        '\n', ' ').replace(brand.upper(), '').replace('- ', '').strip()
            else:
                model = description.split(', ')[1]

        # Case no.
        if 'Numbers' in info_div.text:
            for p in info_div.findAll('p'):
                if 'Numbers' in p.text:
                    case_number = p.text.split(
                        '\u2003')[1].replace('Case N. ', '')
        else:
            match = re.search('case No. (.+?)[,.]\d', description)
            match_2 = re.search('case No. (.+?)[,.]', description)
            match_3 = re.search('case No.(.+?),', description)
            if match:
                match = re.search('case No. (.+?).. ', description)
                case_number = match.group(1)
            elif match_2:
                case_number = match_2.group(1)
            elif match_3:
                case_number = match_3.group(1)
            else:
                case_number = 'Not Found'

        # Reference
        if 'Numbers' in info_div.text:
            for p in info_div.findAll('p'):
                if 'Reference' in p.text:
                    reference = p.text.split('\u2003')[1].replace('Ref. ', '')
        else:
            match = re.search('Ref. (.+?). ', description)
            match_2 = re.search('Ref.(.+?)[.] ', description)
            if match:
                reference = match.group(1)
            elif match_2:
                reference = match_2.group(1)
            else:
                reference = 'Not Found'

        # Movement
        spec = info_div.findAll(
            'p')[3].text if 'Numbers' in info_div.text else info_div.findAll('p')[3].text

        if 'Cal.' in spec:
            match = re.search('[Mm][.] ?(.+?)[,]', spec)
        elif 'Mouvement' in spec:
            match = re.search('Mouvement (.+?)[.]', spec)
            match_2 = re.search('Mouvement (.+?)$', spec)
        else:
            match = re.search('[Mm][.] ?(.+?)[,.]', spec)

        if match:
            movement = match.group(1)
        elif match_2:
            movement = match_2.group(1)
        else:
            movement = 'Not Found'

        # Material
        material = 'Pending'

        # Year
        if 'Numbers' in info_div.text:
            for p in info_div.findAll('p'):
                if 'Year' in p.text:
                    year = p.text.split('\u2003')[1]
        else:
            match = re.search('Made in the (.+?)[.]', description)
            match_2 = re.search('Made in (.+?)[.]', description)
            match_3 = re.search('Made circa (.+?)[.]', description)
            if match:
                year = match.group(1)
            elif match_2:
                year = match_2.group(1)
            elif match_3:
                year = match_3.group(1)
            else:
                year = 'Not Found'

        # Grading System
        if not soup.select('table.table.table-striped'):
            overall_grade = case_grade = movement_grade = dial_grade = overall_grade_description = case_grade_description = movement_grade_description = dial_grade_description = 'Not Found'
        else:
            grading_system_table = soup.select('table.table.table-striped')[0]

            overall_grade = grading_system_table.findAll(
                'h6')[1].text.split(': ')[1] if len(grading_system_table.findAll(
                    'h6')) >= 2 else 'Not Found'
            case_grade = grading_system_table.findAll(
                'h6')[3].text.split(': ')[1] if len(grading_system_table.findAll(
                    'h6')) >= 4 else 'Not Found'
            movement_grade = grading_system_table.findAll(
                'h6')[5].text.split(': ')[1] if len(grading_system_table.findAll(
                    'h6')) >= 6 else 'Not Found'
            dial_grade = grading_system_table.findAll(
                'h6')[7].text.split(': ')[1] if len(grading_system_table.findAll(
                    'h6')) >= 8 else 'Not Found'

            if len(grading_system_table.findAll('h6')) < 3:
                overall_grade_description = 'Not Found'
            elif len(grading_system_table.findAll('h6')[2].findAll('p')) == 1:
                overall_grade_description = grading_system_table.findAll('h6')[
                    2].p.text
            else:
                txt_arr = []
                for p in grading_system_table.findAll('h6')[2].findAll('p'):
                    txt_arr.append(p.text)
                overall_grade_description = '; '.join(txt_arr)

            if len(grading_system_table.findAll('h6')) < 5:
                case_grade_description = 'Not Found'
            elif len(grading_system_table.findAll('h6')[4].findAll('p')) == 1:
                case_grade_description = grading_system_table.findAll('h6')[
                    4].p.text
            else:
                txt_arr = []
                for p in grading_system_table.findAll('h6')[4].findAll('p'):
                    txt_arr.append(p.text)
                case_grade_description = '; '.join(txt_arr)

            if len(grading_system_table.findAll('h6')) < 7:
                movement_grade_description = 'Not Found'
            elif len(grading_system_table.findAll('h6')[6].findAll('p')) == 1:
                movement_grade_description = grading_system_table.findAll('h6')[
                    4].p.text
            else:
                txt_arr = []
                for p in grading_system_table.findAll('h6')[6].findAll('p'):
                    txt_arr.append(p.text)
                movement_grade_description = '; '.join(txt_arr)

            if len(grading_system_table.findAll('h6')) < 9:
                dial_grade_description = 'Not Found'
            elif len(grading_system_table.findAll('h6')[8].findAll('p')) == 1:
                dial_grade_description = grading_system_table.findAll('h6')[
                    4].p.text
            else:
                txt_arr = []
                for p in grading_system_table.findAll('h6')[8].findAll('p'):
                    txt_arr.append(p.text)
                dial_grade_description = '; '.join(txt_arr)

        # Diameter
        if 'Numbers' in info_div.text:
            for p in info_div.findAll('p'):
                if 'Dimensions' in p.text:
                    diameter = p.text.split('\u2003')[1]
        else:
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

        # Thickness
        match = re.search('Thickness[.:]? (.+?) ', spec)
        match_2 = re.search('Thickness.(.+?) ', spec)
        if match:
            thickness = match.group(1)
        elif match_2:
            thickness = match_2.group(1)
        elif re.search('Thickness ', spec):
            thickness = re.sub('[^0-9]', '', spec.split('Thickness ')[1])
        else:
            thickness = 'Not Found'

        # Sale
        for h4 in soup.findAll('h4'):
            if 'Sold: ' in h4.text:
                h4_arr = h4.text.split(' ')
                sale = '{} {}'.format(h4_arr[2], h4_arr[3])
                break
            else:
                sale = 'No Sale'

        res = {
            'location': location,
            'date': date,
            'lot_number': info_div.h3.text.strip().replace('LOT ', ''),
            'brand': brand,
            'model': model,
            'case_number': case_number,
            'reference': reference,
            'movement': movement,
            'material': material,
            'year': year,
            'overall_grade': overall_grade,
            'case_grade': case_grade,
            'movement_grade': movement_grade,
            'dial_grade': dial_grade,
            'overall_grade_description': overall_grade_description,
            'case_grade_description': case_grade_description,
            'movement_grade_description': movement_grade_description,
            'dial_grade_description': dial_grade_description,
            'diameter': diameter,
            'thickness': thickness,
            'low_estimate': '{} {}'.format(info_div.findAll('h4')[0].text.split(' ')[0], info_div.findAll('h4')[0].text.split(' ')[1]),
            'high_estimate': '{} {}'.format(info_div.findAll('h4')[0].text.split(' ')[0], info_div.findAll('h4')[0].text.split(' ')[3]),
            'sale': sale
        }

        return res
