#! /usr/bin/perl -w

# get the overlap of two sets of data
#
# sample usage
#
# rajulocal@hogwarts:~/work/rutils/perl/overlap$ ./overlap.pl 
# set           	 count 	 pct
# A             	 5 	 0.71
# B             	 4 	 0.57
# A or B        	 7 	 1.00
# A and B       	 2 	 0.29
# A - B         	 3 	 0.43
# B - A         	 2 	 0.29
# notA and notB 	 0 	 0.00
# storing output files under out directory


use strict;
use warnings;
use Getopt::Long;

use File::Path qw(make_path);
use File::Spec::Functions qw(catfile);

my ($scriptname, $usage, $debug, $report);

my ($fileA, $fileB);

&parse_arguments();
&validate_arguments();

open my $hdA, '<', $fileA;
chomp(my @dataA = <$hdA>);
close $hdA;

open my $hdB, '<', $fileB;
chomp(my @dataB = <$hdB>);
close $hdB;

my %hash_dataA = map { $_ => 1 } @dataA;
my %hash_dataB = map { $_ => 1 } @dataB;

my (%hash_AorB, %hash_AandB, %hash_inAnotB, %hash_inBnotA, %hash_notAnotB);


foreach my $key (keys %hash_dataA)
{
    $hash_AorB{$key} = 1;
}
foreach my $key (keys %hash_dataB)
{
    $hash_AorB{$key} = 1;
}

my $unique_elem = keys %hash_AorB;

foreach my $key (keys %hash_AorB)
{
    if (defined $hash_dataA{$key})
    {
        if (defined $hash_dataB{$key})
        {
            $hash_AandB{$key} = 1;
        }
        else
        {
            $hash_inAnotB{$key} = 1;
        }
    }
    elsif (defined $hash_dataB{$key})
    {
        $hash_inBnotA{$key} = 1;
    }
    else
    {
        $hash_notAnotB{$key} = 1;
    }
}

my $stats_hr = &get_stats();
&print_stats();

my %fname_hr;
$fname_hr{'odir'} = 'out';
$fname_hr{'file_AorB'} = 'out_AorB.txt';
$fname_hr{'file_AandB'} = 'out_AandB.txt';
$fname_hr{'file_onlyA'} = 'out_onlyA.txt';
$fname_hr{'file_onlyB'} = 'out_onlyB.txt';
$fname_hr{'file_notAnotB'} = 'out_notAnotB.txt';

&make_path($fname_hr{'odir'});
# mkdir($fname_hr{'odir'}) unless (-d $fname_hr{'odir'});  // use if make_path is not available
print "storing output files under $fname_hr{'odir'} directory\n";
&write_hash_keys_to_file(\%hash_AorB,     catfile($fname_hr{'odir'}, $fname_hr{'file_AorB'})     );
&write_hash_keys_to_file(\%hash_AandB,    catfile($fname_hr{'odir'}, $fname_hr{'file_AandB'})    );
&write_hash_keys_to_file(\%hash_inAnotB,  catfile($fname_hr{'odir'}, $fname_hr{'file_onlyA'})    );
&write_hash_keys_to_file(\%hash_inBnotA,  catfile($fname_hr{'odir'}, $fname_hr{'file_onlyB'})    );
&write_hash_keys_to_file(\%hash_notAnotB, catfile($fname_hr{'odir'}, $fname_hr{'file_notAnotB'}) );


sub parse_arguments
{
    ($scriptname = $0) =~ s!.*/!!;

    $usage = qq(
$scriptname = compute overlap between two files

Switches:
-debug : print debugging output (default: off)

optional arguments:
-fa  : first file name (default: setA.txt)
-fb  : second file name (default: setB.txt)
);
    my ($opt_help);
    GetOptions("help" => \$opt_help,
        "fa=s" => \$fileA,
        "fb=s" => \$fileB,
        "debug" => \$debug
        );
    die $usage if defined $opt_help;

    unless (defined $fileA)
    {
        $fileA = "setA.txt";
    }

    unless (defined $fileB)
    {
        $fileB = "setB.txt";
    }

    unless (defined $debug)
    {
        $debug = 0;
    }

    $report .= "Arguments: \n" .
        "fa\t$fileA\n" .
        "fb\t$fileB\n" .
        "debug\t$debug\n";
}

