from http import HTTPStatus
from pathlib import Path

from flask import Flask, abort, redirect, render_template, request, url_for
from flask.typing import ResponseReturnValue
from werkzeug.exceptions import HTTPException

from display.display_race_report import SortStrategy, filter_report, sort_report
from formula1_race_analysis.q1_session_analyzer import build_q1_report

BASE_DIR = Path("../data")
IGNORE_ERRORS = True


def create_app(base_dir: Path = BASE_DIR) -> Flask:
    app = Flask(__name__)
    race_results = build_q1_report(base_dir, IGNORE_ERRORS)

    @app.route("/")
    def index() -> ResponseReturnValue:
        return redirect(url_for("report"), 301)

    @app.route("/report/")
    def report() -> str:
        order = request.args.get("order", SortStrategy.DESCENDING_ORDER)
        try:
            sort_strategy = SortStrategy(order)
        except ValueError:
            abort(400, description=f"Invalid sort order: '{order}'. Must be 'asc' or 'desc'.")
        sorted_race_results = sort_report(race_results, sort_strategy)
        return render_template("report.html", race_results=sorted_race_results, order=order)

    @app.route("/report/drivers")
    def drivers() -> str:
        return render_template("drivers.html", race_results=race_results)

    @app.route("/report/drivers/")
    def driver_id() -> str:
        driver_id = request.args.get("driver_id")
        filtered_race_results = filter_report(race_results, driver_id)
        if not filtered_race_results:
            abort(
                400,
                description=(
                    f"Identifier '{driver_id}' is not recognized. Try to use 3-letter code like 'KRF': "
                    "the first letters of the first name: 'K', the first letters of the last name: 'R' and "
                    "the first letters of the car model: 'F'."
                ),
            )
        return render_template("driver_id.html", race_results=filtered_race_results, driver_id=driver_id)

    @app.errorhandler(404)
    def page_not_found_error(_: HTTPException) -> tuple[str, int]:
        return ("The page is not found", HTTPStatus.NOT_FOUND)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
