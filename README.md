weblog
======

What will hopefully soon be Mike and Peter's shared blog.

## Current Usage

* Setup `virtualenv` and install dependencies.
```
$ virtualenv env
$ source env/bin/activate
$ pip install -r requirements.txt
```

* Write markdown files in `posts/`, and then run `./gen.py` to compile to HTML.
* Run some webserver from the `www/` directory.
```
$ cd www
$ python -m SimpleHTTPServer
```
