sudo apt -y install python3-venv git make build-essential
git clone https://github.com/raonyguimaraes/pynnotator
cd pynnotator
python3 -m venv venv
source venv/bin/activate
pip install wheel
pip install -r requirements.txt
python setup.py develop
