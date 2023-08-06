import cid
import pytest_cid
import pytest


TEST_STRUCT1_A = [
	{"Hash": "QmQcCtMgLVwvMQGu6mvsRYLjwqrZJcYtH4mboM9urWW9vX",
	 "Name": "fsdfgh", "Size": "16"},
	{"Hash": "Qme7vmxd4LAAYL7vpho3suQeT3gvMeLLtPdp7myCb9Db55",
	 "Name": "",       "Size": "68"}
]

TEST_STRUCT1_B = [
	{"Hash": "bafybeibbwn36kj66vkljrjcr7idsgll43feu6zkteuxtevkz3ectwvs3ha",
	 "Name": "fsdfgh", "Size": "16"},
	{"Hash": "bafybeihkpcnu6r6mikmwhnc2xodgrn42vqyidj24sax3zpfasj4vppnwcq",
	 "Name": "",       "Size": "68"}
]

TEST_STRUCT1_C = [
	{"Hash": cid.make_cid(0, "dag-pb", b'\x12\x20\x21\xb3\x77\xe5\x27\xde\xaa\x96\x98\xa4\x51\xfa\x07\x23\x2d\x7c\xd9\x49\x4f\x65\x53\x25\x2f\x32\x55\x59\xd9\x05\x3b\x56\x5b\x38'),
	 "Name": "fsdfgh", "Size": "16"},
	{"Hash": cid.make_cid(1, "dag-pb", b'\x12\x20\xea\x78\x9b\x4f\x47\xcc\x42\x99\x63\xb4\x5a\xbb\x86\x68\xb7\x9a\xac\x30\x81\xa7\x5c\x90\x2f\xbc\xbc\xa0\x92\x79\x57\xbd\xb6\x14'),
	 "Name": "",       "Size": "68"}
]


TEST_STRUCT2_A = [
	{"Hash": "QmQcCtMgLVwvMQGu6mvsRYLjwqrZJcYtH4mboM9urWW9vX",
	 "Name": "fsdfgh", "Size": "16"},
	{"Hash": "QmYAhvKYu46rh5NcHzeu6Bhc7NG9SqkF9wySj2jvB74Rkv",  # ← This hash is changed!
	 "Name": "",       "Size": "68"}
]

TEST_STRUCT2_B = [
	{"Hash": "f0170122021b377e527deaa9698a451fa07232d7cd9494f6553252f325559d9053b565b38",
	 "Name": "fsdfgh", "Size": "16"},
	{"Hash": "92793123873921578944130930124010611884612608868063604620303126820283332997485244319659",
	 "Name": "",       "Size": "68"}
]


TEST_VALUES_EQ = [
	(TEST_STRUCT1_A, TEST_STRUCT1_B),
	(TEST_STRUCT1_B, TEST_STRUCT1_C),
	(TEST_STRUCT1_C, TEST_STRUCT1_A),
	(TEST_STRUCT2_A, TEST_STRUCT2_B),
]

TEST_VALUES_NE = [
	(TEST_STRUCT1_A, TEST_STRUCT2_A),
	(TEST_STRUCT1_A, TEST_STRUCT2_B),
	(TEST_STRUCT1_B, TEST_STRUCT2_A),
	(TEST_STRUCT1_B, TEST_STRUCT2_B),
	(TEST_STRUCT1_C, TEST_STRUCT2_A),
	(TEST_STRUCT1_C, TEST_STRUCT2_B),
]


@pytest.mark.parametrize("a,b", TEST_VALUES_EQ)
def test_normalize_eq(a, b):
	assert pytest_cid.normalize(a) == pytest_cid.normalize(b)


@pytest.mark.parametrize("a,b", TEST_VALUES_NE)
def test_normalize_ne(a, b):
	assert pytest_cid.normalize(a) != pytest_cid.normalize(b)


@pytest.mark.parametrize("a,b", TEST_VALUES_EQ)
def test_match_eq(a, b):
	assert pytest_cid.match(a) == b
	assert pytest_cid.match(a) == pytest_cid.match(b)


@pytest.mark.parametrize("a,b", TEST_VALUES_NE)
def test_match_ne(a, b):
	assert pytest_cid.match(a) != b
	assert pytest_cid.match(a) != pytest_cid.match(b)
