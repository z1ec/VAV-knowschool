PRICE_CARD_STYLE = {
    "english-teens-adults": {"accent": "#0d47c1", "blob-size": "145px", "blob-top": "-38px", "blob-right": "-38px"},
    "spanish-german": {"accent": "#c9871a", "blob-size": "130px", "blob-bottom": "-34px", "blob-left": "-34px"},
    "chinese-korean": {"accent": "#c62b45", "blob-size": "165px", "blob-bottom": "-50px", "blob-right": "-50px"},
    "italian-latin": {"accent": "#1f8a63", "blob-size": "135px", "blob-top": "-36px", "blob-left": "-36px"},
    "russian": {"accent": "#0039a6", "blob-size": "120px", "blob-bottom": "-20px", "blob-right": "26px"},
    "school-prep": {"accent": "#e08a1e", "blob-size": "155px", "blob-top": "-30px", "blob-right": "20px"},
}


def style_attr(key):
    props = PRICE_CARD_STYLE.get(key, {})
    parts = [f"--price-accent:{v}" if k == "accent" else f"--{k}:{v}" for k, v in props.items()]
    return "; ".join(parts)
