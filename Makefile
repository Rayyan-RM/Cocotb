SIM ?= ghdl
TOPLEVEL_LANG ?= vhdl

# 1. Change 'adder.vhd' to your exact VHDL filename
VHDL_SOURCES += $(PWD)/counter.vhd

# 2. Change 'adder' to the exact name of your VHDL entity
TOPLEVEL = counter

# 3. Change 'test_adder' to your Python filename (leave out the .py)
MODULE = counter_tb

# This line instructs cocotb to output the wave.vcd file for GTKWave
SIM_ARGS += --vcd=wave.vcd

include $(shell cocotb-config --makefiles)/Makefile.sim
