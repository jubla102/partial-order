Installation Guide
<hr>

The system can be completely run in Docker. Therefore, only a Docker installation is required. After cloning the repository, the following commands have to be run in the partial-order directory:

docker build -t partial-orders
docker run -p 8080:8000 partial-orders

Then the application can be reached in a web browser via:
http://localhost:8080/
