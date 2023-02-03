# scholar-export

This CLI tool helps you in exporting publications from Google Scholar for a set
of authors, given their IDs.
Publications are exported in CSV format. Duplicated entries are filtered out if
they share the same <title, author> pair.

## How to use

### Clone the repository
```shell
git clone git@github.com:vcutrona/scholar-export.git
cd scholar-export
```

### Install dependencies

> NOTE: The script has been tested with Python 3.9.

Install the required dependencies by running:

```shell
virtualenv -p python3.9 venv # we suggest to create a virtual environment
source venv/bin/activate
pip install -r requirements.txt
```

### Usage with CLI

To show the command help, simply run:

```shell
python cli.py --help
```

> WARNING: The tool relies on the
> [scholarly](https://pypi.org/project/scholarly/) package, without using a
> proxy. It may happen Google Scholar blocks this tools.

#### Single author
Export publications of a single author by executing the following command:

```shell
python cli.py \
  author \
  --author-id "your-scholar-id" \
  --data-pkl "/path/to/pkl/file" \
  --start-year 1900 \
  --end-year 2030 \
  --output-file "/path/to/output/csv/file"
```

#### Multiple authors

Export publications for multiple users. The Google Scholar IDs are read from a
CSV file. The column containing the IDs must be set as a command parameter.
Given a `researchers.csv` file structured as follows:

| ScholarID | Name      |
| --------- | --------- |
| xyz123    | Research1 |
| qkj987    | Research2 |

The following command will download the publications made by all the listed
authors:

```shell
python cli.py \
  authors \
  --authors-file "researchers.csv" \
  --author-id-column "ScholarID" \
  --data-pkl "/path/to/pkl/file" \
  --start-year 1900 \
  --end-year 2030 \
  --output-file "/path/to/output/csv/file"
```
