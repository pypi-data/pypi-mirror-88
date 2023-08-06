# latex-dirtree-gen

Python version of the Perl [latex-dirtree-generator](https://github.com/d-koppenhagen/latex-dirtree-generator) by [Danny Koppenhagen](https://github.com/d-koppenhagen).

## Usage

```
usage: latex-dirtree-gen [-h] [-d DEPTH] [--color] directory

positional arguments:
  directory             project root

optional arguments:
  -h, --help            show this help message and exit
  -d DEPTH, --depth DEPTH
                        how many directories should the program descend
  --color               draw directories in red
```

## Examples

```
# use default settings
latex-dirtree-gen .
# set depth to two directores and print directory names in red
latex-dirtree-gen -d 2 --color .
```

Sample output:

```
\dirtree{%
 .1 .
 .2 pdf.
 .3 cover.pdf.
 .2 text.
 .3 01-introduction.tex.
 .3 02-content.tex.
 .3 99-other.tex.
 .3 04-email.tex.
 .2 README.md.
 .2 main.tex.
 .2 main.pdf.
 .2 .gitignore.
}
```

Just a basic dirtree, just as you'd expect.

## Contributing

If you find an error or have an improvement idea, file an issue!
