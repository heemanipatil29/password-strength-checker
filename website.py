from reportlab.pdfgen import canvas
from flask import send_file
from flask import Flask, request
latest_report = ""
latest_score = ""
latest_strength = ""
latest_suggestions = ""

app = Flask(__name__)
@app.route("/")
def home():
    return """
    <html>
    <body style="background: url('/static/cybersecurity.jpg') center/cover no-repeat;">
    <p style="color:#FFFFFF; font-size:70px; font-family:'times new roman';text-align:center">Password</p>
    <form action="/page2" method="POST">
    <p style="color:#FFFFFF; text-align:left; font-size:35;">Enter Password:
    <input type="Password" name="Password" placeholder="Enter Password" style="width:300px; height:35px;"></p>
    
    
    <p style="color:#FFFFFF; text-align:left; font-size:35;">Enter Confirm Password:
    <input type="Password" name="Confirm_Password" placeholder="Enter Confirm Password" style="width:300px; height:35px;"></p>
    <a href="/page2"><button type="submit" style="width:180px; height:60px; font-size:25px; color:black; background-color:#00C853;">NEXT</button></a></form>
     </body></head></html>
    </body>
    </html>
    """
@app.route("/page2", methods=["GET", "POST"])
def page2():
    password = request.form.get("Password")
    confirm_password = request.form.get("Confirm_Password")
    Suggestions = ""
    length_check = "✅ Passed" if len(password) >= 8 else "❌ Failed"
    upper_check = "✅ Found" if any(c.isupper() for c in password) else "❌ Not Found"
    lower_check = "✅ Found" if any(c.islower() for c in password) else "❌ Not Found"
    number_check = "✅ Found" if any(c.isdigit() for c in password) else "❌ Not Found"

    special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?/"
    special_check = "✅ Found" if any(c in special_chars for c in password) else "❌ Not Found"

    password_match = "✅ Matched" if password == confirm_password else "❌ Not Matched"

    score = 0

    if len(password) >= 8:
        score += 20
    if any(c.isupper() for c in password):
        score += 20
    if any(c.islower() for c in password):
        score += 20
    if any(c.isdigit() for c in password):
        score += 20
    if any(c in special_chars for c in password):
        score += 20

    if score  < 40:
        strength = "🔴 Weak"
    elif score  < 80:
        strength = "🟡 Medium"
    else:
        strength = "🟢 Strong"

    if strength == "🔴 Weak":
        Suggestions = """
        • Increase password length.<br>
        • Add uppercase letters, numbers, and symbols.<br>
        • Avoid common or predictable passwords.
        """

    elif strength == "🟡 Medium":
        Suggestions = """
        • Use more unique character combinations.<br>
        • Increase password length.<br>
        • Enable Multi-Factor Authentication (MFA).
        """

    else:
        Suggestions = """
        • Strong password detected.<br>
        • Use a unique password for each account.<br>
        • Enable Multi-Factor Authentication (MFA).
        """

    global latest_report
    latest_report = f"""
        Password Strength Report

        Password Length: {length_check}
        Uppercase Letter: {upper_check}
        Lowercase Letter: {lower_check}
        Number: {number_check}
        Special Character: {special_check}
        Password Match: {password_match}

        Strength Score: {score}/100
        Password Strength: {strength}

        Suggestions:
        {Suggestions}
        """

    return f"""
    <html>
    <body style="background: url('/static/cybersecurity.jpg') center/cover no-repeat;">

    <h1 style="text-align:center;font-weight:bold; color:#FFFFFF"><b>Password Strength Report</h1></b>

    <table border="1" style="margin:auto; border-collapse:collapse; color:#FFFFFF; width:40%;">
        <tr>
            <th>Check</th>
            <th>Result</th>
        </tr>

        <tr>
            <td>Password Length</td>
            <td>{length_check}</td>
        </tr>

        <tr>
            <td>Uppercase Letter</td>
            <td>{upper_check}</td>
        </tr>

        <tr>
            <td>Lowercase Letter</td>
            <td>{lower_check}</td>
        </tr>

        <tr>
            <td>Number</td>
            <td>{number_check}</td>
        </tr>

        <tr>
            <td>Special Character</td>
            <td>{special_check}</td>
        </tr>

        <tr>
            <td>Password Match</td>
            <td>{password_match}</td>
        </tr>

    </table>

    <h2 style="text-align:center; color:#FFFFFF">
    Strength Score : {score}/100
    </h2>

    <h2 style="text-align:center; color:#FFFFFF">
    Password Strength : {strength}
    </h2>
    <h2 style="text-align:center; color:#FFFFFF">Suggestions</h2>

<div style="width:60%; margin:auto; background-color:#1F2937;
padding:15px; border-radius:10px; color:white; font-size:20px; line-height:35px; text-align:left;">
{Suggestions}
</div>
   
    <a href="/download"><button style="width:220px; height:60px; font_size:22px; background-color:#16A34A; color:white; border-radius:10px;">Download Report</button></a>
    </body></html>
    """
@app.route("/download")
def download():
    print(latest_report)
    pdf_file = "password_report.pdf"

    c = canvas.Canvas(pdf_file)


    y = 760
    for line in latest_report.split("\n"):
        if "Not Found" in line or "Failed" in line or "Not Matched" in line:
            c.setFillColorRGB(1, 0, 0)  # Red

        elif "Passed" in line or "Found" in line or "Matched" in line:
            c.setFillColorRGB(0, 0.7, 0)  # Green

        elif "Password Strength" in line and "Strong" in line:
            c.setFillColorRGB(0, 0.7, 0)

        elif "Password Strength" in line and "Medium" in line:
            c.setFillColorRGB(1, 0.6, 0)

        elif "Password Strength" in line and "Weak" in line:
            c.setFillColorRGB(1, 0, 0)

        else:
            c.setFillColorRGB(0, 0, 0)
        line = line.replace("<br>", "")
        c.drawString(50, y, line)
        y -= 20

    c.save()

    return send_file(pdf_file, as_attachment=True)

import os

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))