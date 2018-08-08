import os
import hashlib
import sys

all_files = set()
s1 = set()
s2 = set()
Dup = set()

def get_hash(filename, chunk, hash=hashlib.sha1):
	hashobj = hash()
	file = open(filename, 'rb')
	if chunk > 1024:
		file.seek(chunk/2)
	hashobj.update(file.read(chunk))
	hashed = hashobj.digest()
	file.close()
	return hashed

def get_all_filepaths(path, s):
	if path[len(path)-1] != '/':
		path += '/'
	one = [path + p for p in os.listdir(path) if not p.startswith('.')]
	for f in one:
		if os.path.isdir(f):
			get_all_filepaths(f, s)
		else:
			s.add(f)
		
def get_all_dups():
	hashes_by_size = {}
	for filename in all_files:
		filesize = os.path.getsize(filename)
		duplicate = hashes_by_size.get(filesize)
		if duplicate:
			hashes_by_size[filesize].append(filename)
		else:
			hashes_by_size[filesize] = []
			hashes_by_size[filesize].append(filename)
	for __, files in hashes_by_size.items():
		if len(files) < 2:
			continue
		incremental(files, 1024)

def incremental(dup_contendors, chunk):
	new_file_hashes = {}
	for filename in dup_contendors:
		new_hash = get_hash(filename, chunk)
		duplicate = new_file_hashes.get(new_hash)
		if duplicate:
			new_file_hashes[new_hash].append(filename)
		else:
			new_file_hashes[new_hash] = []
			new_file_hashes[new_hash].append(filename)
	for __, files in new_file_hashes.items():
		if len(files) < 2:
			continue
		if os.path.getsize(files[0]) > chunk:
			incremental(files, 2*chunk)
		else:
			for filename in files:
				Dup.add(filename)

def intersection():
	return Dup
def union():
	return all_files.difference(Dup.intersection(s2))
def difference():
	return s1.difference(Dup)
def symmetric_difference():
	return all_files.difference(Dup)

op = None
path1 = '.'
path2 = '.'
if len(sys.argv) >= 2:
	op = sys.argv[1]
if len(sys.argv) >= 3:
	path1 = sys.argv[2]
if len(sys.argv) >= 4:
	path2 = sys.argv[3]
#path1 = '/home/dnivog/C++/SetOpOnFileSystem/test1'
#path2 = '/home/dnivog/C++/SetOpOnFileSystem/test2'
get_all_filepaths(path1, s1) 
get_all_filepaths(path2, s2)
all_files = s1.union(s2)
get_all_dups()

if op == '-u':
	print union()
if op == '-i':
	print intersection()
if op == '-d':
	print difference()
if op == '-sd':
	print symmetric_difference()

