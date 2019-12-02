#!/bin/zsh

touch codes.txt

ctr=0

for i in `ls train`
do
	j=${i: : -4}
	cp 'train/'$i 'test/image'$ctr'.png'
	echo -e $j >> codes.txt
	ctr=$((ctr + 1))
done