#!/usr/bin/perl

# print unique lines in a file by preserving the order and retaining the latest
# of duplicated lines.

# You can also do this as a one liner. For example
# % cat input.txt | perl -MList::MoreUtils=uniq -e 'print reverse uniq reverse <>'

use List::MoreUtils qw(uniq);	# uniq guarantees the original order

@lines = <>;
@latest_unique = reverse uniq reverse @lines;
print @latest_unique;


# sample usage
# rajulocal@hogwarts:~/work/rutils/perl/latest_unique$ ./latest_unique.pl input.txt 
# ls -al
# top
# cd /usr/bin
# whoami
# ls -rt
# rajulocal@hogwarts:~/work/rutils/perl/latest_unique$ cat input.txt 
# whoami
# ls -al
# top
# whoami
# ls -rt
# cd /usr/bin
# whoami
# ls -rt
#
# cleaning up bash history
# rajulocal@hogwarts:~$ ~/work/rutils/perl/latest_unique/latest_unique.pl ~/.bash_history  > ~/.bash_history_tmp
# rajulocal@hogwarts:~$ mv ~/.bash_history_tmp ~/.bash_history

