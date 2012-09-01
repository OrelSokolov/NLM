res1=`ls *.mp4`
if [ "$res1"  != "" ];
then
mv *.mp4 /home/oleg/vids/
fi

result=`ls *.flv`
if [ "$result"  != "" ];
then
mv *.flv /home/oleg/vids/
fi

echo "----------|/home/oleg/vids/|-----------"
ls /home/oleg/vids/
echo "----------|network|-----------"
ls
echo "----------|Uploading|-----------"
python "videos.py" "/home/oleg/vids/"

cd /home/oleg/vids/

result=`find *.flv`
if [ "$result"  != "" ]
then
rm *.flv
fi


result=`find *.mp4`
if [ "$result"  != "" ]
then
rm *.mp4
fi
	
echo "----------|/home/oleg/vids/|-----------"
ls /home/oleg/vids/
