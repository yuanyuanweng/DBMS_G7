# PickPet

PickPet is a Flask + SQLite stray dog adoption website. Visitors can browse dogs, create an account, save favourites, submit adoption applications, and view application updates. Admin users can review applications and manage dog records.

## Quick Start

### 1. Clone the project

```bash
git clone https://github.com/yuanyuanweng/DBMS_G7.git
cd DBMS_G7
```

### 2. Create and activate an environment

Conda example:

```bash
conda create -n DMBS python=3.12
conda activate DMBS
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the website

```bash
python run.py
```

Open:

```text
http://127.0.0.1:5000/
```

The project already includes a working SQLite database at:

```text
database/pickpet.db
```

## AI Story Generator (IMPORTANT)

Dog detail pages include an AI story generator.

This project uses Ollama locally, so no OpenAI API key or paid API billing is required.

To enable AI story generation:

1. Install Ollama:

```text
https://ollama.com/download
```

2. Pull the model:

```bash
ollama pull llama3.2
```

3. Keep Ollama running, then use the **Generate AI Story** button on a dog detail page.

If Ollama is not available, the app returns a fallback story instead of crashing.

## Test Accounts

Regular user:

```text
Email: user1@test.com
Password: user1
```

Admin/staff:

```text
Email: admin1@test.com
Password: admin1
```

Other seeded users follow the same pattern, for example:

```text
staff1@test.com / staff1
user2@test.com / user2
user7@test.com / user7
```

## Database Notes

Main database files:

```text
database/pickpet.db
database/schema.sql
database/seed.sql
```

The app also runs small startup migrations from:

```text
app/db_migrations.py
```

These keep older local SQLite databases compatible by ensuring needed columns, tables, and views exist.

## Project Structure

```text
app/
  __init__.py              Flask app setup and blueprint registration
  database.py              SQLite connection helper
  db_migrations.py         Startup database compatibility helpers
  main_routes.py           Homepage route
  admin/                   Admin dashboard routes
  ai/                      AI story route and generator
  applications/            Adoption application routes
  auth/                    Login/register/logout routes
  dogs/                    Dog listing/detail/create/edit routes
  models/                  Database access methods
  static/                  CSS, JS, images, uploads
  templates/               Jinja templates

database/
  pickpet.db               Current SQLite database
  schema.sql               Database schema
  seed.sql                 Seed data
```

## Common Pages

```text
/                  Homepage
/find-a-dog/       Dog listing
/find-a-dog/<id>   Dog detail
/login             Login
/register          Register
/my-applications   User application history
/admin/dashboard   Admin dashboard
```