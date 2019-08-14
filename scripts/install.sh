sudo apt -y install python3-venv git make build-essential 
sudo apt-get install -y gcc git python3-dev zlib1g-dev make zip libssl-dev \
libbz2-dev liblzma-dev libcurl4-openssl-dev build-essential libxml2-dev \
apache2 zlib1g-dev bcftools build-essential cpanminus curl git libbz2-dev libcurl4-openssl-dev \
liblocal-lib-perl liblzma-dev default-libmysqlclient-dev libpng-dev libpq-dev libssl-dev manpages \
mysql-client openssl perl perl-base pkg-config python3-dev python3-pip python3-setuptools \
sed tabix unzip vcftools vim wget zlib1g-dev apache2 build-essential cpanminus curl git \
libpng-dev libssl-dev locales manpages mysql-client openssl perl perl-base unzip vim wget libgd-dev
git clone https://github.com/raonyguimaraes/pynnotator
cd pynnotator
python3 -m venv venv
source venv/bin/activate
pip install wheel
pip install -r requirements.txt
python setup.py develop
