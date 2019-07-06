# Check keywords in websites' homepage and subpage

The script checks wether keywords are available in the website and its subpage or not, and output to a `.csv` file.

The script requires chromedriver to crawl websites using ajax request.

*  The website urls are set in `./data/check_list.csv`
*  The keywords are set in the variable KEY_WORDS in the script

Sample output: `./data/sample_output.csv`

## Env
* Python 3.7.3
* MacOS: using other OSs requires setup another `chromedriver`

## Setup
Download and configure [chromedriver](https://sites.google.com/a/chromium.org/chromedriver/home)

```
make setup
```

## Run
```
make run
```
