import pytest
from fastapi.testclient import TestClient

import database
from main import app


@pytest.fixture
def client(tmp_path):
    db_path = tmp_path / "test.db"

    database.set_db_name(str(db_path))
    database.init_db()

    with TestClient(app) as client:
        yield client


def test_root(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Experiment API is running"}


def test_create_experiment(client):
    response = client.post(
        "/experiments",
        json={
            "name": "pytest experiment",
            "frequency": "2.5",
            "damping": "0.2",
            "amplitude": "4.7",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] > 0
    assert data["name"] == "pytest experiment"
    assert data["frequency"] == 2.5
    assert data["damping"] == 0.2
    assert data["amplitude"] == 4.7


def test_get_experiments(client):
    response = client.get("/experiments")

    assert response.status_code == 200
    assert response.json() == []


def test_get_experiment(client):
    create_response = client.post(
        "/experiments",
        json={
            "name": "test experiment",
            "frequency": 2.5,
            "damping": 0.2,
            "amplitude": 4.7,
        },
    )

    assert create_response.status_code == 201

    experiment_id = create_response.json()["id"]

    response = client.get(f"/experiments/{experiment_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == experiment_id
    assert data["name"] == "test experiment"
    assert data["frequency"] == 2.5
    assert data["damping"] == 0.2
    assert data["amplitude"] == 4.7


def test_update_experiment(client):
    # 建立資料
    create_response = client.post(
        "/experiments",
        json={
            "name": "test experiment",
            "frequency": 2.5,
            "damping": 0.2,
            "amplitude": 4.7,
        },
    )

    assert create_response.status_code == 201

    experiment_id = create_response.json()["id"]

    # 更新資料
    update_response = client.put(
        f"/experiments/{experiment_id}",
        json={
            "name": "test update",
            "frequency": 5.5,
            "damping": 0.5,
            "amplitude": 9.7,
        },
    )

    assert update_response.status_code == 200

    data = update_response.json()

    assert data["id"] == experiment_id
    assert data["name"] == "test update"
    assert data["frequency"] == 5.5
    assert data["damping"] == 0.5
    assert data["amplitude"] == 9.7


def test_delete_experiment(client):
    # 建立資料
    create_response = client.post(
        "/experiments",
        json={
            "name": "test experiment",
            "frequency": 2.5,
            "damping": 0.2,
            "amplitude": 4.7,
        },
    )

    assert create_response.status_code == 201

    experiment_id = create_response.json()["id"]

    # 刪除資料
    delete_response = client.delete(
        f"/experiments/{experiment_id}",
    )

    assert delete_response.status_code == 204

    # 確認 get 拿不到資料
    get_response = client.get(f"/experiments/{experiment_id}")

    assert get_response.status_code == 404


def test_create_experiment_invalid_frequency(client):
    response = client.post(
        "/experiments",
        json={
            "name": "invalid experiment",
            "frequency": -1,
            "damping": 0.2,
            "amplitude": 4.7,
        },
    )

    assert response.status_code == 422


def test_get_invalid_experiment_id(client):
    response = client.get("/experiments/999999")

    assert response.status_code == 404


def test_delete_invalid_experiment_id(client):
    response = client.delete("/experiments/999999")
    
    assert response.status_code == 404


def test_create_invalid_experiment_does_not_create_data(client):
    response = client.post(
        "/experiments",
        json={
            "name": "invalid experiment",
            "frequency": -1,
            "damping": 0.2,
            "amplitude": 4.7,
        },
    )

    assert response.status_code == 422

    response = client.get("/experiments")

    assert response.status_code == 200
    assert response.json() == []