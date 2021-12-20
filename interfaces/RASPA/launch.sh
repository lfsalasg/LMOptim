#/bin/bash

function displaytime {
  local T=$1
  local D=$((T/60/60/24))
  local H=$((T/60/60%24))
  local M=$((T/60%60))
  local S=$((T%60))
  (( $D > 0 )) && printf '%d-' $D
  printf "%02.0f:" $H
  printf "%02.0f:" $M
  printf "%02.0f" $S
}

function Help(){
	echo -e "Run a set of isoterms based a set of P-T conditions\n"
	echo -e "Syntaxis: launch.sh [OPTIONS] <project_name>\n"
	echo -e "[OPTIONS]:"
	echo -e "\t-h: Show help"
	echo -e "\t-d: Specify the name of the datafile. Otherwise is ./fugacity.dat"
	echo -e "\t-t: Set the max time to run each project. Otherwise the script assigns time according to the built-in function (also if 0). Time in minutes.\n"
	echo "Prepared by Luis Salas"
}

#Default parameters
datafile="./fugacity.dat"
manTime=0

while getopts ":hd:t:" option; do
    case $option in
        h) #Display help
            Help
            exit;;
        d) #Data file with P and T
            datafile=$OPTARG;;
		t) #Max time for each launched job
			manTime=$OPTARG;;
        \?) #Invalid option
            echo "Error: Given options $OPTARG are invalid"
            exit;;
    esac
done


NAME=${@:$OPTIND:1}'_'
DATA=$(wc  -l < $datafile)


echo $DATA points found...

for i in $(seq 1 $DATA)
do
	#Create a new folder and move everything 
	mkdir $NAME$i
	cp simulation.input $NAME$i
	cp run.sh $NAME$i
	cp pseudo_atoms.def $NAME$i
	cp MFI1.cssr $NAME$i
	cp force_field_mixing_rules.def $NAME$i
	cp force_field.def $NAME$i
	cp CO2.def $NAME$i
	cp $datafile $NAME$i/fugacity.dat
	
	cd $NAME$i
	
	#Replace the values from fugacity.dat to simulation.input
	LINE1=$(cat fugacity.dat | awk 'NR=='$i' {print $1}')
	LINE2=$(cat fugacity.dat | awk 'NR=='$i' {print $2}')
	sed -i 's/pressure/'$LINE1'/' simulation.input
	sed -i 's/temperature/'$LINE2'/' simulation.input
	#mv simulation.input2 simulation.input
	
	sed -i 's/filename/'$NAME$i'/' run.sh
	#Set max time
	LC_NUMERIC="C"
	pressure=$(printf "%f" $LINE1)

	if [ $manTime -eq 0 ]
	then	
		maxTime=$(echo "(0.019146 * $pressure + 149.8)*1.2" | bc)
	else
		maxTime=$manTime
	fi
	maxTime=$(echo $maxTime | awk '{print int($1)*60}')
	maxTime=$(displaytime $maxTime)
	sed -i 's/maxTime/'$maxTime'/' run.sh


	sbatch run.sh
	echo Launching job with T=$LINE2 and P=$LINE1. Max time=$maxTime
	cd ..
done

mkdir ../../tmp/$NAME
cp ../../workplace/RASPA/* ../../tmp/$NAME/
cd ../../tmp/$NAME

i=0


for p in params
do
	sed -i 's/{'$i'}/'$p'/' pseudo_atoms.def
	sed -i 's/{'$i'}/'$p'/' force_field_mixing_rules.def
	sed -i 's/{'$i'}/'$p'/' force_field.def
	sed -i 's/{'$i'}/'$p'/' simulation.input
done

cd ../
tasks = $(wc  -l < $datafile)
i=0
while [ $i -le $tasks ]
do
	
	for core in cores
	do
		mkdir $NAME$i
		rsync -a $NAME/ $NAME$i
		
		cd $NAME$i

		#Replace the values from fugacity.dat to simulation.input
		LINE1=$(cat fugacity.dat | awk 'NR=='$i' {print $1}')
		LINE2=$(cat fugacity.dat | awk 'NR=='$i' {print $2}')
		sed -i 's/&1/'$LINE1'/' simulation.input
		sed -i 's/&2/'$LINE2'/' simulation.input
		bash run.sh
		i=$(($i+1))
		
		cd ../
	done
	wait
	
done


	
