import csv
import os
import pickle

import pandas as pd
from loguru import logger
from scholarly import scholarly, MaxTriesExceededException


class ScholarPubsCollector:

    def __init__(self, start_year, end_year, overwrite=False, data_pkl=None):
        self._start_year = start_year
        self._end_year = end_year
        self._overwrite = overwrite
        self._data_pkl = data_pkl
        self._authors = {}
        if data_pkl and os.path.exists(data_pkl):
            logger.info(f"Loading authors data from {data_pkl} ... ")
            self._authors = pickle.load(open(data_pkl, "rb"))

    def update_author(self, author_id):
        try:
            author = scholarly.fill(scholarly.search_author_id(author_id), sections=['publications'])
        except MaxTriesExceededException:
            logger.error(f"Author not found. Skipping entry ... ")
            return None
        except AttributeError:
            logger.error(f"No publications found. Skipping entry ... ")
            return None

        author_pubs = {}

        if author_id in self._authors and self._authors[author_id] and not self._overwrite:
            logger.warning(f"Initializing author {author_id} publications with available data ... ")
            author_pubs = {pub["author_pub_id"]: pub for pub in self._authors[author_id]["publications"]}

        if "publications" in author:
            for article in author['publications']:
                article_id = article["author_pub_id"]
                if self._overwrite or not (article_id in author_pubs and author_pubs[article_id]["filled"]):
                    if 'pub_year' in article['bib'] and \
                            self._start_year <= int(article['bib']['pub_year']) <= self._end_year:
                        author_pubs[article_id] = scholarly.fill(article)
                    else:
                        author_pubs[article_id] = article
                # else: just keep the existing entry
            author["publications"] = list(author_pubs.values())

        return author

    def update_authors(self, authors_file, author_id_column):
        df = pd.read_csv(authors_file)

        author_id_column_index = list(df.columns).index(author_id_column)

        for tup in df.itertuples(name=None, index=False):
            author_id = tup[author_id_column_index]
            logger.info(f'Processing entry {tup} ...')

            self._authors[author_id] = self.update_author(author_id)
            if self._data_pkl:
                pickle.dump(self._authors, open(self._data_pkl, "wb"))

    def to_csv(self, output_file):

        pubs = []
        for author_pubs in self._authors.values():
            if author_pubs:
                pubs += [{**{"source_author_id": pub["author_pub_id"].split(":")[0]}, **pub["bib"]}
                         for pub in author_pubs["publications"]
                         if "pub_year" in pub["bib"] and
                         self._start_year <= int(pub["bib"]["pub_year"]) <= self._end_year]
        logger.info(f"Writing publications to {output_file} ...")

        pd.DataFrame(pubs).groupby(["title", "author"]).first() \
            .reset_index() \
            .to_csv(output_file, index=False, quoting=csv.QUOTE_ALL)
