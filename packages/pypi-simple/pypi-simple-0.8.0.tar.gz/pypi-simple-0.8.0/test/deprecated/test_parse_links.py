import pytest
from   pypi_simple import parse_links

def test_basic():
    with pytest.warns(DeprecationWarning):
        links = list(parse_links('''
            <html>
            <head><title>Basic test</title></head>
            <body>
            <a href="one.html">link1</a>
            <a href="two.html">link-two</a>
            <span href="zero.html">not-a-link</span>
            </body>
            </html>
        '''))
    assert links == [
        ('link1', 'one.html', {'href': 'one.html'}),
        ('link-two', 'two.html', {'href': 'two.html'}),
    ]

def test_base_url():
    with pytest.warns(DeprecationWarning):
        links = list(parse_links('''
            <html>
            <head><title>Test with base_url</title></head>
            <body>
            <a href="one.html">link1</a>
            <a href="two.html">link-two</a>
            <span href="zero.html">not-a-link</span>
            </body>
            </html>
        ''', base_url='https://test.nil/base/'))
    assert links == [
        ('link1', 'https://test.nil/base/one.html', {'href': 'one.html'}),
        ('link-two', 'https://test.nil/base/two.html', {'href': 'two.html'}),
    ]

def test_base_tag():
    with pytest.warns(DeprecationWarning):
        links = list(parse_links('''
            <html>
            <head>
                <title>Test with &lt;base&gt; tag</title>
                <base href="https://nil.test/path/"/>
            </head>
            <body>
            <a href="one.html">link1</a>
            <a href="two.html">link-two</a>
            <span href="zero.html">not-a-link</span>
            </body>
            </html>
        '''))
    assert links == [
        ('link1', 'https://nil.test/path/one.html', {'href': 'one.html'}),
        ('link-two', 'https://nil.test/path/two.html', {'href': 'two.html'}),
    ]

def test_target_base_tag():
    with pytest.warns(DeprecationWarning):
        links = list(parse_links('''
            <html>
            <head>
                <title>Test with &lt;base&gt; tag</title>
                <base target="_new"/>
            </head>
            <body>
            <a href="one.html">link1</a>
            <a href="two.html">link-two</a>
            <span href="zero.html">not-a-link</span>
            </body>
            </html>
        '''))
    assert links == [
        ('link1', 'one.html', {'href': 'one.html'}),
        ('link-two', 'two.html', {'href': 'two.html'}),
    ]

def test_bare_base_and_href_base_tag():
    with pytest.warns(DeprecationWarning):
        links = list(parse_links('''
            <html>
            <head>
                <title>Test with &lt;base&gt; tag</title>
                <base/>
                <base href="https://nil.test/path/"/>
            </head>
            <body>
            <a href="one.html">link1</a>
            <a href="two.html">link-two</a>
            <span href="zero.html">not-a-link</span>
            </body>
            </html>
        '''))
    assert links == [
        ('link1', 'https://nil.test/path/one.html', {'href': 'one.html'}),
        ('link-two', 'https://nil.test/path/two.html', {'href': 'two.html'}),
    ]

def test_many_base_tags():
    # I'm not sure if this is how HTML is supposed to work, but it is how pip
    # works: <https://git.io/fAVZF>
    with pytest.warns(DeprecationWarning):
        links = list(parse_links('''
            <html>
            <head>
                <title>Test with &lt;base&gt; tag</title>
                <base href="https://nil.test/path/"/>
                <base href="https://example.invalid/subdir/"/>
            </head>
            <body>
            <a href="one.html">link1</a>
            <a href="two.html">link-two</a>
            <span href="zero.html">not-a-link</span>
            </body>
            </html>
        '''))
    assert links == [
        ('link1', 'https://nil.test/path/one.html', {'href': 'one.html'}),
        ('link-two', 'https://nil.test/path/two.html', {'href': 'two.html'}),
    ]

def test_base_url_and_absolute_base_tag():
    with pytest.warns(DeprecationWarning):
        links = list(parse_links('''
            <html>
            <head>
                <title>Test with both base_url and an absolute &lt;base&gt; tag</title>
                <base href="https://nil.test/path/"/>
            </head>
            <body>
            <a href="one.html">link1</a>
            <a href="two.html">link-two</a>
            <span href="zero.html">not-a-link</span>
            </body>
            </html>
        ''', base_url='https://test.nil/base/'))
    assert links == [
        ('link1', 'https://nil.test/path/one.html', {'href': 'one.html'}),
        ('link-two', 'https://nil.test/path/two.html', {'href': 'two.html'}),
    ]

def test_base_url_and_relative_base_tag():
    with pytest.warns(DeprecationWarning):
        links = list(parse_links('''
            <html>
            <head>
                <title>Test with both base_url and a relative &lt;base&gt; tag</title>
                <base href="subdir/"/>
            </head>
            <body>
            <a href="one.html">link1</a>
            <a href="two.html">link-two</a>
            <span href="zero.html">not-a-link</span>
            </body>
            </html>
        ''', base_url='https://test.nil/base/'))
    assert links == [
        ('link1', 'https://test.nil/base/subdir/one.html', {'href': 'one.html'}),
        ('link-two', 'https://test.nil/base/subdir/two.html', {'href': 'two.html'}),
    ]

