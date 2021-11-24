import re

STYLE_PATTERN = re.compile("\x1b\[\d+m")


class StyleContext:
    mapping = {
        "\x1b[31m": ("color", "red"),
        "\x1b[32m": ("color", "green"),
        "\x1b[33m": ("color", "orange"),
        "\x1b[36m": ("color", "blue"),
        "\x1b[1m": ("tag", "strong"),
        "\x1b[0m": ("clear", None),
    }

    def __init__(self):
        self.styles = []

    def get(self, match: re.Match):
        try:
            style = self.mapping[match.group(0)]
        except KeyError:
            return ""

        kind, value = style
        if kind == "color":
            self.styles.append(style)
            return '<span color="%s">' % value
        elif kind == "tag":
            self.styles.append(style)
            return "<%s>" % value
        elif kind == "clear":
            output = ""
            for k in range(len(self.styles)):
                rkind, rvalue = self.styles.pop(-1)
                if rkind == "color":
                    output += "</span>"
                elif rkind == "tag":
                    output += "</%s>" % rvalue
            return output


def cli_style_to_html(output: str):
    context = StyleContext()
    return re.sub(STYLE_PATTERN, context.get, output)
