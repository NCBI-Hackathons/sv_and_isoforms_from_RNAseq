

# Histogram given bed file 

"""
This module helps visualize what structural variants _might_ look
like, given RNA-seq data.

Usage:
    python2/3 base_histogram.py bed_file_list.txt pdf_file_name \
                                 sequence_length
Expected inputs: 
    bed_file_list.txt  -- a simple list as a txt file of blasout.BED files
    normalization_file.txt -- a file of the number of Mbases per read
                              this is used to normalize the abundances
    pdf_file_name      -- (str) name of pdf file to be created
    # Deprecated
    sequence_length   -- (int) (optional) length of the sequence
"""


import numpy as np
import matplotlib.pyplot as plt
import sys
import scipy.stats as stats



def populate_N(accessions, N=8597):
  """
  Thing. accessions = [[5, 90], [70, 88]]
  """
  hgram = [0 for i in range(N)]
  for acc in accessions:
    for h in range(acc[0], acc[1]):  # 566, 567, 568, ... acc[1]
      hgram[h] += 1 # increment
  return hgram



def single_hgram(hgram, title=None, fname='sample.pdf', show=False,
                 link=None):
  """ Show """
  import matplotlib.cm as cm
  plt.figure(dpi=150, figsize=(6,2))
  xs = list(range(len(hgram)))
  colors = [cm.jet(float(i)/max(hgram)) for i in hgram]
  for h in range(len(hgram)):
    b = plt.bar(xs[h], hgram[h], width=1., color=colors[h], 
                edgecolor=colors[h]) #alpha=colors[h],
    # b.set_urls(['http://www.ytmnd.com'])
  
  # Aesthetics 
  if title is not None:
    if link is not None:
      pass # Add a link here? 
    else:
      plt.title(title)
  plt.xlabel('Base')
  plt.ylabel('Relative coverage')
  if fname is not None:
    plt.savefig(fname)
  if show:
    plt.show()
  return



def multi_hgram(hgrams, title=None, fname=None, show=False,
                link=None):
  """ """
  import matplotlib.cm as cm
  plt.figure(dpi=150, figsize=(6,2))
  xs = list(range(max([len(h) for h in hgrams])))
  maxmax = max([max(hg) for hg in hgrams])
  # Color each line thing
  for hgram in hgrams:
    colors = [cm.jet(float(i)/maxmax) for i in hgram]
    for h in range(len(hgram)):
      plt.scatter(xs[h], hgram[h], marker='o', color=colors[h], s=2)
              #edgecolor='none') #alpha=colors[h], 
    plt.plot(xs[:len(hgram)], hgram, linewidth=1., color='k', alpha=0.4)
  if title is not None:
    plt.title(title)
  plt.xlabel('Base')
  plt.ylabel('Relative coverage')
  if fname is not None:
    plt.savefig(fname)
  if show:
    plt.show()
  return



def heatmap(hgrams, groups, title=None, fname=None, show=False, 
            order='spearman', srrs=None):
  """
  Future versions will include some statistical ordering. Maybe.
  Groups is either ints or strings.
  """
  from scipy.stats import spearmanr
  rows, cols = len(hgrams), max([len(h) for h in hgrams])
  plt.figure(figsize=(6,6))
  
  # Get group stuff
  uni_groups = list(set(groups))
  ngroups = len(uni_groups)
  group_dict = {n: uni_groups[n] for n in range(ngroups)}
  # Make arr for heatmap
  arr = np.zeros((rows+ngroups-1, cols)) 
  for gro in range(len(uni_groups)):
    for hg in range(len(hgrams)): # Should be same length as groups
      if groups[hg] == uni_groups[gro]:
        arr[hg+gro,:len(hgrams[hg])] = hgrams[hg]
    arr[hg+gro,:len(hgrams[hg])] = [1 if i%2==0 else 0 for i in range(len(hgrams[hg]))]
  arr = np.array(arr)
  
  # Plotting stuff!
  heatmap = plt.pcolor(arr)
  plt.xlabel('Base number')
  plt.ylabel('Accession number')
  for gr in range(ngroups):
    plt.text(gr*20,0, '%i: %s' %(gr, uni_groups[gr]))
  if srrs is not None:
    plt.x
  if fname is not None:
    plt.savefig(fname)
  if show:
    plt.show()
  return



