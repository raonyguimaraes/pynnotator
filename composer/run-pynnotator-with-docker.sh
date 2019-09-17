wget www.mendelmd.org/pynnotator-data.latest.tar
tar -xf pynnotator-data.latest.tar
docker-compose run pynnotator pynnotator test
