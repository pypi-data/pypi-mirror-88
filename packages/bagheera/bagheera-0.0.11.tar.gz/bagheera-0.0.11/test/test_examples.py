import pytest
import os
import bagheera.main as main
from bagheera.parser.parser import print_ast
import itertools
from difflib import SequenceMatcher


fdescs_old = os.walk(os.path.join("test","examples"))
next(fdescs_old)

def fdesc2id(fdesc):
    path, dirs, files = fdesc
    return path

fdescs,id_old = itertools.tee(fdescs_old)
ids = map(fdesc2id,id_old)


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


@pytest.mark.parametrize('fdesc', fdescs, ids=ids)
def test_examples(fdesc):
    path, dirs, files = fdesc
    assert len(dirs) == 0
    parsed = None
    parsed_ast = None
    ast = None
    expected = None
    for filename in files:
        if filename.endswith(".b"):
            parsed = main.parse(os.path.join(path,filename))
            parsed_ast = parsed.dump()
        elif filename.endswith(".out"):
            with open(os.path.join(path,filename)) as f:
                expected = f.read()
        elif filename.endswith(".ast"):
            with open(os.path.join(path,filename)) as f:
                ast = f.read()
    print_ast(parsed_ast)
    assert similar(parsed_ast, ast) == 1

