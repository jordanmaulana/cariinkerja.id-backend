# Django Admin Starter Pack

Launch tons of mobile apps, web apps, n8n workflows powered by Django.
Everything is quickly set up using Django. A lot of things are worry free.
Your AI copilots perform well too with much less context to do the executions.

## Initial features

- Initial standard features: auth, forgot password, edit profile.
- Dashboard: including paginations and template-ready to append.

## Todo

- [ ] Change the `SECRET-KEY` in `core/settings.py`
- [ ] Setup database config in `core/settings.py`

## How to setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requiremnets.txt
source ./bin/install-tailwind.sh
```

## How to run

```bash
npm run tw
./manage.py runserver
```

## URL

Admin panel
http://localhost:8000/admin

API Docs
http://localhost:8000/swagger/
or
http://localhost:8000/redoc/

## Cheatsheet

Create new apps

```bash
cd apps/
../manage.py startapp product
```

Run server

```bash
./manage.py runserver
```

Run tailwind

```bash
npm run tw
```
