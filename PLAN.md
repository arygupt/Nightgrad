# Nightgrad Boilerplate Plan

## Goal

Write `philosophy.md` as the foundation for **Nightgrad**: a local iPhone night-vision experiment powered by tinygrad and WebGPU.

The document should describe a serious technical direction, not imply that this is already a simple production app. The target is:

- local execution on iPhone
- no cloud inference
- camera frames processed on-device
- tinygrad used as the tensor/compiler layer
- WebGPU used as the intended GPU execution path

Because tinygrad is Python-first and iPhone GPU access is exposed through browser or native APIs, this should be framed as a runtime-porting experiment.

## Language Choice

`philosophy.md` itself should be written in plain English.

The implementation described by `philosophy.md` should use:

- **Python** for tinygrad tensor code, image enhancement logic, model definitions, and offline experiments.
- **TypeScript** for the iPhone Safari/PWA shell, camera capture, frame transfer, and JavaScript WebGPU bridge.
- **WGSL** for WebGPU compute shaders.

Do not make Swift the first implementation language. A native iOS app would push the project toward Metal/Core ML, which is practical but no longer proves the tinygrad-WebGPU idea directly.

## How Nightgrad Uses tinygrad

The philosophy should describe tinygrad as the core computational engine, not merely a training dependency.

The intended frame pipeline is:

1. Capture a frame from the iPhone camera in Safari.
2. Convert frame bytes into a tensor-compatible buffer.
3. Pass that buffer into tinygrad running in a browser-hosted Python environment.
4. Run a low-light enhancement graph:
   - normalize RGB values
   - reduce noise
   - lift shadows
   - preserve highlights
   - optionally run a small convolutional enhancement model
5. Let tinygrad schedule and lower the tensor operations.
6. Execute supported operations through WebGPU.
7. Display the enhanced frame back to a canvas.

The first prototype should process still images. Live video should only be attempted after still-frame processing works end to end on the target iPhone.

## What tinygrad WebGPU Means

`tinygrad WebGPU` means tinygrad targets a WebGPU backend for tensor execution.

In a normal desktop tinygrad setup, this means tinygrad code is written in Python, then lowered into GPU work that can run through tinygrad's WebGPU runtime path.

On iPhone Safari, the situation is different:

- Safari exposes WebGPU through JavaScript APIs such as `navigator.gpu`.
- tinygrad does not automatically gain access to that browser API just because Python code is running.
- A browser-hosted Python runtime would need a bridge into JavaScript WebGPU.
- The project may need a custom tinygrad backend, a tinygrad fork, or a reduced tinygrad-compatible execution path.

So the iPhone-local version should define tinygrad WebGPU as:

> tinygrad tensor code running inside a browser-hosted Python environment, with tensor operations lowered into WGSL/WebGPU compute work executed by Safari's WebGPU implementation.

This is the hardest and most important technical claim in the project.

## Proposed `philosophy.md` Boilerplate

Use this structure for `philosophy.md`:

1. **Title**
   - `Nightgrad: Night Vision on Your Phone`

2. **Thesis**
   - Phones already have good sensors and increasingly capable GPUs.
   - Nightgrad explores whether a small, hackable local tensor stack can turn low-light frames into usable images without cloud processing.

3. **Why tinygrad**
   - tinygrad is small enough to understand.
   - It exposes tensors, lowering, scheduling, and runtimes more directly than larger ML frameworks.
   - It is a better fit for learning and experimentation than treating ML inference as an opaque black box.

4. **Why iPhone-local**
   - Night vision is latency-sensitive.
   - Camera frames are private.
   - A useful prototype should work without sending images to a server.

5. **Why WebGPU**
   - WebGPU is the most plausible browser-accessible path to portable GPU compute.
   - On iPhone, WebGPU creates a possible route from Safari camera frames to local GPU work.
   - The project should treat iPhone WebGPU support as a capability that must be verified on the target device.

6. **The hard part**
   - tinygrad is Python-first.
   - iPhone Safari WebGPU is JavaScript-first.
   - Running tinygrad itself on iPhone requires connecting those two worlds.
   - That bridge is the core research project.

7. **First milestone**
   - Process one dark still image with tinygrad on desktop Python.
   - Then run one trivial WebGPU compute shader in iPhone Safari.
   - Then connect tinygrad-style tensor execution to browser WebGPU for one small operation.

