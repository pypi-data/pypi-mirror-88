# TSQuery

Run [Tree Sitter](https://tree-sitter.github.io) queries from the command line.


# Installation

```shell
pip install tsquery
```

# Usage

Parsers (`.so` files) should be installed somewhere in `$XDG_DATA_HOME` or
`$XDG_DATA_DIRS`. Use the
[official Tree Sitter CLI tool](https://tree-sitter.github.io/tree-sitter/creating-parsers#tool-overview)
to compile a grammar to parser source.

For example, this command prints the names of functions defined in a toy Python
program:

```shell
# Write a toy Python program
cat > example.py <<EOF
def baz():
    return 1

def foo(bar):
    if bar:
        baz()
EOF

# Run a query against it
tsquery '(function_definition name: (identifier) @func.name)' example.py
```

See also `example.sh` in this repository.
