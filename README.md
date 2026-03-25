Project Overview:

This project is a Digital Banking Backend API built using FastAPI (with SQLite).

It simulates core features of apps like PhonePe / Paytm, including:

1.User authentication
2.Wallet balance management
3.Fund transfers 
4.Email notifications
5.OTP-based secure transactions 
6.PDF transaction statements



Tech Stack:

1.FastAPI – API framework
2.SQLite – Database
3.JWT (python-jose) – Authentication
4.SMTP (Gmail) – Email service
5.ReportLab – PDF generation
6.Pydantic – Request validation



Project Structure:

Bash
fastapi_app/
│
├── main.py              # Main API routes
├── database.py          # DB connection
├── schemas.py           # Request models
├── auth.py              # JWT + password hashing
├── dependencies.py      # Auth middleware
├── email_utils.py       # Email sending
├── otp_utils.py         # OTP generation & verification
├── utils.py             # PDF generator
├── .env                 # Email credentials
└── requirements.txt



Features Implemented:

1.Authentication

    User Signup
    User Login
    JWT Token generation

2.Wallet System

    Default balance on signup: ₹1000
    Check balance endpoint

3.Fund Transfer

    Small Transfers (≤ ₹500)
    Direct transfer
    Email notification sent

    Large Transfers (> ₹500)

    Step-by-step secure flow:

        1.User initiates transfer
        2.OTP is generated
        3.OTP sent via email
        4.User submits OTP
        5.Transaction completes
        6.Confirmation email sent

4.Email Notifications

Emails are sent for:

    OTP verification
    Successful transactions

5.OTP Security

    6-digit OTP generated
    Stored in database (otp_store)
    Expiry: 5 minutes
    Verified before transaction

6.Transaction History

    View all transactions (credit/debit)
    Includes:

        Sender
        Receiver
        Amount
        Date

7.PDF Statement

    Download transaction statement
    Generated using ReportLab




Email Setup:

Configure .env

    Environment
    EMAIL_USER=your_email@gmail.com
    EMAIL_PASS=your_app_password        #use generated app code not directly app_password



🧪 Testing
Open Swagger UI:

http://127.0.0.1:9000/docs
Test endpoints:

    /auth/signup
    /auth/login
    /account/balance
    /account/transfer



Key Learnings:

    Secure API design
    JWT authentication
    OTP-based 2FA
    Async email handling
    Database transactions
    Error handling in FastAPI