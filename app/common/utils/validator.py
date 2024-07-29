class URLUtil:
    @staticmethod
    def request_formatter(url: str):

        if not url.startswith("https"):
            url = f"https://{url}"
        return url

    @staticmethod
    def validate_url(url: str) -> str:
        if url.startswith("https"):
            url = url.lstrip("https://")

        if "www" in url:
            url = url.lstrip("www.")
        return url
