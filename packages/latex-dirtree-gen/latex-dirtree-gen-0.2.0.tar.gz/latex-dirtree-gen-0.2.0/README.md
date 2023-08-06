# latex-dirtree-gen

Python version of the Perl [latex-dirtree-generator](https://github.com/d-koppenhagen/latex-dirtree-generator) by [Danny Koppenhagen](https://github.com/d-koppenhagen).

## Usage

```
usage: latex-dirtree-gen [-h] [-v] [-d DEPTH] [--color] [--dots] directory

positional arguments:
  directory               project root

optional arguments:
  -h, --help              show this help message and exit
  -v, --version           show program's version number and exit
  -d DEPTH, --depth DEPTH how many directories should the program descend
                          (default: 5)
  --color                 draw directories in red
                          (default: False)
  --dots                  add dots inside of folders that have not been visited
                          (default: False)
```

## Examples

Default settings

```
$ latex-dirtree-gen .
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

Depth of one and red directory names

```
$ latex-dirtree-gen -d 1 --color .
\dirtree{%
 .1 .
 .2 pdf.
 .3 cover.pdf.
 .2 text.
 .2 README.md.
 .2 main.tex.
 .2 main.pdf.
 .2 .gitignore.
}
```

Depth of one and visible unvisited directories

```
$ latex-dirtree-gen -d 1 --dots .
\dirtree{%
 .1 .
 .2 pdf.
 .3 cover.pdf.
 .2 text.
 .3 \dots.
 .2 README.md.
 .2 main.tex.
 .2 main.pdf.
 .2 .gitignore.
}
```


## Contributing

If you find an error or have an improvement idea, file an issue!
