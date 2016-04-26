This directory contains variant calls, error-corrected reads, and
mappings for the sequencing data for the NA12787 cell line.
 
Files included in this directory:

sorted_final_merged.bam - Contains all raw continuous long reads
 mapped using blasr v1.3.2 to the hg19 human reference genome.

sorted_final_merged.bam.bai - Accompanying bam index for
 sorted_final_merged.bam file.

corrected_reads_gt4kb.fasta - Error-correction of all reads was
    performed using Falcon following the general principles proposed
    in Chin et al. In short, all long reads greater than 3kb are
    aligned to one another using Blasr. These reads were then grouped
    together by selecting the top alignments (using a coverage cutoff
    of 40). A consensus was formed for each read; the resulting read
    was trimmed at the ends to eliminate potential chimeras and
    low-quality sequence (here we require at least 5X coverage of a
    given base). From this set reads greater than 4kb were used for
    consensus calling).

NA12878.sorted.vcf.gz - VCF file of structural variants. This file was
    produced using three different variant detection methods: PBHoney,
    a custom pipeline and (on assembled sequences) the Chaisson et
    al. methodology from "Resolving the complexity of the human genome
    using single-molecule sequencing" (Nature, 2015). Structural
    variations were classified simply as either a deletion or
    insertion. Each entry in this file is a member of the superset of
    all events called by all variant callers. Because calls were
    accepted based on the number of different variant callers that
    supported the event in question, the QUAL field is currently 
    not populated. If an event is predicted by at least 3 different
    variant callers, the FILTER field entry is simply PASS otherwise
    it is listed as lt3. While each of the methods used is imprecise
    on boundary calling by design, for each event, the most precise
    boundary definitions are indicated in the CIPOS field (and CIEND
    for deletion events). The NS field is a bit vector describing
    which caller configurations supported the event, Each position
    represents the conclusion of one caller in this order:

    	 1. PBHoney/rawReads/blasr1.3.1 
	 2. custom/rawReads/blasr1.3.1
	 3. PBHoney+ECReads+blasr1.3.1 
	 4. custom+ECReads+blasr1.3.1
	 5. assembly
	 6. custom+ECReads+blasr1.3.2
	 7. custom+rawReads+blasr1.3.2

    A bit vector of 0101111 for example, meant that the event was
    supported by the second, fourth, fifth, sixth and seventh
    combination of mappers and event callers in that list.  Note,
    if an assembly based call (5 column) is not present then the SV
    pos (and end) reflect a buffer (50bp for custom pipeline and 100bp
    for PBHoney); note, this buffer is also added (times 2) to the 
    SVLEN field.

    There are two additional flags included in the INFO field: 

    	  BL - An event which was not called by a method using blasr
    	  v1.3.1 which WAS subsequently called using the same variant
    	  caller paired with blasr 1.3.2.
	  
	  ZU - An event for which phasing was not possible or for
    	  which zygosity could not be reliably determined. The
    	  genotype for these events in NA12878 is listed as 0/1 by
    	  default.  Note, because the phasing approach used our
    	  knowledge of raw reads, variants calling from assembly were
    	  NOT attempted for phasing analysis.

    The genotype field is populated based on spanning raw reads.  In
    the case of no reads supporting the reference a column is marked
    as homozygous (1/1); in the case of a raw reads spanning an SV
    which intersected a proximal phased SNP, it is indicated as either
    paternal (1|0) or maternal (0|1). Here, there are two
    circumstances where the genotype 0/1 is employed. The first is
    if the variant is heterozygous but the phase could not be
    determined. The second is when the zygosity was not assessed
    (assembly). In both cases, the genotype is accompanied by a ZU
    flag in the entry's INFO field.
