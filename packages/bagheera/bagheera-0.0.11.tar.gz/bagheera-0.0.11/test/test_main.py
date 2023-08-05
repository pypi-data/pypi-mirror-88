from bagheera.main import parse
import pyparsing
import io


def test_main():
    try:
        parse(io.StringIO("module vflgengvxnelv"))
    except pyparsing.ParseException:
        pass