from main import modify_html, modify_string, modify_href


def test_modify_href():
    assert modify_href("//example.com", "example.com") == ""
    assert modify_href("https://example.com/foo/bar?a=1&b=xyz#frag", "example.com") == "/foo/bar?a=1&b=xyz#frag"
    assert modify_href("//subdomain.example.com", "example.com") == "//subdomain.example.com"
    assert modify_href("https://example.com/foo/bing.com", "bing.com") == \
           "https://example.com/foo/bing.com"


def test_modify_string():
    assert modify_string('a bb ccc dddd eeeee ffffff ggggggg') == 'a bb ccc dddd eeeee ffffff™ ggggggg'
    assert modify_string('6-character, 6-letter, 6-char') == '6-character, 6-letter, 6-char™'


def test_modify_string_missing_tm():
    assert modify_string(' пришёл. (I came.)') == ' пришёл™. (I came.)'


def test_modify_string_extra_tm():
    assert modify_string("Not sure if you'd like an advice or merely sharing your experience, \
but after reading your comment I spent an hour or so trying to provide a simple rule of thumb. To my \
surprise, I failed miserably. But I scraped some info together in the process, so I'll post it in a hope \
that it might give you a better™ perspective. Mind you, I'm not a linguist or a teacher.") \
           == "Not sure if you'd like an advice™ or merely™ sharing your experience, \
but after reading your comment I spent an hour or so trying™ to provide a simple™ rule of thumb. To my \
surprise, I failed™ miserably. But I scraped some info together in the process, so I'll post it in a hope \
that it might give you a better™ perspective. Mind you, I'm not a linguist or a teacher."


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
