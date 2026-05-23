# TODO - Photo Album Management (CBVs + RBAC + Cloudinary + Render-ready)

## Plan (edit + implementation steps)

1. **Introduce authentication & RBAC**
   - Pending implementation
2. **Convert function-based views to Class-Based Views (CBVs)**
   - Pending implementation
   - Add role model/flags
   - Add login requirement to all CRUD views.
   - Standard users can upload/create and edit their own items (if required) or have limited permissions; album admins can edit/delete any.
   - Add permission checks using Django native auth (`@login_required`, `UserPassesTestMixin`, `PermissionRequiredMixin`, or group-based checks).

3. **Convert function-based views to Class-Based Views (CBVs)**
   - Replace `gallery_view`, `edit_recipe`, `delete_recipe` with CBVs.
   - Implement:
     - List/Search + Pagination (ListView-like)
     - Create (CreateView)
     - Update (UpdateView)
     - Delete (DeleteView) with Cloudinary permanent deletion.

4. **Update URL routing**
   - Wire CBVs in `gallery/urls.py`.

5. **Update templates to match CBV endpoints**
   - Ensure forms submit to CBV create/update.
   - Ensure delete confirmation posts to CBV delete.

6. **Ensure Cloudinary is the only media backend in production**
   - Keep `CloudinaryField` for stored images.
   - Remove/disable local media serving expectations in production.
   - Avoid adding `static(settings.MEDIA_URL, ...)` unless DEBUG.

7. **Production-safe settings**
   - In `recipe_project/settings.py`:
     - Use env vars for `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`.
     - Remove hardcoded `DEBUG=True` and `ALLOWED_HOSTS=['*']`.
     - Configure database using `DATABASE_URL` (PostgreSQL) via `dj_database_url`.
     - Add typical security middleware settings as needed for production.

8. **Deployment readiness for Render**
   - Ensure `requirements.txt` and settings align.
   - Confirm `build.sh`/gunicorn usage if present.

## Test/Verification

- Run migrations locally.
- Run Django tests/smoke test:
  - Login + create photo
  - Search + pagination
  - Edit/update with RBAC
  - Delete with Cloudinary destroy
