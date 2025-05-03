
## Install environemtn
```bash
# Install dora-rs
export DORA_VERSION=v0.3.5 # Check for the latest release
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

