# -*- coding: utf-8 -*-
"""Preprocess the dataset"""

import codecs
from math import sqrt
import sys, getopt
relations=['event','hyper','mero','collective_noun','prefix$pre','prefix$re','prefix$anti','noun_singplur',
'verb_3rd','verb_3rd_past','verb_3rd','verb_past','ATTRIBUTE$Action:ObjectAttribute','ATTRIBUTE$Object:TypicalAction(noun.verb)',
'ATTRIBUTE$ObjectState(noun:noun)','CASERELATIONS$Action:Object','CASERELATIONS$Action:Recipient','CASERELATIONS$Agent:Instrument',
'CASERELATIONS$Agent:Object','CASERELATIONS$Agent:Recipient','CASERELATIONS$Object:Instrument','CASERELATIONS$Object:Recipient',
'CASERELATIONS$Recipient:Instrument','CAUSE-PURPOSE$Action/Activity:Goal','CAUSE-PURPOSE$Agent:Goal','CAUSE-PURPOSE$Cause:CompensatoryAction',
'CAUSE-PURPOSE$Cause:Effect','CAUSE-PURPOSE$EnablingAgent:Object','CAUSE-PURPOSE$Instrument:Goal','CAUSE-PURPOSE$Instrument:IntendedAction',
'CAUSE-PURPOSE$Prevention','CLASS-INCLUSION$Functional','CLASS-INCLUSION$PluralCollective','CLASS-INCLUSION$SingularCollective',
'CLASS-INCLUSION$Taxonomic','PART-WHOLE$Activity:Stage','PART-WHOLE$Collection:Member','PART-WHOLE$Creature:Possession',
'PART-WHOLE$Event:Feature','PART-WHOLE$Item:TopologicalPart','PART-WHOLE$Mass:Potion','PART-WHOLE$Object:Component',
'PART-WHOLE$Object:Stuff','REFERENCE$Concealment','REFERENCE$Expression','REFERENCE$Knowledge','REFERENCE$Plan',
'REFERENCE$Representation','REFERENCE$Sign:Significant','SPACE-TIME$Attachment','SPACE-TIME$Contiguity','SPACE-TIME$Item:Location',
'SPACE-TIME$Location:Action/Activity','SPACE-TIME$Location:Instrument/AssociatedItem','SPACE-TIME$Location:Process/Product',
'SPACE-TIME$Sequence','SPACE-TIME$TimeAction/Activity','lvc','vn-deriv']
    
def pick_random_relations(n):
    relat=[]
    k=len(relations)
    for i in range(n):
        relat.append(ralat[randint(0,k)])
    return relat

import numpy as np

def generate_random_vectors(file_lexicon, out):
	reader=codecs.open(file_lexicon, 'r')
	writer=codecs.open(out, 'w')
	for line in reader.readlines():
		line=line.replace('\n','')
		vec=np.random.uniform(-0.3, 1.0, size=(1,300)) ## the normalized vector won't be in [0.3,1], may be fix be
		unit=(vec/np.linalg.norm(vec)).tolist()[0]
		writer.write(line+' '+' '.join(map(str, unit))+'\n')
	reader.close()
	writer.close()

def count_pairs_diff_relations(filename):
    reader=codecs.open(filename,'r')
    pairs={}
    for line in reader.readlines():
        tokens=line.split(',')
        if   (tokens[1]+','+tokens[2]) not in pairs:  
                pairs[tokens[1]+','+tokens[2]]=[]

        pairs[tokens[1]+','+tokens[2]].append(tokens[0])
    k=0
    for key,value in pairs.iteritems():
        if len(value)>1:
            print key.replace('\n','') + ':'+', '.join(value) 
            k+=1
    print 'Total:', k
 
## leave only those relations where both words have corresponding vectors
def intersect_data_vectors(file_relations, file_vectors_vocab,out):
    reader=codecs.open(file_vectors_vocab,'r')
    vocab=[]
    for line in reader.readlines():
        line=line.replace('\n','').replace(' ','')
        if line not in vocab:
            vocab.append(line)
            
    reader.close() 
    print 'Vocabularity size:', len(vocab), ',', vocab[1], '.'
    reader=codecs.open(file_relations,'r')
    writer=codecs.open(out,'w')
    k=0
    for line in reader.readlines():
        line=line.replace('\n','')
        tokens=line.split(',')
        if (tokens[1] in vocab) and (tokens[2] in vocab):
            writer.write(line+'\n')
            print line
            k+=1
    print 'Number of word vectors:',k
            
    writer.close()
    reader.close()


