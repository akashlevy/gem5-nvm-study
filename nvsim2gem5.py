# Import libraries
import re
from glob import glob


# NVSim regular expressions
re_mem    = re.compile(r'nvsim/nvsim\.(.+)\.(.+)\.rpt')
re_bank   = re.compile(r'Bank Organization: (\d+) x (\d+)')

re_area   = re.compile(r'Total Area = ([\d\.]+)([um])m x ([\d\.]+)([um])m = ([\d\.]+)([um])m\^2')

re_tREAD  = re.compile(r'Read Latency = ([\d\.]+)([pn])s')
re_tWRITE = re.compile(r'Write Latency = ([\d\.]+)ns')
re_tSET   = re.compile(r'SET Latency = ([\d\.]+)ns')
re_tRESET = re.compile(r'RESET Latency = ([\d\.]+)ns')

re_eREAD  = re.compile(r'Read Dynamic Energy = ([\d\.]+)([pn])J')
re_eWRITE = re.compile(r'Write Dynamic Energy = ([\d\.]+)([pn])J')
re_eSET   = re.compile(r'SET Dynamic Energy = ([\d\.]+)([pn])J')
re_eRESET = re.compile(r'RESET Dynamic Energy = ([\d\.]+)([pn])J')

re_pLEAK  = re.compile(r'Leakage Power = ([\d\.]+)(m?)W')


# Read all the reports
data = []
for rptname in glob('nvsim/*.rpt'):
  # Read report
  rpt = open(rptname).read()

  # Parse report
  print(rptname)
  row = {
    'mem':    re_mem.search(rptname).group(1),
    'opt':    re_mem.search(rptname).group(2),
    'banks':  int(re_bank.search(rpt).group(1)) * int(re_bank.search(rpt).group(2)),
    'width':  float(re_area.search(rpt).group(1)) * (1e-3 if re_area.search(rpt).group(2) == 'u' else (1 if re_area.search(rpt).group(2) == 'm' else None)), # mm
    'height': float(re_area.search(rpt).group(3)) * (1e-3 if re_area.search(rpt).group(4) == 'u' else (1 if re_area.search(rpt).group(4) == 'm' else None)), # mm
    'area':   float(re_area.search(rpt).group(5)) * (1e-6 if re_area.search(rpt).group(6) == 'u' else (1 if re_area.search(rpt).group(6) == 'm' else None)), # mm^2
    'tREAD':  float(re_tREAD.search(rpt).group(1)) * (1 if re_tREAD.search(rpt).group(2) == 'n' else (1e-3 if re_tREAD.search(rpt).group(2) == 'p' else None)), # ns
    'eREAD':  float(re_eREAD.search(rpt).group(1)) * (1e-9 if re_eREAD.search(rpt).group(2) == 'n' else (1e-12 if re_eREAD.search(rpt).group(2) == 'p' else None)), # J
    'pLEAK':  float(re_pLEAK.search(rpt).group(1)) * (1e-3 if re_pLEAK.search(rpt).group(2) == 'm' else (1 if re_pLEAK.search(rpt).group(2) == '' else None)) # W
    }
  try:
    row['tWRITE'] = float(re_tWRITE.search(rpt).group(1)) # ns
    row['eWRITE'] = float(re_eWRITE.search(rpt).group(1)) * (1e-9 if re_eWRITE.search(rpt).group(2) == 'n' else (1e-12 if re_eWRITE.search(rpt).group(2) == 'p' else None)) # J
  except AttributeError:
    tSET = float(re_tSET.search(rpt).group(1)) # ns
    tRESET = float(re_tRESET.search(rpt).group(1)) # ns
    eSET = float(re_eSET.search(rpt).group(1)) * (1e-9 if re_eSET.search(rpt).group(2) == 'n' else (1e-12 if re_eSET.search(rpt).group(2) == 'p' else None)) # J
    eRESET = float(re_eRESET.search(rpt).group(1)) * (1e-9 if re_eRESET.search(rpt).group(2) == 'n' else (1e-12 if re_eRESET.search(rpt).group(2) == 'p' else None)) # J
    row['tWRITE'] = max(tSET, tRESET) # ns
    row['eWRITE'] = 0.5 * (eSET + eRESET) # J

  # Append to data
  data.append(row)


# Export data to CSV
with open('nvsim/nvsim.csv', 'w') as f:
  f.write('mem,opt,banks,tREAD,tWRITE,eREAD,eWRITE,pLEAK\n')
  for row in data:
    f.write('{},{},{},{},{},{},{},{}\n'.format(
      row['mem'],
      row['opt'],
      row['banks'],
      row['tREAD'],
      row['tWRITE'],
      row['eREAD'],
      row['eWRITE'],
      row['pLEAK']
    ))


# Create NVMInterface.py
with open('NVMInterface.py', 'w') as f:
  f.write(open('NVMInterface.tmpl.py').read())
  for row in data:
    f.write('''
# {mem} {opt}-Optimized
class {mem}_{opt}_Opt(NVM_DIMM):
    banks_per_rank = {banks}
    tREAD = "{tREAD}ns"
    tWRITE = "{tWRITE}ns"

'''.format(**row))