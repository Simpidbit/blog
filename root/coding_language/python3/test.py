import markdown

with open(".\\Python3.10_match_case.md", "rt") as f:
    md = f.read()

print(markdown.markdown(md))
