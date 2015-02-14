#! /usr/bin/perl -w

# Display the status of an installed application that matches a keyword
# For example
# <scriptname> octave
# will show the status of all the applications that contain the keyword octave
# in their names.

# after writing this script, I found out that the same functionality can be
# achieved by "apt-show-versions -r keyword". But I am keeping this script
# around for reference.

use strict;
use warnings;
use autodie;

my $keyword = $ARGV[0];
my $debug = 0;

&upgrade_by_keyword($keyword);

sub upgrade_by_keyword()
{
    (my $scriptname = $0) =~ s!.*/!!g;

    my $usage = qq(
# Display the status of an installed application that matches a keyword
# usage:
# $scriptname <keyword>
#
# For example
# $scriptname octave
# will show the status of all the applications that contain the keyword octave
# in their names.
    );

    my ($keyword) = @_;
    if ($keyword)
    {
        print "keyword = $keyword\n" if $debug;
    }
    else
    {
        print "$usage\n";
        die "Error: no keyword supplied. aborting...";
    }

    my $cmd = "dpkg -l \*$keyword\* | grep ^ii | awk '{print \$2}'";
    print "cmd = $cmd\n" if $debug;
    chomp(my @apps =`$cmd`);
    if (@apps)
    {
        print "apps = @apps\n" if $debug;
        $cmd = "apt-show-versions @apps";
        system($cmd);
    }
}
