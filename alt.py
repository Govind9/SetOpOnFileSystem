import os
import hashlib

all_files = []

def chunk_reader(file, chunk_size=1024):
	while True:
		chunk = file.read(chunk_size)
		if not chunk:
			return
		yield chunk

def get_hash(filename, fc_only=False, hash=hashlib.sha1):
	hashobj = hash()
	file = open(filename, 'rb')
	if fc_only:
		hashobj.update(file.read(1024))
	else:
		for chunk in chunk_reader(file):
			hashobj.update(chunk)
	hashed = hashobj.digest()
	file.close()
	return hashed

def get_all_filepaths(path):
	one = [path + '/' + p for p in os.listdir(path)]
	for f in one:
		if os.path.isdir(f):
			get_all_filepaths(f)
		else:
			all_files.append(f)
		
def get_all_duplicates(paths):
	dup = []
	hashes_by_size = {}
	hashes_on_1k = {}
	hashes_full = {}
	for path in paths:
		try:
			filesize = os.path.getsize(path)
		except (OSError):
			pass
		duplicate = hashes_by_size.get(filesize)

		if duplicate:
			hashes_by_size[filesize].append(path)
		else:
			hashes_by_size[filesize] = []
			hashes_by_size[filesize].append(path)
	print hashes_by_size
	for __, files in hashes_by_size.items():
		if len(files) < 2:
			continue
		for filename in files:
			small_hash = get_hash(filename, fc_only=True)
			duplicate = hashes_on_1k.get(small_hash)
			if duplicate:
				hashes_on_1k[small_hash].append(filename)
			else:
				hashes_on_1k[small_hash] = []
				hashes_on_1k[small_hash].append(filename)
	print "eheheheheheh"
	print hashes_on_1k
	print "eheheheheheh"
	for __, files in hashes_on_1k.items():
		if len(files) < 2:
			continue
		for filename in files:
			full_hash = get_hash(filename, fc_only=False)
			duplicate = hashes_full.get(full_hash)
			if duplicate:
				hashes_full[full_hash].append(filename)
			else:
				hashes_full[full_hash] = []
				hashes_full[full_hash].append(filename)
	print hashes_full
	for __, files in hashes_full.items():
		if len(files) < 2:
			continue
		for filename in files:
			dup.append(filenames)
	return dup
path1 = '/home/dnivog/C++/SetOpOnFileSystem/test1'
path2 = '/home/dnivog/C++/SetOpOnFileSystem/test2'
get_all_filepaths(path1) 
get_all_filepaths(path2)
dup = get_all_duplicates(all_files)
print "\n\n\n\n"
print dup
