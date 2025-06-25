OTP_EMAIL_BODY = """
    <!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Your OTP Code</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    body {
      margin: 0;
      padding: 0;
      background-color: #f3f4f6;
      font-family: 'Inter', sans-serif;
      color: #111827;
    }

    .email-wrapper {
      max-width: 600px;
      margin: 0 auto;
      padding: 40px 20px;
      background-color: #ffffff;
      border-radius: 12px;
      box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
    }

    h2 {
      color: #111827;
      font-size: 24px;
      margin-top: 0;
    }

    p {
      font-size: 16px;
      line-height: 1.6;
      color: #4b5563;
    }

    .otp {
      display: inline-block;
      margin: 24px 0;
      padding: 16px 32px;
      font-size: 28px;
      letter-spacing: 4px;
      font-weight: 600;
      color: #111827;
      background-color: #facc15;
      border-radius: 8px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    .footer {
      margin-top: 40px;
      font-size: 14px;
      color: #9ca3af;
      text-align: center;
    }

    .emoji {
      font-size: 22px;
    }
  </style>
</head>
<body>
  <div class="email-wrapper">
    <h2>Hey {user_name} 👋</h2>
    <p>Welcome to <strong>Our Service</strong> — we're pumped to have you join us!</p>

    <p>To complete your registration, here’s your one-time password (OTP):</p>

    <div class="otp">🔐 {otp_code}</div>

    <p>This code will expire in <strong>60 minutes</strong>. For your security, please don’t share it with anyone. 🙏</p>

    <p>If you didn’t try to sign up, feel free to ignore this message — no action needed.</p>

    <p>See you inside 🚀,<br><strong>The Our Service Team</strong></p>

    <div class="footer">
      You’re receiving this email because someone entered your email during sign-up.
    </div>
  </div>
</body>
</html>

"""
OTP_EMAIL_SUBJECT = "Complete Your Registration – Your OTP Inside"
