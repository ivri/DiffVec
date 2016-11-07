from sklearn import cluster
from scipy import sparse as ssp
from sklearn import datasets
import numpy as np
from sklearn.metrics.pairwise import pairwise_distances,euclidean_distances,manhattan_distances,rbf_kernel
from math import pow,fabs,sqrt
from scipy.spatial.distance import pdist,squareform
#spectral_clustering
#affinity : array-like or sparse matrix, shape: (n_samples, n_samples)
#The affinity matrix describing the relationship of the samples to
#embed. **Must be symmetric**.

import sys,getopt,os
from sklearn.metrics import silhouette_score,homogeneity_score,adjusted_rand_score,v_measure_score


## the file format is like ATTRIBUTE$Action:ObjectAttribute+apple_picker 0.0355908 0.030281698 -0.0216665 -0.0733128 -0.0105301 0.2072842 
## '+' separates relation name from the word pair; $ stands for subclass
def load_data(filename,top):
    reader=open(filename,'r')
    X=[]
    words=[]
    pair_id=0
    class_ids={}
    id=0
    truth=[]
    for line in reader.readlines():
        tokens=line.split(' ')
        X.append(map(float, tokens[1:]))
        words.append(tokens[0])
        _class=line.split('+')[0]
	if top:
		if '$' in _class:
			_class=_class.split('$')[0]
		if _class=='CLASS-INCLUSION':
			_class='hyper'
		if _class=='PART-WHOLE':
			_class='mero'
        if _class not in class_ids.keys():
            class_ids[_class]=id
	    print _class	
            id+=1
        truth.append(class_ids[_class])
        pair_id+=1
    reader.close()
    return X,words,truth

def knn_sclustering(X,n_clust,k):
    print 'Basic spectral clustering using knn matrix'
    spectral = cluster.SpectralClustering(n_clusters=n_clust,n_neighbors=k,
                                        eigen_solver='arpack', affinity='nearest_neighbors')
    labels= spectral.fit(X).labels_
#    print 'SilL:',silhouette_score(X,labels)
    return labels

from decimal import *
import numpy as np
import scipy
def norm(a):
    return  1-round(float('{0:.4f}'.format(Decimal(a))),3)

##inversed cosine
def cos(X): 
    dist=np.zeros(shape=(X.shape[0],X.shape[0]))
    for i in range(X.shape[0]):
        for j in range(X.shape[0]):
            dist[i,j]=1.0-(np.dot(X[i],X[j])+0.000001)/(sqrt(np.dot(X[i],X[i]))*sqrt(np.dot(X[j],X[j]))+0.000001)
    return dist            

def affin_sclustering(X,n_clust, distance='euclid', gamma=0.1, std=1):
    print 'Basic spectral clustering using affinity matrix'
    if distance=='cosine':
        similarity=cos(X)#pairwise_distances(X, metric='cosine')
    elif distance=='euclid':
        dist=euclidean_distances(X)
        if std:
            similarity = np.exp(-gamma * dist/dist.std())
        else:
            similarity = np.exp(-gamma * dist)
    labels = cluster.spectral_clustering(similarity,n_clusters=n_clust, eigen_solver='arpack')
    return labels

def get_arguments(argv):
    file_vectors=''
    clust_type='affin'
    clusters=40
    distance='euclid'
    cluster_param=0
    std=1
    #Parse command line arguments
    try:
        opts, args = getopt.getopt(argv[1:], "f:c:n:d:p:s") #["help","file", "clustering", "number", "dist", "param", "std"])
        print opts,args
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-f", "--file"):
            file_vectors = arg
        elif opt in ("-c", "--clustering"):
            clust_type = arg
        elif opt in ("-n", "--number"):
            clusters = arg
        elif opt in ("-d", "--dist"):
            distance = arg
        elif opt in ("-p", "--param"):
            cluster_param = arg
        elif opt in ("-s", "--std"):
            std = 0     
        elif opt in ("-o", "--output"):
            outputdir = arg
    return file_vectors,clust_type, clusters, distance, cluster_param, std



def usage():
    usage_text = '''
    Script does spectral clustering of word embeddings provided in the standart format
    USAGE: ''' + os.path.basename(__file__) + ''' -f <file_vectors> -c <clust_type:affin, knn> -n <number_of_clusters> -d <distance:euclid, cosine> -p <parameter: gamma, k(NN)> [-s <std>]  -h (help) 

    '''
    print usage_text
    sys.exit(' ')


                    
def main(argv):
    file_vectors,clust_type, clusters, distance, cluster_param, std = get_arguments(argv)
    fname='.'.join(map(str,[file_vectors.split('/')[-1],clust_type, clusters, distance, cluster_param, std]))
    writer=open(fname,'w') ## better to put in EX1, EX2, .. folders
    print 'clustering:',clust_type
    print 'clusters:',clusters
    print 'cluster_param:',cluster_param
    print 'std:',std
        
    X,words,truth=load_data(file_vectors,True)
    X=np.array(X)
    
    if clust_type=='affin':
        labels=affin_sclustering(X, n_clust=int(clusters), distance=distance, gamma=float(cluster_param), std=bool(std)) 
    else:
        labels=knn_sclustering(X, n_clust=int(clusters), k=int(cluster_param)) 
    
    writer.write('\nVMeas:'+ str(v_measure_score(truth,labels)))
    writer.write('\nRand:'+str(adjusted_rand_score(truth,labels)))
    writer.write('\nHomogen:'+str(homogeneity_score(truth,labels))+'\n')
        
    i=0
    for word in words:
        writer.write(word+' : '+str(labels[i])+'\n')
        i+=1   
    writer.close()       
    #print labels
    
#-------------------------------
if __name__ == "__main__":
    if len(sys.argv[1:]) < 6:
        usage()
    else:
        main(sys.argv)
