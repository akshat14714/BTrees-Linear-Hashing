import sys
import os

def insert_in_hash_table (num):
	global S, total_block_count, output_buffer

	hash_val = num % b

	if hash_val < p:
		hash_val = num % b_new
	if hash_val not in linHash:
		linHash[hash_val] = [[]]

	flag = 0

	for i in range(block_count[hash_val]):
		if num in linHash[hash_val][i]:
			flag = 1

	if flag == 0:
		S += 1
		temp = block_count[hash_val] - 1
		if len(linHash[hash_val][temp]) >= (B * 0.25):
			total_block_count += 1
			temp += 1
			block_count[hash_val] += 1
			linHash[hash_val].append([])
		linHash[hash_val][temp].append(num)
		#print str(num)
		output_buffer.append(num)
		if len(output_buffer) >= ((B * 1.0) / 4.0):
			for val in output_buffer:
				print(str(val))
			output_buffer = []

	if hash_table_too_full():
		create_new_bucket()

def hash_table_too_full():

	density = (S * 400.0) / (B * total_block_count)
	if density > 75.0:
		return 1
	return 0

def create_new_bucket():
	global bucket_count, p, b, b_new, total_block_count

	bucket_count += 1
	#rehash values
	replace_array = []

	for i in range(block_count[p]):
		for value in linHash[p][i]:
			replace_array.append(value)

	total_block_count -= block_count[p]

	linHash[p], block_count[p] = [[]], 1
	total_block_count += 1

	linHash[bucket_count - 1] = [[]]
	block_count[bucket_count - 1] = 1
	total_block_count += 1

	for value in replace_array:
		hash_val = value % b_new

		if hash_val not in linHash:
			linHash[hash_val] = [[]]
			block_count[hash_val] = 1
			total_block_count += 1

		flag = 0
		for j in range(block_count[hash_val]):
			if value in linHash[hash_val][j]:
				flag = 1

		if flag == 0:
			temp = block_count[hash_val] - 1
			if len(linHash[hash_val][temp]) >= (B * 0.25):
				temp += 1
				block_count[hash_val] += 1
				total_block_count += 1
				linHash[hash_val].append([])
			linHash[hash_val][temp].append(value)
	p += 1

	if bucket_count == b_new:
		b = b * 2
		b_new = b * 2
		p = 0

	return 1

if __name__ == "__main__":
	filename = sys.argv[1]

	M = int(sys.argv[2])
	B = int(sys.argv[3])

	if not os.path.isfile(filename):
		print("Invalid File")
		exit(-1)

	input_buffer, output_buffer = [], []

	pointer_count = ((B - 8) / 12) + 1

	if pointer_count <= 2:
		pointer_count = 2
	if M <= 2:
		M = 2
	if B <= 20:
		B = 20

	i, p, S, b, b_new = 0, 0, 0, 2, 4
	bucket_count = 2
	linHash, block_count = {}, {}
	total_block_count = 2
	block_count[0], block_count[1] = 1, 1

	with open(filename) as fh:
		for line in fh:
			num = int(line.strip())
			input_buffer.append(num)
			if len(input_buffer) >= (((M-1) * B * 1.0) / 4.0) :
				for val in input_buffer:
					insert_in_hash_table(val)
				input_buffer = []

		for val in input_buffer:
			insert_in_hash_table(val)
		input_buffer = []

	for val in output_buffer:
		print(str(val))
	output_buffer = []