from models.link import Link

def normalize_link(link: Link) -> Link:
    if link.linkedin:
        link.linkedin = link.linkedin.strip().rstrip("/")
    if link.github:
        link.github = link.github.strip().rstrip("/")
    if link.portfolio:
        link.portfolio = link.portfolio.strip().rstrip("/")
    link.other = [
        url.strip().rstrip("/") for url in link.other
    ]
    return link