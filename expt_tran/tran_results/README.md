# SPICE Model Transient Analysis Results

*Generated on: 2025-05-11 03:23:15*

## Analysis Overview

This directory contains all results from the transient analysis of the MOSFET SPICE model.
The analysis covers large-signal transient, switching, delay effects, power dissipation, quasi-static behavior, and charge conservation tests.

## Data Files

| File | Description |
|------|-------------|
| tran_large_signal.txt | Gate and drain voltages, terminal currents for large-signal analysis |
| tran_switching.txt | Input/output voltages and current for inverter switching analysis |
| tran_switching_power.txt | Power dissipation during switching |
| tran_delay.txt | Propagation delay through inverter chain |
| tran_power_27C.txt | Power/energy data at 27°C |
| tran_power_100C.txt | Power/energy data at 100°C |
| tran_quasi_static.txt | Quasi-static behavior data |
| tran_charge.txt | Terminal currents and charges for conservation analysis |

## Plot Files

| File | Description |
|------|-------------|
| large_signal_transient.png | Gate/drain voltages and drain current vs time |
| switching_response.png | Inverter input/output and power dissipation |
| delay_effect.png | Signal propagation through inverter chain |
| power_dissipation.png | Power comparison at different temperatures |
| energy_consumption.png | Energy consumption comparison at different temperatures |
| quasi_static.png | Quasi-static time-domain behavior |
| quasi_static_iv.png | Quasi-static I-V relationship |
| charge_conservation.png | Terminal currents and charges |
| total_charge.png | Total charge conservation analysis |

## Analysis Results Summary

| Analysis Type | Status | Key Findings |
|--------------|--------|-------------|
| Large-Signal Transient | ✓ | Max Current: 1.200e+00 A, Rise Time: 80.002 ns |
| Switching Simulations | ✓ | Propagation Delay: 0.154 ns |
| Delay Effect | ✓ | Total Chain Delay: 0.170 ns |
| Power Dissipation | ✓ | Temp Coeff: 2.746e-05 W/°C |
| Quasi-Static Analysis | ✓ | I-V characteristics analyzed |
| Charge Conservation | ✓ | Error: 195.132351% |
