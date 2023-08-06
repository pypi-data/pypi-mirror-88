# Statis

**Statis** is a system info and monitoring tool based on desktop notifications.
Its purpose is similar to that of traditional status bars or CLI tools, but
with the explicit goal of staying out of the way while not being used – saving
screen space and system resources. To this end, all its output occurs through
your notification daemon, making it ideal for quick access via key bindings.


## Table of Contents

* [Features](#features)
* [Installation](#installation)
  - [Requirements](#requirements)
  - [Stable Release](#stable-release)
  - [Development Version](#development-version)
* [Usage](#usage)
* [Key Binding Examples](#key-binding-examples)
* [Built-in Notifiers](#built-in-notifiers)
* [Contributors](#contributors)
* [License](#license)


## Features

* 10 built-in notifiers for resource usage (CPU, RAM, etc.), general info,
  [and more](#built-in-notifiers)
* Straightforward monitoring & alerts for many of said notifiers' measurements
* Notification-based output to enable more minimalist, status bar–less desktops
* Process only runs for output or while monitoring, saving on system resources


## Installation

### Requirements

* `Python 3.7+`
* Your favorite notification daemon
* `libnotify` (not required when using [`Dunst`](https://github.com/dunst-project/dunst))

### Stable Release

```shell
pip install --user statis
```

### Development Version

```shell
git clone https://gitlab.com/BVollmerhaus/statis
cd statis
pip install --user .
```


## Usage

### Direct Invocation

Each of Statis' outputs is provided by a corresponding notifier, multiple of
which are generally grouped into modules.

```shell
statis [options] [module [notifier] [notifier_args...]]
```

A notifier is run by specifying its module and name. For example, the `memory`
module's `used` notifier is invoked with:

```shell
statis memory used
```

If a notifier's name is identical to its containing module, it can also be
invoked with just that:

```shell
statis time
```

Additional arguments may be passed to both `statis` and, if applicable, the
invoked notifier:

```shell
statis --urgency "low" date --format "Week %W"
```

> This includes `-h` to display further usage information and list all
> supported arguments.

### Monitoring

Many notifiers can continuously monitor their measurement and alert if it
exceeds a certain threshold or changes at all.

This is done via the `-m` argument, which may either contain a threshold in
the format `[<|>][=] <value> <unit>` at which to alert, or an empty string
(`""`) to do so on all changes. Whether a notifier supports monitoring and
with which units is part of its help message.

```shell
# Alert when memory usage exceeds 4 GB
statis -m "4GB" memory used

# Alert when used swap space is 2 GB or more
statis -m ">=2GB" memory used-swap
```

Most notifiers also support percentage-based monitoring by supplying `%` as
the threshold unit:

```shell
statis -m "75%" memory used
```


## Key Binding Examples

Statis itself does not implement key binding; please use your DE/WM's native
functionality for this.

### i3

```
bindsym $mod+c exec --no-startup-id statis cpu usage
```
> Tip: i3's [binding modes](https://i3wm.org/docs/userguide.html#binding_modes)
> may be especially useful for this purpose.

### awesome

```lua
awful.key({ modkey }, "c", function()
  awful.spawn("statis cpu usage", false)
end)
```

### bspwm (sxhkd)

```
super + c
    statis cpu usage
```


## Built-in Notifiers

Statis currently includes the following notifiers (grouped by **`module`**):

* **`battery`**
  - `charge`
* **`cpu`**
  - `frequency`
  - `governor`
  - `usage`
* **`date`**
* **`memory`**
  - `free`
  - `free-swap`
  - `used`
  - `used-swap`
* **`time`**


## Contributors

### Maintainer

* [Benedikt Vollmerhaus](https://gitlab.com/BVollmerhaus)

### Others

* [Matthias Bräuer](https://gitlab.com/Braeuer) (Creative Input)


## License

Statis is licensed under the MIT license. See
[LICENSE](https://gitlab.com/BVollmerhaus/statis/blob/master/LICENSE)
for more information.
