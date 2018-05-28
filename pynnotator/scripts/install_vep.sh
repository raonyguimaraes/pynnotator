#!/bin/bash

### docker container for ensembl-vep


# update aptitude and install some required packages
# a lot of them are required for Bio::DB::BigFile
# sudo apt-get update && sudo apt-get -y install apache2 build-essential cpanminus curl git libmysqlclient-dev libpng-dev libssl-dev manpages mysql-client openssl perl perl-base unzip vim wget
# install ensembl dependencies
# sudo cpanm DBI DBD::mysql Bio::DB::HTS::Faidx

# create vep user
#useradd -r -m -U -d /home/vep -s /bin/bash -c "VEP User" -p '' vep
#usermod -a -G sudo vep
#USER vep
export parent=`dirname $PWD`
echo $parent
# export grandparent=`dirname $parent`

#cd $HOME
#cd ../libs/vep/

export HOME=$parent/vep

# clone git repositories
mkdir -p src
cd src

git clone https://github.com/Ensembl/ensembl.git
git clone https://github.com/Ensembl/ensembl-vep.git

# get VEP dependencies

bash ensembl-vep/travisci/get_dependencies.sh
export PERL5LIB=$PERL5LIB:$HOME/src/bioperl-live-release-1-6-924
export KENT_SRC=$HOME/src/kent-335_base/src
export HTSLIB_DIR=$HOME/src/htslib
export MACHTYPE=x86_64
export CFLAGS="-fPIC"
export DEPS=$HOME/src

# and run the complilation/install as root
bash ensembl-vep/travisci/build_c.sh

# install htslib binaries (need bgzip, tabix)
cd htslib
sudo make install

# install bioperl-ext, faster alignments for haplo
cd $HOME/src
git clone https://github.com/bioperl/bioperl-ext.git
cd bioperl-ext/Bio/Ext/Align/
perl -pi -e"s|(cd libs.+)CFLAGS=\\\'|\$1CFLAGS=\\\'-fPIC |" Makefile.PL
perl Makefile.PL
make
sudo make install

# install perl dependencies
cd $HOME/src
cpanm --installdeps --with-recommends --notest --cpanfile ensembl/cpanfile .
cpanm --installdeps --with-recommends --notest --cpanfile ensembl-vep/cpanfile .

# switch back to vep user
# update bash profile
echo >> $HOME/.profile && \
echo PATH=$HOME/src/ensembl-vep:\$PATH >> $HOME/.profile && \
echo export PATH >> $HOME/.profile

# setup environment
export PATH=$parent/vep/src/ensembl-vep:$PATH

# run INSTALL.pl
cd $HOME/src/ensembl-vep
chmod u+x *.pl
# rm -rf Bio 
#
./INSTALL.pl -a a -l --NO_TEST
# ./INSTALL.pl -a acf -s homo_sapiens -c $parent/data/vep_data --ASSEMBLY GRCh37 --NO_TEST
