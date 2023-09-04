import os

for memory in ["RRAM", "PCRAM", "STTRAM"]:
  for opt in ["Area", "ReadEDP", "ReadDynamicEnergy", "ReadLatency"]:
    os.system(f"make se MEMORY={memory}_{opt}_Opt")
    os.system(f"mkdir -p gem5/{memory}/{opt}")
    os.system(f"mv m5out/* gem5/{memory}/{opt}")
