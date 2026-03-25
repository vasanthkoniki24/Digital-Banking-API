import random
from datetime import datetime, timedelta
from database import cursor, conn

otp_store = {}

def generate_otp():
    return str(random.randint(100000, 999999))

def store_otp(username, otp):
    expiry = datetime.now() + timedelta(minutes=5)

    cursor.execute(
        "INSERT INTO otp_store (username, otp, expires_at) VALUES (?, ?, ?)",
        (username, otp, expiry.strftime("%Y-%m-%d %H:%M:%S"))
    )
    conn.commit()

    print("✅ OTP STORED:", username, otp)   # 👈 ADD THIS

# def verify_otp(username, otp):
#     cursor.execute(
#         "SELECT otp, expires_at FROM otp_store WHERE username=? ORDER BY id DESC LIMIT 1",
#         (username,)
#     )
#     row = cursor.fetchone()

#     if not row:
#         return False, "OTP not found"

#     stored_otp, expiry = row

#     if stored_otp != otp:
#         return False, "Invalid OTP"

#     if datetime.now() > datetime.strptime(expiry, "%Y-%m-%d %H:%M:%S"):
#         return False, "OTP expired"

#     return True, "OTP verified"


def verify_otp(username, otp):
    cursor.execute(
        "SELECT otp, expires_at FROM otp_store WHERE username=? ORDER BY id DESC LIMIT 1",
        (username,)
    )

    row = cursor.fetchone()

    print("DEBUG DB ROW:", row)   # 👈 ADD THIS

    if not row:
        return False, "OTP not found"

    stored_otp, expiry = row

    if stored_otp != otp:
        return False, "Invalid OTP"

    if datetime.now() > datetime.strptime(expiry, "%Y-%m-%d %H:%M:%S"):
        return False, "OTP expired"

    return True, "OTP verified"