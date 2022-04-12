from main import modify_html, modify_string


def test_modify_string():
    s = 'a bb ccc dddd eeeee ffffff™ ggggggg'
    assert modify_string(s) == s
    assert modify_string('6-character, 6-letter, 6-char') == '6-character, 6-letter, 6-char™'


def test_modify_html_no_change():
    s = '<html><body>Hello World</body></html>'
    assert modify_html(s) == s
    s = """<html lang="en">
<head><meta charset="utf-8">
<title>title</title>
<link href="styles.css">
<script src="script.js">script</script>
</head>
<body>
<h1>Hello World</h1>
<div>
No 6-letter words here: a be cee
comma,
<button>6-character tags are ignored</button>
</div>
</body>
</html>
"""
    assert modify_html(s) == s


def test_modify_html_change():
    s = '<html><body>Hello World</body></html>'
    assert modify_html('<html><body>Hello World2!</body></html>') == '<html><body>Hello World2&trade;!</body></html>'
    assert modify_html("""<html lang="en">
<head><meta charset="utf-8">
<title>title2</title>
<link href="styles.css">
<script src="script.js">script</script>
</head>
<body>
<h1>Hello World2</h1>
<div>
Some 6 letter words are here: kitten, master
<button>6-char tags are ignored</button>
</div>
</body>
</html>
""") == """<html lang="en">
<head><meta charset="utf-8">
<title>title2</title>
<link href="styles.css">
<script src="script.js">script</script>
</head>
<body>
<h1>Hello World2&trade;</h1>
<div>
Some 6 letter&trade; words are here: kitten&trade;, master&trade;
<button>6-char&trade; tags are ignored</button>
</div>
</body>
</html>
"""
