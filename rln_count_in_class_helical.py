#!/usr/bin/python

# counts the number of particles in a data file from relion 2d or 3d classification
 

import sys
import operator

if len(sys.argv) < 2:
	sys.exit('USAGE: rln-count-in-classes.py <xxx_data.star>')
if '_data.star' not in sys.argv[1]:
	sys.exit('USAGE: rln-count-in-classes.py <xxx_data.star>')

modelfile = sys.argv[1].replace('_data.star','_model.star')
rawfile = sys.argv[1].replace('_data.star','')

###---------function: read the star file get the header, labels, and data -------------#######
def read_starfile(f):
    alldata = open(f,'r').readlines()
    labelsdic = {}
    data = []
    header = []
    for i in alldata:
        if '#' in i:
            labelsdic[i.split('#')[0].strip()] = int(i.split('#')[1])-1
        if len(i.split()) > 3:
            data.append(i.split())
        if len(i.split()) < 3:
            header.append(i.strip("\n"))
    return(labelsdic,header,data)
#---------------------------------------------------------------------------------------------#

(labelsdic,header,data) = read_starfile(sys.argv[1])

classes = {}

for line in data:
    classnumber = line[labelsdic['_rlnClassNumber']]
    if classnumber in classes.keys():
            classes[classnumber][0] += 1
    else:
             classes[classnumber] = [1]

resdata = []
model_info = open(modelfile,'r').readlines()

n = 0
for i in model_info[:50]:
	if '_rlnOverallFourierCompleteness #6' in i:	
		line = n
	n+=1

n = 0
for i in model_info[line+3:line+len(classes)+3]:
	linesplit = i.split()
	classname = linesplit[0].split('_')[-1].replace('.mrc','')
	stripname = str(int(classname.split('.')[0].replace('class','')))
	classes[stripname].append(linesplit[4])
	classes[stripname].append(linesplit[6])
	classes[stripname].append(linesplit[7])
sorted_classes = classes.keys()
sorted_classes.sort(key=int)
print '\nClass\t#parts\tResolution\tRise\t\tTwist'
for i in sorted_classes:
	print i,'\t',classes[i][0],'\t',classes[i][1],'\t',classes[i][2],'\t',classes[i][3]
	
print '\nClass\t#parts\tResolution\tRise\t\tTwist'
sorted_classes2 = sorted(classes.items(), key=operator.itemgetter(1))
sorted_classes2.reverse()
for i in sorted_classes2:
	print i[0],'\t',i[1][0],'\t',i[1][1],'\t',i[1][2],'\t',i[1][3]
