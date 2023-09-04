ARCH := X86
GEM5_DIR := /home/ubuntu/gem5
GEM5 := $(GEM5_DIR)/build/$(ARCH)/gem5.opt
SCRIPT := $(GEM5_DIR)/configs/deprecated/example/se.py
CMD := mlbench/linux_$(ARCH)_benchmark_model
MODEL := squeezenet
MODEL_TFLITE := mlbench/models/$(MODEL)/$(MODEL).tflite
MEMORY := NVM_2400_1x64

se:
	cp -f NVMInterface.py $(GEM5_DIR)/src/mem/
	cd $(GEM5_DIR) && scons build/X86/gem5.opt && cd -
	$(GEM5) $(SCRIPT) $(CACHE) --mem-type=$(MEMORY) --cmd=$(CMD) --options="--warmup_min_secs=0 --num_runs=1 --min_secs=0 --graph=$(MODEL_TFLITE)"

run:
	$(CMD) --graph=$(MODEL_TFLITE)

expt:
	python gem5expt.py
