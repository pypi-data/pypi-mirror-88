from ..unpaywall import Unpaywall, Unpaywall_arXiv, Unpaywall_DOI


def test_unpaywall_doi():
    doi = "10.1371/journal.pcbi.1007250"
    unpaywall = Unpaywall_DOI(doi)
    assert isinstance(unpaywall.oa_locations, list)
    assert unpaywall.best_pdf.has_creative_commons_license


def test_unpaywall_arxiv():
    arxiv_id = "1912.04616"
    unpaywall = Unpaywall_arXiv(arxiv_id, use_doi=False)
    assert isinstance(unpaywall.oa_locations, list)
    best_pdf = unpaywall.best_pdf
    assert isinstance(best_pdf, dict)
    assert best_pdf["url"] == "https://arxiv.org/pdf/1912.04616.pdf"
    assert best_pdf["url_for_landing_page"] == "https://arxiv.org/abs/1912.04616"
    assert best_pdf["license"] == "cc-by-sa"


def test_unpaywall_from_citekey():
    """
    https://arxiv.org/abs/1906.11964 is now published in https://doi.org/10.1162/qss_a_00023.
    Therefore, locations are coming from Unpaywall_DOI since defaulting to use_doi=True.
    """
    unpaywall = Unpaywall.from_citekey("arxiv:1906.11964v3")
    assert isinstance(unpaywall, Unpaywall_arXiv)
    best_pdf = unpaywall.best_pdf
    assert best_pdf["url_for_landing_page"] == "https://doi.org/10.1162/qss_a_00023"


def test_unpaywall_from_csl_item():
    csl_item = {
        "id": "ijxfHyzg",
        "URL": "https://arxiv.org/abs/1908.11459",
        "title": "Introducing: The Game Jam License",
        "note": "license: http://arxiv.org/licenses/nonexclusive-distrib/1.0/\nstandard_id: arxiv:1908.11459",
    }
    unpaywall = Unpaywall.from_csl_item(csl_item)
    assert isinstance(unpaywall, Unpaywall_arXiv)
    best_pdf = unpaywall.best_pdf
    assert best_pdf["url_for_landing_page"] == "https://arxiv.org/abs/1908.11459"


def test_unpaywall_from_csl_item_with_doi():
    csl_item = {
        "id": "ijxfHyzg",
        "URL": "https://arxiv.org/abs/1908.11459",
        "title": "Introducing: The Game Jam License",
        "note": "license: http://arxiv.org/licenses/nonexclusive-distrib/1.0/\nstandard_id: arxiv:1908.11459",
        "DOI": "10.1145/3337722.3341844",
    }
    unpaywall = Unpaywall.from_csl_item(csl_item)
    # Unpaywall.from_csl_item uses DOI lookup when available
    assert isinstance(unpaywall, Unpaywall_DOI)
    assert unpaywall.best_pdf["url_for_pdf"]
