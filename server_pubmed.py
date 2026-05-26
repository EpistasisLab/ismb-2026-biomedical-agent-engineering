import os
import xml.etree.ElementTree as ET
from Bio import Entrez
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel

Entrez.email = os.getenv("NCBI_EMAIL", "your-email@example.com")
mcp = FastMCP("pubmed-server")


class Article(BaseModel):
    pmid: str
    title: str | None = None
    journal: str | None = None
    year: str | None = None


@mcp.tool()
def search_pubmed(query: str, max_results: int = 5) -> list[Article]:
    """Search PubMed for articles matching a query."""
    ids = Entrez.read(Entrez.esearch(db="pubmed", term=query, retmax=max_results))["IdList"]
    summaries = Entrez.read(Entrez.esummary(db="pubmed", id=",".join(ids))) if ids else []
    return [
        Article(
            pmid=s["Id"],
            title=s["Title"],
            journal=s.get("FullJournalName", ""),
            year=s.get("PubDate", "")[:4],
        )
        for s in summaries
    ]


@mcp.tool()
def get_abstract(pmid: str) -> str:
    """Fetch the abstract for a PubMed article by PMID."""
    with Entrez.efetch(db="pubmed", id=pmid, rettype="abstract", retmode="text") as h:
        return h.read()


@mcp.tool()
def get_full_text(pmid: str) -> str:
    """Fetch full article text for a PubMed paper by PMID.

    Returns the parsed body text for open-access papers available in PubMed Central (PMC).
    Falls back to the abstract for papers not in PMC (~60% of PubMed).
    """
    # Resolve PMID → PMCID via elink
    links = Entrez.read(Entrez.elink(dbfrom="pubmed", db="pmc", id=pmid))
    pmc_ids = (
        [link["Id"] for link in links[0]["LinkSetDb"][0]["Link"]]
        if links and links[0].get("LinkSetDb")
        else []
    )

    if not pmc_ids:
        with Entrez.efetch(db="pubmed", id=pmid, rettype="abstract", retmode="text") as h:
            return "[Abstract only — full text not available in PMC]\n\n" + h.read()

    with Entrez.efetch(db="pmc", id=pmc_ids[0], rettype="full", retmode="xml") as h:
        root = ET.fromstring(h.read())

    sections = []

    for title_el in root.iter("article-title"):
        if title_el.text:
            sections.append("Title: " + title_el.text.strip())
            break

    for abstract_el in root.iter("abstract"):
        text = " ".join(t.strip() for t in abstract_el.itertext() if t.strip())
        if text:
            sections.append("Abstract:\n" + text)
            break

    for sec in root.iter("sec"):
        heading_el = sec.find("title")
        heading = heading_el.text.strip() if heading_el is not None and heading_el.text else ""
        paras = [
            " ".join(t.strip() for t in p.itertext() if t.strip())
            for p in sec.findall("p")
        ]
        paras = [p for p in paras if p]
        if paras:
            sections.append((f"\n{heading}:\n" if heading else "\n") + "\n".join(paras))

    return "\n\n".join(sections) if sections else "[Could not parse PMC full text]"


if __name__ == "__main__":
    mcp.run()  # stdio transport; use mcp.run(transport="sse") for HTTP
