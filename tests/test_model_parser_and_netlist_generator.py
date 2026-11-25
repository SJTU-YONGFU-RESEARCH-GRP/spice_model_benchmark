"""Tests for ModelParser and NetlistGenerator on-the-fly SPICE evaluation."""

import os
import tempfile
from pathlib import Path
import pytest

from spice_model_benchmark.model_parser import ModelParser, DeviceSpec, parse_spice_val
from spice_model_benchmark.netlist_generator import NetlistGenerator
from spice_model_benchmark import benchmark_spice_model


def test_parse_spice_val():
    assert parse_spice_val("1.2") == pytest.approx(1.2)
    assert parse_spice_val("45n") == pytest.approx(45e-9)
    assert parse_spice_val("10u") == pytest.approx(10e-6)
    assert parse_spice_val("1meg") == pytest.approx(1e6)
    assert parse_spice_val("100k") == pytest.approx(1e5)
    assert parse_spice_val("1f") == pytest.approx(1e-15)


def test_model_parser_inline_model(tmp_path):
    spice_card = """* Sample SPICE Model
.model nmos_core nmos (LEVEL=54 VERSION=4.5 VTH0=0.35 TOX=1.4n LMIN=45n WMIN=100n)
.model pmos_core pmos (LEVEL=54 VERSION=4.5 VTH0=-0.38 TOX=1.4n LMIN=45n WMIN=100n)
.subckt sky130_fd_pr__nfet_01v8 d g s b
M1 d g s b nmos_core L=0.15u W=1.0u
.ends
"""
    model_file = tmp_path / "test_model.inc"
    model_file.write_text(spice_card)

    parser = ModelParser()
    info = parser.parse(model_file)

    assert len(info.devices) == 3
    assert len(info.nmos_devices) == 2
    assert len(info.pmos_devices) == 1

    nmos = info.primary_nmos
    assert nmos is not None
    assert nmos.name == "nmos_core"
    assert nmos.polarity == "nmos"
    assert nmos.level == 54
    assert nmos.device_type == "primitive"

    pmos = info.primary_pmos
    assert pmos is not None
    assert pmos.name == "pmos_core"
    assert pmos.polarity == "pmos"

    # Test subcircuit device
    subckt_dev = info.get_device("sky130_fd_pr__nfet_01v8")
    assert subckt_dev is not None
    assert subckt_dev.device_type == "subcircuit"
    assert subckt_dev.inst_prefix == "X"
    assert subckt_dev.default_vdd == 1.8


def test_model_parser_freepdk45():
    model_path = Path("models/public-models/freepdk45/nom.inc")
    if not model_path.exists():
        pytest.skip("freepdk45/nom.inc not present in models repo")

    parser = ModelParser()
    info = parser.parse(model_path)

    assert len(info.devices) >= 8
    assert info.primary_nmos is not None
    assert info.primary_nmos.name == "NMOS_VTG"
    assert info.primary_pmos is not None
    assert info.primary_pmos.name == "PMOS_VTG"


def test_netlist_generator(tmp_path):
    dut = DeviceSpec(
        name="NMOS_TEST",
        polarity="nmos",
        default_l=45e-9,
        default_w=10e-6,
        default_vdd=1.2,
    )
    pmos = DeviceSpec(
        name="PMOS_TEST",
        polarity="pmos",
        default_l=45e-9,
        default_w=20e-6,
        default_vdd=1.2,
    )

    model_file = tmp_path / "dummy_model.inc"
    model_file.write_text(".model NMOS_TEST nmos (LEVEL=54)\n.model PMOS_TEST pmos (LEVEL=54)")

    gen_dir = tmp_path / "generated_netlists"
    gen = NetlistGenerator(output_dir=gen_dir)

    # ngspice netlists
    ng_nets = gen.generate_ngspice_netlists(model_file, dut, pmos_dut=pmos)
    assert set(ng_nets.keys()) == {"dc", "ac", "transient", "noise", "gummel"}
    for name, p in ng_nets.items():
        assert p.exists()
        content = p.read_text()
        assert "dummy_model.inc" in content
        assert "NMOS_TEST" in content

    # Spectre netlists
    scs_nets = gen.generate_spectre_netlists(model_file, dut, pmos_dut=pmos)
    assert set(scs_nets.keys()) == {"dc", "ac", "transient", "noise", "_sp", "_nqs"}
    for name, p in scs_nets.items():
        assert p.exists()
        content = p.read_text()
        assert "dummy_model.inc" in content
        assert "NMOS_TEST" in content


def test_on_the_fly_benchmark_execution(tmp_path):
    """Verify that benchmark_spice_model executes without any dependency on a 'netlists' directory."""
    model_path = Path("models/public-models/freepdk45/nom.inc")
    if not model_path.exists():
        pytest.skip("freepdk45/nom.inc not found")

    out_dir = tmp_path / "bench_results"
    # Run only DC mode for fast verification
    success = benchmark_spice_model(
        model_file=model_path,
        output_dir=out_dir,
        modes=["dc"],
    )

    assert success is True
    # Verify that netlists were generated inside the output_dir
    assert (out_dir / "netlists" / "dc_circuit.cir").exists()
    assert (out_dir / "data" / "iv_data_25.txt").exists()
    assert (out_dir / "REPORT.md").exists()
