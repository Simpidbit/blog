def combine_multi_space(s) -> str:
    news = s.replace('  ', ' ')
    while news != s:
        s = news
        news = s.replace('  ', ' ')
    return news


if __name__ == '__main__':
    s = "hello   world  aaa awef j    ao"
    print(s)
    print(combine_multi_space(s))
