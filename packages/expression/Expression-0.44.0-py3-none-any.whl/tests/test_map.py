from typing import Callable, Dict, ItemsView, Iterable, Tuple

from expression.collections import FrozenList, Map, map
from hypothesis import given
from hypothesis import strategies as st


def test_map_empty():
    m: Map[str, int] = map.empty
    assert map.is_empty(m)
    assert len(m) == 0
    assert not m


def test_map_non_empty():
    m: Map[str, int] = map.empty.add("test", 42)
    assert not map.is_empty(m)
    assert len(m) == 1
    assert m


@given(st.dictionaries(keys=st.text(), values=st.integers()))
def test_map_create(xs: Dict[str, int]):
    items: Iterable[Tuple[str, int]] = xs.items()
    m = map.create(items)
    assert len(m) == len(xs)


@given(st.dictionaries(keys=st.text(), values=st.integers()))
def test_map_of_seq(xs: Dict[str, int]):
    items: ItemsView[str, int] = xs.items()
    m = map.of_seq(items)
    assert len(m) == len(xs)


@given(st.dictionaries(keys=st.text(), values=st.integers()))
def test_map_remove(xs: Dict[str, int]):
    items: ItemsView[str, int] = xs.items()
    m = Map.of_seq(items)

    keys = xs.keys()
    count = len(m)
    for key in keys:
        m = m.remove(key)
        count -= 1
    assert len(m) == count == 0


@given(st.dictionaries(keys=st.text(), values=st.integers()))
def test_map_to_seq(xs: Dict[str, int]):
    items: ItemsView[str, int] = xs.items()
    ys = map.of_seq(items).to_seq()

    assert sorted(list(items)) == list(ys)


@given(st.dictionaries(keys=st.text(), values=st.integers()))
def test_map_to_list(xs: Dict[str, int]):
    items = FrozenList(xs.items())
    ys = map.of_frozenlist(items).to_seq()

    assert sorted(list(items)) == list(ys)


@given(st.dictionaries(keys=st.text(), values=st.integers()))
def test_map_map(xs: Dict[str, int]):
    items = FrozenList(xs.items())

    mapper: Callable[[str, int], int] = lambda k, v: v * 20
    ys = map.of_frozenlist(items).map(mapper)
    print(xs, ys)

    expected = [(k, mapper(k, v)) for k, v in sorted(list(items))]
    assert expected == list(ys.to_list())
