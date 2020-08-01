# ocsw-cli - Octave Cloud command-line tool

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


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
