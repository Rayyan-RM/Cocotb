import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer, ClockCycles
import random

async def reset_dut(dut, cycles: int = 3):
    """Assert asynchronous/synchronous active-LOW reset."""
    dut.arstn.value = 0  # Active LOW reset (0 means RESET)
    dut.en.value = 0 
    await ClockCycles(dut.clk, cycles)
    dut.arstn.value = 1  # De-assert reset (1 means RUN)
    await RisingEdge(dut.clk)
    
# Test 1: Testing in reset state
@cocotb.test()
async def test_reset(dut):
    """After reset, count must be 0."""
    cocotb.start_soon(Clock(dut.clk, 10, unit='ns').start())
    
    # System starts unreset but disabled
    dut.arstn.value = 1
    dut.en.value = 0
    await ClockCycles(dut.clk, 5)
    
    dut._log.info("Resetting System")
    await reset_dut(dut, cycles=3)
    
    assert dut.count.value == 0, f"Expected 0 during reset, got {dut.count.value}"
    dut._log.info("Reset Test Pass!")

# Test 2: Counter increment when enable = 1
@cocotb.test()
async def test_counter_up(dut):
    """Counter will increase by 1."""
    cocotb.start_soon(Clock(dut.clk, 10, unit='ns').start())
    await reset_dut(dut)
    
    dut.en.value = 1
    N = 20  # number of cycles to test
    
    for expected in range(1, N + 1):
        await RisingEdge(dut.clk)
        # Give GHDL 1ps to evaluate the delta cycle changes
        await Timer(1, unit='ps') 
        actual = int(dut.count.value)
        assert actual == expected, f"Cycle {expected}: count={actual}, expected={expected}"
        
    dut._log.info(f"PASS: counted correctly for {N} cycles")
    
# Test 3: Check value is held when enable is 0
@cocotb.test()
async def test_counter_holds(dut):
    """Counter need to hold the prev value."""
    cocotb.start_soon(Clock(dut.clk, 10, unit='ns').start()) # Fixed missing ()
    await reset_dut(dut)
    
    # Let counter run for 5 cycles
    dut.en.value = 1
    await ClockCycles(dut.clk, 5) # Fixed invalid RisingEdge argument
    await Timer(1, unit='ps')
    
    hold_value = int(dut.count.value)
    assert hold_value == 5, f"Expected 5, got {hold_value}" 
    
    # Disabling en and verifying it holds its value
    dut.en.value = 0 
    for _ in range(10):
        await RisingEdge(dut.clk)
        await Timer(1, unit='ps')
        current = int(dut.count.value)
        assert current == hold_value, f"Count changed while en=0: {hold_value} → {current}"
        
    dut._log.info(f"PASS: count held at {hold_value} for 10 gated cycles")
