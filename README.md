# ocsw-cli - Octave Cloud command-line tool

[![Build Status](https://travis-ci.com/maxim-s-barabash/ocsw.svg?branch=master)](https://travis-ci.com/maxim-s-barabash/ocsw)
[![PyPI version](https://badge.fury.io/py/ocsw.svg)](https://badge.fury.io/py/ocsw)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)


This is not an official implementation of the command line interface (CLI) for 
the [Octave Cloud REST API](https://octave-api.sierrawireless.io/v5.0).

The ocsw makes calls to Octave Cloud Infrastructure APIs to provide 
the functionality implemented for the various services. These are REST APIs that 
use HTTPS requests and responses.

## API Reference

This package includes a client implementing the api described in https://rest.octave.dev/

## Requirements

To install and use the CLI, you must have:

- An Octave Cloud Infrastructure account. A user created in that account, in a group with a policy that grants the desired permissions. This account user can be that calls the API.

- System use token-based authentication. You can get the API token for your user by logging into [Octave Cloud](https://octave.sierrawireless.io/), On the lower left side of the main page, you will see Master Token option. Click here and a pop up will display your token along with the user you will use with the Octave Cloud APIs.

## Installation

As per usual:

```shell
pip install ocsw
```

## Environment variables

| VARIABLE             | Description                                        |
|----------------------|----------------------------------------------------|
| OCTAVE_CLOUD_API_URL | default: https://octave-api.sierrawireless.io/v5.0<br>End point octave cloud |
| OCTAVE_CLOUD_TOKEN   | Master Token                                       |
| OCTAVE_CLOUD_USER    | Your user id                                       |
| OCTAVE_CLOUD_COMPANY | Identifier of one of the company                   |


## Usage
```
usage: ocsw-cli [-h] [-H] [-C PATH] [-D] [-v] [--show-secrets]  ...

Manage and monitor your devices

optional arguments:
  -h, --help      show this help message and exit
  -H              show help from all command
  -C PATH         location of configuration path (default ".")
  -D, --debug     enable debug output
  -v, --version   show program's version number and exit
  --show-secrets  decrypt secrets and displays plain text

commands:
  
    blueprint     Manage blueprints
    cloud         Manage cloud
    cloud_action  Manage cloud actions
    company       Manage companies
    device        Manage devices
    edge_action   Manage edge actions
    firmware      Manage firmware's
    group         Manage user groups
    stream        Manage streams
    user          Manage users
    identity      Display detailed information about current user
    login         Log in to a Octave Cloud
    logout        Log out from a Octave Cloud
    release       Display Octave API Version Information
```
## Command: blueprint
```
usage: ocsw-cli blueprint [-h] COMMAND ...

Manage blueprints

positional arguments:
  COMMAND
    ls        display blueprint list
    inspect   display detailed information on one or more blueprints

optional arguments:
  -h, --help  show this help message and exit
```
## Command: cloud
```
usage: ocsw-cli cloud [-h] COMMAND ...

Manage Cloud

positional arguments:
  COMMAND
    fetch     download objects and refs from cloud

optional arguments:
  -h, --help  show this help message and exit
```
## Command: cloud_action
```
usage: ocsw-cli cloud_action [-h] COMMAND ...

Manage cloud actions

positional arguments:
  COMMAND
    inspect   display detailed information on one or more cloud actions
    ls        list cloud action

optional arguments:
  -h, --help  show this help message and exit
```
## Command: company
```
usage: ocsw-cli company [-h] COMMAND ...

Manage companies

positional arguments:
  COMMAND
    ls        display company list
    inspect   display detailed information on one or more companies
    switch    set company active

optional arguments:
  -h, --help  show this help message and exit
```
## Command: device
```
usage: ocsw-cli device [-h] COMMAND ...

Manage devices

positional arguments:
  COMMAND
    actions   list device edge actions
    create    creating device
    inspect   display detailed information on one or more devices
    lc        list devices configuration
    li        list devices identity
    ls        list devices connectivity
    rm        remove one or more devices
    tags      set device tags
    events    display recent events
    changes   display recent changes

optional arguments:
  -h, --help  show this help message and exit
```
## Command: edge_action
```
usage: ocsw-cli edge_action [-h] COMMAND ...

Manage edge actions

positional arguments:
  COMMAND
    inspect   display detailed information on one or more edge actions
    ls        list edge action

optional arguments:
  -h, --help  show this help message and exit
```
## Command: firmware
```
usage: ocsw-cli firmware [-h] COMMAND ...

Manage firmwares

positional arguments:
  COMMAND
    ls        list of available firmware
    note      display notes on one or more firmware

optional arguments:
  -h, --help  show this help message and exit
```
## Command: group
```
usage: ocsw-cli group [-h] COMMAND ...

Manage user groups

positional arguments:
  COMMAND
    ls        display user group list
    inspect   display detailed information on one or more user groups

optional arguments:
  -h, --help  show this help message and exit
```
## Command: stream
```
usage: ocsw-cli stream [-h] COMMAND ...

Manage streams

positional arguments:
  COMMAND
    ls        display streams list
    inspect   display detailed information on one or more streams
    events    display stream events list

optional arguments:
  -h, --help  show this help message and exit
```
## Command: user
```
usage: ocsw-cli user [-h] COMMAND ...

Manage users

positional arguments:
  COMMAND
    ls        display user list
    inspect   display detailed information on one or more users

optional arguments:
  -h, --help  show this help message and exit
```
## Command: identity
```
usage: ocsw-cli identity [-h]

Display detailed information about current user

optional arguments:
  -h, --help  show this help message and exit
```
## Command: login
```
usage: ocsw-cli login [-h] [-t] [-u] [COMPANY]

Log in to a Octave Cloud

positional arguments:
  COMPANY           company name

optional arguments:
  -h, --help        show this help message and exit
  -t , --token      token
  -u , --username   username
```
## Command: logout
```
usage: ocsw-cli logout [-h]

Log out from a Octave Cloud

optional arguments:
  -h, --help  show this help message and exit
```
## Command: release
```
usage: ocsw-cli release [-h]

Display Octave API Version Information

optional arguments:
  -h, --help  show this help message and exit
```
