# Simple CFG

A library to easily manage program configuration, for python.

# Installation

`pip install simplecfg`

# Quick Start
```python
import simplecfg
from os.path import join

__config_dir = join(simplecfg.dir.APP_DATA, "Program")

config = simplecfg.Config(__config_dir, "config")

config.set("name", "Max")
config.set("age", 17)
config.set("hobbies", ["coding", "hiking", "photography"])

for k in config.get_keys():
    print(k + " => " + str(config.get(k)))
```

Outputs:

```
age => 17
hobbies => ['coding', 'hiking', 'photography']
name => Max
```

# Usage

Simply `import simplecfg`, then instantiate a `simplecfg.Config(directory, name)`
object! Assuming *config* is an instance of simplecfg.Config:

### constructor(String *directory*, String *filename*): simplecfg.Config

Creates the Config object. *directory* is the directory
where the config file should be stored
(see [Predefined Directories](#predefined-directories)).
If it does not exist, it will be created automatically.
*filename* is the name of the config file.

### *config*.get(String *key*): Any

Returns the stored value for *key*. Will return whichever
type the value is stored as, with some exceptions (see below).

### *config*.set(String *key*, Any *value*): Void

Stores *value* at *key*. While any type can be
stored, only strings, numbers, booleans, lists, and dicts
are fully supported. This is because Simple CFG converts all
data into JSON, which does not support all python types (tuples,
complex objects, etc...). Those will be converted into their JSON
compatible equivalents.

### *config*.get_keys(): List

Returns a list of all keys.

### *config*.wipe(): Void

Erases the configuration, but does **not** delete the physical file.

### *config*.delete(): Void

Completely deletes the configuration file.

## Predefined Directories

Simple CFG contains some predefined directories (in `simplecfg.dir`,
automatically imported) to assist in configuration file placement.

### HOME

Resolves to the local user's folder (~).

### APP_DATA

| Linux | Windows | Mac OS |
| --- | --- | --- |
| ~/.local/share | ~\AppData\Roaming | ~/Library/Application Support |

### CONFIG

The same as APP_DATA, except resolves to ~/.config on Linux.

### DOCUMENTS

Resolves to ~/Documents

### CWD

Resolves to the current working directory. **NOT RECOMMENDED!**
You may run into permission issues with this one!

### TEMP

| Linux | Windows | Mac OS |
| --- | --- | --- |
| /tmp | ~\AppData\Local\Temp | /tmp |