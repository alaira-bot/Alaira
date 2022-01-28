import logging

from rich import print as rprint


colors = {
    "TRACE": f"dim white",
    "TRACE_HIKARI": f"dim white",
    "DEBUG": "white",
    "INFO": "bright_white",
    "WARNING": "gold1",
    "ERROR": "orange_red1",
    "CRITICAL": "bold bright_red",
}
color_patterns = {
    "socket": "green",
    "main": "blue",
    "database": "cornflower_blue",
    "hikari.bot": "magenta",
    "hikari.gateway": "magenta",
    "discord.http": "red",
    "": "yellow",
}

color_patterns_cache = {"": "yellow"}

ignored = {"yougan-websocket": ["Unknown op %s recieved from Node::%s"]}


def lprint(
    line_type: str,
    source: str,
    message: str,
    *,
    line_type_style: str = "bright_white",
    source_style: str = "bright_white",
    message_style: str = None,
):
    leading = (
        f"[{line_type_style}]{line_type[0]}[/{line_type_style}] "
        f" "
        f"[{source_style}]{source[:15]:>15}[/{source_style}] "
        f"[{line_type_style}]»[/{line_type_style}] "
    )
    lines = message.splitlines()
    rprint(
        f"{leading}[{message_style or line_type_style}]{lines[0]}[/{message_style or line_type_style}]"
    )
    if len(lines) > 1:
        # 31 spaces
        rprint(
            "\n".join(
                f"                           [{message_style or line_type_style}]{line}"
                f"[/{message_style or line_type_style}]"
                for line in lines[1:]
            )
        )


class LoggingHandler(logging.Logger):
    def handle(self, record: logging.LogRecord) -> None:
        if record.msg in ignored.get(record.name, ()):
            return
        name = record.name
        level = record.levelno  # noqa F841
        level_name = record.levelname
        message = record.msg % record.args
        lprint(
            level_name,
            name,
            message,
            line_type_style=colors[level_name],
            source_style=self._get_color(name),
        )

    # noinspection PyMethodMayBeStatic
    def _get_color(self, name: str) -> str:
        if name in color_patterns_cache:
            return color_patterns_cache[name]
        for nm, color in color_patterns.items():
            if name.startswith(nm):
                color_patterns_cache[name] = color
                return color
        return color_patterns[""]
