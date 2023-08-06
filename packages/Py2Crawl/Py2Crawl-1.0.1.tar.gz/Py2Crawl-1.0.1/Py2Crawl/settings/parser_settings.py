class ParserSettings:
    xpath_urls = [
        "//a/@href", "//audio/@src", "//button/@formaction", "//img/@src", "//link/@href", "//script/@src",
        "//video/@src", "//source/@src", "//track/@src", "//embed/@src", "//object/@data"
    ]
    xpath_headlines = [
        "//h1/text()", "//h2/text()", "//h3/text()", "//h4/text()", "//h5/text()", "//h6/text()"
    ]
