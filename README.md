# 🔐 Authenticator

A Python-based authentication and user management service with:
- User signup & login
- Password hashing & reset
- Time-based One-Time Passwords (TOTP/OTP)
- Session management & logout
- Extensible design for web apps or APIs

---

## ✨ Features
✅ Secure user signup and login  
✅ Session handling (create, invalidate)  
✅ OTP-based 2FA authentication  
✅ Password reset logic  
✅ Mailer integration for notifications (`communications/email.py`)  
✅ Lightweight & modular — built for easy integration with larger apps  

---

## 🧑‍💻 Getting Started

### 🐍 Prerequisites
- **Python ≥3.10**
- `pip` or `poetry`
- Local database (see `db.py` for connection details)
- `.env` file for secret keys and DB credentials

### ⚙️ Installation
```bash
git clone https://github.com/hansraj1999/authenticator.git
cd authenticator
pip install -r requirements.txt

🏃‍♂️ Run Locally

cd local_setup
docker compose up --build

🤝 Contributing
Fork the repo & create a feature branch

Commit & push your changes

Open a pull request!



---
📄 License
MIT License. See LICENSE file for details.

✅ Let me know if you’d also like a **sample TOTP snippet**, a **fully working `README.md` file**, or help adjusting this to your style (e.g. add badges, logo, deployment section, etc.)! 🎨
