# Process the csv file
python3 sleeprating.py
cd data
sed -i .bak '1s/^/Time,Phase\'$'\n/g' actual_data.csv
sshpass -p 'blazingasians' scp sleeprating.txt asians@46.101.14.145:/var/www/html
sshpass -p 'blazingasians' scp actual_data.csv asians@46.101.14.145:/var/www/html
