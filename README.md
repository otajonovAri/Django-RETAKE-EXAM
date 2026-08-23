# 🌍 Dunyo shaharlari ma'lumotnomasi

Imtihon topshirig'i **№20** — shaharlar ma'lumotnomasi: qo'shish, ko'rish,
o'zgartirish va o'chirish (CRUD), mamlakat bo'yicha filtratsiya va
jadval ko'rinishidagi veb-interfeys.

Loyiha topshiriq talablaridan tashqari to'liq ishlab chiqarishga tayyor
holatga keltirilgan: REST API + Swagger, Excel/CSV eksporti, yorug'/qorong'i
rejim, WCAG 2.1 AA muvofiqligi, Docker va CI.

---

## ✅ Topshiriq talablari

| Talab | Holati | Qayerda |
|---|---|---|
| Shahar qo'shish / ko'rish / o'zgartirish / o'chirish | ✅ | [cities/views.py](cities/views.py) |
| Har bir shaharda nom, aholi, mamlakat | ✅ | [cities/models.py](cities/models.py) |
| Mamlakat bo'yicha filtratsiya | ✅ | `filter_cities()` |
| Ro'yxat jadval ko'rinishida | ✅ | [city_list.html](cities/templates/cities/city_list.html) |

## 🎁 Qo'shimcha imkoniyatlar

| Imkoniyat | Tafsilot |
|---|---|
| **Mamlakat CRUD** | Ro'yxat, tafsilot, tahrirlash, o'chirish (o'chirishda nechta shahar yo'qolishi ogohlantiriladi) |
| **Qidiruv va saralash** | Nom/mamlakat bo'yicha qidiruv, har bir ustun bo'yicha saralash |
| **Eksport** | CSV (Excel uchun BOM bilan) va `.xlsx` — **joriy filtr saqlanadi** |
| **REST API** | DRF, sahifalash, filtr, qidiruv, saralash |
| **Swagger / ReDoc** | `/api/docs/` va `/api/redoc/` — fayllari lokal, internetsiz ham ochiladi |
| **Yorug'/qorong'i rejim** | Tizim sozlamasiga ergashadi, tanlov saqlanadi |
| **Foydalanish qulayligi** | WCAG 2.1 AA — pastda batafsil |
| **Xato sahifalari** | Maxsus 404 / 403 / 500 |
| **Sozlamalar** | `.env` orqali, ishlab chiqarishda xavfsizlik standart yoqiq |
| **Docker + CI** | `Dockerfile` va GitHub Actions |
| **Testlar** | **61 ta** avtomatik test |

---

## 🛠 Texnologiyalar

- **Backend:** Python 3.12, Django 5.2
- **API:** Django REST Framework, django-filter, drf-spectacular (OpenAPI 3)
- **Ma'lumotlar bazasi:** SQLite (Django ORM)
- **Frontend:** Django Template + o'z dizayn tizimi (tashqi CDN yo'q)
- **Eksport:** openpyxl
- **Sozlama:** python-dotenv

