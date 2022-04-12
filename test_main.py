from main import modify_html, modify_string


def test_modify_string():
    s = 'a bb ccc dddd eeeee ffffff ggggggg'
    assert modify_string(s) == s


def test_modify_html():
    s = '<html><body>Hello World</body></html>'
    assert modify_html(s) == s
    s = """<html lang="en">
<head><meta charset="utf-8">
<title>title</title>
<link href="styles.css">
<script src="script.js"></script>
</head>
<body>
<h1>Hello World</h1>
<div>
No 6-character words here: a be cee
comma,
<button>6-character tags are ignored</button>
</div>
</body>
</html>
"""
    assert modify_html(s) == s
