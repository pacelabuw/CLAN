# CLAN language swapper
Console app for switching default language in chat transcription files for bilingual data analysis.

## Installation steps
- Install [Python](https://www.python.org/) (>=3.10).
- Recommended: Use [conda](https://docs.conda.io/projects/miniconda/en/latest/) or
[venv](https://docs.python.org/3/library/venv.html) to create and activate an environment.
- Run command in terminal:
> pip install -r requirements.txt
- Optional: To run tests in terminal:
> pytest
- You can now run the swapper:
> python cha_swapper.py

## Use
To use, either the installation needs to be complete or you will need a generated executable file.
Then follow steps:
1. Run the swapper, it will create input/ and output/ directories.
2. Add the .cha files that you want to swap. Currently the swapper only supports files that have
two languages, any other number of languages will fail.
3. Run the swapper again, the swapped files will be in the output/ directory.

## Create an executable
This script was intended to be ran as a simple executable for ease of use. Once installation is
complete an executable can be generated by running command:
> pyinstaller -F src/cha_swapper.py

The executable will be available in in the dist/ directory. An executable can only be used with the
same OS it was generated with (ie Windows, Mac, Linux).

## How to cite (APA 7)
Clayton, J. (2024). _CLAN language swapper_ (Version 1.0.3). Pacelab. https://github.com/pacelabuw/CLAN_language_swapper. 
