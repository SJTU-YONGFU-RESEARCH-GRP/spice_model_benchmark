from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Protocol, Tuple


@dataclass
class UnifiedModelDescriptor:
    """Unified description of a device model across backends.

    This is intentionally minimal and backend-agnostic. All concrete
    backends (SPICE / Verilog-A / data-driven) should be able to
    populate this structure.
    """

    backend: str  # "spice", "veriloga", "data"
    source: Path
    name: Optional[str] = None
    terminals: List[str] = field(default_factory=list)
    parameters: Dict[str, Any] = field(default_factory=dict)
    meta: Dict[str, Any] = field(default_factory=dict)


class ModelBackend(Protocol):
    """Protocol for model backends used by the benchmark pipeline.

    A backend is responsible for describing the model and, if necessary,
    preparing analysis-specific circuit netlists that instantiate the
    model in a way compatible with the chosen simulator.
    """

    def describe(self) -> UnifiedModelDescriptor:
        """Return a unified descriptor of the underlying model."""

    def prepare_circuits(
        self,
        dc_circuit: Optional[Path],
        transient_circuit: Optional[Path],
        noise_circuit: Optional[Path],
        ac_circuit: Optional[Path],
        output_dir: Path,
    ) -> Tuple[Optional[Path], Optional[Path], Optional[Path], Optional[Path]]:
        """Return (possibly adapted) circuit file paths for each mode.

        Backends can generate new netlists under ``output_dir`` or simply
        pass through the provided paths unchanged.
        """


class SpiceModelBackend:
    """Backend for traditional SPICE model files (.inc/.lib/.model).

    Currently this is a light-weight wrapper used to keep the public
    API stable while introducing a common backend abstraction. It
    simply passes through the provided circuit files unchanged.
    """

    def __init__(self, model_file: Path) -> None:
        self._model_file = model_file

    def describe(self) -> UnifiedModelDescriptor:
        return UnifiedModelDescriptor(
            backend="spice",
            source=self._model_file,
            name=self._model_file.name,
        )

    def prepare_circuits(
        self,
        dc_circuit: Optional[Path],
        transient_circuit: Optional[Path],
        noise_circuit: Optional[Path],
        ac_circuit: Optional[Path],
        output_dir: Path,
    ) -> Tuple[Optional[Path], Optional[Path], Optional[Path], Optional[Path]]:
        # For now we do not modify circuits here. More advanced logic
        # (e.g. auto-adapting base netlists using generate_spice_netlist)
        # can hook in at this layer later.
        return dc_circuit, transient_circuit, noise_circuit, ac_circuit


class VerilogABackend:
    """Placeholder backend for Verilog-A models.

    The intention is to eventually support Verilog-A modules by parsing
    their interfaces and generating simulator-specific wrapper
    netlists. For now this backend exists only to make the public API
    future-proof.
    """

    def __init__(self, model_file: Path) -> None:
        self._model_file = model_file

    def describe(self) -> UnifiedModelDescriptor:
        return UnifiedModelDescriptor(
            backend="veriloga",
            source=self._model_file,
            name=self._model_file.name,
        )

    def prepare_circuits(
        self,
        dc_circuit: Optional[Path],
        transient_circuit: Optional[Path],
        noise_circuit: Optional[Path],
        ac_circuit: Optional[Path],
        output_dir: Path,
    ) -> Tuple[Optional[Path], Optional[Path], Optional[Path], Optional[Path]]:
        raise NotImplementedError(
            "Verilog-A backend is not implemented yet. "
            "This placeholder exists to reserve the interface."
        )


class DataModelBackend:
    """Placeholder backend for data-driven (e.g. ML/table) models.

    In the future this backend can encapsulate models implemented in
    Python/NumPy/PyTorch/etc. and provide an alternative to SPICE-based
    simulation. For now it only documents the intended interface.
    """

    def __init__(self, descriptor: UnifiedModelDescriptor) -> None:
        self._descriptor = descriptor

    def describe(self) -> UnifiedModelDescriptor:
        return self._descriptor

    def prepare_circuits(
        self,
        dc_circuit: Optional[Path],
        transient_circuit: Optional[Path],
        noise_circuit: Optional[Path],
        ac_circuit: Optional[Path],
        output_dir: Path,
    ) -> Tuple[Optional[Path], Optional[Path], Optional[Path], Optional[Path]]:
        raise NotImplementedError(
            "Data-driven backend is not wired into the SPICE pipeline yet. "
            "Use the Python API for direct evaluation instead."
        )


def create_model_backend(backend: str, model_file: Path) -> ModelBackend:
    """Factory helper to construct a backend implementation.

    Args:
        backend: Backend kind ("spice", "veriloga", "data").
        model_file: Path to the model description file.

    Returns:
        A concrete backend implementing :class:`ModelBackend`.
    """
    backend_lower = backend.lower()
    if backend_lower == "spice":
        return SpiceModelBackend(model_file)
    if backend_lower == "veriloga":
        return VerilogABackend(model_file)
    if backend_lower == "data":
        # For data-driven models we currently require the caller to
        # construct a full UnifiedModelDescriptor; this branch is kept
        # for future extension and will raise for now.
        raise NotImplementedError(
            "Data-driven backend via create_model_backend is not supported yet. "
            "Please construct a DataModelBackend explicitly when this feature "
            "is implemented."
        )
    raise ValueError(f"Unsupported backend kind: {backend}")
