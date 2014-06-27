#! /usr/bin/perl -w

# get the script name

# Sample usage:
# rajulocal@hogwarts:~$ work/rajuutils/perl/script_name.pl 
# full name = work/rajuutils/perl/script_name.pl
# script name = script_name.pl

use strict;
use warnings;

(my $fullname = $0);
(my $scriptname = $0) =~ s!.*/!!;

print "full name = $fullname\n";
print "script name = $scriptname\n";
