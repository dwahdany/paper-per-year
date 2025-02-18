# Paper Per Year

A UVX command to visualize an academic author's publications per year using data from Google Scholar.

## Note
Numbers are not everything and number of published papers is certainly no metric for academic success.

## Installation

1. Clone this repository
2. Add the `bin` directory to your PATH or create a symlink to `bin/uvx-paper-per-year` in a directory that's in your PATH

## Usage

```bash
uvx paper-per-year [OPTIONS] AUTHOR_NAME
```

For example:
```bash
# Save plot in current directory with default style
uvx paper-per-year "Adam Dziedzic"

# Save plot in a specific directory with custom style
uvx paper-per-year "Adam Dziedzic" -o ~/Documents/plots --style whitegrid --context poster
```


![Example plot for Adam Dziedzic](Adam_Dziedzic.pdf)



The command will:
1. Search for authors matching the provided name
2. Display a list of found authors with their affiliations
3. Prompt you to select the correct author
4. Generate a beautiful PDF plot showing the number of publications per year
5. Save the plot as `Author_Name.pdf` in the specified directory
6. Output year-count data to stdout for potential piping

### Options

- `-o, --output-dir`: Directory to save the output PDF (default: current directory)
- `--style`: Plot style (choices: darkgrid, whitegrid, dark, white, ticks; default: darkgrid)
- `--context`: Plot scaling context (choices: paper, notebook, talk, poster; default: talk)

### Plot Features

- Beautiful Seaborn-styled visualizations
- Publication counts displayed on top of each bar
- Automatically adjusted layout and spacing
- High-resolution output (300 DPI)
- Multiple style options for different use cases

### Output Format

The command outputs the year-count data to stdout in a tab-separated format:
```
YEAR    COUNT
2020    5
2021    3
2022    7
...
```

This allows for easy piping to other commands, for example:
```bash
# Get total publication count
uvx paper-per-year "Adam Dziedzic" | awk '{sum += $2} END {print sum}'

# Find the most productive year
uvx paper-per-year "Adam Dziedzic" | sort -k2 -nr | head -n1
```

## Requirements

- Python 3.13 or higher
- scholarly
- numpy
- matplotlib
- seaborn
- click
