pwd
#if [ $PAGES -ne $COUNTPAGES ] ; then
    #if [ $COUNTPAGES -ne 0 ] ; then
        #echo "Pages from codes and counts mismatches"
        #exit
    #fi
#fi

cd codes/
rm -f out.txt
for file in ./* ; do
    tesseract $file stdout | grep 978 >> out.txt
    echo "parsed codes$file code page"
done

cd ../counts/
rm -f out.txt
for file in ./* ; do
    convert $file -antialias -resize 200% $file
    tesseract $file -psm 6 stdout | grep [0-9] >> out_tmp.txt
    echo "parsed count$file count page"
done

# unroll digits one by one
for line in `cat out_tmp.txt`; do
    for letter in `echo $line | grep -o .`; do
        echo $letter >>  out.txt
    done
done

rm -f out_tmp.txt
cat out.txt
