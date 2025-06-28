# tests/test_crud.py

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import crud

import pytest
from unittest.mock import MagicMock
from app import crud


def test_create_user_adds_id_and_lowercases_email(mocker):
    # Arrange
    input_data = {
        "email": "TeSt@Example.com",
        "name": "Ash Ketchum"
    }

    # Mock Firestore doc_ref with auto-generated ID
    mock_doc_ref = MagicMock()
    mock_doc_ref.id = "abc123"

    # Mock collection().document() to return our mock_doc_ref
    mock_collection = MagicMock()
    mock_collection.document.return_value = mock_doc_ref

    mocker.patch("app.crud.db.collection", return_value=mock_collection)

    # Act
    result = crud.create_user(input_data)

    # Assert: doc_ref.set was called with merged data
    expected_data = {
        "id": "abc123",
        "email": "test@example.com",
        "name": "Ash Ketchum"
    }

    mock_doc_ref.set.assert_called_once_with(expected_data)

    # Assert: returned values
    assert result["message"] == "User has registered successfully"
    assert result["id"] == "abc123"
    assert result["email"] == "test@example.com"


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


def test_get_pokemons_by_user_id(mocker):
    mock_docs = [MagicMock()]
    mock_collection = MagicMock()
    mock_collection.where.return_value = mock_collection  # chain .where().where().get()
    mock_collection.get.return_value = mock_docs

    mocker.patch("app.crud.db.collection", return_value=mock_collection)
    mocker.patch("app.crud.FieldFilter", return_value="filter")

    result = crud.get_pokemons_by_user_id("user123")

    mock_collection.where.assert_called()
    assert result == mock_docs


def test_add_pokemon_to_user_collection(mocker):
    mock_doc_ref = MagicMock()
    mock_doc_ref.id = "doc123"
    mock_collection = MagicMock()
    mock_collection.document.return_value = mock_doc_ref

    mocker.patch("app.crud.db.collection", return_value=mock_collection)

    data = {
        "id": 1,
        "imageUrl": "https://example.com/image.png",
        "name": "Pikachu",
        "type": "Electric"
    }

    result = crud.add_pokemon_to_user_collection("user123", data)

    mock_doc_ref.set.assert_called_once_with({
        "id": 1,
        "imageUrl": "https://example.com/image.png",
        "name": "Pikachu",
        "type": "Electric",
        "owner_id": "user123"
    })

    assert result["message"] == "Pokemon captured successfully"
    assert result["id"] == "doc123"
    assert result["status"] == 200


def test_remove_pokemon_from_user_collection_found(mocker):
    mock_snap = MagicMock()
    mock_snap.exists = True
    mock_snap.reference.delete.return_value = None

    mock_stream = iter([mock_snap])
    mock_collection = MagicMock()
    mock_collection.where.return_value = mock_collection
    mock_collection.limit.return_value = mock_collection
    mock_collection.stream.return_value = mock_stream

    mocker.patch("app.crud.db.collection", return_value=mock_collection)

    result = crud.remove_pokemon_from_user_collection("user123", 1)

    mock_snap.reference.delete.assert_called_once()
    assert result["message"] == "Pokemon released successfully"


def test_remove_pokemon_from_user_collection_not_found(mocker):
    mock_collection = MagicMock()
    mock_collection.where.return_value = mock_collection
    mock_collection.limit.return_value = mock_collection
    mock_collection.stream.return_value = iter([])

    mocker.patch("app.crud.db.collection", return_value=mock_collection)

    result = crud.remove_pokemon_from_user_collection("user123", 1)

    assert result["error"] == "No matching Pokémon found"