from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.responses import FileResponse
from fastapi.security import HTTPBearer
from datetime import datetime

from database import cursor, conn
from schemas import UserCreate, Login, Transfer
from auth import hash_password, verify_password, create_token
from dependencies import get_current_user
from utils import generate_pdf
from email_utils import send_email
from otp_utils import generate_otp, store_otp, verify_otp

app = FastAPI(title="Digital Banking API")

security = HTTPBearer()

OTP_THRESHOLD = 500  # 🔥 configurable

# =========================
# AUTH APIs
# =========================

@app.post("/auth/signup")
def signup(user: UserCreate):
    cursor.execute("SELECT * FROM banking_userdata WHERE username=?", (user.username,))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="User already exists")

    cursor.execute(
        "INSERT INTO banking_userdata (username, email, password, balance) VALUES (?, ?, ?, ?)",
        (user.username, user.email, hash_password(user.password), 1000)
    )
    conn.commit()

    return {"message": "User created successfully"}


@app.post("/auth/login")
def login(data: Login):
    cursor.execute("SELECT * FROM banking_userdata WHERE username=?", (data.username,))
    user = cursor.fetchone()

    if not user or not verify_password(data.password, user[3]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token({"sub": data.username})
    return {"access_token": token}


# =========================
# ACCOUNT APIs
# =========================

@app.get("/account/balance")
def balance(current_user=Depends(get_current_user)):
    cursor.execute(
        "SELECT balance FROM banking_userdata WHERE username=?",
        (current_user["username"],)
    )
    result = cursor.fetchone()

    if not result:
        raise HTTPException(status_code=404, detail="User not found")

    return {"balance": result[0]}


@app.post("/account/transfer")
def transfer(
    data: Transfer,
    background_tasks: BackgroundTasks,
    user=Depends(get_current_user)
):
    sender_username = user["username"]

    # 🔍 Get receiver
    cursor.execute(
        "SELECT id, email FROM banking_userdata WHERE username=?",
        (data.receiver,)
    )
    receiver = cursor.fetchone()

    if not receiver:
        raise HTTPException(status_code=404, detail="Receiver not found")

    receiver_id, receiver_email = receiver

    # 🔍 Get sender details
    cursor.execute(
        "SELECT balance, email FROM banking_userdata WHERE id=?",
        (user["id"],)
    )
    sender_data = cursor.fetchone()

    if not sender_data:
        raise HTTPException(status_code=404, detail="Sender not found")

    sender_balance, sender_email = sender_data

    # 💰 Balance check
    if sender_balance < data.amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    # =========================
    # 🔐 OTP LOGIC
    # =========================
    # =========================
    if data.amount > OTP_THRESHOLD:

        # STEP 1 → SEND OTP
        if data.otp is None:
            otp = generate_otp()
            store_otp(user["username"], otp)

            print("DEBUG OTP:", otp)  # 🔥 for testing

            background_tasks.add_task(
                send_email,
                sender_email,
                "OTP Verification",
                f"Your OTP is {otp}"
            )

            return {"message": "OTP sent to your email"}

        # STEP 2 → VERIFY OTP
        valid, msg = verify_otp(user["username"], data.otp)

        if not valid:
            raise HTTPException(status_code=400, detail=msg)

    # =========================
    # 💸 PROCESS TRANSFER
    # =========================
    cursor.execute(
        "UPDATE banking_userdata SET balance = balance - ? WHERE id=?",
        (data.amount, user["id"])
    )

    cursor.execute(
        "UPDATE banking_userdata SET balance = balance + ? WHERE id=?",
        (data.amount, receiver_id)
    )

    cursor.execute("""
        INSERT INTO banking_transaction (sender_id, receiver_id, amount, timestamp)
        VALUES (?, ?, ?, ?)
    """, (user["id"], receiver_id, data.amount, datetime.now()))

    conn.commit()

    # =========================
    # 📧 EMAIL NOTIFICATION
    # =========================
    email_body = f"""
Transaction Successful!

Amount: ₹{data.amount}
From: {sender_username}
To: {data.receiver}
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Thank you for using Digital Bank.
"""

    background_tasks.add_task(
        send_email,
        sender_email,
        "Transaction Alert",
        email_body
    )

    return {"message": "Transfer successful"}


# =========================
# TRANSACTIONS APIs
# =========================

@app.get("/transactions/history")
def history(user=Depends(get_current_user)):
    cursor.execute("""
        SELECT t.id, u1.username, u2.username, t.amount, t.timestamp
        FROM banking_transaction t
        JOIN banking_userdata u1 ON t.sender_id = u1.id
        JOIN banking_userdata u2 ON t.receiver_id = u2.id
        WHERE t.sender_id=? OR t.receiver_id=?
        ORDER BY t.id DESC
    """, (user["id"], user["id"]))

    rows = cursor.fetchall()

    result = []
    for row in rows:
        txn_type = "DEBIT" if row[1] == user["username"] else "CREDIT"

        result.append({
            "transaction_id": row[0],
            "type": txn_type,
            "amount": row[3],
            "from": row[1],
            "to": row[2],
            "date": row[4]
        })

    return result


@app.get("/transactions/statement")
def statement(user=Depends(get_current_user)):
    cursor.execute("""
        SELECT t.id, u1.username, u2.username, t.amount, t.timestamp
        FROM banking_transaction t
        JOIN banking_userdata u1 ON t.sender_id = u1.id
        JOIN banking_userdata u2 ON t.receiver_id = u2.id
        WHERE t.sender_id=? OR t.receiver_id=?
        ORDER BY t.id DESC
    """, (user["id"], user["id"]))

    transactions = cursor.fetchall()

    file = generate_pdf(transactions, user["username"])

    return FileResponse(
        path=file,
        filename=file,
        media_type='application/pdf'
    )