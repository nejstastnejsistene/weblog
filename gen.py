#!/usr/bin/env python

import datetime
import os
import time
import markdown
import jinja2
import json


input_dir = 'posts'
output_dir = 'www'


class WeblogDB(dict):
    '''Simple JSON database for storing information about blog posts.'''

    def __init__(self, file='weblog.json'):
        self.file = file
        try:
            with open(self.file) as f:
                dict.__init__(self, json.load(f))
        except (IOError, ValueError):
            dict.__init__(self)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        with open(self.file, 'w+') as f:
            json.dump(self, f, indent=4, separators=(', ', ': '))


# Create a simple jinja environment.
loader = jinja2.FileSystemLoader('.')
env = jinja2.Environment(loader=loader)

# Some custom jinja filters.
def formatdate(x, fmt='%c'):
    return datetime.datetime.fromtimestamp(x).strftime(fmt)
env.filters['markdown'] = markdown.markdown
env.filters['formatdate'] = formatdate

with WeblogDB() as db:
    # Iterate through all files in the input directory.
    for dirpath, dirnames, filenames in os.walk(input_dir):
        for filename in filenames:
            # Calculate the input and output paths.
            input = os.path.join(dirpath, filename)
            output = input.replace(input_dir, output_dir, 1)
            output = os.path.splitext(output)[0] + '.html'

            # Create a DB entry for new posts.
            if output not in db:
                db[output] = { 'created': int(time.time())
                             , 'edited': None
                             }
            namespace = db[output]

            # Make output directories if they don't already exist.
            dirname = os.path.dirname(output)
            if not os.path.exists(dirname):
                os.makedirs(dirname)

            # Render the html and output it.
            with open(output, 'w+') as f:
                f.write(env.get_template(input).render(**namespace))
