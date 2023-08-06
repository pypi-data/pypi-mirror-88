# LITETOKENS-CLI
```
#
#
#   ██▓     ██▓▄▄▄█████▓▓█████▄▄▄█████▓ ▒█████   ██ ▄█▀▓█████  ███▄    █   ██████ 
#  ▓██▒    ▓██▒▓  ██▒ ▓▒▓█   ▀▓  ██▒ ▓▒▒██▒  ██▒ ██▄█▒ ▓█   ▀  ██ ▀█   █ ▒██    ▒ 
#  ▒██░    ▒██▒▒ ▓██░ ▒░▒███  ▒ ▓██░ ▒░▒██░  ██▒▓███▄░ ▒███   ▓██  ▀█ ██▒░ ▓██▄   
#  ▒██░    ░██░░ ▓██▓ ░ ▒▓█  ▄░ ▓██▓ ░ ▒██   ██░▓██ █▄ ▒▓█  ▄ ▓██▒  ▐▌██▒  ▒   ██▒
#  ░██████▒░██░  ▒██▒ ░ ░▒████▒ ▒██▒ ░ ░ ████▓▒░▒██▒ █▄░▒████▒▒██░   ▓██░▒██████▒▒
#  ░ ▒░▓  ░░▓    ▒ ░░   ░░ ▒░ ░ ▒ ░░   ░ ▒░▒░▒░ ▒ ▒▒ ▓▒░░ ▒░ ░░ ▒░   ▒ ▒ ▒ ▒▓▒ ▒ ░
#  ░ ░ ▒  ░ ▒ ░    ░     ░ ░  ░   ░      ░ ▒ ▒░ ░ ░▒ ▒░ ░ ░  ░░ ░░   ░ ▒░░ ░▒  ░ ░
#    ░ ░    ▒ ░  ░         ░    ░      ░ ░ ░ ▒  ░ ░░ ░    ░      ░   ░ ░ ░  ░  ░  
#      ░  ░ ░              ░  ░            ░ ░  ░  ░      ░  ░         ░       ░  
#                                                                                 
#
```

A command line tool, to quick set up, turn on/off (multiple) litetokens nodes(full/solidity), and monitor running status.

| Python | JDK |
|--------|-----|
| 3.7+   | 1.8 |

* Learn more about litetokens on [LITETOKENS Developer Hub](https://developers.litetokens.org/docs/full-node)

* Join the community on [LITETOKENS Discord](https://discord.gg/GsRgsTD)

* Source code on [Github](https://github.com/litetokens/litetokens-cli)

* Project on [Pypi](https://pypi.org/project/litetokenscli/)

## Install

### pip

> pip install --upgrade pip

```
pip install litetokenscli
```

#### FAQs on installation

1. How to fix "fail to build a wheel for psutil" error?

    a. please check if you installed clang correctly, or install it using homebrew:

    ```
    brew install --with-toolchain llvm
    ```

    b. please check if you are using python 3.x

2. How to test in virtual environment?
    
    a. create virtual environment

    ```
    python3 -m venv venv
    ```

    b. activate venv

    ```
    . ./venv/bin/activate
    ```

    c. install litetokenscli in venv

    ```
    pip install litetokenscli
    ```

    d. when done testing, or using the venv - to deactivate venv

    ```
    deactivate
    ```

## Usage

| Command                                                                              | Functions                          | Example1        | Example2                                                                                                      |
|--------------------------------------------------------------------------------------|------------------------------------|-----------------|---------------------------------------------------------------------------------------------------------------|
| litetokens-cli init --version                                                              | Init dirs and fetch code.          | litetokens-cli init   | litetokens-cli init --version 3.1.3                                                                                 |
| litetokens-cli config --nettype --fullhttpport --solhttpport --fullgrpcport --solgrpcport  | Create and customize config files. | litetokens-cli config | litetokens-cli config --nettype main --fullhttpport 8500 --solhttpport 8600 --fullgrpcport 50051 --solgrpcport 5001 |
| litetokens-cli run --nodetype                                                              | Run node.                          | litetokens-cli run    | litetokens-cli run --nodetype sol                                                                                   |
| litetokens-cli stop --pid                                                                  | Stop node.                         | litetokens-cli stop   | litetokens-cli stop --pid 7777                                                                                      |
| litetokens-cli status --node                                                               | Monitor nodes status.              | litetokens-cli status | litetokens-cli status --node 777                                                                                    |
| litetokens-cli quick                                                                       | Quick start.                       | litetokens-cli quick  | litetokens-cli quick                                                                                                |
| litetokens-cli -h, --help                                                                  | Check help manual.                 | litetokens-cli -h     | litetokens-cli --help                                                                                               |
#### overall

```
litetokens-cli -h
```
```
usage: litetokens-cli [-h] {init,config,run,stop,status,quick} ...

which subcommand do you want?

optional arguments:
  -h, --help            show this help message and exit

subcommands:
  {init,config,run,stop,status,quick}
    init                Init dirs and fetch code.
    config              Create customize config files.
    run                 Run node.
    stop                Stop node.
    status              Monitor nodes status.
    quick               Quick start. (run a full private node by one command)
```

##### subcommand: init

```
litetokens-cli init -h
```
```
usage: litetokens-cli init [-h] [--version VERSION]

optional arguments:
  -h, --help         show this help message and exit
  --version VERSION  specify java-litetokens version
```

##### subcommand: config

```
litetokens-cli config -h
```
```
usage: litetokens-cli config [-h] [--nettype NETTYPE] [--fullhttpport FULLHTTPPORT]
                       [--solhttpport SOLHTTPPORT] [--fullrpcport FULLRPCPORT]
                       [--solrpcport SOLRPCPORT] [--enablememdb ENABLEMEMDB]

optional arguments:
  -h, --help            show this help message and exit
  --nettype NETTYPE     specify net type [main, private]
  --fullhttpport FULLHTTPPORT
                        specify full http port
  --solhttpport SOLHTTPPORT
                        specify solidity http port
  --fullrpcport FULLRPCPORT
                        specify full rpc port
  --solrpcport SOLRPCPORT
                        specify solidity rpc port
  --enablememdb ENABLEMEMDB
```

##### subcommand: run

```
litetokens-cli run -h
```
```
usage: litetokens-cli run [-h] [--nodetype NODETYPE]

optional arguments:
  -h, --help           show this help message and exit
  --nodetype NODETYPE  specify node type [full, sol]
```

##### subcommand: stop

```
litetokens-cli stop -h
```
```
usage: litetokens-cli stop [-h] --pid PID

optional arguments:
  -h, --help  show this help message and exit
  --pid PID   stop node by given pid
```

##### subcommand: status

```
litetokens-cli status -h
```
```
usage: litetokens-cli status [-h] [--node NODE]

optional arguments:
  -h, --help   show this help message and exit
  --node NODE  check specific node detail by pid
```
