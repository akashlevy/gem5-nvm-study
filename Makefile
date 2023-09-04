ARCH := X86
GEM5_DIR := /home/ubuntu/gem5
GEM5 := $(GEM5_DIR)/build/$(ARCH)/gem5.opt
SCRIPT := $(GEM5_DIR)/configs/deprecated/example/se.py
CMD := mlbench/linux_$(ARCH)_benchmark_model
MODEL := squeezenet
MODEL_TFLITE := mlbench/models/$(MODEL)/$(MODEL).tflite
CPU_TYPE := X86TimingSimpleCPU
MEM_TYPE := DDR3_1600_8x8
CACHE := --caches --l1d_size=32kB --l1i_size=32kB --l1d_assoc=8 --l1i_assoc=8 --l2cache --l2_size=256kB --l2_assoc=8

nvm:
	cp -f NVMInterface.py $(GEM5_DIR)/src/mem/
	cd $(GEM5_DIR) && scons build/X86/gem5.opt && cd -

se:
	$(GEM5) $(SCRIPT) $(CACHE) --mem-type=$(MEM_TYPE) --cpu-type=$(CPU_TYPE) --cmd=$(CMD) --options="--warmup_min_secs=0 --num_runs=1 --min_secs=0 --graph=$(MODEL_TFLITE)"

run:
	$(CMD) --graph=$(MODEL_TFLITE)

expt:
	python3 gem5expt.py
