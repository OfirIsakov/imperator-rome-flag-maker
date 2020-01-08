# Imperator: Rome - Flag Maker
Flag maker for the game `Imperator: Rome`

Feel free to pull request anything you want.


## Usage
Run `python3 main.py` in the cmd.

Flags will get generated based on the `countries.txt` file and will be outputed into the 'flags' folder


### If theres an update to the game:
* Copy the file from: `ImperatorRome/game/common/coat_of_arms/coat_of_arms/00_pre_scripted_countries.txt` and rename it to: `countries.txt`.
* Copy the file from: `ImperatorRome/game/common/named_colors/default_colors.txt` and rename it to: `colors.txt`.
* Copy the file from: `ImperatorRome/game/localization/english/countries_l_english.yml` and rename it to: `names.yml`.
* Copy the 3 folders from: `ImperatorRome/game/gfx/coat_of_arms`.
* Run `main.py` again.

### TODO
- [ ] Add color change to the Emblem object in `emblem.py`.
