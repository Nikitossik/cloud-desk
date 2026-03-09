from coolname import generate_slug
from slugify import slugify

def generate_name_and_slug(name: str | None, slug_len: int = 3) -> tuple[str, str]:
    if not name or len(name.strip()) == 0:
        slugname = generate_slug(slug_len)
        return slugname, slugname
    
    name = name.strip()
    slugname = slugify(name, max_length=150, word_boundary=True)
    return name, slugname