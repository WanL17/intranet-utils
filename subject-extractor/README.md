# subject-extractor

Extract all subjects from a module

## Usage

> The program will probably run slowly for modules with lots of projects inside.
> That is expected as to not put too much charge on the servers.

```sh
uv run main.py --help
```

Extract subjects from `G-CPE-100` from `LYN-1`:

```sh
uv run main.py --module G-CPE-100 --city LYN-1
```

Extract subjects to a certain folder:

```sh
uv run main.py --module G-CPE-100 --city LYN-1 --files-dir cool-files
```
