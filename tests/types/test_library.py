from refspy.types.library import Library


def test_library():
    nt = Library(id=1, name="New Testament", abbrev="NT", code="nt", books=[])
    assert nt.id == 1
    assert nt.name == "New Testament"
    assert nt.abbrev == "NT"
    assert nt.code == "nt"
    assert nt.books == []
