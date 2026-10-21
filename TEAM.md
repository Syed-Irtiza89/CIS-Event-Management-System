# Team guide (read this first)

Project: **CIS Event Management System**

This GitHub repo is for the whole group. One person does not own every file.
Read this page before you clone or edit anything.

---

## Members

Fill your real name and GitHub username in this table (Student 1 already filled).

| Student | Role | GitHub username | What you work on |
|---|---|---|---|
| Student 1 | Database Developer | Syed-Irtiza89 | models, PostgreSQL, migrations, sample data, model tests |
| Student 2 | *(write your name)* | *(github id)* | pages / templates / CSS / student + organizer screens |
| Student 3 | *(write your name)* | *(github id)* | login, register, urls, extra views / API if needed |
| Student 4 | *(write your name)* | *(github id)* | extra tests, report, screenshots, demo notes |

If your group has different roles, only change **your row**. Do not delete Student 1 work.

---

## Who can edit which files

| Path | Who should edit | Notes |
|---|---|---|
| `events/models.py` | Student 1 only | other members IMPORT these models, do not rewrite them |
| `events/migrations/` | Student 1 only | if you need a new column, ask Student 1 |
| `events/admin.py` | Student 1 (small changes ok) | |
| `events/tests.py` | Student 1 | others can add their own test files |
| `events/management/commands/load_sample_data.py` | Student 1 | |
| `cis_project/settings.py` | ask first | you may add your app name in `INSTALLED_APPS` |
| `cis_project/urls.py` | frontend / backend students | add `include()` for your app, do not remove `admin/` |
| `events/views.py` | currently empty | you can use it OR make a new app |
| new folder like `pages/` or `accounts/` | other students | this is the safe way |

**Rule:** do not delete another student’s files. If GitHub shows a conflict, talk in the group chat first.

---

## How teammates join this repo

Repo owner (Student 1) must invite you:

1. Open the GitHub repo
2. **Settings** → **Collaborators** → **Add people**
3. Type the member GitHub username
4. Member checks email / GitHub notifications and **Accepts**

After accept, clone the repo (steps in README).

---

## Git rules (so we do not overwrite each other)

1. Never work directly on `main` for a big feature (if you already did a small fix, tell the group).
2. Make your own branch:

```text
student2-frontend
student3-auth
student4-testing
```

3. Before you start work:

```text
git checkout main
git pull
git checkout -b your-branch-name
```

4. After you finish:

```text
git add .
git commit -m "short message of what you did"
git push -u origin your-branch-name
```

5. On GitHub open a **Pull Request** into `main`.
6. At least one other member should look at the PR before merge.

Do **not** use `git push --force` on `main`.

Do **not** commit these files:

- `venv/`
- `.env`  (this has your own PostgreSQL password)
- `__pycache__/`

---

## How other students use the database

Do not create a second Event table. Use the models that are already here.

```python
from django.contrib.auth.models import User
from events.models import UserProfile, Event, Registration
```

Roles:

- `request.user.profile.role == "student"`
- `request.user.profile.role == "organizer"`

Register a student for an event:

```python
from django.core.exceptions import ValidationError

try:
    Registration.objects.create(event=event, student=request.user)
except ValidationError as e:
    # show this error on the page
    print(e)
```

Useful helpers already on Event:

- `event.registered_count()`
- `event.seats_left()`
- `event.is_full()`
- `event.registrations.all()`
- `request.user.organized_events.all()`

Sample login after `python manage.py load_sample_data`:

- password for all sample users: `password123`
- organizers: `organizer1`, `organizer2`
- students: `ali`, `sara`, `hamza`, `ayesha`

---

## If you need a new database field

Example: you want `event.poster` or `profile.semester`.

1. Write in the group chat what field you need
2. Student 1 adds it in `events/models.py`
3. Student 1 runs `makemigrations` / `migrate`
4. Then you use the new field

If two people change `models.py` at the same time, migrations will break.

---

## Suggested work split

**Student 1 (done in this repo)**

- entities and ER diagram
- Django models + constraints
- PostgreSQL settings
- sample data command
- model tests

**Student 2 (frontend)**

- home page, event list, event detail
- registration button for students
- organizer event form (create/edit event)

**Student 3 (auth / extra backend)**

- signup + login pages (Django auth)
- logout
- connect urls to views
- permission: student vs organizer

**Student 4 (testing / report)**

- test the pages
- screenshots for the report
- write how to run the full system

You can change this split if your teacher gave different roles. Just update the table at the top.
