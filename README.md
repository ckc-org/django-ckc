django-ckc [<img src="https://ckcollab.com/assets/images/badges/badge.svg" alt="CKC" height="20">](https://ckcollab.com)
==========
tools, utilities, etc. we use across projects @ [ckc](https://ckcollab.com)


## installing

```bash
pip install django-ckc
```

```python
# settings.py
INSTALLED_APPS = (
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
    # ... add ckc
    "ckc",
)
```

## distributing

```bash
# change version in setup.cfg
$ ./setup.py sdist
$ twine upload dist/*
```
