#!/usr/bin/perl5.16
while (<>) { 
        next if /^#/;
        chomp;
        @a=split(/\t/,$_); 
        %b = map{split (/=/, $_)} split (/;/,$a[8]);
        print join("\t", ($a[0], $a[3],$b{ID},$b{Reference_seq},$b{Variant_seq},'.','.',$a[8], '1|0', '1|1' )), "\n";
}
