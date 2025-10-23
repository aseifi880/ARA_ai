import re
from urllib.parse import urlparse


def remove_extra_space(text: str) -> str:
    regex = re.compile(r"[\t\n]+")
    return regex.sub("", text)


def multiline_to_one(text: str) -> str:
    regex = re.compile(r"[\r\n]+")
    return regex.sub("", text)


def get_url_path_with_params(url: str) -> str:
    parsed = urlparse(url)
    return parsed.path + "?" + parsed.query


# def main():


# if __name__ == '__main__':
#     main()
