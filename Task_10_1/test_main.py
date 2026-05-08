from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_item_not_found():
    response = client.get("/items/forbidden")
    assert response.status_code == 404
    assert response.json() == {
        "status": "error",
        "message": "Item Not Found",
        "detail": "The item 'forbidden' was not found in the inventory."
    }
    print("Test Item Not Found: PASSED")

def test_insufficient_permissions():
    response = client.get("/admin/guest")
    assert response.status_code == 403
    assert response.json() == {
        "status": "error",
        "message": "Access Denied",
        "detail": "User 'guest' does not have permission to perform this action."
    }
    print("Test Insufficient Permissions: PASSED")

def test_success_item():
    response = client.get("/items/apple")
    assert response.status_code == 200
    assert response.json() == {"item": "apple", "status": "available"}
    print("Test Success Item: PASSED")

def test_success_admin():
    response = client.get("/admin/admin")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome, admin!"}
    print("Test Success Admin: PASSED")

if __name__ == "__main__":
    test_item_not_found()
    test_insufficient_permissions()
    test_success_item()
    test_success_admin()
    print("\nAll tests passed!")
