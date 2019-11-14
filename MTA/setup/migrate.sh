#!/bin/bash
# migrate.sh make -- initiate django db migrations and create index

cd "$(dirname "$0")"
pushd ../django_app/mta/
./manage.py migrate
./manage.py makemigrations
./manage.py migrate
python3 mta2014/create_index.py

# generate empty migration file, edit to update schema (not automatically generated by Django)
./manage.py makemigrations mta2014 --empty
pushd mta2014/migrations/
file=$(find . -iname 0002*)
file=${file:2}

ed -s $file <<< $'-2,$d\nwq'
sed -i '1s,^,DATABASE = "mta2014"\n,' $file

echo -e '\n\toperations = [' >>  $file
echo -e '\t\tmigrations.RunSQL(' >>  $file
echo -e '\t\t\t"ALTER TABLE {}_trip ALTER COLUMN created SET DEFAULT statement_timestamp()".format(DATABASE),' >> $file
echo -e '\t\t),' >> $file
echo -e '\t\tmigrations.RunSQL(' >>  $file
echo -e '\t\t\t"ALTER TABLE {}_vehicle ALTER COLUMN created SET DEFAULT statement_timestamp()".format(DATABASE),' >> $file
echo -e '\t\t)' >> $file
echo -e '\t]' >> $file

sed -i $'s/\t/    /g' $file

pushd ../../
./manage.py migrate
