I created a customer network with the following command. 
docker network create containers_network
This network will be used for docker containers communication.

Create a jars,jobs,notebooks folders.
In jars folder do the following 
curl -o postgresql-42.3.1.jar https://jdbc.postgresql.org/download/postgresql-42.3.1.jar