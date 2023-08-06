
SSH CLI Tools
=============

|PyPI| |CI| |Codecov|

**SSH CLI Tools** provides a set of commands for interacting remotely and easily
with IoT-Lab Linux nodes. See `here <https://www.iot-lab.info/docs/boards/iot-lab-a8-m3/>`_
to get more information on this kind of node.

All available actions provided by **SSH CLI Tools** are available as sub-commands
of `iotlab-ssh`.

The provided sub-commands are:

=================== ==========================================================================================
 Sub-command        Function
=================== ==========================================================================================
 **flash**           Flash the given firmware on the nodes co-microcontroller
 **reset**           Reset the nodes co-microcontroller
 **wait-for-boot**   Block the execution until all nodes have booted or maximum wait time has expired
 **run-script**      Run a given script in background (screen session) on the given nodes
 **run-cmd**         Run a command on the given nodes
 **copy-file**       Copy a file on SSH frontend homedir directory (*~/shared/.iotlabsshcli*)
=================== ==========================================================================================

**SSH CLI Tools** can be used in conjunction with the
`IoT-Lab CLI Tools <https://github.com/iot-lab/cli-tools>`_ commands like
`iotlab-auth` and `iotlab-experiment`.

Installation:
-------------

You need python `pip <https://pip.pypa.io/en/stable/>`_.
To do a system-wide install of the ssh-cli-tools use pip (or pip3 for
Python 3)::

    $ sudo pip install iotlabsshcli

Pip version >= 9.0 is known to work ; you may need to upgrade.
See `<INSTALLING.md>`_ for details on installation options.

Requirements:
-------------

Linux nodes are reachable through a gateway SSH server (IoT-LAB SSH
frontend). For this reason you must verify that your SSH public key used by
ssh-cli-tools has been recorded in your IoT-LAB user profile. You can find how
to configure your IoT-LAB SSH access in this
`documentation <https://www.iot-lab.info/docs/getting-started/ssh-access/>`_.

Examples:
---------

Start an experiment, wait for it to be ready, wait for all nodes boot:
......................................................................

.. code-block::

    $ iotlab-experiment submit -d 120 -l saclay,a8,1-10
    {
        "id": 65535
    }
    $ iotlab-experiment wait
    Waiting that experiment 65535 gets in state Running
    "Running"
    $ iotlab-ssh wait-for-boot
    {
        "wait-for-boot": {
            "0": [
                "node-a8-2.saclay.iot-lab.info",
                "node-a8-3.saclay.iot-lab.info",
                "node-a8-5.saclay.iot-lab.info",
                "node-a8-6.saclay.iot-lab.info",
                "node-a8-7.saclay.iot-lab.info",
                "node-a8-9.saclay.iot-lab.info",
                "node-a8-10.saclay.iot-lab.info"
            ],
            "1": [
                "node-a8-4.saclay.iot-lab.info",
                "node-a8-8.saclay.iot-lab.info"
            ]
        }
    }


**Note:** node-a8-4 and node-a8-8 are broken in Saclay.

Flash a firmware on the co-microcontroller of the working nodes:
................................................................

.. code-block::

    $ iotlab-ssh flash <firmware.elf> -l saclay,a8,2-3+5-7+9-10
    {
        "flash": {
            "0": [
                "node-a8-2.saclay.iot-lab.info",
                "node-a8-3.saclay.iot-lab.info",
                "node-a8-5.saclay.iot-lab.info",
                "node-a8-6.saclay.iot-lab.info",
                "node-a8-7.saclay.iot-lab.info",
                "node-a8-9.saclay.iot-lab.info",
                "node-a8-10.saclay.iot-lab.info"
            ]
        }
    }

Reset the co-microcontroller of one node:
.........................................

.. code-block::

    $ iotlab-ssh reset -l saclay,a8,2
    {
        "reset": {
            "0": [
                "node-a8-2.saclay.iot-lab.info"
            ]
        }
    }

Use the *--verbose* option to get the commands output:
......................................................

