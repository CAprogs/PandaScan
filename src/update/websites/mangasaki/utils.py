MANGAS_IDS = {"828267": "wind-dry-branch", 
            "786221": "i-stole-male-leads-first-night",
            "768320": "boxer",
            "708222": "cuckoos-fiancee",
            "693277": "white-blood",
            "616103": "hunter-x-hunter",
            "500789": "dr-stone",
            "431938": "golden-kamuy",
            "421434": "one-punch-man",
            "336908": "god-high-school",
            "307322": "hardcore-leveling-warrior",
            "306043": "boruto-naruto-next-generations",
            "305498": "gintama",
            "304546": "chainsaw-man",
            "304025": "dragon-ball-super",
            "304020": "shokugeki-no-soma",
            "303938": "boku-no-hero-academia",
            "303936": "one-piece"
            }


def get_manga_name(manga_name):
    """get manga name if exists.

    Args:
        manga_name (str): manga name

    Returns:
        str: normalized manga name
    """

    if manga_name in MANGAS_IDS.keys():
        manga_name = MANGAS_IDS.get(manga_name)
    return manga_name
