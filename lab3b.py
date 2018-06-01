#!/bin/python

import sys
import csv
import math

def main():
	if len(sys.argv) != 2:
		sys.stderr.write("Wrong number of arguments\n")
      	sys.exit(1)

    try:
    	f = open(sys.argv[1],'r')
    	csv_file = csv.reader(f)
    except:
    	sys.stderr.write("Cannot open the input file\n")
    	sys.exit(1)

    # for storing the information
    inode_list = []
    indirect_entries = []
    bfree_list = []
    ifree_list = []
    dirent_list = []

    #count
    total_blocks = 0
    total_inodes = 0
    block_size = 0
    inode_size = 0
    bg_inode_table = 0
    first_inode_block = 0

    for line in csv_file:
    	if line[0] == "SUPERBLOCK":
    		total_blocks = int(line[1])
    		total_inodes = int(line[2])
    		block_size = int(line[3])
    		inode_size = int(line[4])
    		bg_inode_table = int(line[7])
    	elif line[0] == "GROUP":
    		first_inode_block = int(line[8])
    	elif line[0] == "BFREE":
    		bfree_list.append(int(line[1]))
    	elif line[0] == "IFREE":
    		ifree_list.append(int(line[1]))
    	elif(line[0] == "INODE"):
        	inode_list.append(line)
      	elif(line[0] == "INDIRECT"):
         	indirect_entries.append(line)
      	elif(line[0] == "DIRENT"):
         	dirent_list.append(line)


    # handle the 





















