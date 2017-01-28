import codecs
import random
import sys
def shuffle_relations(file_relations,oppos_out, shuff_out):
    lines=open(file_relations, 'r').readlines()
    L, L2, Opp, L3 =[], {}, {}, {}
    for line in lines:
	## split pair of words
        tokens=line.replace('\r\n','').replace('\n','').split(',')
        L.append(tokens[1]+','+tokens[2])
	if tokens[0] not in L2:
		L2[tokens[0]]=[]
	if tokens[1] not in L2[tokens[0]]:
		L2[tokens[0]].append(tokens[1])
	L3[tokens[1]+','+tokens[2]]=tokens[0]+','+tokens[1]+','+tokens[2]
    for line in lines:
        tokens=line.replace('\r\n','').replace('\n','').split(',')
        if (tokens[2]+','+tokens[1]) not in L:
            Opp[tokens[2]+','+tokens[1]]='oppos_'+tokens[0]
 
    writer=codecs.open(oppos_out,'w')
    for key,value in Opp.iteritems():
        writer.write(value+','+key+'\n')
    writer.close()
	
    L4=[]
    writer=codecs.open(shuff_out, 'w')
    print L2.keys()
    for key,value in L3.iteritems():
        tokens=value.split(',')
        subset=set(L2[tokens[0]]).difference(set(tokens[1]))
        result=random.choice(list(subset))+","+tokens[2]
        if result not in L3.keys():
            if result not in L4:
		if result not in Opp.keys():
                	writer.write("shuff_"+tokens[0]+','+result+'\n')
                	L4.append(result)
    writer.close()

import getopt
def main(argv):
	semantic=''
	try:
		opts, args = getopt.getopt(argv,"s:",["seman="])
	except getopt.GetoptError:
		print 'generate_NS.py -s <semanticrels>'
		sys.exit(2)
	for opt, arg in opts:
		if opt in ("-s", "--seman"):
			semantic = arg
	shuffle_relations(semantic,semantic+'.oppos.csv',semantic+'.shuff.csv')

if __name__ == "__main__":
   main(sys.argv[1:])


