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
            json.dump(self, f, indent=4, sort_keys=True,
                               separators=(', ', ': '))


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
            input = os.path.join(dirpath, filename)

            # Create a DB entry for new posts.
            if input not in db:
                db[input] = { 'created': int(time.time())
                            , 'edited': None
                            , 'edits': []
                            }

            # Render the template into a module, and determine output path.
            namespace = db[input]
            module = env.get_template(input).make_module(namespace)

            # Use explicitly declared url, or else use the input's file name.
            url = getattr(module, 'url', None)
            if url is None:
                url = os.path.basename(input)
                url = os.path.splitext(url)[0] + '.html'
            output = os.path.join(output_dir, url)

            # Handle renamed output files.
            old_output = db[input].get('output')
            if output != old_output:
                db[input]['output'] = output
                if old_output is not None:
                    # Write a redirect file to the old file name.
                    with open(old_output, 'w+') as f:
                        t = env.get_template('redirect.html')
                        f.write(t.render(url=url))
                    db[input]['edited'] = int(time.time())
                    mesg = "Changed url to '{}'".format(url)
                    db[input]['edits'].append(mesg)

            # Make output directories if they don't already exist.
            dirname = os.path.dirname(output)
            if not os.path.exists(dirname):
                os.makedirs(dirname)

            # Write the html to the output file.
            with open(output, 'w+') as f:
                f.write(unicode(module).lstrip())