def create_word_vectors_concat(file_relations,file_vectors, out):
    vectors={}
    reader=codecs.open(file_vectors,'r')
    for line in reader.readlines():
        line=line.replace(' \n','').replace('\n','')
        if '3000000' not in line:## w2v --> skip the first line
                tokens=line.split(' ')
                vectors[tokens[0]]=map(float,tokens[1:])
    print 'Volume:', len(vectors)
    reader.close()
    writer=codecs.open(out,'w')
    reader=codecs.open(file_relations,'r')
    for line in reader.readlines():
        tokens=line.replace('\n','').split(',')
        if ((tokens[1] in vectors) and (tokens[2] in vectors)):
                if (tokens[1]<>tokens[2]):
                       writer.write(tokens[0]+'+'+'_'.join(tokens[1:])+' '+' '.join(map(str,vectors[tokens[1]]))+' '+' '.join(map(str,vectors[tokens[2]]))+'\n')
    writer.close()

    
def create_word_vectors(file_relations,file_vectors, out): 
    vectors={}
    reader=codecs.open(file_vectors,'r')
    for line in reader.readlines():
        line=line.replace(' \n','').replace('\n','')
       	tokens=line.split(' ')
        vectors[tokens[0]]=map(float,tokens[1:])
    print 'Volume:', len(vectors)
    reader.close()
    writer=codecs.open(out,'w')
    reader=codecs.open(file_relations,'r')
    for line in reader.readlines():
        tokens=line.replace('\n','').split(',')
	if ((tokens[1] in vectors) and (tokens[2] in vectors)):
		if (tokens[1]<>tokens[2]):
        		diff=[b-a for a,b in zip(vectors[tokens[1]],vectors[tokens[2]])]
        		writer.write(tokens[0]+'+'+'_'.join(tokens[1:])+' '+' '.join(map(str,diff))+'\n')
    writer.close()

import numpy as np
def count_distances(file_relations,file_vectors, out): 
    vectors={}
    reader=codecs.open(file_vectors,'r')
    for line in reader.readlines():
        line=line.replace(' \n','').replace('\n','')
        tokens=line.split(' ')
        vectors[tokens[0]]=map(float,tokens[1:])
    print 'Volume:', len(vectors)
    reader.close()
    writer=codecs.open(out,'w')
    reader=codecs.open(file_relations,'r')
    for line in reader.readlines():
        tokens=line.replace('\n','').split(',')
        diff=[b-a for a,b in zip(vectors[tokens[1]],vectors[tokens[2]])]
        res=sqrt(sum(map(lambda x: pow(x,2), diff)))
	cos=np.dot(vectors[tokens[1]],vectors[tokens[2]])/(sqrt(np.dot(vectors[tokens[1]],vectors[tokens[1]]))*sqrt(np.dot(vectors[tokens[2]],vectors[tokens[2]])))
        writer.write(tokens[0]+'+'+'_'.join(tokens[1:])+' '+str(res)+' '+str(cos)+'\n')
    writer.close()
    
def check_normalized(file_vectors):
    reader=codecs.open(file_vectors,'r') 
    for i in range(0,9):
        line=reader.readline().replace(' \n','').replace('\n','')
        tokens=line.split(' ')[1:]
        values=map(float,tokens)
        result=sum(map(lambda x: pow(x, 2),values))
        print sqrt(result)
    reader.close()
    
def generate_ext_vocab(file_relations,out):
    dic=[]
    reader=codecs.open(file_relations,'r')
    for line in reader.readlines():
        tokens=line.replace('\n','').split(',')
        if tokens[1] not in dic:
            dic.append(tokens[1])
        if tokens[2] not in dic:
            dic.append(tokens[2])
    reader.close()
    writer=codecs.open(out,'w')
    rand=[]
    for item1 in dic:
        for item2 in dic:
            if (item1!=item2):
                writer.write('rand,'+item1+','+item2+'\n')
    writer.close()        

def main(argv):
	semantic=''
	vector=''
	output=''
	try:
		opts, args = getopt.getopt(argv,"s:v:o:",["seman=","vectors=", "output="])
	except getopt.GetoptError:
		print 'preprocess.py -s <semanticrels> -v <vectors> -o <outputfile>'
		sys.exit(2)
	for opt, arg in opts:
		if opt in ("-s", "--seman"):
			semantic=arg
		elif opt in ("-v", "--vectors"):
			vector=arg
		elif opt in ("-o","--output"):
			output=arg
	create_word_vectors(semantic,vector,output)

if __name__ == "__main__":
   main(sys.argv[1:])



#create_word_vectors('word_pairs_9classes.NOISE2.csv', '../data/GoogleNews-vectors-negative300.fx.txt','word_pairs_9classes.NOISE3.csv.vec')        

