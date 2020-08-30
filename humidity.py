import magic
import argparse
import png
import os
import math

MIME = magic.Magic(mime=True)

def get_size_as_byte_vals(size):
	try:
		size_as_bytes = size.to_bytes(3, 'big')
		return [size_as_bytes[0], size_as_bytes[1], size_as_bytes[2]]
	except OverflowError:
		return []

def get_byte_val(byte):
	return int.from_bytes(byte, 'big') if byte else 0

def encode(input_path, output_path):
	input_size_bytes = os.path.getsize(input_path)
	approx_pixel_count = math.ceil(input_size_bytes / 3)
	image_data_container_dim = math.ceil(math.sqrt(approx_pixel_count))
	
	input_file = open(input_path, 'rb')
	image_rows = [[get_byte_val(input_file.read(1)) for _ in range(3 * image_data_container_dim)] for _ in range(image_data_container_dim)]
	input_file.close()
	image_data = [byte for row in image_rows for byte in row]
	
	size_as_byte_vals = get_size_as_byte_vals(input_size_bytes)
	if not size_as_byte_vals:
		print("Input too large. Maximum input size is 15 MB")
		return

	image_data_with_size_header = size_as_byte_vals + image_data

	output_dim = image_data_container_dim + 2
	final_image_data = image_data_with_size_header + [0 for _ in range(3 * output_dim * output_dim - len(image_data_with_size_header))]
	
	output_file = open(output_path, 'wb')
	png_writer = png.Writer(output_dim, output_dim, greyscale=False)
	png_writer.write_array(output_file, final_image_data)
	output_file.close()

def decode(input_path, output_path):
	png_reader = png.Reader(filename=input_path)
	(_, _, data, _) = png_reader.read_flat()
	
	output_size_bytes = 65536 * data[0] + 256 * data[1] + data[2]
	audio_data = b''.join(map(lambda byte_val: byte_val.to_bytes(1, 'big'), data[3:output_size_bytes + 3]))

	if not MIME.from_buffer(audio_data).startswith('audio'):
		print("Invalid input image")
		return

	output_file = open(output_path, 'wb')
	output_file.write(audio_data)
	output_file.close()

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('input_path')
	parser.add_argument('output_path')
	args = parser.parse_args()

	mime_type = MIME.from_file(args.input_path)

	if mime_type.startswith('audio'):
		encode(args.input_path, args.output_path)
	elif mime_type == 'image/png':
		decode(args.input_path, args.output_path)
	else:
		print("Invalid input file format")
