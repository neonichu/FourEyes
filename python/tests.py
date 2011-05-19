#!/usr/bin/env python

from goggles import to_varint32

sz = 27985
x = str(to_varint32(sz)).encode('hex')
a = str(to_varint32(sz + 32)).encode('hex')
b = str(to_varint32(sz + 14)).encode('hex')
c = str(to_varint32(sz + 10)).encode('hex')

if not x == "d1da01":
	print "x = %s is wrong." % x
if not a == "f1da01":
	print "a = %s is wrong." % a
if not b == "dfda01":
	print "b = %s is wrong." % b
if not c == "dbda01":
	print "c = %s is wrong." % c

from goggles import goggles_recognize

result = goggles_recognize('hello.jpg')
if not result[1:].startswith('Hello, goggles!'):
	print "Unexpected result '%s' from Goggles." % result
