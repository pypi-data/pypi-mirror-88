# Convert LG QuickMemo+ files into single, text-only JSON file

[![Workflow](https://github.com/movecodemove/convert-lqm-to-json/workflows/.github/workflows/workflow.yml/badge.svg)](https://github.com/movecodemove/convert-lqm-to-json/actions)

## Installation
`$ pip install [--user] convert-lqm-to-json`

## Usage
`$ convert-lqm-to-json [-h] [-o [<...>]] [-v] [<source1>] ... [<sourceN>]`

#### Arguments

    <source>                Paths or glob patterns for resolving .lqm files;
                            defaults to current directory.

#### Options

    -o  (--output-dir)      Output directory; defaults to current directory.
    -h  (--help)            Print help message.
    -v  (--version)         Print application version.
