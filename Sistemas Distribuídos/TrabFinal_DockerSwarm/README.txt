*********** rodar aplicacao ***********

docker swarm init

docker build -t iot/coletor ./coletor
docker build -t iot/sensor ./sensor

docker stack deploy -c stack.yml iot

*********** acessar o painel ***********
http://localhost:5000/painel


*********** se fizer alteracoes no python *********** 
docker build -t iot/coletor ./coletor
docker service update --force iot_coletor

docker build -t iot/sensor ./sensor
docker service update --force iot_sensor_temperatura
docker service update --force iot_sensor_umidade
docker service update --force iot_sensor_vento
