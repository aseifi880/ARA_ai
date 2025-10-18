import re


def remove_extra_space(text: str) -> str:
    regex = re.compile(r'[\t\n]+')
    return regex.sub('', text)


# def main():


# if __name__ == '__main__':
#     main()
