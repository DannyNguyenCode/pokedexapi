# tests/test_crud.py

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import crud

import pytest
from unittest.mock import MagicMock
from app import crud


def test_create_user(mocker):
    data = {"email": "test@example.com"}
    fake_doc = MagicMock()
    fake_doc.id = "doc123"

    mock_doc = MagicMock(return_value=fake_doc)
    mock_collection = MagicMock(document=mock_doc)
    mocker.patch("app.crud.db.collection", return_value=mock_collection)

    result = crud.create_user(data)

    assert result["message"] == "User has registered successfully"
    assert result["id"] == "doc123"
    assert result["email"] == "test@example.com"
    fake_doc.set.assert_called_once_with(data)


def test_get_user_by_email(mocker):
    mock_docs = [MagicMock()]
    mock_get = MagicMock(return_value=mock_docs)
    mock_where = MagicMock(return_value=MagicMock(get=mock_get))
    mock_collection = MagicMock(where=mock_where)

    mocker.patch("app.crud.db.collection", return_value=mock_collection)

    result = crud.get_user_by_email("test@example.com")

    assert result == mock_docs


def test_get_user_by_id(mocker):
    mock_doc = MagicMock()
    mock_get = MagicMock(return_value=mock_doc)
    mock_document = MagicMock(return_value=MagicMock(get=mock_get))
    mock_collection = MagicMock(document=mock_document)

    mocker.patch("app.crud.db.collection", return_value=mock_collection)

    result = crud.get_user_by_id("123")
    assert result == mock_doc


def test_update_user(mocker):
    data = {"email": "updated@example.com"}
    mock_update = MagicMock()
    mock_doc = MagicMock(update=mock_update)
    mock_collection = MagicMock(document=MagicMock(return_value=mock_doc))

    mocker.patch("app.crud.db.collection", return_value=mock_collection)

    result = crud.update_user("123", data)

    assert result["message"] == "user has been updated"
    mock_update.assert_called_once_with(data)


def test_delete_user(mocker):
    mock_delete = MagicMock()
    mock_doc = MagicMock(delete=mock_delete)
    mock_collection = MagicMock(document=MagicMock(return_value=mock_doc))

    mocker.patch("app.crud.db.collection", return_value=mock_collection)

    result = crud.delete_user("123")

    assert result["message"] == "user has been deleted"
    mock_delete.assert_called_once()


def test_list_users(mocker):
    mock_docs = [MagicMock()]
    mock_get = MagicMock(return_value=mock_docs)
    mock_collection = MagicMock(get=mock_get)

    mocker.patch("app.crud.db.collection", return_value=mock_collection)

    result = crud.list_users()

    assert result == mock_docs
    mock_get.assert_called_once()