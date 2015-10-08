# Simple tool to render documents based on tilt

## Usage

### Basic Usage

Render documents with tilt. A `yield` in one document trigger the processing of
the next document:

~~~sh
tilt-render outer-template.erb inner-template.slim content.md
~~~

### Context

A YAML file can be used as a context:

~~~sh
tilt-render --data data.yaml outer-template.erb inner-template.slim content.md
~~~
