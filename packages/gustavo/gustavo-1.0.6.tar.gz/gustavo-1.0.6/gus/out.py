import sys
import gus.const as THE


def std_format(status):
    return f'[{status["desc"]}] [{status["code"]}] {status["url"]}'


def json_format(status):
    return '{"url": \'' + status["url"] + '\', "status": ' + str(status["code"]) + "}"


def rtf_format(status):
    color = r"\cf2"  # grey
    if status["desc"] == THE.GOOD:
        color = r"\cf4"  # green
    elif status["desc"] == THE.FAIL:
        color = r"\cf3"  # red
    return f'{color} [{status["code"]}] [{status["desc"]}] {status["url"]}'


# standard output
def to_console(results, output):
    print(results) if output == "json" else print("\n".join(results))


# creates an rtf file and writes results
def to_rtf(results, output):
    try:
        with open("output.rtf", "w") as rtf_file:
            rtf_file.write(THE.RTF + "\\\n".join(results) + "}")
            print("output.rtf is ready")
    except:
        print("error writing list")
        sys.exit(1)
