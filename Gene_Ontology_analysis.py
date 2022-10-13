# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 11:58:46 2022

@author: Patrícia de Pinho
"""

import pandas

# variables	----------

GO_codes_file = "GOs_Database.txt" #should have GOs of interest
Information_table_file = "ProteinsData.xlsx" #input table
column_of_interest = ["GO_UniProt", "GO_eggNOG"] #name columns of interest
last_column_name = "GOs_of_interest" #name of the column combining results

# functions	----------

def	read_codes(fname):
    """ read a filename and convert to a dictionary
    input: tsv
    output: dictionary go2text, dictionary go2code, dictionary text2go"""
	
    go2text = {} # go2text[go] = text
    go2code = {} # go2code[go] = code
    text2go = {} # text2go[text] = [go1, go2, ...]
	
    with open(fname, "r") as GO_file:
        GO = GO_file.readlines()
        i = 0
        for line in GO:
            if i > 0: 
                lin = line.split("\n")
                l=lin[0].split("\t")
                text = l[0]
                code = l[1]
                go = l[2]
				
                go2text[go] = text
                go2code[go] = code
                if text not in text2go:
                    text2go[text] = []
                text2go[text].append(go)
            i += 1
	
    return go2text, go2code, text2go

# pipeline	----------

go2text, go2code, text2go = read_codes(GO_codes_file)
mx = pandas.read_excel(Information_table_file, dtype = str)

new_info = {}

for index, row in mx.iterrows():
	# merge all GOs
	gos_list = set()
	for col in column_of_interest:
		for go in str(row[col]).split("; "):
			gos_list.add(go)
	if "all_GOs" not in new_info.keys():
		new_info["all_GOs"] = []
	info_all_GOs = ", ".join(list(gos_list))
	new_info["all_GOs"].append(info_all_GOs)
	
	# get info per GO of interest
	combined = []
	for cat in text2go.keys():
		if cat not in new_info.keys():
			new_info[cat] = []
		info = "NO"
		for go in text2go[cat]:
			if go in gos_list:
				info = "YES"
		if info == "YES":
			combined.append(go2code[go])
		new_info[cat].append(info)
	
	#add last column combining stuff
	if last_column_name not in new_info.keys():
		new_info[last_column_name] = []
	combined_merged = ", ".join(combined)
	new_info[last_column_name].append(combined_merged)

for info_key in new_info.keys():
	mx[info_key] = new_info[info_key]

mx.to_csv("GO_Classification.tsv", index = False, header=True, sep ="\t")