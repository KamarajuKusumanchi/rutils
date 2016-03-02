#! /usr/bin/env perl

# Sample usage
#
# % make_bkup.pl ~/.vimrc
# /home/rajulocal/.vimrc -> /home/rajulocal/.vimrc_RK_20160302_073829
#
# % make_bkup.pl ~/.vimrc
# /home/rajulocal/.vimrc --> /home/rajulocal/.vimrc_RK_20160302_073829

use strict;
use warnings;
use autodie;
use File::Spec;   # for rel2abs
use Date::Format; # for time2str
use Getopt::Long; # for GetOptions

my $debug=0;
my $dry_run=0;
my $usage;
my $scriptname;

my $fname;

&parse_arguments();
&make_bkup($fname);

sub parse_arguments()
{
    ($scriptname = $0) =~ s!.*/!!;
    my ($help);

    $usage = qq(
$scriptname = Make backup of a file.
Syntax:
$scriptname <Option(s)> filename
Options:
  -debug        : print debugging output (default : off);
  -dry          : dry run. Do not execute the commands (default : off);
  -help         : print this help message (default : off);
);

    GetOptions("help!" => \$help,
               "debug!" => \$debug,
               "dry!" => \$dry_run);

    die $usage if defined $help;
    
    $fname = $ARGV[0];
    if (!(defined $fname))
    {
        print "Error: unable to determine the file that needs to be backed up.\n";
        die $usage;
    }
}

sub last_modified_on()
{
    my ($fname) = @_;
    my $date_time = time2str("%Y%m%d_%H%M%S", (stat($fname))[9]);
    return $date_time;
}

sub get_dest_file_name()
{
    my ($src, $midfix) = @_;
    my $src_abs = File::Spec->rel2abs( $src );
    # get the directory from a file path
    my ($src_volume, $src_dir, $src_file) = File::Spec->splitpath( $src_abs );

    print "src_abs = $src_abs\n" if $debug;
    print "src_volume = $src_volume\n" if $debug;
    print "src_dir = $src_dir\n" if $debug;
    print "src_file = $src_file\n" if $debug;
    
    my ($dest_volume, $dest_dir, $dest_file, $dest_abs);

    $dest_volume = $src_volume;
    if (-w $src_dir)
    {
        $dest_dir = $src_dir;
    }
    else
    {
        my $tmp_dir= "$ENV{HOME}/x";
        $dest_dir = $tmp_dir;
    }

    # Todo:- make this user definable
    $midfix = "_RK_" unless defined($midfix);
    print "midfix = $midfix\n" if $debug;

    $dest_file = $src_file . $midfix . &last_modified_on($src_abs);

    $dest_abs = File::Spec->catpath($dest_volume, $dest_dir, $dest_file);

    print "dest_volume = $dest_volume\n" if $debug;
    print "dest_dir = $dest_dir\n" if $debug;
    print "dest_file = $dest_file\n" if $debug;
    print "dest_abs = $dest_abs\n" if $debug;

    return $dest_abs;
}

sub make_bkup()
{
    my ($src_abs) = @_;
    my $dest_abs = &get_dest_file_name( $src_abs );

    if (!(-e $dest_abs))
    {
        my $cmd = "cp $src_abs $dest_abs";
        print "$src_abs -> $dest_abs\n";
        system($cmd) unless $dry_run;
    }
    else
    {
        warn "$dest_abs already exists. Using force copy.\n" if $debug;
        my $cmd = "cp -f $src_abs $dest_abs";
        # The two minus signs in the output signify that a force copy is used.
        print "$src_abs --> $dest_abs\n";
        system($cmd) unless $dry_run;
    }

    print "This is a dry run\n" if ($dry_run);
}
