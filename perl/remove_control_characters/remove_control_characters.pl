#! /usr/bin/perl

# remove the control characters in files titled YYYY-MM-DD.txt
#
# A bash equivalent of this script is
# rajulocal@hogwarts ~/work/rutils/perl/remove_control_characters/data
#  % for i in 2015-01-02.txt  2015-02-04.txt  2015-03-17.txt
# do
# echo $i | cut -f 1 -d'.'
# perl -p -e "s/([\000-\037]{3})./\n/g" $i | perl -p -e "s/\015<br>/\n/g" | grep -v '^$'; done
# 2015-01-02
# IBM     100
# SPY     200
# 2015-02-04
# SPY     100
# IBM     200
# 2015-03-17
# RTY     100
# AAAPL   200
# VZ      50
#

use strict;
use warnings;

my @files=@ARGV;
foreach my $file (@files)
{
	if ($file =~ m/(\d\d\d\d-\d\d-\d\d)\.txt/)
	{
		my $date=$1;
		print "$date\n";
		# read and print the file contents
		open(my $IFNAME, '<', $file);
		while (<$IFNAME>)
		{
			s/([\000-\037]{3})./\n/g;
			s/\015<br>/\n/g;
			print $_;
		}
		close($IFNAME);
	}
}

# sample usage
# rajulocal@hogwarts ~/work/rutils/perl/remove_control_characters
#  % ./remove_control_characters.pl data/*txt  | grep -v '^$'
# 2015-01-02
# IBM     100
# SPY     200
# 2015-02-04
# SPY     100
# IBM     200
# 2015-03-17
# RTY     100
# AAAPL   200
# VZ      50
# 
