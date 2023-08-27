ARCH := X86
GEM5_DIR := gem5
GEM5 := $(GEM5_DIR)/build/$(ARCH)/gem5.opt
SCRIPT := se.py
CMD := mlbench/linux_$(ARCH)_benchmark_model
MODEL := squeezenet
MODEL_TFLITE := mlbench/models/$(MODEL)/$(MODEL).tflite

CACHE := 
#--caches --l1d_size=32kB --l1i_size=32kB --l1d_assoc=8 --l1i_assoc=8 --l2cache --l2_size=256kB --l2_assoc=8
MEMORY := --mem-type=RRAM

se:
	cp -f NVMInterface.py $(GEM5_DIR)/src/mem/
	$(GEM5) $(SCRIPT) $(CACHE) $(MEMORY) --cmd=$(CMD) --options="--warmup_min_secs=0 --num_runs=1 --min_secs=0 --graph=$(MODEL_TFLITE)"

run:
	$(CMD) --graph=$(MODEL_TFLITE)
