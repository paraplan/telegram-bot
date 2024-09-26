import re

import jinja2

from src.bot.utils.datetime import datetime_filter


def render_template(template_name: str, data: dict | None = None) -> str:
    if data is None:
        data = {}
    jinja_env = _get_template_env()
    jinja_env.filters["datetime_filter"] = datetime_filter
    template = jinja_env.get_template(template_name)
    rendered = template.render(**data).replace("\n", " ")
    rendered = rendered.replace("<br>", "\n")
    rendered = re.sub(" +", " ", rendered).replace(" .", ".").replace(" ,", ",")
    rendered = "\n".join(line.strip() for line in rendered.split("\n"))
    rendered = rendered.replace("{FOURSPACES}", "    ")
    rendered = rendered.replace("{TWOSPACES}", "  ")
    return rendered


def _get_template_env():
    if not getattr(_get_template_env, "template_env", None):
        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader("templates"),
            trim_blocks=True,
            lstrip_blocks=True,
            autoescape=True,
        )

        _get_template_env.template_env = env  # type: ignore

    return _get_template_env.template_env  # type: ignore