sub validate_arguments()
{
    print $report if ($debug);

    # do the input files exist and are readable?
    unless (-f $fileA and -r $fileA)
    {
        die "unable to read from $fileA: $!";
    }
    unless (-f $fileB and -r $fileB)
    {
        die "unable to read from $fileB: $!";
    }
}

sub get_stats()
{
    my %stats_hash;

    $stats_hash{'num_A'} = keys %hash_dataA;
    $stats_hash{'num_B'} = keys %hash_dataB;
    $stats_hash{'num_AorB'} = keys %hash_AorB;
    $stats_hash{'num_AandB'} = keys %hash_AandB;
    $stats_hash{'num_onlyA'} = keys %hash_inAnotB;
    $stats_hash{'num_onlyB'} = keys %hash_inBnotA;
    $stats_hash{'num_notAnotB'} = keys %hash_notAnotB;

    $stats_hash{'pct_A'}     = $stats_hash{'num_A'} / $stats_hash{'num_AorB'};
    $stats_hash{'pct_B'}     = $stats_hash{'num_B'} / $stats_hash{'num_AorB'};
    $stats_hash{'pct_AorB'}  = $stats_hash{'num_AorB'} / $stats_hash{'num_AorB'};
    $stats_hash{'pct_AandB'} = $stats_hash{'num_AandB'} / $stats_hash{'num_AorB'};
    $stats_hash{'pct_onlyA'} = $stats_hash{'num_onlyA'} / $stats_hash{'num_AorB'};
    $stats_hash{'pct_onlyB'} = $stats_hash{'num_onlyB'} / $stats_hash{'num_AorB'};
    $stats_hash{'pct_notAnotB'} = $stats_hash{'num_notAnotB'} / $stats_hash{'num_AorB'};

    return \%stats_hash;
}

sub print_stats()
{
    # print "count A       = $stats_hr->{'num_A'}\n";
    # print "count B       = $stats_hr->{'num_B'}\n";
    # print "count A or B  = $stats_hr->{'num_AorB'}\n";
    # print "count A and B = $stats_hr->{'num_AandB'}\n";
    # print "count A - B   = $stats_hr->{'num_onlyA'}\n";
    # print "count B - A   = $stats_hr->{'num_onlyB'}\n";
    # print "count notA and notB = $stats_hr->{'num_notAnotB'}\n";


    printf "set           \t count \t pct\n";
    printf "A             \t $stats_hr->{'num_A'} \t %.2f\n",        $stats_hr->{'pct_A'};
    printf "B             \t $stats_hr->{'num_B'} \t %.2f\n",        $stats_hr->{'pct_B'};
    printf "A or B        \t $stats_hr->{'num_AorB'} \t %.2f\n",     $stats_hr->{'pct_AorB'} ;
    printf "A and B       \t $stats_hr->{'num_AandB'} \t %.2f\n",    $stats_hr->{'pct_AandB'};
    printf "A - B         \t $stats_hr->{'num_onlyA'} \t %.2f\n",    $stats_hr->{'pct_onlyA'};
    printf "B - A         \t $stats_hr->{'num_onlyB'} \t %.2f\n",    $stats_hr->{'pct_onlyB'};
    printf "notA and notB \t $stats_hr->{'num_notAnotB'} \t %.2f\n", $stats_hr->{'pct_notAnotB'};
}

sub write_hash_keys_to_file()
{
    my ($hashref, $ofname) = @_;
    print "writing to $ofname\n" if $debug;

    open my $OFNAME, ">", $ofname;

    foreach my $key (sort keys %$hashref)
    {
        print $OFNAME $key, "\n";
    }
    close $OFNAME;
}
