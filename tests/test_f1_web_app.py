import html
from http import HTTPStatus

import pytest
from flask.testing import FlaskClient


class TestF1WebApp:
    def test_redirect_from_root_to_report_page(self, client: FlaskClient) -> None:
        # Given
        response = client.get("/")
        # Then
        assert response.status_code == HTTPStatus.MOVED_PERMANENTLY
        assert response.headers["Content-Type"] == "text/html; charset=utf-8"
        assert response.location.endswith("/report/")

    def test_report_page_returns_success_status(self, client: FlaskClient) -> None:
        # Given
        response = client.get("/report/", follow_redirects=True)
        # Then
        assert response.status_code == HTTPStatus.OK
        assert "Formula1 Race Report" in response.get_data(as_text=True)

    def test_invalid_sort_order(self, client: FlaskClient) -> None:
        # Given
        response = client.get("/report/?order=invalid")
        # Then
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert b"Invalid sort order" in response.data

    def test_correct_sort_order(self, client: FlaskClient) -> None:
        # Given
        response = client.get("/report/?order=asc")
        # Then
        assert response.status_code == HTTPStatus.OK

    def test_invalid_driver_id_request(self, client: FlaskClient) -> None:
        # Given
        client_request = "vvv"
        response = client.get(f"/report/drivers/?driver_id={client_request}")
        expected_message = (
            f"Identifier '{client_request}' is not recognized. Try to use 3-letter code like 'KRF': "
            "the first letters of the first name: 'K', the first letters of the last name: 'R' and the first "
            "letters of the car model: 'F'."
        )
        # Then
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert expected_message in html.unescape(response.get_data(as_text=True))

    def test_correct_driver_id_request(self, client: FlaskClient) -> None:
        # Given
        response = client.get("/report/drivers/?driver_id=FAM")
        # Then
        assert response.status_code == HTTPStatus.OK

    def test_drivers_page(self, client: FlaskClient) -> None:
        # Given
        response = client.get("/report/drivers")
        # Then
        assert response.status_code == HTTPStatus.OK

    def test_page_is_not_found(self, client: FlaskClient) -> None:
        # Given
        response = client.get("/report/drive_id")
        # Then
        assert response.status_code == HTTPStatus.NOT_FOUND
