# CBTaskBulker - A Run Multiple/Parallel Tasks through Carbon Black

The main objective of CBTaskBulker is facilitate the DFIR daily task in Threat Hunting, Compromise Assessment, and Incident Response in his environment, where he/she needs to run binaries - such as Loki, Hoarder, KAPE - across the environment and trough Carbon Black Response  

## CB API Token Configuration

To use CBTaskBulker, you need to acquire a user token from CB, where the user MUST have a "Live Response" Privilege. You can follow this link to configure API Token ["API Credentials"](https://cbapi.readthedocs.io/en/latest/#api-credentials)

Below is an example of how to configure the token in windows
- Create folder in the is path
```bash
C:\Users\<user>\.carbonblack
```
- Create "credentials.response" file
```bash
C:\Users\<user>\.carbonblack\credentials.response
```
- Write the follwing in "credentials.response" file
```bash
[default]
url = https://<CB Server IP>:<CB Server Port>/
token = <CB API Token>
ssl_verify = False

```
## Features
CBTaksBulker has the following functions:
- Run binaries on remote endpoint/s
- Get binaries result from remote endpoint/s
- Clean task folder
- Multi-Threading (each thread will utilize a session for each endpoint)

## Usage

The script relays on "Sensor ID" for choosing which endpoint should be targeted, and you can get by:
- Browse CB Server
- Go to "Sensores"
- Click on the desired Endpoint/Computer Name
- Get "Sensor ID"

To Start using you need to do: 
- Store all targeted endpoint "Sensor ID" in "id.txt", then use the help to run CBTaskBulker
- Verify/Change "run.bat" to fit your needs
    - Make sure that the results are stored in ".\DFIR_TASK\output" folder
- Run your task and chill :)

 
```bash
$ python CBTaskBulker.py -h
usage: CBTaskBulker.py [-h] [--get] [--clean] [--ml] [--threads THREADS]

CBTaskBulker - Run Multiple Tasks through Carbon Black

optional arguments:
  -h, --help         show this help message and exit
  --get              Get files in output folder
  --clean            Clean DFIR_Task folder
  --ml               Enable Multi Thread mode
  --threads THREADS  Number of threads to be used (Each thread will utilize a dedicated LR session)
```

# Refrences
[cbapi: Carbon Black API for Python](https://cbapi.readthedocs.io/en/latest/)