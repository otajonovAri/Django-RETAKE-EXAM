# 🌍 Dunyo shaharlari ma'lumotnomasi

Imtihon topshirig'i **№20** — shaharlar ma'lumotnomasi: qo'shish, ko'rish,
o'zgartirish va o'chirish (CRUD), mamlakat bo'yicha filtratsiya va
jadval ko'rinishidagi veb-interfeys.

## ✅ Topshiriq talablari va bajarilishi

| Talab | Holati | Qayerda |
|---|---|---|
| Shahar qo'shish / ko'rish / o'zgartirish / o'chirish | ✅ | [cities/views.py](cities/views.py) |
| Har bir shaharda nom, aholi, mamlakat | ✅ | [cities/models.py](cities/models.py) |
| Mamlakat bo'yicha filtratsiya | ✅ | `CityListView.get_queryset()` |
| Ro'yxat jadval ko'rinishida | ✅ | [cities/templates/cities/city_list.html](cities/templates/cities/city_list.html) |

Qo'shimcha: nom/mamlakat bo'yicha qidiruv, ustunlar bo'yicha saralash,
sahifalash (15 tadan), statistika, mamlakatlar kesimi, Django admin paneli,
yorug'/qorong'i rejim va **26 ta avtomatik test**.

## ♿ Foydalanish qulayligi (WCAG 2.1 AA)

Interfeys `/accessibility-review` bo'yicha tekshirilgan va tuzatilgan:

- **Kontrast:** barcha matnlar >= 4.5:1, chegaralar >= 3:1 — ikkala rejimda
  brauzerda hisoblab tasdiqlangan (eng past qiymat 4.83:1).
- **Klaviatura:** skip-link, ko'rinadigan fokus halqasi (`:focus-visible`),
  musbat `tabindex` ishlatilmagan, filtr o'zi yuborilmaydi (3.2.2).
- **Skrinrider:** `<caption>`, `scope="col|row"`, `aria-sort`, jonli xabar
  hududi (`role="status"`), har bir amal havolasining nomi noyob.
- **Formalar:** `required`, `aria-invalid`, `aria-describedby` orqali xato va
  izoh maydonga bog'langan; xatolar `role="alert"` bilan e'lon qilinadi.
- **Moslashuvchanlik:** sahifa gorizontal skroll qilmaydi, keng jadval o'z
  qutisi ichida suriladi; bosish maydonlari >= 24px (asosiylari 44px).
- **Harakat:** `prefers-reduced-motion` hurmat qilinadi.

Bu talablar `cities/tests.py` ichidagi `AccessibilityTests` sinfida qulflangan.

## 🛠 Texnologiyalar

- **Backend:** Python 3.12, Django 5.2
- **Ma'lumotlar bazasi:** SQLite (Django ORM)
- **Frontend:** Django Template + o'z dizayn tizimi (tashqi CDN'siz, offline ishlaydi)
- **UI:** yorug'/qorong'i rejim, responsiv jadval, WCAG 2.1 AA muvofiqligi

## 📦 O'rnatish va ishga tushirish

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_cities
python manage.py runserver
```

Brauzerda oching: <http://127.0.0.1:8000/>

Admin panel uchun (ixtiyoriy):

```bash
python manage.py createsuperuser
```

Keyin <http://127.0.0.1:8000/admin/> manzilida kiring.

## 🧪 Testlar

```bash
python manage.py test
```

26 ta test:

- **CRUD va biznes-mantiq (13 ta):** qo'shish/tahrirlash/o'chirish, mamlakat
  bo'yicha filtr, qidiruv, saralash, takroriy shahar nomini rad etish.
- **Foydalanish qulayligi (13 ta):** skip-link, ARIA atributlari, `aria-sort`,
  jonli xabar hududi, forma xatolarining bog'lanishi va h.k.

## 🔗 Sahifalar

| URL | Vazifasi |
|---|---|
| `/` | Shaharlar jadvali + filtr + qidiruv + saralash |
| `/shahar/qoshish/` | Yangi shahar qo'shish |
| `/shahar/<id>/` | Shahar tafsilotlari |
| `/shahar/<id>/tahrirlash/` | Shaharni tahrirlash |
| `/shahar/<id>/ochirish/` | O'chirishni tasdiqlash |
| `/mamlakatlar/` | Mamlakatlar bo'yicha statistika |
| `/mamlakatlar/qoshish/` | Yangi mamlakat qo'shish |
| `/admin/` | Django admin paneli |

## 🗄 Ma'lumotlar modeli

**Country** — `name` (unikal), `code` (ISO, ixtiyoriy)

**City** — `name`, `population`, `country` (FK → Country), `is_capital`,
`created_at`, `updated_at`

Bitta mamlakat ichida shahar nomi takrorlanmaydi (`UniqueConstraint`).
Mamlakat o'chirilsa, unga tegishli shaharlar ham o'chadi (`CASCADE`).

## 📁 Fayllar tuzilishi

```
DJango-RETAKE EXAM/
├── cityproject/              # Django loyiha sozlamalari
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py / asgi.py
├── cities/                   # Asosiy ilova
│   ├── management/commands/
│   │   └── seed_cities.py    # Namuna ma'lumotlar
│   ├── migrations/
│   ├── templates/
│   │   ├── base.html         # Skip-link, nav, jonli xabarlar
│   │   └── cities/           # list / detail / form / delete / _field
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── static/
│   ├── css/style.css         # Dizayn tizimi (light + dark)
│   └── js/theme.js           # Rejim almashtirgichi
├── DescriptionProject.txt    # Topshiriq matni
├── manage.py
├── requirements.txt
└── README.md
```
