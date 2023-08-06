# latex-todo-gen

Extract all TODOs and FIXMEs from LaTeX project.

## Usage

```
-h, --help                Show this help message and exit
--outfile OUTFILE
-o OUTFILE                Output file.
                          Supported extensions: md, tex, pdf.
                          Default: TODO.md
--directories DIRECTORIES
-d DIRECTORIES            Comma separated list of directories.
                          Default: text
--files FILES
-f FILES                  Comma separated list of files.
                          Defaults to none.
--keywords KEYWORDS
-k KEYWORDS               Comma separated list of keywords.
                          Default: FIXME,TODO,NOTE
--scheme SCHEME           Color scheme for output PDF file.
                          Options: light, plain, mariana, marianne, dark.
                          Default: light
--description DESCRIPTION Set output file description.
                          Default: Statistics for this LaTeX project.
--footer FOOTER           Set file footer.
                          Defaults to link to this project.
```

Multiple output files supported:

- Markdown (`.md`). This is a default.
- LaTeX (`.tex`).
- PDF (`.pdf`). Generates `.tex` file and converts it using the `latex` package.

Several color schemes for output PDF are supported (see [Gitlab docs page](https://gitlab.com/matyashorky/latex-todo-gen/-/blob/main/docs/schemes.md)).

## Examples
```bash
# Use default settings
latex-todo-gen

# Set custom keywords
latex-todo-gen -k "REVIEW,FIXME,TODO,NOTE"

# Set description and output file as PDF
latex-todo-gen --description "This file is generated on every commit." -o "WIP.pdf"

# Set source directories and one main file
latex-todo-gen -d "src,settings" -f "main.tex"

# Set color scheme for output PDF
latex-todo-gen -o "TODO.pdf" --scheme marianne
```

## Limitations

LaTeX sometimes fails when it tries to render a UTF-8 character it doesn't know. The `\lstset` in the template tries to encode most of diacritics for european alphabets, as well as some of the common characters. If you encounter an error, let me know via issues.

## Contributing

**PRs are welcome.** I'm currently looking for:

- pre-commit: I haven't been able to make it work, it seemed not to be able to locate the python script.
- Load setup from config file. Maybe `.todo-gen.yaml`?
- Universal TODO generator. This has proven to be much more universal program: you can just swap latex' `%` with python's `#` and you've got python-todo-gen. I'm probably migrate it sometime, but for now, it's just latex.
- Multiple lines below the keyword: `# TODO3` would append three lines instead of one
