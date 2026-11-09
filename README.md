# Vox raster tests

Native raster differential tests and verification evidence for [Vox](https://github.com/vox-browser/vox). Large generated receipts live here so browser implementation reviews stay small. Focused unit tests and their compact frozen inputs remain beside the implementation in Vox.

`IMPORT.json` records the original commit, paths and SHA-256 hashes. The imported evidence files retain their exact bytes, including failed attempts and historical limitations. Old absolute paths and commit IDs in these receipts describe the original runs, not the current machine.

Run the version pinned by Vox through its launcher:

```sh
cd /path/to/vox
CPU_RASTER_CHECKS=largeshadowlayers V_BIN=/path/to/v \
  python3 tools/run_memory_bounded.py --limit-gib 3 \
  --lock Build/raster-check.lock --report Build/raster-check.json -- \
  sh tools/gg_migration/test_cpu_raster.sh /tmp/vox-raster-check 1000 20261172
```

The launcher fetches the exact commit in `tools/raster_tests.json` into a cache, rejects changed checkouts, and sets `VOX_SOURCE_DIR`. For local suite development, use `python3 tools/raster_tests.py --checkout /path/to/vox-tests TOOL [ARGS...]` after updating the pin to a committed revision. Do not copy browser sources into this repository or its output directories.

To run this checkout directly:

```sh
VOX_SOURCE_DIR=/path/to/vox V_BIN=/path/to/v \
  sh tools/gg_migration/test_cpu_raster.sh /tmp/vox-raster-check 1000 20261172
```

The reference alone links Skia. Linux uses `VOX_SOURCE_DIR/Build/deps/skia`, or `CPU_RASTER_SKIA_ROOT`; macOS uses the Ladybird vcpkg library, or `LADYBIRD_SOURCE_DIR`. Source, oracle, compiler, native-library, fixture and font hashes must remain unchanged. `CPU_RASTER_TEST_PROD=1` selects `-prod -gc none`; keep no-GC runs in bounded processes under Vox's memory guard. Use a fresh output path outside Vox's `Build/` for generated C and binaries. Logs and guard reports can live in `Build/` while a job runs; retain the concise report and necessary evidence here, then clean scratch outputs.

Native fixture tools read the focused V tests and fixture data from `VOX_SOURCE_DIR`; they never derive expected pixels from the V renderer. For example:

```sh
VOX_SOURCE_DIR=/path/to/vox python3 tools/gg_migration/native_large_blur_hashes.py \
  /tmp/vox-raster-check/skia_cpu_oracle.dylib /tmp/native-blurs.json --verify
```

Evidence for CPU components does not establish a Skia-free browser build. The complete browser still has Skia services and fallbacks; consult Vox's migration report for the current removal work.
