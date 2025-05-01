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

2. Copy `plugin.ron` and `floww.py` to you pop-launcher plugins folder

> Check [Plugin Directories](https://github.com/pop-os/launcher?tab=readme-ov-file#plugin-directories)

```bash
cd floww-pop-launcher-plugin
cp plugin.ron floww.py ~/.local/share/pop-launcher/plugins
```

1. Make `floww.py` executable

```bash
chmod +x ~/.local/share/pop-launcher/plugins/floww.py
```

## Usage

1. Launch pop-launcher and run

```
fl <workflow-name>
```
