#! /usr/bin/perl -w

use strict;
use warnings;
use autodie;

my $keyword = $ARGV[0];

&lookup($keyword);

sub lookup()
{
    my ($key) = @_;

    my $cmd = "dict $key | gview -";
    system($cmd);
}
