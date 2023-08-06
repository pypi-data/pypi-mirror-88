import requests

ABBR_BASE = "https://abbr.acdh.oeaw.ac.at/api/abbreviations/?format=json"


def yield_abbr(abbr_base=ABBR_BASE, limit=False):
    """ iterator to yield all abbreviations from abbr_base

    :param abbr_base: The Base-URL of the abbreviation-service
    :type abbr_base: str

    :param limit: Bool to flag if only a short sample\
    of abbreviations should be fetched, defaults to `False`
    :type limit: bool

    :return: An iterator yielding abbreviations
    :rtype: iterator
    """

    next = True
    url = abbr_base
    counter = 0
    if limit:
        max_samples = 5
    while next:
        response = requests.request("GET", url)
        result = response.json()
        if result.get('next', False):
            url = result.get('next')
        else:
            next = False
        results = result.get('results')
        for x in results:
            text = x.get('orth')
            print(text)
            counter += 1
            if limit:
                if counter <= max_samples:
                    next = False
                    yield(text)
            else:
                yield(text)
