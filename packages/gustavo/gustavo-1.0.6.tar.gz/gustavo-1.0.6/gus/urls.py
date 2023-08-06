import sys
import concurrent.futures
import re
import requests
import gus.const as THE
import gus.out as out

from progress.spinner import Spinner

# open file and return list of regex matches
def get_list(sourcefile, ignorefile):
    try:
        if sourcefile == "TELESCOPE":
            posts = requests.get("http://localhost:3000/posts")
            urls = re.findall("/posts/[a-zA-Z0-9]{10}", posts.text)
            return ["http://localhost:3000" + url for url in urls]
        else:
            with open(sourcefile) as src:
                found = re.findall(THE.ALL_URLS_REGEX, src.read())
            return strip_ignored(found, ignorefile)
    except:
        print(f"error opening {sourcefile}")
        sys.exit(1)


# check if url is nested; add url to list if domain not on ignore list; return list
def strip_ignored(raw_list, ignorefile):
    ignore_list = get_ignore_list(ignorefile)
    clean_list = []
    for string in raw_list:
        url = check_nested(string)
        domain = re.split(THE.DOMAIN_REGEX, url)[0]
        if domain not in ignore_list:
            clean_list.append(url)
    return clean_list


# open ignore file and return list of domains to ignore
def get_ignore_list(ignorefile):
    try:
        if ignorefile:
            with open(ignorefile) as src:
                text = src.read()
                found = re.findall(THE.IGNORE_URLS_REGEX, text, flags=re.MULTILINE)
                comment = re.search(THE.COMMENTS_REGEX, text, flags=re.MULTILINE)
            return found if comment or found else sys.exit(1)
        return []
    except:
        print(f"error with ignore file: {ignorefile}")
        sys.exit(1)


# checks first and last character against nested dictionary
def check_nested(string):
    first = string[0]
    last = string[-1]
    if first in THE.NESTED and THE.NESTED.get(first) == last:
        string = string[1:-1]
    return string


# request header and return HTTP response code and description
def get_status(url):
    try:
        conn = requests.head(url, timeout=2.5)
        code = conn.status_code
        series = str(code)[0]
        desc = THE.UNKN
        if series == "2":
            desc = THE.GOOD
        elif series == "4":
            desc = THE.FAIL
    except:  # all exceptions default to status == 400
        code = 400
        desc = THE.FAIL
    finally:
        return {"url": url, "code": code, "desc": desc}


# checks if string is nested; gets status code and decscription; applies desired format; returns processed list
def process_list(urlist, wanted, output):
    processed = []
    formatted = (
        out.rtf_format
        if output == "rtf"
        else out.json_format
        if output == "json"
        else out.std_format
    )
    spinner = Spinner("Checking URLs ")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = [executor.submit(get_status, url) for url in urlist]
        for connection in concurrent.futures.as_completed(results):
            status = connection.result()
            if status["desc"] in wanted:
                processed.append(formatted(status))
            spinner.next()
    spinner.writeln("\033[F")  # move cursor to the beginning of previous line
    spinner.finish()
    return processed
