# mkdocs-nav-includer-plugin
MkDocs plugin that improve nav management

## Tutorial

- Install `nav-includer`:
  ```
  pip install mkdocs-nav-includer-plugin
  ```
- Add `navincluder` to your plugin list in the `mkdocs.yml` file
- Add Yaml file in the `docs/` folder
- Include it with `@include folders/nav.yml` in nav

## example

`mkdocs.yml:`
```yaml
plugins:
  - navincluder:
      include_regex: "@include (?P<path>.*)"  # OPTIONAL parameter to give the regex that match include
      relative_path: True  # OPTIONAL parameter to specificy if markdown file path in included yaml should be relative or not

nav:
  - Index: index.md
  - Hello:
    - index: index.md
  - Services:
    - "HelloWorld": "@include included/nav.yml"
```

`docs/included/nav.yml`:
```yaml
- index: index.md
- "Foo":
  - Bar 1: foo/bar1.md
  - Bar 2: foo/bar2.md
```
