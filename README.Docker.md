### Building and running your application

When you're ready, start your application by running:
`docker compose up --build`.

Your application will be available at http://localhost:8001.

Your application will be available at http://localhost:5173.
#### docker building
Make sure that docker-compose.yml has
  frontend:
    build: ./frontend
    container_name: careconnected_frontend
    ports:
      - "5173:5173"
    volumes:
      - ./frontend:/app  # Mount the frontend code for live changes
      - node_modules:/app/node_modules  # Use a named volume for node_modules
    command: ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
    depends_on:
      - backend  # Optional: wait for the backend to be ready

volumes:
  node_modules:
### Deploying your application to the cloud

First, build your image, e.g.: `docker build -t myapp .`.
If your cloud uses a different CPU architecture than your development
machine (e.g., you are on a Mac M1 and your cloud provider is amd64),
you'll want to build the image for that platform, e.g.:
`docker build --platform=linux/amd64 -t myapp .`.

Then, push it to your registry, e.g. `docker push myregistry.com/myapp`.

Consult Docker's [getting started](https://docs.docker.com/go/get-started-sharing/)
docs for more detail on building and pushing.

### References
* [Docker's Python guide](https://docs.docker.com/language/python/)