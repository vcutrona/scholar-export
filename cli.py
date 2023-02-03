import sys

import click

from collectors import ScholarPubsCollector


@click.group()
def export():
    pass


@export.command()
@click.option("--author-id", type=str, required=True, help="The Google Scholar ID of the author.")
@click.option("--start-year", type=int, default=1900, show_default=True,
              help="Filter out publications published before this year.")
@click.option("--end-year", type=int, default=2100, show_default=True,
              help="Filter out publications published after this year.")
@click.option("--overwrite", help="Overwrite publications stored in the .pkl file with new data.", is_flag=True)
@click.option("--data-pkl", type=click.Path(), default=None, show_default=True,
              help="The .pkl file to store authors data. "
                   "If the file exists, it is used to initialize the data collector.")
@click.option("--output-file", type=click.Path(), default="publications.csv", show_default=True,
              help="The output .csv file.")
def author(author_id, start_year, end_year, output_file, overwrite, data_pkl):
    collector = ScholarPubsCollector(start_year, end_year, overwrite=overwrite, data_pkl=data_pkl)
    collector.update_author(author_id)
    collector.to_csv(output_file)


@export.command()
@click.option("--authors-file", type=str, required=True, help="A csv file containing the list of authors, "
                                                              "with their Google Scholar ID.")
@click.option("--author-id-column", type=str, required=True, help="The name of the column containing the Scholar IDs.")
@click.option("--start-year", type=int, default=1900, show_default=True,
              help="Filter out publications published before this year.")
@click.option("--end-year", type=int, default=2100, show_default=True,
              help="Filter out publications published after this year.")
@click.option("--overwrite", help="Overwrite publications stored in the .pkl file with new data.", is_flag=True)
@click.option("--data-pkl", type=click.Path(), default=None, show_default=True,
              help="The .pkl file to store authors data. "
                   "If the file exists, it is used to initialize the data collector.")
@click.option("--output-file", type=click.Path(), default="publications.csv", show_default=True,
              help="The output .csv file.")
def authors(authors_file, author_id_column, start_year, end_year, output_file, overwrite, data_pkl):
    collector = ScholarPubsCollector(start_year, end_year, overwrite=overwrite, data_pkl=data_pkl)
    collector.update_authors(authors_file, author_id_column)
    collector.to_csv(output_file)


if __name__ == '__main__':
    sys.exit(export())
