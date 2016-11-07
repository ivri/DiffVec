## the files are expected to be in EX1, EX2, ..., EX\d folders 
for i in 10 20 30 40 50 60 70 80 #number of clusters
do
	sum=0
	for j in 1  2  3  4  5  6 #experiments
	do
		t=$(grep -Ph 'VMeas:([0-9.]+)' /EX"$j"/fname.affin."$i".euclid.0.1.1 | sed 's/VMeas://' | bc)
		sum=$(echo $sum + $t | bc) 
	done
	avg=$(echo "$sum/6.0" |bc -l)
	printf "Average input for clusters=$i  : %.3f\n" $avg
done
