from shooki import (
    html, div, img
)


def test_html():
    assert str(html) == '<html></html>'
    assert str(html()) == '<html></html>'
    assert str(html[div]) == '<html><div></div></html>'
    assert str(html[div.content]) == "<html><div class='content'></div></html>"
    assert str(html[div.content[img(src='jpg')]]) == "<html><div class='content'><img src='jpg'></img></div></html>"
