#!/usr/bin/perl -w
# Courtesy : John Orr <john.orr@catapult.com> posted on vim mailing list.

use strict;
my $v = 'vim -f';
my $vd = 'vim -d -f';

my $dir = '.';
if (scalar @ARGV)
{
    $dir = $ARGV[0];
}
my $cmd = "find $dir -maxdepth 1 -name '.*.sw*'";
# my $cmd = "find $dir -name '.*.sw*'";
my @files=`$cmd`;

foreach my $file (@files)
{
    my $filepath;
    my $filename;
    my $newfile;
    my $oldfile;
    chomp $file;
    if ($file =~ /^(.*)\/\.(.*)\.sw.$/)
    {
        $filepath = $1;
        $filename = $2;
        $oldfile = "$filepath/$filename";
        $newfile = $filepath . "/new_" . $filename;
        $cmd = "$v -r $file -c 'write $newfile|quit'";
        print "$cmd\n";
        system($cmd);
        unlink "$file";

        if (system("diff '".$oldfile."' '".$newfile."'"))
        {
            # Files differ
            print "'$oldfile' differs from '$newfile'\n";
            system("$vd '$oldfile' '$newfile'");
        }
        else
        {
            print "'$oldfile' not changed\n";
            unlink "$newfile";
        }
    }
}