.. code-block::

    $ iotlab-ssh --verbose reset -l saclay,a8,2
    Connecting via SSH proxy saclay.iot-lab.info:22 -> node-a8-2.saclay.iot-lab.info:22
    [node-a8-2.saclay.iot-lab.info]	Open On-Chip Debugger 0.9.0-dirty (2016-04-15-00:55)
    [node-a8-2.saclay.iot-lab.info]	Licensed under GNU GPL v2
    [node-a8-2.saclay.iot-lab.info] For bug reports, read
    [node-a8-2.saclay.iot-lab.info]	http://openocd.org/doc/doxygen/bugs.html
    [node-a8-2.saclay.iot-lab.info]	adapter speed: 1000 kHz
    [...]
    [node-a8-2.saclay.iot-lab.info]	TargetName         Type       Endian TapName            State
    [node-a8-2.saclay.iot-lab.info]	--  ------------------ ---------- ------ ------------------ ------------
    [node-a8-2.saclay.iot-lab.info] 0* stm32f1x.cpu       cortex_m   little stm32f1x.cpu       running
    [node-a8-2.saclay.iot-lab.info]	Info : JTAG tap: stm32f1x.cpu tap/device found: 0x3ba00477 (mfg: 0x23b, part: 0xba00, ver: 0x3)
    [node-a8-2.saclay.iot-lab.info]	Info : JTAG tap: stm32f1x.bs tap/device found: 0x06414041 (mfg: 0x020, part: 0x6414, ver: 0x0)
    [node-a8-2.saclay.iot-lab.info]	shutdown command invoked
    [node-a8-2.saclay.iot-lab.info]	Return Value: 0
    {
        "reset": {
            "0": [
                "node-a8-2.saclay.iot-lab.info"
            ]
        }
    }

Run a command on two nodes:
...........................

.. code-block::

    $ iotlab-ssh --verbose run-cmd "uname -a" -l saclay,a8,2-3
    Connecting via SSH proxy saclay.iot-lab.info:22 -> node-a8-2.saclay.iot-lab.info:22
    [node-a8-2.saclay.iot-lab.info]	Linux node-a8-2 3.18.5-iotlab+ #9 Thu Sep 1 16:17:22 CEST 2016 armv7l GNU/Linux
    [node-a8-3.saclay.iot-lab.info]	Linux node-a8-3 3.18.5-iotlab+ #9 Thu Sep 1 16:17:22 CEST 2016 armv7l GNU/Linux
    {
        "run-cmd": {
            "0": [
                "node-a8-2.saclay.iot-lab.info",
                "node-a8-3.saclay.iot-lab.info"
            ]
        }
    }

Run a command on SSH frontend:
..............................

.. code-block::

    $ iotlab-ssh --verbose run-cmd "uname -a" --frontend
    [saclay.iot-lab.info]	Linux saclay 3.16.0-4-amd64 #1 SMP Debian 3.16.36-1+deb8u1 (2016-09-03) x86_64 GNU/Linux
    {
        "run-cmd": {
            "0": [
                "saclay.iot-lab.info"
            ]
        }
    }

Copy file on SSH frontend homedir directory (~/shared/.iotlabsshcli):
.....................................................................

.. code-block::

    $ iotlab-ssh copy-file test.tar.gz
    {
        "run-cmd": {
            "0": [
                "saclay.iot-lab.info"
            ]
        }
    }
    $ iotlab-ssh run-cmd "tar -xzvf ~/shared/.iotlabsshcli/test.tar.gz -C ~/shared/.iotlabsshcli/" --frontend
    {
        "run-cmd": {
            "0": [
                "saclay.iot-lab.info"
            ]
        }
    }

**Note:** shared homedir directory is mounted (via NFS) by Linux nodes during experiment.

Run the script `/tmp/test.sh` on `node-a8-2` in saclay:
.......................................................

.. code-block::

    $ iotlab-ssh run-script /tmp/test.sh -l saclay,a8,2
    {
        "run-script": {
            "0": [
                "node-a8-2.saclay.iot-lab.info"
            ]
        }
    }

**Note:** a screen session is launched on the node
to actually run the script and provide easy access to outputs if needed.
When the script ends, the screen session is terminated and the logs are gone.

.. code-block::

    root@node-a8-2:~# screen -ls
    There is a screen on:
           1877.<login>-<exp_id>   (Detached)
    1 Socket in /tmp/screens/S-root.

**Note:** similar to run command you can pass the *--frontend* option if
you want to launch a script in background on the SSH frontend.


.. |PyPI| image:: https://badge.fury.io/py/iotlabsshcli.svg
   :target: https://badge.fury.io/py/iotlabsshcli
   :alt: PyPI package status

.. |CI| image:: https://github.com/iot-lab/ssh-cli-tools/workflows/CI/badge.svg
    :target: https://github.com/iot-lab/ssh-cli-tools/actions?query=workflow%3ACI+branch%3Amaster
    :alt: CI status

.. |Codecov| image:: https://codecov.io/gh/iot-lab/ssh-cli-tools/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/iot-lab/ssh-cli-tools/branch/master
   :alt: Codecov coverage status
