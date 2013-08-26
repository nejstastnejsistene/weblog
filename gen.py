#!/usr/bin/env python

import os
import markdown
import jinja2


input_dir = 'posts'
output_dir = 'www'


# Create a simple jinja environment and a markdown filter.
loader = jinja2.FileSystemLoader('.')
env = jinja2.Environment(loader=loader)
env.filters['markdown'] = markdown.markdown

# Iterate through all files in the input directory.
for dirpath, dirnames, filenames in os.walk(input_dir):
    for filename in filenames:
        # Calculate the input and output paths.
        input = os.path.join(dirpath, filename)
        output = input.replace(input_dir, output_dir, 1)
        output = os.path.splitext(output)[0] + '.html'

        # Make output directories if they don't already exist.
        dirname = os.path.dirname(output)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        # Render the html and output it.
        with open(output, 'w+') as o:
            o.write(env.get_template(input).render())
