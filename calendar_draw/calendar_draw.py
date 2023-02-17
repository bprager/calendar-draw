import logging
import sys
import os

import cairo

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


def draw():
    # creating a SVG surface
    # here geek is file name & 700, 700 is dimension
    with cairo.SVGSurface("geek.svg", 700, 700) as surface:
        # creating a cairo context object
        context = cairo.Context(surface)

        # creating a rectangle(square) for left eye
        context.rectangle(100, 100, 100, 100)

        # creating a rectangle(square) for right eye
        context.rectangle(500, 100, 100, 100)

        # creating position for the curves
        x, y, x1, y1 = 0.1, 0.5, 0.4, 0.9
        x2, y2, x3, y3 = 0.4, 0.1, 0.9, 0.6

        # setting scale of the context
        context.scale(700, 700)

        # setting line width of the context
        context.set_line_width(0.04)

        # move the context to x,y position
        context.move_to(x, y)

        # draw the curve for smile
        context.curve_to(x1, y1, x2, y2, x3, y3)

        # setting color of the context
        context.set_source_rgba(0.4, 1, 0.4, 1)

        # stroke out the color and width property
        context.stroke()


def main():
    draw()


if __name__ == "__main__":
    main()
