#! /usr/bin/perl -w

# Remove empty lines, commented lines before printing the contents of a file.

use strict;
use warnings;

&print_sources_list($ARGV[0]);

sub print_sources_list
{
    my ($fname) = @_;
    open my $FNAME, "<", $fname;
    my @lines = <$FNAME>;
    close $FNAME;

    foreach my $line (@lines)
    {
        if ($line =~ /^\s*$/) 
        {
            next;
        }
        if ($line =~ /^\s*#/)
        {
            next;
        }
        print $line;
    }
}
