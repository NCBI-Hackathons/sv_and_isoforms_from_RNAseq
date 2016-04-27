#!/usr/bin/perl -w
use strict;

my ($accessionFile, $fastaFile) = @ARGV;

open IN, "$accessionFile";
while (my $line = <IN>){
	chomp $line;
	my $cmd = "blastn_vdb -max_target_seqs 5000 -db $line -query $fastaFile -outfmt 6 -out $line.blastout\n";
	print $cmd;
	system $cmd;
}
close IN;

exit


#open FILELIST, "$accessionFile";
#while (my $file = <FILELIST>){
#	chomp $file;
#	open OUT, ">$file.blastout.BED";
#	open IN, "$file.blastout";
	###FILE CONTENTS###
	#gi|320461721|ref|NM_001202435.1|:1-8342	gnl|SRA|SRR1273697.45877182.2	100.000	76	0	0	5281	5356	1	76	8.52e-30	141
	#gi|320461721|ref|NM_001202435.1|:1-8342	gnl|SRA|SRR1273697.45877182.1	100.000	76	0	0	5422	5497	76	1	8.52e-30	141
	#gi|320461721|ref|NM_001202435.1|:1-8342	gnl|SRA|SRR1273697.45854432.2	100.000	76	0	0	4763	4838	1	76	8.52e-30	141
	###################
#	while (my $line = <IN>){
#		chomp $line;
#		my @clms = split(/\t/, $line);
#		my $start = $clms[6];
#		my $end = $clms[7];
		#my $begin = ($genStart-$end);
		#my $last = ($genStart-$start);
#		print OUT "$fastaFile\t$start\t$end\n";
#	}
#	close IN;
#	close OUT;
#}

		