def test_uppercase():
    with pytest.warns(DeprecationWarning):
        links = list(parse_links('''
            <html>
            <head>
                <title>Test with uppercase tags &amp; attributes</title>
                <BASE HREF="https://nil.test/path/"/>
            </head>
            <body>
            <A HREF="one.html">link1</a>
            <A HREF="two.html">link-two</A>
            <span href="zero.html">not-a-link</span>
            </body>
            </html>
        '''))
    assert links == [
        ('link1', 'https://nil.test/path/one.html', {'href': 'one.html'}),
        ('link-two', 'https://nil.test/path/two.html', {'href': 'two.html'}),
    ]

def test_whitespace():
    with pytest.warns(DeprecationWarning):
        links = list(parse_links('''
            <html>
            <head>
                <title>Test links with leading &amp; trailing whitespace</title>
            </head>
            <body>
            <a href="one.html"> whitespaced  </a>
            <a href="two.html">multiple words</a>
            <a href="three.html"> <!-- comment -->  preceded by a comment </a>
            </body>
            </html>
        '''))
    assert links == [
        ('whitespaced', 'one.html', {'href': 'one.html'}),
        ('multiple words', 'two.html', {'href': 'two.html'}),
        ('preceded by a comment', 'three.html', {'href': 'three.html'}),
    ]

def test_a_name():
    with pytest.warns(DeprecationWarning):
        links = list(parse_links('''
            <html>
            <head>
                <title>Test that &lt;a&gt; tags without href are ignored</title>
            </head>
            <body>
            <a href="one.html">link1</a>
            <a name="two">target</a>
            </body>
            </html>
        '''))
    assert links == [('link1', 'one.html', {'href': 'one.html'})]

def test_bare():
    with pytest.warns(DeprecationWarning):
        links = list(parse_links('''
            <a href="one.html">link1</a>
            <a href="two.html">link-two</a>
            <span href="zero.html">not-a-link</span>
        '''))
    assert links == [
        ('link1', 'one.html', {'href': 'one.html'}),
        ('link-two', 'two.html', {'href': 'two.html'}),
    ]

def test_escaped_attrib():
    with pytest.warns(DeprecationWarning):
        links = list(parse_links('''
            <a href="https://files.pythonhosted.org/packages/05/35/aa8dc452b753bd9b405a0d23ee3ebac693edd2d0a5896bcc2c98f6263039/txtble-0.1.0-py2.py3-none-any.whl#sha256=25103e370ee304327751856ef5ecd7f59f9be88269838c7b558d4ac692d3e375" data-requires-python="&gt;=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, &lt;4">txtble-0.1.0-py2.py3-none-any.whl</a><br/>
        '''))
    assert links == [(
        'txtble-0.1.0-py2.py3-none-any.whl',
        "https://files.pythonhosted.org/packages/05/35/aa8dc452b753bd9b405a0d23ee3ebac693edd2d0a5896bcc2c98f6263039/txtble-0.1.0-py2.py3-none-any.whl#sha256=25103e370ee304327751856ef5ecd7f59f9be88269838c7b558d4ac692d3e375",
        {
            "href": "https://files.pythonhosted.org/packages/05/35/aa8dc452b753bd9b405a0d23ee3ebac693edd2d0a5896bcc2c98f6263039/txtble-0.1.0-py2.py3-none-any.whl#sha256=25103e370ee304327751856ef5ecd7f59f9be88269838c7b558d4ac692d3e375",
            "data-requires-python": ">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, <4",
        },
    )]

def test_escaped_text():
    with pytest.warns(DeprecationWarning):
        links = list(parse_links('''
            <a href="https://test.nil/simple/files/project-0.1.0-p&#xFF;42-none-any.whl">project-0.1.0-p&#xFF;42-none-any.whl</a>
        '''))
    assert links == [(
        'project-0.1.0-p\xFF42-none-any.whl',
        "https://test.nil/simple/files/project-0.1.0-p\xFF42-none-any.whl",
        {
            "href": "https://test.nil/simple/files/project-0.1.0-p\xFF42-none-any.whl",
        },
    )]

def test_named_escaped_text():
    with pytest.warns(DeprecationWarning):
        links = list(parse_links('''
            <a href="https://test.nil/simple/files/project-0.1.0-p&yuml;42-none-any.whl">project-0.1.0-p&yuml;42-none-any.whl</a>
        '''))
    assert links == [(
        'project-0.1.0-p\xFF42-none-any.whl',
        "https://test.nil/simple/files/project-0.1.0-p\xFF42-none-any.whl",
        {
            "href": "https://test.nil/simple/files/project-0.1.0-p\xFF42-none-any.whl",
        },
    )]
