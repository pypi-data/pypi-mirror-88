VERSION = "***** Get-Url-Status (GUS) Text-As-Visual-Output (TAVO) ***** version 0.1.6"

# all urls starting with http:// or https:// including leading char in case url is nested
ALL_URLS_REGEX = r".?http[s]?://[a-zA-Z0-9- _.~!*\'();:@&=+$,/?%#[\]]+."
IGNORE_URLS_REGEX = r"^https?://.*[^\s/]"  # line starts with http:// or https://
COMMENTS_REGEX = r"^#.*"  # line starts with #
DOMAIN_REGEX = r"(?<!/|:)/"

NESTED = {"(": ")", "[": "]", ">": "<", '"': '"'}

OUTPUT = "std"
RTF = """{\\rtf1\\ansi\\ansicpg1252\\cocoartf2513\\cocoatextscaling0\\cocoaplatform0{\\fonttbl\\f0\\fswiss\\fcharset0 Helvetica;}
{\\colortbl;\\red255\\green255\\blue255;\\red87\\green87\\blue87;\\red252\\green41\\blue19;\\red159\\green242\\blue92;}
{\\*\\expandedcolortbl;;\\cssrgb\\c41531\\c41531\\c41531;\\cssrgb\\c100000\\c25745\\c7993;\\cssrgb\\c67668\\c94348\\c43431;}
\\cf0"""

GOOD = "GOOD"
FAIL = "FAIL"
UNKN = "UNKN"
ALL = [GOOD, FAIL, UNKN]
