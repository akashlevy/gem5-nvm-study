ARCH := X86
GEM5_DIR := gem5
GEM5 := $(GEM5_DIR)/build/$(ARCH)/gem5.opt
SCRIPT := $(GEM5_DIR)/configs/deprecated/example/se.py
CMD := mlbench/linux_$(ARCH)_benchmark_model
MODEL := squeezenet
MODEL_TFLITE := mlbench/models/$(MODEL)/$(MODEL).tflite

se:
        $(GEM5) $(SCRIPT) --cmd=$(CMD) --options="--graph=$(MODEL_TFLITE)"

run:
        $(CMD) --graph=$(MODEL_TFLITE)
