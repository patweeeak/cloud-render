# Recipe Asset Manager

A production-ready Photo Album Management web application built with Django, featuring Role-Based Access Control (RBAC), Cloudinary media storage, and PostgreSQL database — deployed on Render.

🌐 **Live App:** [cloud-render-dep5.onrender.com](https://cloud-render-dep5.onrender.com)
📁 **Repository:** [github.com/patweeeak/cloud-render](https://github.com/patweeeak/cloud-render)

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Role-Based Access Control](#role-based-access-control)
- [Project Structure](#project-structure)
- [Local Development Setup](#local-development-setup)
- [Environment Variables](#environment-variables)
- [Deployment to Render](#deployment-to-render)
- [Cloudinary Integration](#cloudinary-integration)
- [Screenshots](#screenshots)

---

## Overview

Recipe Asset Manager is an enterprise-grade image gallery application that allows users to upload, manage, and browse recipe photos. It enforces strict role-based permissions — separating standard users from album administrators — and stores all media securely on Cloudinary's CDN.

---

## Features

- 🔐 User authentication (login, logout, registration)
- 👥 Role-Based Access Control (standard user vs. album admin)
- 🖼️ Image upload and storage via Cloudinary
- ✏️ Full CRUD operations on photos (admin only for edit/delete)
- 🔍 Search and pagination
- ☁️ PostgreSQL database via Render
- 🚀 Production deployment on Render with environment-secured credentials

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | Django 6.x (Python) |
| Database | PostgreSQL (Render managed) |
| Media Storage | Cloudinary |
| Static Files | WhiteNoise |
| Deployment | Render |
| Auth | Django built-in authentication |

---

## Role-Based Access Control

The application enforces two distinct roles using Django's native authentication system:

| Permission | Standard User | Album Admin (Staff/Superuser) |
|---|---|---|
| View gallery | ✅ | ✅ |
| Upload photos | ✅ | ✅ |
| Search photos | ✅ | ✅ |
| Edit photos | ❌ | ✅ |
| Delete photos | ❌ | ✅ |
| Access Django admin | ❌ | ✅ |

**Standard users** are regular authenticated accounts with no staff privileges.

**Album admins** are accounts with `is_staff=True` or `is_superuser=True`, set via the Django admin panel at `/admin`.

---

## Project Structure

```
cloud-render/
├── gallery/
│   ├── migrations/
│   │   ├── 0001_initial.py
│   │   └── 0002_alter_recipephoto_image.py
│   ├── templates/
│   │   ├── gallery/
│   │   │   ├── delete.html
│   │   │   ├── edit.html
│   │   │   └── home.html
│   │   └── registration/
│   │       └── login.html
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── rbac.py
│   ├── urls.py
│   └── views.py
├── recipe_project/
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── .env
├── .gitignore
├── manage.py
├── README.md
└── requirements.txt
```

---

## Local Development Setup

### Prerequisites
- Python 3.10+
- Git

### Steps

**1. Clone the repository**
```bash
git clone https://github.com/patweeeak/cloud-render.git
cd cloud-render
```

**2. Create and activate a virtual environment**
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Create a `.env` file** in the project root (see [Environment Variables](#environment-variables) below)

**5. Run migrations**
```bash
python manage.py migrate
```

**6. Create a superuser**
```bash
python manage.py createsuperuser
```

**7. Start the development server**
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000`

---

## Environment Variables

Create a `.env` file in the project root. **Never commit this file.**

```env
SECRET_KEY=your-long-random-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

# Leave blank to use SQLite locally
# DATABASE_URL=postgresql://...

DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=yourpassword
```

> For production on Render, `DATABASE_URL` must be set to the **Internal Database URL** from your Render PostgreSQL service.

---

## Deployment to Render

### 1. Push to GitHub
```bash
git add .
git commit -m "deploy"
git push
```

### 2. Create PostgreSQL on Render
Render Dashboard → **New +** → **PostgreSQL** → Free plan → Create

### 3. Create Web Service on Render
Render Dashboard → **New +** → **Web Service** → Connect GitHub repo

| Setting | Value |
|---|---|
| Runtime | Python 3 |
| Build Command | `pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate` |
| Start Command | `gunicorn recipe_project.wsgi:application` |

### 4. Set Environment Variables on Render

| Key | Value |
|---|---|
| `SECRET_KEY` | Generate a strong random string |
| `DATABASE_URL` | Internal Database URL from Render PostgreSQL |
| `CLOUDINARY_CLOUD_NAME` | From Cloudinary dashboard |
| `CLOUDINARY_API_KEY` | From Cloudinary dashboard |
| `CLOUDINARY_API_SECRET` | From Cloudinary dashboard |
| `DEBUG` | `False` |
| `RENDER_EXTERNAL_HOSTNAME` | `cloud-render-dep5.onrender.com` |

### 5. Create superuser on production
Render → cloud-render → **Shell**:
```bash
python manage.py createsuperuser
```

---

## Cloudinary Integration

All uploaded images are stored on [Cloudinary](https://cloudinary.com) — not on the local filesystem. This is enforced in production via:

```python
# settings.py
STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    ...
}
```

Cloudinary credentials are loaded exclusively from environment variables and are never hardcoded in the repository.

When a photo is deleted, the application also calls `cloudinary_uploader.destroy()` to remove the image from Cloudinary storage — ensuring no orphaned files remain.

---

## Screenshots

<img width="1363" height="646" alt="image" src="https://github.com/user-attachments/assets/93f93e66-0c87-422a-aeb8-2784923ef75b" />

<img width="1362" height="643" alt="image" src="https://github.com/user-attachments/assets/cfae9be5-a89b-4d41-8aa0-566b55772c0e" />

<img width="1364" height="647" alt="image" src="https://github.com/user-attachments/assets/b9fdb33a-3a67-4c34-8ad0-a32dabc8fd6a" />


---

## License

This project was developed as an academic requirement for **MSIT 213** at Eastern Visayas State University (EVSU).
