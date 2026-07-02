from xkoranate.rng import Mt19937


def test_same_seed_produces_same_sequence():
    a = Mt19937(42)
    b = Mt19937(42)
    assert [a.next32() for _ in range(10)] == [b.next32() for _ in range(10)]


def test_different_seeds_produce_different_sequences():
    a = Mt19937(1)
    b = Mt19937(2)
    assert [a.next32() for _ in range(10)] != [b.next32() for _ in range(10)]


def test_call_is_alias_for_next32():
    a = Mt19937(7)
    b = Mt19937(7)
    assert a() == b.next32()


def test_next32_within_min_max_bounds():
    r = Mt19937(123)
    for _ in range(1000):
        v = r.next32()
        assert r.min() <= v <= r.max()


def test_seed_resets_sequence():
    r = Mt19937(1)
    first_run = [r.next32() for _ in range(5)]
    r.seed(1)
    second_run = [r.next32() for _ in range(5)]
    assert first_run == second_run


def test_shuffle_is_a_permutation_of_the_input():
    r = Mt19937(99)
    original = list(range(20))
    shuffled = list(original)
    r.shuffle(shuffled)
    assert sorted(shuffled) == original


def test_shuffle_is_deterministic_for_a_given_seed():
    seq_a = list(range(10))
    seq_b = list(range(10))
    Mt19937(5).shuffle(seq_a)
    Mt19937(5).shuffle(seq_b)
    assert seq_a == seq_b
