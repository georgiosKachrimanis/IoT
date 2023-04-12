
#! /usr/bin/env python
# Be careful there are different operators for integers and strings
# The scripting language is really strict with spaces...

with open('run.sh', 'w') as rsh:
    rsh.write('''
#! /usr/bin/bash    
count=10
read -p "Enter  a number: " number
if [ $count -gt  $number ] # There is a whole list of operators you can use.
then
  echo "condition is true $count is > $number"
elif [ $count -eq $number ]
then
        echo "The numbers are equal"
else
        echo "condition is false $count is NOT  > $number"
fi

echo  "test case number 2"

if (( $count >  $number )) # There is a whole list of operators you can use.
then
  echo "condition is true $count is > $number"
else
echo "condition is false $count is not > $number"
fi

    ''')
