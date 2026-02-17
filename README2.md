# newarcheryscoringcrx

## 001 Installation

```
```

## 002 Site Name, Logo, and Global Colors

```
```

## 003 Adding Basic Pages

```
```

## 004 Navbar

```
```

## Add Content and Custom CSS

```
Part 1
Adding a Hero Unit to the Home Page
```

## 006 Create scoring app

```bash
Part 1
python manage.py startapp scoring
# Create class models.Archer 
Part 2
classes of Archer* created
```

## 007 Scoring app - Part 1 

```
Part 1
Models, snippetview and pages added
templates in scoring\templates\scoring\pages
```

## 007 Scoring app - Part 2

```
Part 2
Models, snippetview and pages added
templates in scoring\templates\scoring\pages
```

## 008 Scoring app templates - Part 1

```
Part 1
Working on page templates
```

## 009 Create app fill_db - Part 1

```
Part 1
Create fill_db
```

```bash
python manage.py startapp fill_db
```

```bash
# Start with
del db.sqlite3
pyclean .
python manage.py makemigrations
python manage.py migrate
python manage.py populate_db
```

## 010 Create app common

```
Not used
```

```bash
# Part 1
python manage.py startapp common
# Part 2
# Working on populate_db.py
```

## 011 Wagtail AI

[https://wagtail-ai.readthedocs.io/latest/]

```bash
Part 1
pip install wagtail-ai
```
 ## 012 Update populate_db.py

```
Work on def create_sample_archers(self):

```

# 013 Working on scoring.admin.py

```
```

```bash
# Working on scoring.admin.py
# Installation of wagtail-flexible-forms 

$ pip install wagtail-flexible-forms

INSTALLED_APPS = [
    ...,
    "wagtail_flexible_forms",
    ...,
]
```

# 014 speadsheetgrid app and working on scoring.admin

```
```

```bash
python manage.py startapp spreadsheet
```

# 015 Install neapolitan

```
```

```bash
pip install neapolitan
```

# 016 CRUD - Read data

```
scoring.views.Archer
```