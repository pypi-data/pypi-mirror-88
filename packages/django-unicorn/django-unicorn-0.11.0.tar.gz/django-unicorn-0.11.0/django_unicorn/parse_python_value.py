# parsePythonValue.py
#
# Copyright, 2006, by Paul McGuire
#
import pyparsing as pp


cvtBool = lambda t: t[0] == "True"
cvtInt = lambda toks: int(toks[0])
cvtReal = lambda toks: float(toks[0])
cvtTuple = lambda toks: tuple(toks.asList())
cvtDict = lambda toks: dict(toks.asList())
cvtList = lambda toks: [toks.asList()]

# define punctuation as suppressed literals
lparen, rparen, lbrack, rbrack, lbrace, rbrace, colon, comma = map(
    pp.Suppress, "()[]{}:,"
)

integer = pp.Regex(r"[+-]?\d+").setName("integer").setParseAction(cvtInt)
real = pp.Regex(r"[+-]?\d+\.\d*([Ee][+-]?\d+)?").setName("real").setParseAction(cvtReal)
tupleStr = pp.Forward()
listStr = pp.Forward()
dictStr = pp.Forward()

unistr = pp.unicodeString().setParseAction(lambda t: t[0][2:-1])
quoted_str = pp.quotedString().setParseAction(lambda t: t[0][1:-1])
boolLiteral = pp.oneOf("True False", asKeyword=True).setParseAction(cvtBool)
noneLiteral = pp.Keyword("None").setParseAction(pp.replaceWith(None))

listItem = (
    real
    | integer
    | quoted_str
    | unistr
    | boolLiteral
    | noneLiteral
    | pp.Group(listStr)
    | tupleStr
    | dictStr
)

tupleStr <<= (
    lparen + pp.Optional(pp.delimitedList(listItem)) + pp.Optional(comma) + rparen
)
tupleStr.setParseAction(cvtTuple)

listStr <<= (
    lbrack + pp.Optional(pp.delimitedList(listItem) + pp.Optional(comma)) + rbrack
)
listStr.setParseAction(cvtList, lambda t: t[0])

dictEntry = pp.Group(listItem + colon + listItem)
dictStr <<= (
    lbrace + pp.Optional(pp.delimitedList(dictEntry) + pp.Optional(comma)) + rbrace
)
dictStr.setParseAction(cvtDict)

