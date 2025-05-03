
## Install environemtn
```bash
# Install dora-rs
export DORA_VERSION=v0.3.10 # Check for the latest release
export ARCHITECTURE=$(uname -m)
wget https://github.com/dora-rs/dora/releases/download/${DORA_VERSION}/dora-${DORA_VERSION}-${ARCHITECTURE}-macOS.zip
unzip dora-${DORA_VERSION}-${ARCHITECTURE}-macOS.zip
python3 -m venv .venv
source .venv/bin/activate
pip install dora-rs==${DORA_VERSION}
PATH=$PATH:$(pwd)
dora --help

# Install requirements
pip install -r requirements.txt
```



COmputer

dora daemon --machine-id computer --coordinator-addr 192.168.1.150:53290

dora start dataflow_small.yml --coordinator-addr 192.168.1.150 --coordinator-port 53290



# 
Install dora-rs on raspberry pi:
```bash
cargo install dora-cli --locked
```

Install dora-rs on macos:
```bash
pip install dora-rs --upgrade   
pip install dora-rs-cli --upgrade
```


Run 
On remove machine 
dora coordinator
dora daemon --machine-id A --coordinator-addr 192.168.1.86

On current machine 
dora daemon --machine-id B --coordinator-addr 192.168.1.86 --local-listen-port 53290
dora start dataflow_small.yml --coordinator-addr 192.168.1.86 --coordinator-port 6012

