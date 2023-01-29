# Themis-ML: A system for automated feedback suggestions of programming exercises

This system implements an approach for automated feedback suggestions of programming exercises based on prior manual feedback. It is integrated into the [Themis](https://github.com/ls1intum/Themis) App, as well as the LMS [Artemis](https://github.com/ls1intum/Artemis).

## Architecture
Themis-ML is built using a microservice architecture. For now, it has two components:

  1.  **Load Balancer:** Provides Service in the form of a HTTP REST API to communicate with the Themis App (and probably also Artemis).
  2.  **Feedback Suggestion:** Component for generating automated feedback suggestions based on Machine Learning models.

## Testing

In local deployment, the server can be accessed via `localhost`.

Using the `docker-compose.yml` file included in the root directory of the repository is the easiest way to start the system.
 
The execution of
```
docker-compose up -d
```
will automatically build and start all components. (The `-d` parameter will run containers in the background).
By default, a traefik-container will manage API-Endpoints and expose them on port 80 (default HTTP-port).
Traefik provides a dashboard to monitor the status of the underlying components on port 8080.

In the development process the whole system or a single component (container) can be re-built and started using e.g.
```
docker-compose up -d --build
```
or
```
docker-compose up -d --build feedback-suggestion
```

To stop the whole system or a single container (as seen in the command above) use either
```
docker-compose stop
```
to stop all running containers or
```
docker-compose down
```
to stop and remove all containers.

## Production

In production deployment, the server can be accessed via `ios2223cit.ase.cit.tum.de`.

Using the `docker-compose.production.yml` file included in the root directory of the repository is the easiest way to start the system.

The execution of
```
docker compose -f docker-compose.production.yml up -d
```
will automatically build and start all components.

All the other commands above have to be adapted accordingly for production.
