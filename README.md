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

2. Copy the `plugin` folder to your pop-launcher plugins folder as `floww`

> Check [Plugin Directories](https://github.com/pop-os/launcher?tab=readme-ov-file#plugin-directories)

```bash
cd floww-pop-launcher-plugin
mkdir -p ~/.local/share/pop-launcher/plugins/floww
cp plugin/* ~/.local/share/pop-launcher/plugins/floww
```

3. Make `floww.py` executable

```bash
chmod +x ~/.local/share/pop-launcher/plugins/floww/floww.py
```

## Usage

1. Launch pop-launcher and run

```
fl <workflow-name>
```
