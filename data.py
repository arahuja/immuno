import numpy as np 
from amino_acid import peptide_to_indices

def load_lines(filename):
  f = open(filename)
  result = f.read().splitlines()
  f.close()
  return result

def load_9mers(filename):
  lines = load_lines(filename)
  result = [peptide_to_indices(line) for line in lines]
  return np.array(result)

IMMA2_IMM_FILE = 'IMMA2_imm.txt'
IMMA2_NON_FILE = 'IMMA2_non.txt'
def load_dataset(imm_file, non_file):
  imm = load_9mers(imm_file) 
  non = load_9mers(non_file)
  X = np.vstack([imm, non])
  Y = np.ones(len(X), dtype='bool')
  Y[len(imm):] = 0
  return X, Y
  
def load_imma2():
  return load_dataset(IMMA2_IMM_FILE, IMMA2_NON_FILE)
  

IEDB_IMM_FILE = 'IEDB_TCELL_HUMAN_IMM.txt'
IEDB_NON_FILE = 'IEDB_TCELL_HUMAN_NON.txt'

def load_iedb(exclude_imma2 = True, peptide_length = 9):
  
  iedb_imm_lines = load_lines(IEDB_IMM_FILE) 
  iedb_non_lines = load_lines(IEDB_NON_FILE)  
  
  if exclude_imma2:
    imma2_set = set(load_lines(IMMA2_IMM_FILE))
    imma2_set = imma2_set.union(set(load_lines(IMMA2_NON_FILE))) 
    iedb_imm_lines = [line for line in iedb_imm_lines 
                      if line not in imma2_set]
    iedb_non_lines = [line for line in iedb_non_lines
                      if line not in imma2_set]
  
  iedb_imm = [peptide_to_indices(line) for line in iedb_imm_lines]
  iedb_imm = np.array([line for line in iedb_imm 
                       if len(line) == peptide_length])
  iedb_non = [peptide_to_indices(line) for line in iedb_non_lines]
  iedb_non = np.array([line for line in iedb_non 
                       if len(line) == peptide_length])
  X = np.vstack([iedb_imm, iedb_non])
  Y = np.ones(len(X), dtype='bool')
  Y[len(iedb_imm):] = 0
  return X, Y
  

  
  
  



def transform(X, fns, positions = None, mean = False, pairwise_ratios = False):
  X2 = []
  for x in X:
    row = []
    for fn in fns:
      row_entries = [fn(xi) for xi in x]
      if positions:
        row_entries = [xi for i, xi in enumerate(row_entries) if i in positions]
      if mean:
        row.append(np.mean(row_entries))
      else:
        row.extend(row_entries)
      if pairwise_ratios:
	for i, y in enumerate(row_entries):
	  for j, z in enumerate(row_entries):
	    if i < j:
              if z == 0:
	        ratio = 0
              else:
                ratio = y / z
	      row.append(ratio)
    X2.append(row)
  X2 = np.array(X2)
  return X2

import toxin 
def load_toxin_features(imm_file = IMMA2_IMM_FILE, non_file = IMMA2_NON_FILE, substring_length=3, positional=False):
  imm = load_lines(imm_file)
  non = load_lines(non_file)
  
  if positional:
    imm_toxin_features = toxin.positional_toxin_features(imm, length=substring_length)
    non_toxin_features = toxin.positional_toxin_features(non, length=substring_length)
  
  else:
    imm_toxin_features = toxin.toxin_features(imm, length=substring_length)
    non_toxin_features = toxin.toxin_features(non, length=substring_length)
  
  X = np.vstack([imm_toxin_features, non_toxin_features])
  Y = np.ones(len(X), dtype='bool')
  Y[len(imm):] = 0
  return X, Y

  