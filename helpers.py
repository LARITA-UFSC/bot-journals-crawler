'''
    https://pkp.sfu.ca/ojs/
'''
from bs4 import BeautifulSoup
import requests
import re

from db import DB


class OpenJournalSystems():

    def __factory_soup(self, url):
        r = requests.get(url)
        data = r.text
        return BeautifulSoup(data, 'html.parser')

    def extract(self, url):

        def filter_field(id, description, pkp):
            return [d['document'] for d in metadata_document if d['id'] in id and d['description'] in description and d['pkp'] in pkp]

        soup_metadata = self.__factory_soup(url)
        content = soup_metadata.find('div', id='content')

        if not content:
            return None

        table = content.find('table', class_='listing')

        if not table:
            return None

        rows = table.find_all('tr', valign='top')

        if len(rows) == 0:
            return None

        metadata_document = []
        for row in rows[1:]:
            elements = row.find_all('td')

            metadata = {
                'id': elements[0].get_text().strip(),
                'description': elements[1].get_text().strip(),
                'pkp': elements[2].get_text().strip(),
                'document': elements[3].get_text().strip(),
            }

            metadata_document.append(metadata)

        title = filter_field('1.', 'Título', 'Título do documento')[0]
        authors = filter_field(
            '2.', 'Autor', 'Nome do autor, afiliação institucional, país')
        keywords = filter_field('3.', 'Assunto', 'Palavras-chave(s)')[0]
        summary = filter_field('4.', 'Descrição', 'Resumo')[0]
        url_view = filter_field('10.', 'Identificador',
                                'Identificador de Recurso Uniforme (URI)')[0]

        soup_url_pdf = self.__factory_soup(url_view)

        url_pdf = ''
        div_pdf = soup_url_pdf.find('div', id='articleFullText')
        if div_pdf:
            url_pdf = div_pdf.a['href']

        fields = {
            'title': title,
            'authors': authors,
            'keywords': keywords,
            'summary': summary,
            'url_view': url_view,
            'url_pdf': url_pdf,

            'raw_data': metadata_document,
            'html_doc': soup_metadata.prettify(),
        }

        return fields


class CoreCrawler():

    def __init__(self, seed):
        self.seed = seed

    def run(self, document):

        print(f'Starting: {self.seed}')

        ojs = OpenJournalSystems()

        subpath = f'rt/metadata/{document}'
        url = f'{self.seed}{subpath}'

        print(f'--> extracting {url}')
        fields = ojs.extract(url)

        if fields:
            print('  DONE')
            return fields
        else:
            print('  CONTENT NOT FOUND')
            return None


def crawling(seed, documents, journal):

    def run():
        crawler = CoreCrawler(seed)
        db = DB()

        for doc in documents:
            fields = crawler.run(doc)
            if fields:
                db.save(fields, journal)
                # yield fields
    run()
    # save_file(list(run()))

# def save_file(fields):
#     print('Saving file')
#     import json
#     with open('data.json', 'a+') as file:

#         d = []

#         for field in fields:
#             d.append({
#                 'title': field['title'],
#                 'url_view': field['url_view'],
#                 'url_pdf': field['url_pdf'],
#             })

#         file.write(json.dumps(d))
