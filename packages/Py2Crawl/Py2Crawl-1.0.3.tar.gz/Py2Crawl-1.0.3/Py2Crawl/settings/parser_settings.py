class ParserSettings:
    xpath_urls = [
        "//a/@href", "//audio/@src", "//button/@formaction", "//img/@src", "//link/@href", "//script/@src",
        "//video/@src", "//source/@src", "//track/@src", "//embed/@src", "//object/@data"
    ]
    xpath_headlines = [
        "//h1/text()", "//h2/text()", "//h3/text()", "//h4/text()", "//h5/text()", "//h6/text()"
    ]
    skip_extensions = [
        ".aif", ".cda", ".mid", ".midi", ".mp3", ".mpa", ".ogg", ".wav", ".wma", ".wpl", ".7z", ".arj",
        ".deb", ".pkg", ".rar", ".rpm", ".tar.gz", ".z", ".zip", ".bin", ".dmg", ".iso", ".vcd", ".csv",
        ".dat", ".tar", ".log", ".email", ".eml", ".emlx", ".msg", ".oft", ".ost", ".pst",
        ".vcf", ".apk", ".bat", ".bin", ".cgi", ".pl", ".exe", ".jar", ".msi", ".py", ".wsf", ".fnt",
        ".fon", ".otf", ".ttf", ".ai", ".bmp", ".gif", ".ico", ".jpeg", ".jpg", ".png", ".ps", ".psd",
        ".svg", ".tif", ".tiff", ".cer", ".cfm", ".css", ".part", ".key", ".odp", ".pps", ".ppt",
        ".pptx", ".ods", ".xls", ".xlsm", ".xlsx", ".ini", ".icns", ".3g2", ".3pg", ".avi", ".flv",
        ".h264", ".m4v", ".mkv", ".mov", ".mp4", ".mpg", ".mpeg", ".rm", ".swf", ".vob", ".wmv", ".doc",
        ".docx", ".odt", ".pdf", ".rtf", ".tex", ".wpd"
    ]
    skip_chars = [
        ")", "(", "[", "]", "{", "}", "\\", "+", "*", "'", "\"", "<", ">", "|", "@", "€", "!", "§", "$", "%", "&", "=",
        "?", "#", "~"
    ]
