title: Using set -o errexit in bash script
category: Shell
date: 2016-04-30
status: draft

## Unexpected behaviour

**noset-e**:

    #!/bin/bash
    mv input output &> /dev/null
    echo "Append this to the file" >> output

We now look at the output:

    $ ./noset-e
    $ echo $?
    0
    $ cat output
    Append this to the file
    $ echo "This is the input file" > input
    $ ./noset-e
    $ echo $?
    0
    $ cat output
    This is the input file
    Append this to the file

**set-e**:

    #!/bin/bash
    set -o errexit  # or shot set -e
    mv input output &> /dev/null
    echo "Append this to the file" >> output

And again the output:

    $ ./set-e
    $ echo $?
    1
    $ cat output
    cat: output: No such file or directory
    $ echo "This is the input file" > input
    $ ./set-e
    $ echo $?
    0
    $ cat output
    This is the input file
    Append this to the file

## Using traps

    #!/bin/bash

    set -o errexit

    # Create a trap to remove the temporary file he temporary file again
    trap 'rm tmp' EXIT

    # Create a temporary file
    touch tmp

    # Here the script always fail
    false

    echo "This never runs"
