#download gnomead data
export parent=`dirname $PWD`
cd $parent/data/
mkdir -p gnomead
cd gnomead
gsutil -m cp -r gs://gnomad-public/release/2.0.2/vcf .