ARCH := X86
GEM5_DIR := gem5
GEM5 := $(GEM5_DIR)/build/$(ARCH)/gem5.opt
SCRIPT := $(GEM5_DIR)/configs/deprecated/example/se.py
CMD := mlbench/linux_$(ARCH)_benchmark_model
MODEL := squeezenet
MODEL_TFLITE := mlbench/models/$(MODEL)/$(MODEL).tflite

CACHE = --caches --l1d_size=32kB --l1i_size=32kB --l1d_assoc=8 --l1i_assoc=8 --l1d_mshrs=4 --l1i_mshrs=4 --l2cache --l2_size=256kB --l2_assoc=8 --l2_mshrs=16

se:
        $(GEM5) $(SCRIPT) $(CACHE) --cmd=$(CMD) --options="--graph=$(MODEL_TFLITE)"

run:
        $(CMD) --graph=$(MODEL_TFLITE)
