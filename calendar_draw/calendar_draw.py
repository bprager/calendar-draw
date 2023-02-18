import calendar
import logging
import os
import sys
from datetime import datetime, timedelta

import cairo

INCH_TO_POINTS = 72
MM_TO_POINTS = 3.83465
BORDER_MM = 10
PADDING_MM = 3
# Landscape
LETTER_HEIGHT = 8.5 * INCH_TO_POINTS
LETTER_WIDTH = 11.0 * INCH_TO_POINTS
# Fonts attributes
FONT_SIZE = 12

# setup logging
FORMATTER = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(message)s")
log = logging.getLogger(__name__)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(FORMATTER)
# file_handler = logging.FileHandler(LOG_FILE)
# file_handler.setFormatter(FORMATTER)
log.addHandler(console_handler)
# log.addHandler(file_handler)
if "DEBUG" in os.environ:
    log.setLevel(logging.DEBUG)
else:
    log.setLevel(logging.INFO)


def draw(startdate: datetime, teams: dict):
    max_name = ""
    for team in teams.keys():
        log.debug(f"team: {teams[team]}")
        members = list(teams[team].keys())
        max_member = max(members, key=len)
        if len(max_member) > len(max_name):
            max_name = max_member
    log.debug(f"the longest name is {max_name} ")

    # single team for now
    team = list(teams.keys())[0]

    # Set beginning of the month
    start = startdate.replace(day=1)
    first, days = calendar.monthrange(start.year, start.month)

    # creating a SVG surface
    # Landscape letter dimensions
    width = LETTER_WIDTH - (2 * BORDER_MM) * MM_TO_POINTS
    height = LETTER_HEIGHT - (2 * BORDER_MM) * MM_TO_POINTS

    # Dummy surface for dimensions
    with cairo.SVGSurface("dummy.svg", 0, 0) as dummy:
        # creating a cairo context object
        context = cairo.Context(dummy)

        context.select_font_face(
            # "Open Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL
            os.getenv("FONT", default="Arial"),
            cairo.FONT_SLANT_NORMAL,
            cairo.FONT_WEIGHT_NORMAL,
        )

        context.set_font_size(FONT_SIZE)
        # calculate name column width
        name_column = context.text_extents(max_name).width + 2 * PADDING_MM
        # calculate cell height
        cell_dim = context.text_extents(max_name).height + 2 * PADDING_MM
        cell_dim = 1.6 * cell_dim
        # surface dimensions
        width = name_column + days * cell_dim

        # setting color of the context
        context.set_source_rgba(0.1, 0.1, 0.1, 1)
        log.debug(f"name column width: {name_column} ")
        log.debug(f"cell dimension: {cell_dim} ")

    os.remove("dummy.svg")

    # test first team only
    team = teams[list(teams.keys())[0]]
    log.debug(f"len(team): {len(team)}")
    height = (len(team) + 4) * cell_dim + 2 * BORDER_MM
    width = name_column + days * cell_dim + 2 * BORDER_MM

    log.debug(f"height: {height}, width: {width}")

    log.debug(f"test this team only: {team}")

    with cairo.SVGSurface("test.svg", width, height) as surface:
        # creating a cairo context object
        context = cairo.Context(surface)

        context.select_font_face(
            # "Open Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL
            os.getenv("FONT", default="Arial"),
            cairo.FONT_SLANT_NORMAL,
            cairo.FONT_WEIGHT_NORMAL,
        )

        context.set_font_size(FONT_SIZE)

        # setting color of the context

        context.set_line_width(0.3)

        # context.stroke()

        # draw header
        # month
        context.set_source_rgba(0.1, 0.1, 0.1, 0.5)
        context.rectangle(
            BORDER_MM, BORDER_MM, width - 2 * BORDER_MM + PADDING_MM, cell_dim
        )
        context.stroke()
        context.move_to(
            BORDER_MM + name_column + PADDING_MM, BORDER_MM + cell_dim - PADDING_MM
        )
        context.set_source_rgb(0.1, 0.1, 0.1)
        context.show_text(f"{start.strftime('%b, %Y')}")
        # TODO: week
        context.set_source_rgba(0.1, 0.1, 0.1, 0.5)
        context.rectangle(
            BORDER_MM,
            BORDER_MM + cell_dim,
            width - 2 * BORDER_MM + PADDING_MM,
            cell_dim,
        )
        context.stroke()
        # days
        context.set_source_rgba(0.1, 0.1, 0.1, 0.5)
        context.rectangle(
            BORDER_MM,
            BORDER_MM + 2 * cell_dim,
            width - 2 * BORDER_MM + PADDING_MM,
            2 * cell_dim,
        )
        context.stroke()
        delta = timedelta(days=1)
        day = start
        end = day + days * delta
        x = BORDER_MM + name_column + PADDING_MM
        y = BORDER_MM + 3 * cell_dim - PADDING_MM
        while day < end:
            context.set_source_rgba(0.1, 0.1, 0.1, 0.5)
            context.rectangle(x, y - cell_dim + PADDING_MM, cell_dim, 2 * cell_dim)
            context.stroke()
            # center text
            if day.weekday() < 5:
                context.set_source_rgb(0.1, 0.1, 0.1)
            else:
                context.set_source_rgb(1, 0, 0)
            context.set_font_size(FONT_SIZE - 4)
            middle = context.text_extents(day.strftime("%a").upper()).width / 2
            context.move_to(x + cell_dim / 2 - middle, y)
            context.show_text(day.strftime("%a").upper())
            context.set_font_size(FONT_SIZE - 2)
            middle = context.text_extents(day.strftime("%d").upper()).width / 2
            context.move_to(x + cell_dim / 2 - middle, y + 0.7 * cell_dim)
            context.show_text(f"{day.strftime('%d')}")
            day = day + delta
            x = x + cell_dim

        # Names
        x = BORDER_MM + PADDING_MM
        y = BORDER_MM + 5 * cell_dim - PADDING_MM
        context.move_to(x, y)
        for name in list(team.keys()):
            context.move_to(x, y)
            context.set_source_rgb(0.1, 0.1, 0.1)
            context.show_text(name)
            context.set_source_rgba(0.1, 0.1, 0.1, 0.5)
            context.rectangle(
                BORDER_MM,
                y - cell_dim + PADDING_MM,
                days * cell_dim + name_column + PADDING_MM,
                cell_dim,
            )
            context.stroke()
            y += cell_dim

        return


def build_dict(config: dict) -> tuple[dict, set]:
    teams = config["TEAMS"].split(",")
    team_dict = {}
    countries = set()
    for team in teams:
        member_dict = {}
        team = team.strip()
        members = config[team].split("\n")
        for member in members:
            if member:
                record = member.split(",")
                name = record[0].strip()
                country = record[1].strip()
                member_dict[name] = country
                countries.add(country)
                team_dict[team] = member_dict
        log.debug(f"member_dict: {member_dict}")
    return team_dict, countries


def main():
    draw()


if __name__ == "__main__":
    main()
