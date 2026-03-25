from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from datetime import datetime


def generate_pdf(transactions, username):
    file_name = f"{username}_statement.pdf"

    c = canvas.Canvas(file_name, pagesize=A4)
    width, height = A4

    # =========================
    # WATERMARK
    # =========================
    c.setFont("Helvetica-Bold", 60)
    c.setFillColorRGB(0.92, 0.92, 0.92)
    c.saveState()
    c.translate(width/2, height/2)
    c.rotate(45)
    c.drawCentredString(0, 0, "DIGITAL BANK")
    c.restoreState()

    # =========================
    # HEADER
    # =========================
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, height - 50, "Bank Statement")

    c.setFont("Helvetica", 11)
    c.drawString(50, height - 70, f"User: {username}")
    c.drawString(50, height - 90, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # =========================
    # TABLE HEADER
    # =========================
    y = height - 130

    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(colors.darkblue)

    c.drawString(50, y, "ID")
    c.drawString(80, y, "Type")
    c.drawString(130, y, "From")
    c.drawString(220, y, "To")
    c.drawString(310, y, "Amount")
    c.drawString(390, y, "Date")

    c.line(50, y - 5, width - 50, y - 5)

    # =========================
    # TABLE DATA
    # =========================
    y -= 30
    c.setFont("Helvetica", 11)

    for txn in transactions:
        txn_id, sender, receiver, amount, created_at = txn

        # Determine type + color
        if username == sender:
            txn_type = "DEBIT"
            amount_text = f"- ₹{amount}"
            c.setFillColor(colors.red)
        elif username == receiver:
            txn_type = "CREDIT"
            amount_text = f"+ ₹{amount}"
            c.setFillColor(colors.green)
        else:
            continue

        if y < 100:
            c.showPage()
            y = height - 100

        c.drawString(50, y, str(txn_id))
        c.drawString(80, y, txn_type)
        c.drawString(130, y, sender)
        c.drawString(220, y, receiver)
        c.drawString(310, y, amount_text)
        c.drawString(390, y, str(created_at))

        y -= 25

    # =========================
    # FOOTER
    # =========================
    c.setFont("Helvetica-Oblique", 9)
    c.setFillColor(colors.grey)
    c.drawString(50, 40, "This is a system generated statement.")

    c.save()

    return file_name