import os
import sys

# Add the project root to sys.path so we can import app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from app.main import app
from app.database.database import Base, engine

# Ensure clean DB for testing
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

client = TestClient(app)

def run_tests():
    print("Testing Foundation...")
    assert client.get("/docs").status_code == 200

    print("Testing Users and Authentication...")
    # Register User A
    res_a = client.post("/user/", json={"email": "userA@test.com", "password": "password"})
    assert res_a.status_code == 201
    
    # Register User B
    res_b = client.post("/user/", json={"email": "userB@test.com", "password": "password"})
    assert res_b.status_code == 201

    # Login User A
    res_login_a = client.post("/login/", data={"username": "userA@test.com", "password": "password"})
    assert res_login_a.status_code == 200
    token_a = res_login_a.json()["access_token"]
    auth_a = {"Authorization": f"Bearer {token_a}"}

    # Login User B
    res_login_b = client.post("/login/", data={"username": "userB@test.com", "password": "password"})
    assert res_login_b.status_code == 200
    token_b = res_login_b.json()["access_token"]
    auth_b = {"Authorization": f"Bearer {token_b}"}

    print("Testing Wallets...")
    # Create Wallet A (INR)
    res_wal_a = client.post("/wallet/", json={"currency": "INR"}, headers=auth_a)
    assert res_wal_a.status_code == 201
    wallet_a_id = res_wal_a.json()["id"]

    # Create Wallet B (INR)
    res_wal_b = client.post("/wallet/", json={"currency": "INR"}, headers=auth_b)
    assert res_wal_b.status_code == 201
    wallet_b_id = res_wal_b.json()["id"]

    # Prevent cross-user access
    res_cross = client.get(f"/wallet/{wallet_b_id}", headers=auth_a)
    assert res_cross.status_code == 404

    # Duplicate currency wallet creation
    res_dup = client.post("/wallet/", json={"currency": "INR"}, headers=auth_a)
    assert res_dup.status_code == 409

    print("Testing Transfer Validation...")
    # Attempt transfer without balance
    tx_req = {
        "receiver_wallet_id": wallet_b_id,
        "amount": 100.00,
        "currency": "INR",
        "idempotency_key": "test_idempotency_key_1"
    }
    res_tx_fail = client.post("/transaction/transfer", json=tx_req, headers=auth_a)
    assert res_tx_fail.status_code == 400
    assert res_tx_fail.json()["detail"] == "Insufficient balance"

    print("Testing Successful Transfer and Ledger...")
    # Cheat: give user A some balance directly in DB to test transfer
    from app.database.database import SessionLocal
    from app.models.wallet import Wallet
    db = SessionLocal()
    w_a = db.query(Wallet).filter(Wallet.id == wallet_a_id).first()
    w_a.balance = 500.00
    db.commit()
    db.close()

    # Successful transfer
    tx_req["idempotency_key"] = "test_idempotency_key_success"
    res_tx = client.post("/transaction/transfer", json=tx_req, headers=auth_a)
    assert res_tx.status_code == 201
    
    # Check duplicate idempotency key
    res_tx_dup = client.post("/transaction/transfer", json=tx_req, headers=auth_a)
    assert res_tx_dup.status_code == 409
    
    # Verify balances
    w_a_res = client.get(f"/wallet/{wallet_a_id}", headers=auth_a)
    assert float(w_a_res.json()["balance"]) == 400.00
    
    w_b_res = client.get(f"/wallet/{wallet_b_id}", headers=auth_b)
    assert float(w_b_res.json()["balance"]) == 100.00
    
    print("Testing Ledger...")
    # Verify Ledger
    ledger_a_res = client.get(f"/ledger/{wallet_a_id}", headers=auth_a)
    assert ledger_a_res.status_code == 200
    ledger_a = ledger_a_res.json()
    assert len(ledger_a) == 1
    assert ledger_a[0]["entry_type"] == "DEBIT"
    assert float(ledger_a[0]["amount"]) == 100.00
    assert float(ledger_a[0]["balance_after"]) == 400.00
    
    ledger_b_res = client.get(f"/ledger/{wallet_b_id}", headers=auth_b)
    assert ledger_b_res.status_code == 200
    ledger_b = ledger_b_res.json()
    assert len(ledger_b) == 1
    assert ledger_b[0]["entry_type"] == "CREDIT"
    assert float(ledger_b[0]["amount"]) == 100.00
    assert float(ledger_b[0]["balance_after"]) == 100.00

    print("All checks passed.")

if __name__ == "__main__":
    run_tests()