8. **Long-term vision**
   - A local iPhone camera view that brightens dark scenes in real time.
   - A tiny model or hand-written tensor pipeline small enough to inspect and modify.
   - No cloud, no closed inference service, and no hidden camera pipeline.

## Implementation Milestones

### 1. Desktop tinygrad proof

- Create a Python script that loads a dark image.
- Convert the image to a tinygrad `Tensor`.
- Implement a simple enhancement pipeline with tensor operations.
- Run it on CPU first.
- Run tinygrad's WebGPU path separately on a supported desktop setup.
- Save the enhanced output image.

Success means tinygrad can express the image-processing graph before any iPhone work begins.

### 2. iPhone Safari WebGPU proof

- Build a minimal TypeScript page.
- Request a WebGPU adapter and device from Safari.
- Run a tiny WGSL compute shader.
- Copy the result back and display it.
- Test directly on the target iPhone.

Success means the target phone can run local WebGPU compute.

### 3. Browser Python proof

- Load Python in the browser with a WASM Python runtime such as Pyodide.
- Try importing tinygrad.
- Record unsupported modules, native assumptions, filesystem assumptions, and dependency issues.
- Reduce the tinygrad surface area if full tinygrad does not load.

Success means the project knows whether full tinygrad can run or whether a tinygrad subset/fork is required.

### 4. tinygrad-to-browser-WebGPU bridge

- Define the smallest backend bridge needed for one tensor operation.
- Move data between JavaScript buffers and browser-hosted Python.
- Generate or adapt WGSL compute code for that operation.
- Dispatch WebGPU work through JavaScript.
- Return the result to the Python/tinygrad side.

Success means one tinygrad-owned tensor operation executes on iPhone WebGPU.

### 5. Still-frame Nightgrad demo

- Capture or upload one dark frame on iPhone.
- Run the tinygrad-backed enhancement path.
- Render the enhanced result to a canvas.
- Compare CPU/browser fallback output against WebGPU output.

Success means the project can honestly claim local iPhone image enhancement using the tinygrad experiment path.

### 6. Live camera experiment

- Process repeated frames.
- Measure latency, memory, heat, and battery impact.
- Lower resolution until the loop is stable.
- Add back quality only after the frame loop works.

Success means the prototype can approach live night vision without pretending still-frame performance is real-time performance.

## Constraints and Risks

- Running tinygrad itself on iPhone is experimental.
- Browser Python plus WebGPU bridging may be too slow for live video.
- Safari WebGPU support must be verified on the exact iPhone and iOS version.
- WKWebView support may differ from Safari support, so an App Store wrapper should not be the first target.
- Full tinygrad may not run cleanly in browser-hosted Python.
- A reduced tinygrad subset may be necessary for the first working demo.
- Battery, heat, memory pressure, and camera permissions are core constraints, not polish issues.

## Test Plan

- Confirm tinygrad can run a basic tensor operation on desktop Python.
- Confirm the enhancement pipeline works on a still image.
- Confirm WebGPU compute works in iPhone Safari.
- Confirm browser-hosted Python can load enough tinygrad functionality for the prototype.
- Confirm one tinygrad-owned operation can execute through browser WebGPU.
- Confirm a dark still image can be enhanced locally on iPhone.
- Compare CPU and WebGPU outputs for rough numerical sanity.
- Measure frame time before attempting live preview.

## Acceptance Criteria

The boilerplate in `philosophy.md` is complete when it:

- names the project and thesis clearly
- explains why the project uses tinygrad
- explains why the target is local iPhone execution
- defines tinygrad WebGPU accurately
- admits the browser Python/WebGPU bridge problem
- describes Python, TypeScript, and WGSL responsibilities
- avoids overclaiming production readiness
- gives a concrete first milestone: still-frame enhancement before live video

## References to Include or Verify

- tinygrad documentation: https://docs.tinygrad.org/
- tinygrad runtime documentation: https://docs.tinygrad.org/runtime/
- WebGPU specification entry point: https://www.w3.org/TR/webgpu/
- WebKit WebGPU updates: https://webkit.org/
- WebGPU browser support data: https://caniuse.com/webgpu

