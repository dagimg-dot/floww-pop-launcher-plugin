# Floww Pop launcher plugin

- This is a [pop-launcher](https://github.com/pop-os/launcher) plugin for [floww](https://github.com/dagimg-dot/floww) (a workflow manager for linux)

## Prerequisites

- [pop-launcher](https://github.com/pop-os/launcher)
- [floww](https://github.com/dagimg-dot/floww)
- [pop-shell-gnome-extension](https://github.com/pop-os/shell) - If you are on GNOME

## Installation

1. Clone this repository

```bash
git clone https://github.com/dagimg-dot/floww-pop-launcher-plugin.git
```

1. Install the plugin

> Check [Plugin Directories](https://github.com/pop-os/launcher?tab=readme-ov-file#plugin-directories), if you don't know where to put the plugin. By default the `Makefile` assumes its `~/.local/share/pop-launcher/plugins`

```bash
cd floww-pop-launcher-plugin
make install
```

## Uninstall

```bash
make uninstall
```

## Usage

1. Launch pop-launcher and run

```
fl <workflow-name>
```

2. If you want to start the workflow starting from the last workspace, use `fa` instead of `fl`

```
fa <workflow-name>
```
