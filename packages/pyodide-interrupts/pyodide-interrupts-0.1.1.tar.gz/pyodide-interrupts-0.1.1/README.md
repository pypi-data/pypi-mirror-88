# pyodide_interrupts
This is a package to allow handling of interrupts inside of Pyodide. 
Pyodide does not have preemptive multitasking. This package enables handling keyboard interrupts in Pyodide.

This defines one context handler `check_interrupts(callback, interval)` which causes `callback` to be called every `interval` instructions.

## Simple Example:
```python
>>> def callback(): print("check")
... with check_interrupts(callback, 10):
...    for i in range(50):
...       print(i, end=",")

0,1,check
2,3,4,5,6,check
7,8,9,10,11,check
12,13,14,15,16,check
17,18,19,20,21,check
22,23,24,25,26,check
27,28,29,30,31,check
32,33,34,35,36,check
37,38,39,40,41,check
42,43,44,45,46,check
47,48,49,check
```

## Sketch of usage

In real usage, I use the following callback:
```python
def check_for_interrupt(interrupt_buffer):
    def helper():
        if interrupt_buffer() == 0:
            return
        raise KeyboardInterrupt()
    return helper
```

`interrupt_buffer` is a javascript wrapper around a `SharedArrayBuffer`. On the main thread:
```javascript
let uuid = uuid();
let interrupt_buffer = new Int32Array(new SharedArrayBuffer(4));
pyodide_worker.postMessage({"cmd" : "execute_python", code, interrupt_buffer, uuid});
let result = await responsePromise(uuid);
// If user cancels, write a nonzero value into our SAB, this will signal pyodide to quit execution of code.
onUserCancel(() => { interrupt_buffer[0] = 2; });
```
On the pyodide worker thread:
```javascript
self.messages = {};
function handleExecutePython(msg){
    // Wrap interrupt buffer in a function that gets its value
    // Pyodide Python <==> Javascript bindings don't understand how to get values out of the SAB directly.
    msg.interrupt_buffer = function(){
        return msg.interrupt_buffer[0]; 
    };
    messages[msg.uuid] = msg;
    self.pyodide.globals["handle_message"](uuid);
}
```
and then the pyodide code:

```python
from js import messages, postMessage
def handle_message(uuid):
    msg = dict(messages[uuid])
    del messages[uuid]
    # Here would use msg["cmd"] to look up handling in a dispatch.
    interrupt_buffer = msg["interrupt_buffer"]
    # check_for_interrupt will raise a KeyboardInterrupt if "onUserCancel" handler is executed on main thread.
    with check_interrupts(check_for_interrupt(interrupt_buffer), 10_000):
        result = run_code(code)
    postMessage({"cmd" : "execute_pyodide_result", "result" : result, "uuid" : uuid })

def run_code(code):
    # Parse code into ast, handle errors, get result out, etc here
```

## Security requirements for `SharedArrayBuffer` to work

I quote from [the MDN docs for SharedArrayBuffer](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/SharedArrayBuffer):

> As a baseline requirement, your document needs to be in a secure context.

> For top-level documents, two headers will need to be set to cross-origin isolate your site:

>    Cross-Origin-Opener-Policy with same-origin as value (protects your origin from attackers)
>    Cross-Origin-Embedder-Policy with require-corp as value (protects victims from your origin)

> Cross-Origin-Opener-Policy: same-origin
> Cross-Origin-Embedder-Policy: require-corp

> To check if cross origin isolation has been successful, you can test against the crossOriginIsolated property available to window and worker contexts

## Building
To build a copy for local use, I recommend creating a virtual environment and then using `pip install .` in that virtual environment.
To upload to pypi, we must build the package for a `manylinux` ABI to insure that the binaries will be compatible with most systems.
The [manylinux](https://github.com/pypa/manylinux) repository provides docker images with the appropriate old versions of CentOS for us to use to build these. To build, run `sudo ./docker_build_wheels.sh`. **Warning:** This will download a ~300mb docker image the first time you do it. Note that you will need to have docker installed for this to work.
The resulting wheels will end up in the `dist` directory and will be suitable for upload to pypi.

## [0.1.0] (2020-07-25)