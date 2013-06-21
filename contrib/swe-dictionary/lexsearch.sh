#!/bin/bash

if [ -z "$2" ]
then
    grep -Pni "^$1\t" swe030224STA.dict
else
    grep -Pni "^$1\t" $2
fi

# echo en text där backslash escapade tecken tolkas
# echo -e "bamseflarn kalasmat\t" > af.txt