def parse_accessions(accfile='/home/ubuntu/autism/SRR924623.blastout.BED'):
  """ Parse accessions file """
  accs = []
  if type(accfile) is not str:
    print("Need a BED file (NM_001 ... 4946  4995)"); return None
  print("Reading %s ..." %accfile)
  with open(accfile, 'r') as fIn:
    for line in fIn:
      if line:
        splitLine = line.split(None)
        try:
          accs.append([int(splitLine[1]), int(splitLine[2])])
        except:
          pass
  return accs



def multi_accession(accfilelist):
  """
  Load all accession files in the passed file list.
  """
  # Find accession files
  if 'txt' not in accfilelist:
    print('Warning -- txt not in file name (%s); will still try to load.'
          %accfilelist)
  accfiles = []
  with open(accfilelist, 'r') as fIn:
    for line in fIn:
      if line:
        accfiles.append(line.strip())
  print('Found %i accession files' %len(accfiles))
  
  # Load each of the accession files
  accessions = [parse_accessions(acc) for acc in accfiles]
  return accessions



def max_seq_length(accessions):
  """
  If not seq length is given, just take the longest possible seq 
  length from the largest accession index.
  """
  return int(max([ac[1] for ac in accessions])) # (NM_001231231 4555 4996) ...



def normed(normfile):
  """ 
  normfile = MBase Run Group \n 1687 SRR309133 0 \n 1624 SRR309135 1 ...
  """
  if normfile is None:
    return None
  normthing = []
  with open(normfile, 'r') as fIn:
    for line in fIn:
      if line:
        normthing.append(line.strip().split(None))
  if max([len(n) for n in normthing]) == 2: # All are same group
    print('All SRRs are the same group!')
    normthing = [[n[0], n[1], 1] for n in normthing] # All get group 1
  if max([len(n) for n in normthing]) == 3: # Groups are present
    newnorm = []
    for n in normthing:
      try:
        newnorm.append([int(n[0]), str(n[1]), int(n[2])])
      except:
        print('Not sure what to do with: (should be #mbases(int), srr(str), group(int))')
        print(n)
  return newnorm



def spit_matrix(hgrams, outfile=None):
  """
  """
  if outfile is not None:
    with open(outfile, 'w') as fOut:
      for hg in hgrams:
        outfile.write(' '.join([str(i) for i in hg]))
    print('Matrix written to %s.' %outfile)
  else:
    print('A filename must be given')
  return


def control(accfile, seq_length=None, outpdfname=None, link=None):
  """ Run evertyhing """
  # Get accessions:
  accessions = parse_accessions(accfile)
  # Check seq length
  if seq_length is None:
    seq_length = max_seq_length(accessions)
  # Populate the histogram
  hgram = populate_N(accessions, seq_length)
  # Plot the thing
  single_hgram(hgram, fname=outpdfname, link=link)
  return



def multi_control(accfilelist, normfile=None, outpdfname=None, 
                  link=None, show=False, graph='heatmap'):
  """ 
  Run multiple everying. graph = {'heatmap', 'lines'}
  """
  # Get accessions
  accession_list = multi_accession(accfilelist)
  # Get a sequence length
  seq_length = max([max_seq_length(acc) for acc in accession_list])
  # Get the histograms
  hgrams = [populate_N(acc, seq_length) for acc in accession_list]
  # Normalize, if desired:
  if normfile is not None:
    normstuff = normed(normfile) # [[#MBases, SRR, group], .... ]
    if len(normstuff) != len(hgrams):
      print('Normstuff must be same length as accession files')
      print('   and should line up (SRRs).'); return None
    hgrams = [hgrams[i]/float(normstuff[i][0]) for i in range(len(hgrams))]
    groups = [n[2] for n in normstuff]
    srrs = [n[1] for n in normstuff] # Get srr names (maybe?)
  else: # hgrams is unchanged but we still want groups
    groups = [1 for i in hgrams]
  # Keep non-zero histograms
  keep = [i for i in range(len(hgrams)) if max(hgrams[i]) > 0.] 
  hgrams, groups = [hgrams[k] for k in keep], [groups[k] for k in keep]
  # Plot the thing
  if graph == 'heatmap':
    heatmap(hgrams, groups, fname=outpdfname, show=show, order=None)
  else:
    multi_hgram(hgrams, groups, fname=outpdfname, link=link, show=show)
  return




##########################################################################

if __name__ == "__main__":
  args = sys.argv
  if len(args) < 2:
    print("Need a list of BED files!")
    sys.exit
  elif len(args) == 2:
    accfile = args[1]
  if len(args) == 3:
    normfile = args[2]
  else:
    normfile = None
  if len(args) == 4:
    pdfname = args[3]
  else:
    pdfname = None
  multi_control(accfile, normfile=normfile, outpdfname=pdfname)








