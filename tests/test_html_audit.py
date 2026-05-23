from agent_seo_engine.html_audit import check_image_alt_coverage


def test_no_images_reports_perfect_coverage():
    result = check_image_alt_coverage("<p>no images here</p>")
    assert result == {
        "total": 0,
        "with_alt": 0,
        "missing_alt": 0,
        "coverage": 1.0,
        "missing": [],
    }


def test_all_images_have_alt():
    html = """
    <img src='hero.jpg' alt='A hero'>
    <img src=\"logo.png\" alt=\"Company logo\" />
    """
    result = check_image_alt_coverage(html)
    assert result["total"] == 2
    assert result["with_alt"] == 2
    assert result["missing_alt"] == 0
    assert result["coverage"] == 1.0
    assert result["missing"] == []


def test_partial_coverage_lists_missing_tags():
    html = (
        "<img src='a.jpg' alt='ok'>"
        "<img src='b.jpg'>"
        "<img src='c.jpg' alt=''>"
        "<img src='d.jpg' alt=\"  \">"
    )
    result = check_image_alt_coverage(html)
    assert result["total"] == 4
    assert result["with_alt"] == 1
    assert result["missing_alt"] == 3
    assert result["coverage"] == 0.25
    assert len(result["missing"]) == 3
    assert any("b.jpg" in snippet for snippet in result["missing"])


def test_unquoted_and_multiline_alt_attributes_are_handled():
    html = """
    <img src=foo.png alt=hello>
    <img
      src='bar.png'
      alt='multi line'
    />
    """
    result = check_image_alt_coverage(html)
    assert result["total"] == 2
    assert result["with_alt"] == 2
    assert result["coverage"] == 1.0


def test_non_string_input_raises_type_error():
    import pytest

    with pytest.raises(TypeError):
        check_image_alt_coverage(b"<img>")
