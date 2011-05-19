#!/usr/bin/env python

def build_bytearray(*args):
	result = bytearray(len(args))
	for i in range(len(args)):
		result[i] = args[i]
	return result

cssid_post_body = build_bytearray(34, 0, 98, 60, 10, 19, 34, 2, 101, 110, 186, 211, 240, 59, 10, 8, 1, 16, 1, 40, 1, 48, 0, 56, 1, 18, 29, 10, 9, 105, 80, 104, 111, 110, 101, 32, 79, 83, 18, 3, 52, 46, 49, 26, 0, 34, 9, 105, 80, 104, 111, 110, 101, 51, 71, 83, 26, 2, 8, 2, 34, 2, 8, 1)

trailing_bytes = build_bytearray(24, 75, 32, 1, 48, 0, 146, 236, 244, 59, 9, 24, 0, 56, 198, 151, 220, 223, 247, 37, 34, 0)

import httplib
import random

def goggles_request(cssid, length):
	conn = httplib.HTTPConnection("www.google.com:80")
	headers = { "Content-type": "application/x-protobuffer",
				"Pragma": "no-cache", "Keep-alive": "true",
				"Content-length": length }
	url = "/goggles/container_proto?cssid=%s" % cssid

	conn.request("POST", url, {}, headers)
	return conn

def goggles_response(conn):
    response = conn.getresponse()
    if response.status is 200:
        return response.read()        
	#print response.status, response.reason

def random_cssid():
	return "%016X" % random.getrandbits(64)

def validate_cssid(cssid):
	conn = goggles_request(cssid, len(cssid_post_body))
	conn.send(cssid_post_body)
	return goggles_response(conn)

def send_photo(cssid, image):
	delim = build_bytearray(10)
	x = len(image)
	
	X = to_varint32(x)
	A = to_varint32(x + 32)
	B = to_varint32(x + 14)
	C = to_varint32(x + 10)

	post_data = "%s%s%s%s%s%s%s%s%s%s" % (delim, A, delim, B,
		delim, C, delim, X, image, trailing_bytes)

	conn = goggles_request(cssid, len(post_data))
	#conn.set_debuglevel(10)
	conn.send(post_data)
	response = goggles_response(conn)
	return response

def to_varint32_generator(value):
 	while ((0x7F & value) != 0):
		i = (0x7F & value)
		if ((0x7F & (value >> 7)) != 0):
			i += 128
		yield i
		value = value >> 7

def to_varint32(value):
	as_list = [i for i in to_varint32_generator(value)]
	return bytearray(as_list)

def goggles_recognize(image_path):
	cssid = random_cssid()
	if validate_cssid(cssid):
		image = file(image_path).read()
		result = send_photo(cssid, image)
		if result:
			# TODO: ProtoBuffer should get parsed, obviously
			text = result.split('\n')[5]
			if ord(text[0]) == 8:
				raise Exception('Error: Could not recognize your image.')
			else:
				return text
		else:
			raise Exception('Error: Could not handle the given file.')

if __name__ == '__main__':
	import sys
	if len(sys.argv) < 2:
		print 'Please specify a JPEG image.'
		sys.exit(1)

	try:
		print goggles_recognize(sys.argv[1])
	except Exception, e:
		print e
