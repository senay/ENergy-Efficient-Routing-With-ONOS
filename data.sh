#!/bin/bash
simulationTime=500
for i in # here place the file names that have the energy and time obtained from EMMA
do
	timeP=0
	timeN=0
	tot=0
	init=0
	RESULT=0
	counter=0
	flowConter=0
	totalEnergy=0
	while read power	time
	do	
		if [ $timeN -eq $init ]
		then
			timeP=$time
			timeN=$time
			counter=1
		else		
			timeP=$timeN
			timeN=$time
			counter=$(($counter+1))
		fi
		if [ $timeP -eq $timeN ]
		then
			tot=`echo $tot + $power | bc`
		else		 		
			RESULT=$(echo "$tot/$counter" | bc -l)
			timeDif=`expr $timeN - $timeP`
			RESULT=$(echo "$RESULT*$timeDif" | bc -l)
			totalEnergy=`echo $totalEnergy + $RESULT | bc`
			counter=0
			tot=0
		fi
	done < $i.'txt'
	flowCounter=$(expr $i*500 | bc)
	RESULT=$(echo "$totalEnergy/$flowCounter" | bc -l)
	RESULT=$(echo "$RESULT/$simulationTime" | bc -l)
	echo $flowCounter
	echo "$i	$RESULT" >>energy.dat
done
