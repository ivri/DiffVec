import codecs
import random
def shuffle_relations(file_relations,oppos_out, shuff_out):
    lines=open(file_relations, 'r').readlines()
    L=[]
    Opp={}
    for line in lines[1:]:
	## split pair of words
        tokens=line.replace('\r\n','').replace('\n','').split(',')[0].split('+')[1].split('_')
        L.append(tokens[0]+','+tokens[1])
    for line in lines[1:]:
        tokens=line.replace('\r\n','').replace('\n','').split(',')[0].split('+')
	words=tokens[1].split('_')
        if (words[1]+','+words[0]) not in L:
            Opp[words[1]+','+words[0]]='oppos_'+tokens[0]
 
    writer=codecs.open(oppos_out,'w')
    for key,value in Opp.iteritems():
        writer.write(value+','+key+'\n')
    writer.close()

	
    lines=codecs.open(file_relations,'r').readlines()
    L2={}
    L3={}
    L4=[]
    for line in lines[1:]:
        tokens=line.replace('\n','').split(',')[0].split('+')
	words=tokens[1].split('_')
        if tokens[0] not in L2:
            L2[tokens[0]]=[]
        if tokens[1] not in L2[tokens[0]]:
            L2[tokens[0]].append(words[0]) 
        L3[words[0]+','+words[1]]=tokens[0]+','+words[0]+','+words[1]
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


def main(argv):
	rels=''
	oppos=''
	shuff=''
	try:
		opts, args = getopt.getopt(argv,"s:",["seman="])
	except getopt.GetoptError:
		print 'generate_NS.py -s <semanticrels>'
		sys.exit(2)
	for opt, arg in opts:
		if opt in ("-s", "--seman"):
			semantic=arg
		
	shuffle_relations(sematic,semantic+'.oppos.csv',semantic+'.shuff.csv')

if __name__ == "__main__":
   main(sys.argv[1:])