## 📦 O'rnatish va ishga tushirish

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py seed_cities
python manage.py runserver
```

Brauzerda oching: <http://127.0.0.1:8000/>

Admin panel va API'da yozish uchun foydalanuvchi yarating:

```bash
python manage.py createsuperuser
```

### Docker bilan

```bash
docker build -t dunyo-shaharlari . && docker run -p 8000:8000 dunyo-shaharlari
```

---

## 🔗 Sahifalar

### Veb interfeys

| URL | Vazifasi |
|---|---|
| `/` | Shaharlar jadvali + filtr + qidiruv + saralash + eksport |
| `/shahar/qoshish/` | Yangi shahar qo'shish |
| `/shahar/<id>/` | Shahar tafsilotlari |
| `/shahar/<id>/tahrirlash/` | Shaharni tahrirlash |
| `/shahar/<id>/ochirish/` | O'chirishni tasdiqlash |
| `/mamlakatlar/` | Mamlakatlar statistikasi |
| `/mamlakatlar/qoshish/` | Yangi mamlakat |
| `/mamlakatlar/<id>/` | Mamlakat va uning shaharlari |
| `/mamlakatlar/<id>/tahrirlash/` | Mamlakatni tahrirlash |
| `/mamlakatlar/<id>/ochirish/` | Mamlakatni o'chirish |
| `/eksport/csv/` | CSV yuklab olish (filtr bilan) |
| `/eksport/excel/` | Excel yuklab olish (filtr bilan) |
| `/admin/` | Django admin paneli |

### REST API

| URL | Vazifasi |
|---|---|
| `/api/docs/` | **Swagger UI** — interaktiv hujjatlar |
| `/api/redoc/` | ReDoc ko'rinishi |
| `/api/schema/` | OpenAPI 3 sxemasi |
| `/api/cities/` | Shaharlar (GET, POST) |
| `/api/cities/<id>/` | Bitta shahar (GET, PUT, PATCH, DELETE) |
| `/api/countries/` | Mamlakatlar (shahar soni va aholisi bilan) |
| `/api/countries/<id>/cities/` | Shu mamlakat shaharlari |

**Ruxsatlar:** `GET` hamma uchun ochiq; `POST/PUT/PATCH/DELETE` uchun tizimga
kirish va model ruxsati kerak (`/api-auth/login/` yoki `/admin/` orqali kiring).

**API misollari:**

```bash
curl "http://127.0.0.1:8000/api/cities/?country=1"
curl "http://127.0.0.1:8000/api/cities/?search=tosh&ordering=-population"
curl "http://127.0.0.1:8000/api/cities/?is_capital=true"
```

---

## ♿ Foydalanish qulayligi (WCAG 2.1 AA)

Interfeys `/accessibility-review` bo'yicha tekshirilgan va tuzatilgan:

- **Kontrast:** barcha matnlar ≥ 4.5:1, chegaralar ≥ 3:1 — ikkala rejimda
  brauzerda hisoblab tasdiqlangan (eng past qiymat 4.83:1).
- **Klaviatura:** skip-link, ko'rinadigan fokus halqasi (`:focus-visible`),
  musbat `tabindex` yo'q, filtr o'zi yuborilmaydi (3.2.2).
- **Skrinrider:** `<caption>`, `scope="col|row"`, `aria-sort`, jonli xabar
  hududi (`role="status"`), har bir amal havolasining nomi noyob.
- **Formalar:** `required`, `aria-invalid`, `aria-describedby` orqali xato va
  izoh maydonga bog'langan; xatolar `role="alert"` bilan e'lon qilinadi.
- **Moslashuvchanlik:** sahifa gorizontal skroll qilmaydi, keng jadval o'z
  qutisi ichida suriladi; bosish maydonlari ≥ 24px (asosiylari 44px).
- **Harakat:** `prefers-reduced-motion` hurmat qilinadi.

Bu talablar `cities/tests.py` ichidagi `AccessibilityTests` sinfida qulflangan.

---

## 🧪 Testlar

```bash
python manage.py test
```

**61 ta test:**

| Sinf | Soni | Nimani tekshiradi |
|---|---|---|
| `CityCrudTests` | 9 | Shahar CRUD, filtr, qidiruv, saralash, takroriy nom |
| `CountryViewTests` | 2 | Mamlakatlar statistikasi |
| `CityModelTests` | 2 | Model xatti-harakati, CASCADE |
| `AccessibilityTests` | 13 | ARIA, skip-link, jonli hudud, forma xatolari |
| `CountryCrudTests` | 7 | Mamlakat tafsiloti, tahrirlash, o'chirish |
| `ExportTests` | 8 | CSV/Excel tuzilishi va filtrga bo'ysunishi |
| `ApiTests` | 18 | API o'qish/yozish, ruxsatlar, sxema |
| `ErrorPageTests` | 2 | Maxsus 404 sahifasi |

Ishlab chiqarish sozlamalarini tekshirish:

```bash
python manage.py check --deploy
```

---

## 🗄 Ma'lumotlar modeli

**Country** — `name` (unikal), `code` (ISO, ixtiyoriy)

**City** — `name`, `population`, `country` (FK → Country), `is_capital`,
`created_at`, `updated_at`

Bitta mamlakat ichida shahar nomi takrorlanmaydi (`UniqueConstraint`) — bu
qoida ham veb-formada, ham API'da tekshiriladi. Mamlakat o'chirilsa, unga
tegishli shaharlar ham o'chadi (`CASCADE`).

---

## ⚙️ Sozlamalar (`.env`)

`.env.example` faylini `.env` nomi bilan nusxalang. Asosiy kalitlar:

| Kalit | Standart | Izoh |
|---|---|---|
| `DJANGO_SECRET_KEY` | ishlab chiqish kaliti | Production'da albatta o'zgartiring |
| `DJANGO_DEBUG` | `True` | Production'da `False` |
| `DJANGO_ALLOWED_HOSTS` | `localhost,127.0.0.1` | Vergul bilan |
| `DJANGO_HTTPS_ONLY` | `True` | `DEBUG=False` da HTTPS majburiy (SSL redirect + HSTS) |
| `DJANGO_BEHIND_PROXY` | `False` | nginx/Traefik orqasida `True` |

`DEBUG=False` va `DJANGO_HTTPS_ONLY=True` bo'lganda `check --deploy`
hech qanday ogohlantirish bermaydi.

---

## 📁 Fayllar tuzilishi

```
DJango-RETAKE EXAM/
├── cityproject/              # Loyiha sozlamalari
│   ├── settings.py           # .env orqali sozlanadi
│   └── urls.py               # veb + API + Swagger
├── cities/                   # Asosiy ilova
│   ├── management/commands/
│   │   └── seed_cities.py    # Namuna ma'lumotlar
│   ├── migrations/
│   ├── templates/
│   │   ├── base.html         # Skip-link, nav, jonli xabarlar
│   │   └── cities/           # list / detail / form / delete / _field
│   ├── admin.py
│   ├── api.py                # DRF ViewSet'lar
│   ├── forms.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py              # 61 ta test
│   ├── urls.py
│   └── views.py              # Veb view'lar + eksport + xato sahifalari
├── templates/errors/         # 404 / 403 / 500
├── static/
│   ├── css/style.css         # Dizayn tizimi (light + dark)
│   └── js/theme.js           # Rejim almashtirgichi
├── .github/workflows/ci.yml  # Testlar har push'da
├── .env.example
├── Dockerfile
├── DescriptionProject.txt    # Topshiriq matni
├── manage.py
├── requirements.txt
└── README.md
```
