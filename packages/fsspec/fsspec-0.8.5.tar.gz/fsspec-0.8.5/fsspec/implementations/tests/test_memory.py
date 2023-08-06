import pytest
import sys


def test_1(m):
    m.touch("/somefile")  # NB: is found with or without initial /
    m.touch("afiles/and/anothers")
    files = m.find("")
    if "somefile" in files:
        assert files == ["afiles/and/anothers", "somefile"]
    else:
        assert files == ["/somefile", "afiles/and/anothers"]

    files = sorted(m.get_mapper(""))
    if "somefile" in files:
        assert files == ["afiles/and/anothers", "somefile"]
    else:
        assert files == ["/somefile", "afiles/and/anothers"]


@pytest.mark.xfail(
    sys.version_info < (3, 6),
    reason="py35 error, see https://github.com/intake/filesystem_spec/issues/148",
)
def test_ls(m):
    m.mkdir("/dir")
    m.mkdir("/dir/dir1")

    m.touch("/dir/afile")
    m.touch("/dir/dir1/bfile")
    m.touch("/dir/dir1/cfile")

    assert m.ls("/", False) == ["/dir/"]
    assert m.ls("/dir", False) == ["/dir/afile", "/dir/dir1/"]
    assert m.ls("/dir", True)[0]["type"] == "file"
    assert m.ls("/dir", True)[1]["type"] == "directory"

    assert len(m.ls("/dir/dir1")) == 2


def test_directories(m):
    with pytest.raises(NotADirectoryError):
        m.mkdir("outer/inner", create_parents=False)
    m.mkdir("outer/inner")

    assert m.ls("outer")
    assert m.ls("outer/inner") == []

    with pytest.raises(OSError):
        m.rmdir("outer")

    m.rmdir("outer/inner")
    m.rmdir("outer")

    assert not m.store


def test_mv_recursive(m):
    m.mkdir("src")
    m.touch("src/file.txt")
    m.mv("src", "dest", recursive=True)
    assert m.exists("dest/file.txt")
    assert not m.exists("src")


def test_rm_no_psuedo_dir(m):
    m.touch("/dir1/dir2/file")
    m.rm("/dir1", recursive=True)
    assert not m.exists("/dir1/dir2/file")
    assert not m.exists("/dir1/dir2")
    assert not m.exists("/dir1")

    with pytest.raises(FileNotFoundError):
        m.rm("/dir1", recursive=True)


def test_rewind(m):
    # https://github.com/intake/filesystem_spec/issues/349
    with m.open("src/file.txt", "w") as f:
        f.write("content")
    with m.open("src/file.txt") as f:
        assert f.tell() == 0


def test_no_rewind_append_mode(m):
    # https://github.com/intake/filesystem_spec/issues/349
    with m.open("src/file.txt", "w") as f:
        f.write("content")
    with m.open("src/file.txt", "a") as f:
        assert f.tell() == 7


def test_moves(m):
    m.touch("source.txt")
    m.mv("source.txt", "target.txt")

    m.touch("source2.txt")
    m.mv("source2.txt", "target2.txt", recursive=True)
    assert m.find("") == ["target.txt", "target2.txt"]
