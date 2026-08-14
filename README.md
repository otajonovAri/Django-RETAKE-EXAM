# 🌍 World Cities Directory (v1.1.0)

Professional darajadagi dunyo shaharlari ma'lumotlar bazasi boshqaruv tizimi.

## 🚀 Status: Active Development
- [x] CRUD Funksionalligi (Tayyor)
- [x] Dinamik Filtratsiya (Tayyor)
- [ ] Eksport (Excel/PDF) - (Rejada)
- [ ] API Documentation (Swagger) - (Rejada)

## 🛠 Texnologiyalar
- **Backend:** Python 3.10+, Flask
- **Database:** SQLite (SQLAlchemy ORM)
- **Frontend:** Bootstrap 5, Jinja2, Chart.js (statistika uchun)

## 📦 O'rnatish
1. `pip install -r requirements.txt`
2. `python app.py`

# File Structure's
```
CityProject/
├── app/
│   ├── static/          # CSS, JS, Rasmlar
│   ├── templates/       # HTML fayllar
│   ├── __init__.py      # App factory
│   ├── models.py        # Database modellari
│   └── routes.py        # Controllerlar
├── migrations/          # Baza versiyalari (Flask-Migrate)
├── .env                 # Maxfiy sozlamalar
├── .gitignore           # Keraksiz fayllar
├── requirements.txt     # Kutubxonalar ro'yxati
└── run.py               # Loyihani ishga tushirish
```