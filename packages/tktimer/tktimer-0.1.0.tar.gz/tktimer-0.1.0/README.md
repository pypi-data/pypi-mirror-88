# tktimer 

**tktimer** is a set of tkinter widgets including a Stopwatch widget and a Countdown widget.

## Installing

```sh
$ pip install tktimer
```

## Usage

The timers have two methods: `start()` and `pause()`.

You can find example programs in `examples/`.

**Available options**:

|     option      | description |  default  |
| --------- |:------------------|----------|
| `parent`  | set the parent widget. ||
| `prefix`  | set text before timer value.| `""`|
| `suffix`  | set text after timer value.|`""`|
| `unit`    | set the unit (available: `second`, `minute`, `hour`, `day`, `week`, `year`).|`second`|
| `beginning` | set starting point (in seconds). specific to `Countdown`.|`10`|
| `update_every`| set updating time every X milliseconds.|`10`|
| `precision`   | set counting precision (number of digits after the decimal point).|`2`|
| `offset`| set time offset (in seconds). specific to `Stopwatch`.|`10`|

## FAQ

**How can I continue the timer after restarting my app?**

You can get the elapsed time (in seconds) with `timer.value.get()` on exit and set `offset` later on, which will make the timer start counting from `offset`. For `Countdown`, tweak `beginning` instead of `offset`.

**I'm not happy with how my timer looks like. Can I change its appearance?**

Yes, timers are ultimately just tkinter labels which means you can do anything you would to an ordinary `tkinter.Label`.

## Licensing

Licensed under the [MIT License](https://opensource.org/licenses/MIT). For details, see [LICENSE](https://github.com/adder46/tktimer/blob/master/LICENSE).