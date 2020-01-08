# SS

This command searches a specific string from a specific directory

## How to use

```
sk -d "directory path" -s "Search keyword"

[Example]


ss -d "." -s "SELECT"


ss -s "SELECT" -m vim


[Example]

gf 

gf -m o

gf -m s -s my_unserilaze
```


## Install

python is required

```
[.bashrc]

alias sk="python3 your_path/ss/sk/sk_main.py"
alias gf="python3 your_path/ss/gf/gf.py"
```
