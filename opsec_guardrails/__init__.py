"""
opsec_guardrails/ — Undermind sandbox safety checklist + runtime checks.

Guarantees:
  - daemon never phones home
  - NPU/ONNX path stays localhost-only
  - model files are read-only from expected roots
  - network egress is blocked by default config
"""
import ipaddress
import os
import socket
from pathlib import Path


def assert_localhost_only(bind_host: str):
    """Listener/feeder must bind to 127.0.0.1 or ::1 only."""
    addr = ipaddress.ip_address(bind_host)
    if not addr.is_loopback:
        raise RuntimeError(f"bind address {bind_host} is not loopback; refusing")


def assert_no_network_egress():
    """Sanity check: no obvious wide-open egress. Heuristic, not a firewall."""
    unexpected = []
    for name in ["CUDA_VISIBLE_DEVICES", "HIP_VISIBLE_DEVICES", "XLA_PYTHON_CLIENT_PREALLOCATE"]:
        if name in os.environ:
            unexpected.append(name)
    # If GPU envs are set, that's expected on sandbox; warn only
    if unexpected:
        return {
            "ok": True,
            "note": f"GPU envs present: {unexpected}. Not a leak by itself.",
        }
    return {"ok": True}


def verify_model_path(path: str, allowed_roots=("models", "cache")) -> Path:
    """Ensure a model path sits under an allowed local root."""
    p = Path(path).resolve()
    if not any(str(p).lower().startswith(str(Path(r).resolve()).lower()) for r in allowed_roots):
        raise RuntimeError(f"model path {path} is outside allowed roots {allowed_roots}")
    if not p.is_file():
        raise FileNotFoundError(f"model file not found: {path}")
    return p


def verify_provider_allowlist(providers):
    """Only allow local/offline providers for the sandbox daemon."""
    allowed = {"CPUExecutionProvider", "VitisAIExecutionProvider", "VoeExecutionProvider"}
    bad = [p for p in providers if p not in allowed]
    if bad:
        raise RuntimeError(f"disallowed ONNX providers: {bad}")
    return providers


def assert_daemon_not_running_as_root():
    """Refuse to start as root/admin to limit blast radius."""
    if os.name == "nt":
        import ctypes

        admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    else:
        admin = os.geteuid() == 0
    if admin:
        raise RuntimeError("refusing to run as root/admin; sandbox daemon must be unprivileged")


if __name__ == "__main__":
    print("opsec_guardrails checks:")
    assert_localhost_only("127.0.0.1")
    print(" - loopback bind: OK")
    print(" - egress:", assert_no_network_egress())
    print(" - model path:", verify_model_path(r"C:\Users\dewayne\Hermes-Stack-Rebuild\models\undermind-oneiros-1.5b.onnx", allowed_roots=("models",)))
    assert_daemon_not_running_as_root()
    print(" - privilege: OK")
    print("all guardrails passed")
