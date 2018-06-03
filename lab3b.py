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

    BG_DATA_BLOCK = int(first_inode_block + math.ceil( (total_inodes * inode_size) / block_size ))
    allocated_blocks = []

    # inode allocation audits
    for item in inode_list:
        block_offset = 0
        for inode in item[12:27]:
            num = item[1]
            Message = 'BLOCK'
            offset = block_offset
            if block_offset == 12:
                Message = 'INDIRECT BLOCK'
            elif block_offset == 13:
                offset = 268
                Message = 'DOUBLE INDIRECT BLOCK'
            elif block_offset == 14:
                offset = 65804
                Message = 'TRIPLE INDIRECT BLOCK'

            if int(inode) < 0 or int(inode) >= total_blocks:
                print("INVALID {} {} IN INODE {} AT OFFSET {}".format(Message,inode,num, offset))
            elif int(inode) < BG_DATA_BLOCK and int(inode) > 0:
                print("RESERVED {} {} IN INODE {} AT OFFSET {}".format(Message, inode, num, offset))
            elif int(block) > 0:
                allocated_blocks.append(int(inode))
            block_offset+=1

    # handle the indirect blocks
    for item in indirect_entries:
        i_type = item[2]
        Message = ''
        if i_type  == '1':
            Message = 'INDIRECT BLOCK'
        elif i_type  == '2':
            Message = 'DOUBLE INDIRECT BLOCK'
        elif i_type  == '3':
            Message = 'TRIPLE INDIRECT BLOCK'

        if int(item[5]) <0 or int(item[5]) >= total_blocks:
            print("INVALID {} {} IN INODE {} AT OFFSET {}".format(Message, item[5], item[1], item[3]))
        elif int(item[5]) < BG_DATA_BLOCK and int(item[5]) > 0:
            print("RESERVED {} {} IN INODE {} AT OFFSET {}".format(Message, item[5], item[1], item[3]))
        elif int(item[5]) > 0:
            allocated_blocks.append(int(item[5]))

    # check the unreferenced and repeatedly allocated blocl
    for item in range(BG_DATA_BLOCK,total_blocks):
        if item not in allocated_blocks and item not in bfree_list:
            print("UNREFERENCED BLOCK {}".format(item))
        if item in BLOCKS_IN_USE and item in BFREE_list:
            print("ALLOCATED BLOCK {} ON FREELIST".format(item))


    ### Check the duplicated blocks
    duplicate_list = []
    block_dict = dict()
    for i in range(BG_DATA_BLOCK,total_blocks):
        block_dict[i] = 0

    for item in inode_list:
        for inode in item[12:27]:
            if int(inode) in block_dict:
                block_dict[int(inode)]+=1
                if block_dict[int(inode)] > 1:
                    if inode not in duplicate_list and inode not in bfree_list:
                        duplicate_list.append(inode)

    for item in indirect_entries:
      if int(item[5]) in block_dict:
            block_dict[int(item[5])] += 1
            if block_dict[int(item[5])] > 1:
               if item[5] not in duplicate_list and item[5] not in BFREE_list:
                  duplicate_list.append(item[5])


    for block in duplicate_list:
        for item in INODE_list:
         block_offset = 0
         inode_num = item[1]
         for inode_block in item[12:24]:
            if block == inode_block:
               print("DUPLICATE BLOCK {} IN INODE {} AT OFFSET {}".format(block, inode_num, block_offset))
            block_offset += 1
         if block == item[24]:
            print("DUPLICATE INDIRECT BLOCK {} IN INODE {} AT OFFSET 12".format(block, inode_num))
         if block == item[25]:
            print("DUPLICATE DOUBLE INDIRECT BLOCK {} IN INODE {} AT OFFSET 268".format(block, inode_num))
         if block == item[26]:
            print("DUPLICATE TRIPLE INDIRECT BLOCK {} IN INODE {} AT OFFSET 65804".format(block, inode_num))
      ### handle indirect duplicates : 
      for item in indirect_entries:
         inode_num = item[1]
         if block == item[5]:
            Message = ''
            if int(item[2]) == 1:
               Message = " " 
            elif int(item[2]) == 2:
               Message = " INDIRECT "
            else :
               Message = " DOUBLE INDIRECT "
            print("DUPLICATE{}BLOCK {} IN INODE {} AT OFFSET {}".format(Message, block, inode_num, item[3]))





if __name__ == '__main__':
   main()


















