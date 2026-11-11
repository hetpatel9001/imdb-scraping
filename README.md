# imdb-scraping

Starter code for scraping IMDb movie pages: search for a title, fetch its
rating, year and summary. Built on `requests` + `BeautifulSoup`.

> Please use this responsibly: respect IMDb's Terms of Use and robots.txt,
> keep request rates low, and use IMDb's official data (or an API) for
> anything beyond personal experiments.

## Usage

```
pip install -r requirements.txt
python3 scraper.py "The Matrix"
python3 scraper.py --open "Dune"
```

Note: IMDb changes its page markup from time to time — if the selectors in
`scraper.py` stop matching, update them to the current markup.
