import magic
import argparse
import png
import os
import math

MIME = magic.Magic(mime=True)
AUDIO_MIME_TYPES = ['audio/mpeg', 'audio/x-wav']
IMAGE_MIME_TYPES = ['image/png']

def encode(input, output):
	input_size_bytes = os.path.getsize(input)
	approx_pixel_count = math.ceil(input_size_bytes / 3)
	output_dim = math.ceil(math.sqrt(approx_pixel_count))

	output_file = open(output, 'wb')

	png_writer = png.Writer(output_dim, output_dim, greyscale=False)

	output_file.close()

def decode(input, output):
	pass

def detect_mime_type(file_path):
	return MIME.from_file(file_path)

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('input')
	parser.add_argument('output')
	args = parser.parse_args()

	mime_type = detect_mime_type(args.input)

	if mime_type in AUDIO_MIME_TYPES:
		encode(args.input, args.output)
	elif mime_type in IMAGE_MIME_TYPES:
		decode(args.input, args.output)
	else:
		print("Invalid input file format")