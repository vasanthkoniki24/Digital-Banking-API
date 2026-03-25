Project Overview:

This project is a Digital Banking Backend API built using FastAPI and Django (with SQLite database).

It simulates core features of apps like PhonePe / Paytm, including:


1.User authentication
2.Wallet balance management
3.Fund transfers 
4.Email notifications
5.OTP-based secure transactions 
6.PDF transaction statements



Tech Stack:

1.FastAPI – API framework
2.Django – Used for database models, admin panel, and migrations
3.SQLite – Database
4.JWT (python-jose) – Authentication
5.SMTP (Gmail) – Email service
6.ReportLab – PDF generation
7.Pydantic – Request validation



Architecture Overview

This project follows a hybrid architecture:

    Django (django_app) is used for:

        Creating and managing database models
        Handling migrations
        Providing admin interface

    FastAPI (fastapi_app) is used for:

        Building REST APIs
        Handling authentication & business logic
        Managing transactions, OTP, and email flow

Both share the same database, ensuring smooth integration




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
    Integration of Django (models) with FastAPI (APIs)



Final Summary

    This project combines:

        Django → for database modeling and admin management
        FastAPI → for high-performance APIs and business logic
        
Together, they form a secure, scalable, and production-ready digital banking backend system.