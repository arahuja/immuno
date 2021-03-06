import numpy as np
import pandas as pd

def load_csv(filename = 'tcell_compact.csv'):
  df = pd.read_csv(filename)
  mhc = df['MHC Allele Name']

  # 
  # Match known alleles such as 'HLA-A*02:01', 
  # broader groupings such as 'HLA-A2'
  # and unknown alleles of the MHC-1 listed either as 
  #  'HLA-Class I,allele undetermined'
  #  or
  #  'Class I,allele undetermined'
  class_1_mhc = mhc.str.contains('Class I,|HLA-[A-C]([0-9]|\*)', na=False)
  
  print "Class I MHC Entries", class_1_mhc.sum()
  
  # just in case any of the results were from mice or other species, 
  # restrict to humans
  human = df['Host Organism Name'].str.startswith('Homo sapiens', na=False)
  
  print "Human entries", human.sum()
  print "Human Class I MHCs", (human & class_1_mhc).sum()
  
  has_epitope_seq = ~(df['Epitope Linear Sequence'].isnull())
  
  mask = class_1_mhc & human & has_epitope_seq
  print "Class I MHC humans w/ epitope sequences", mask.sum()
  
  df = df[mask]
  
  imm_mask = df['Qualitative Measure'] == 'Positive' 
  imm_mask |= df['Qualitative Measure'] == 'Positive-High'
  imm = df['Epitope Linear Sequence'][imm_mask]
  print "# immunogenic sequences", len(imm)
  print "sequence length"
  print imm.str.len().describe()
  
  non_mask = df['Qualitative Measure'] == 'Negative'
  non = df['Epitope Linear Sequence'][non_mask]
  print "# non-immunogenic sequences", len(non)
  print "sequence length", non.str.len().describe()
  
  
  return imm, non 
  