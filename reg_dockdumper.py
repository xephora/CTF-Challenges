#!/usr/bin/env python3
# This is registry docker script to download all blobs from a host.
# Credit: xephora & iilegacyyii
# Educational purposes only :)
import os, argparse


# Setting up argparse
parser = argparse.ArgumentParser(description='Simple script to download all blobs from a registry docker server using a manifest file')

parser.add_argument(
    "file",
    help="manifest file containing sha256 blobSums"
)

parser.add_argument(
    "url",
    help="url to Docker Registry repository. e.g. http://docker.registry.htb/v2/bolt-image/"
)

parser.add_argument(
	"-u", "--http-user",
	help="Username for http basic authentication if required."
)

parser.add_argument(
	"-p", "--http-pass",
	help="Password for http basic authentication if required."
)

args = parser.parse_args()


# Ensure that the given manifest file exists.
if not os.path.exists(args.file):
    print("File: {0} does not exist...".format(args.file))
    exit(1)

# Validate the url ends in a /, if not add one on the end.
if not args.url[::-1][0] == "/":
	args.url += "/"


# Function to parse a manifest file.
def parse_manifest_file(filename):
	hashes = []
	# Read the contents of the given manifest file.
	try:
		with open(filename, "r") as f:
			manifest_raw = f.read()
	except Exception as e:
		print("[!] File not found.\n")
		raise e

	# Get the section of the file containing the blobSums
	manifest_raw = manifest_raw.split("fsLayers")[1].split("\"history\"")[0]
	manifest_lines = manifest_raw.split("\n")

	for line in manifest_lines:
		if "\"blobSum\":" in line:
			hashes.append(line.split("\"blobSum\": \"")[1].split("\"")[0].split("sha256:")[1])

	return hashes


# Function to download the hashes
def download_blobs(hashes):
	if args.http_user and args.http_pass:
		for h in hashes:
			os.system("wget --http-user={0} --http-password={1} -O {2}.tar.gz {3}blobs/:sha256{2} >/dev/null 2>&1".format(args.http_user, args.http_pass, h, args.url))
	else:
		for h in hashes:
			os.system("wget -O {0}.tar.gz {1}blobs/:sha256:{1} >/dev/null 2>&1".format(h, args.url))


# Main
if __name__ == "__main__":
	hashes = parse_manifest_file(args.file)
	download_blobs(hashes)

