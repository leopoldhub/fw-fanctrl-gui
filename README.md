# fw-fanctrl GUI

![Static Badge](https://img.shields.io/badge/Global-9AFF59?style=flat&label=Platform)
![Static Badge](https://img.shields.io/badge/no%20binary%20blobs-30363D?style=flat&logo=GitHub-Sponsors&logoColor=4dff61)

[![Static Badge](https://img.shields.io/badge/Python__3.12-FFDE57?style=flat&label=Requirement&link=https%3A%2F%2Fwww.python.org%2Fdownloads)](https://www.python.org/downloads)

[![Static Badge](https://img.shields.io/badge/fw--fanctrl%20>=%20v1.0.1-12C6FF?style=flat&label=Requirement&link=https%3A%2F%2Fgithub.com%2FTamtamHero%2Ffw-fanctrl)](https://github.com/TamtamHero/fw-fanctrl)

**⚠️ This version requires an experimental version of fw-fanctrl [leopoldhub/fw-fanctrl/full-api-compatibility](https://github.com/leopoldhub/fw-fanctrl/tree/full-api-compatibility) ⚠️**

## Description

fw-fanctrl GUI is a simple multiplatform customtkinter python GUI to interact with
the [fw-fanctrl](https://github.com/TamtamHero/fw-fanctrl) CLI.

It includes a basic GUI, as well as a system tray to easily change your fan profiles on the go.

![gui.png](.documentation/resources/screenshots/gui.png)

<!-- ![tray.png](.documentation/resources/screenshots/tray.png) -->

> **Important information**
>
> This project currently is in its early stage of development, is not complete yet and may be unstable or broken on
> certain platforms at any given point.
>
> Here are the currently supported features:
>
> - selecting/displaying the current strategy
> - resetting to the default strategy
> - reloading the service configuration
> - pausing/resuming the service
>
> Here is the feature plan for the foreseeable future:
>
> - **System tray**
> - **Background launch**
> - selecting the default strategy
> - enabling and selecting the discharging strategy

## Installation

### Requirements

| name   | version | url                                                                  |
|--------|---------|----------------------------------------------------------------------|
| Python | 3.12.x  | [https://www.python.org/downloads](https://www.python.org/downloads) |

### Dependencies

Before installing the GUI, make sure have installed the latest version of
the [fw-fanctrl](https://github.com/TamtamHero/fw-fanctrl) CLI.

| name                  | version | url                                                                                  |
|-----------------------|---------|--------------------------------------------------------------------------------------|
| TamtamHero@fw-fanctrl | latest  | [https://github.com/TamtamHero/fw-fanctrl](https://github.com/TamtamHero/fw-fanctrl) |

### Instructions

[Download the repo](https://github.com/leopoldhub/fw-fanctrl-gui/archive/refs/heads/master.zip) and extract it manually, or
download/clone it with the appropriate tools:

**unix**

```shell
git clone "https://github.com/leopoldhub/fw-fanctrl-gui.git"
```

```shell
curl -L "https://github.com/leopoldhub/fw-fanctrl-gui/archive/refs/heads/master.zip" -o "./fw-fanctrl-gui.zip" && unzip "./fw-fanctrl-gui.zip" -d "./fw-fanctrl-gui" && rm -rf "./fw-fanctrl-gui.zip"
```

**windows**

```shell
git clone "https://github.com/leopoldhub/fw-fanctrl-gui.git"
```

```shell
curl -L "https://github.com/leopoldhub/fw-fanctrl-gui/archive/refs/heads/master.zip" -o "./fw-fanctrl-gui.zip" && tar -xf "./fw-fanctrl-gui.zip" && del "./fw-fanctrl-gui.zip"
```

---

Then go inside the extracted folder with a terminal and install the dependencies with

```bash
pip install .
```

## Run

To run the application, use the following command

```shell
fw_fanctrl_gui
```
<!--
Here are the additional options you can use

| Option           | Optional | Description                                                          |
|------------------|----------|----------------------------------------------------------------------|
| --background, -b | yes      | run the application in the background. does not open the main window |
-->
