# Security Policy

## Scope

`age-progression-studio` processes local face images and writes aged
renders to disk. No network calls are made by default. Model weights
are loaded from `weights/` and are not fetched at runtime.

## Reporting

Email `security@age-progression-studio.dev` with: affected version,
reproduction steps, and impact. We acknowledge within 72 hours.

## Hardening notes

- Weight files are loaded via `torch.load(..., map_location="cpu")`
  with `weights_only=True` when supported.
- ONNX sessions are pinned to local files; no remote URLs.
- Output paths are sanitized against `..` traversal in batch mode.
- CUDA / DirectML kernels are treated as untrusted for image inputs;
  malformed tensors are rejected before inference.

## Supported versions

| Version | Supported |
|---------|-----------|
| 0.6.x   | yes       |
| 0.5.x   | security fixes only |