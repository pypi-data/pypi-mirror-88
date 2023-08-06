"""REST API.

Check the OpenAPI documentation at krcg/templates/openapi.yaml
"""
import json
import os
from typing import Iterable
import urllib.parse

import arrow
import babel
import flask
import pkg_resources  # part of setuptools
import requests

from . import analyzer
from . import config
from . import logging
from . import twda
from . import vtes


class KRCG(flask.Flask):
    """Base API class for Access-Control headers handling."""

    def make_default_options_response(self) -> flask.Response:
        response = super().make_default_options_response()
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
        return response

    def process_response(self, response: flask.Response) -> flask.Response:
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response


logger = logging.logger
base = flask.Blueprint("base", "krcg")


def create_app(test: bool = False):
    if not test:
        vtes.VTES.load_from_vekn(save=False)
        vtes.VTES.configure()
        logger.info("loading TWDA")
        twda.TWDA.load_from_vekn(save=False)
        twda.TWDA.configure()
    logger.info("launching app")
    app = KRCG(__name__)
    app.register_blueprint(base)
    return app


@base.route("/")
@base.route("/index.html")
def swagger():
    """Swagger doc display."""
    return flask.render_template("index.html")


@base.route("/openapi.yaml")
def openapi():
    """OpenAPI schema."""
    return flask.render_template(
        "openapi.yaml",
        version=pkg_resources.require("krcg")[0].version,
    )


@base.route("/card/<text>")
def card(text: str):
    """Get a card."""
    try:
        text = int(text)
    except ValueError:
        pass
    try:
        return flask.jsonify(vtes.VTES.normalized(vtes.VTES[text]))
    except KeyError:
        return "Card not found", 404


@base.route("/deck", methods=["POST"])
def deck_by_cards():
    """Get decks containing cards."""
    data = flask.request.get_json() or {}
    twda.TWDA.configure(
        arrow.get(data.get("date_from") or "1994-01-01"),
        arrow.get(data.get("date_to") or None),
        data.get("players") or 0,
        spoilers=False,
    )
    decks = twda.TWDA
    if data and data.get("cards"):
        A = analyzer.Analyzer(decks)
        try:
            A.refresh(
                *[vtes.VTES.get_name(card) for card in data["cards"]],
                similarity=1,
            )
            decks = A.examples
        except analyzer.AnalysisError:
            return "No result in TWDA", 404
        except KeyError:
            return "Invalid card name", 400
    return flask.jsonify([v.to_dict() for v in decks.values()])


@base.route("/deck/<twda_id>")
def deck_by_id(twda_id):
    """Get a deck given its ID."""
    if not twda_id:
        return "Bad Request", 400
    if twda_id not in twda.TWDA:
        return "Not Found", 404
    return flask.jsonify(twda.TWDA[twda_id].to_dict())


@base.route("/complete/<text>")
def complete(text):
    """Card name completion."""
    lang = _negotiate_locale(flask.request.accept_languages.values())
    return flask.jsonify(vtes.VTES.complete(text, lang))


@base.route("/card", methods=["POST"])
def card_search():
    """Card search."""
    data = flask.request.get_json() or {}
    result = set(int(card["Id"]) for card in vtes.VTES.original_cards.values())
    for type_ in data.get("type") or []:
        result &= vtes.VTES.search["type"].get(type_.lower(), set())
    for clan in data.get("clan") or []:
        clan = config.CLANS_AKA.get(clan.lower()) or clan
        result &= vtes.VTES.search["clan"].get(clan.lower(), set())
    for group in data.get("group") or []:
        result &= vtes.VTES.search["group"].get(group.lower(), set())
    for sect in data.get("sect") or []:
        result &= vtes.VTES.search["sect"].get(sect.lower(), set())
    for trait in data.get("trait") or []:
        result &= vtes.VTES.search["trait"].get(trait.lower(), set())
    for discipline in data.get("discipline") or []:
        discipline = config.DIS_MAP.get(discipline) or discipline
        result &= vtes.VTES.search["discipline"].get(discipline, set())
    for bonus in data.get("bonus") or []:
        result &= vtes.VTES.search.get(bonus.lower(), set())
    if data.get("text"):
        text_search = vtes.VTES.search["text"].search(data["text"])
        text_search |= vtes.VTES.completion.search(data["text"])
        if data.get("lang"):
            lang = _negotiate_locale([data["lang"]])
            if lang in vtes.VTES.search_i18n:
                text_search |= vtes.VTES.search_i18n[lang].search(data["text"])
            if lang in vtes.VTES.completion_i18n:
                text_search |= vtes.VTES.completion_i18n[lang].search(data["text"])
        result &= set(text_search.keys())
    result = sorted(vtes.VTES.get_name(i) for i in result)
    if data.get("mode") == "full":
        result = [vtes.VTES.normalized(card) for card in result]
    return flask.jsonify(result)


@base.route("/submit-ruling/<card>", methods=["POST"])
def submit_ruling(card):
    """Submit a new ruling proposal.

    This posts an issue on the project Github repository.
    """
    try:
        card = int(card)
    except ValueError:
        pass
    try:
        card = vtes.VTES.get_name(card)
    except KeyError:
        return "Card not found", 404
    data = flask.request.get_json() or {}
    text = data.get("text")
    link = data.get("link")
    if not (text and link):
        return "Invalid ruling data", 400
    if urllib.parse.urlparse(link).hostname not in {
        "boardgamegeek.com",
        "www.boardgamegeek.com",
        "groups.google.com",
        "www.vekn.net",
    }:
        return "Invalid ruling link", 400
    tryout = requests.get(link, stream=True)
    if not tryout.ok:
        return "Invalid ruling link", tryout.status_code

    url = "https://api.github.com/repos/lionel-panhaleux/krcg/issues"
    issue = {
        "title": card,
        "body": f"- **text:** {text}\n- **link:** {link}",
    }
    session = requests.session()
    session.auth = (os.getenv("GITHUB_USERNAME"), os.getenv("GITHUB_TOKEN"))
    response = session.post(url, json.dumps(issue))
    if response.ok:
        return flask.jsonify(response.json()), response.status_code
    else:
        return response.text, response.status_code


def _negotiate_locale(preferred: Iterable[str]):
    res = babel.negotiate_locale(
        [x.replace("_", "-") for x in preferred],
        ["en"] + list(config.SUPPORTED_LANGUAGES),
        sep="-",
    )
    # negotiation is case-insensitive but the result uses the case of the first argument
    if res:
        res = res[:-2] + res[-2:].upper()
    return res
