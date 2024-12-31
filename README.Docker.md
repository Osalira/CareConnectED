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

### Readme.md

# CareConnectED Web Application Docker Guide

This document provides a step-by-step guide to build and push Docker images for the CareConnectED web application. This process includes signing in to GitHub Container Registry (ghcr), building Docker images for the frontend and backend, and pushing these images to the registry.

---

## Prerequisites

1. **Docker Installed**: Ensure Docker is installed on your system. For installation instructions, visit [Docker's official website](https://www.docker.com/get-started).

2. **GitHub Account**: You need a GitHub account with access to the repository containing the application code.

3. **Access to GHCR**: Ensure you have permissions to push to the GitHub Container Registry (ghcr.io).

4. **Project Setup**: The project folder should contain `Dockerfile.frontend` and `Dockerfile.backend` files for the respective components.

---

## Step 1: Authenticate with GitHub Container Registry

To authenticate with GitHub Container Registry:

1. **Sign in using Docker CLI**:
   ```bash
   echo "<YOUR_GITHUB_PERSONAL_ACCESS_TOKEN>" | docker login ghcr.io -u <YOUR_GITHUB_USERNAME> --password-stdin
   ```
   Replace `<YOUR_GITHUB_PERSONAL_ACCESS_TOKEN>` with your GitHub Personal Access Token that has `write:packages` and `read:packages` permissions.

2. Verify the login:
   ```bash
   docker info | grep -i "ghcr.io"
   ```

---

## Step 2: Build the Frontend Docker Image

Navigate to the root directory of the project and execute the following command to build the frontend image:

```bash
docker build -t ghcr.io/osalira/careconnected-frontend:v1.0 -f Dockerfile.frontend .
```

### Explanation:
- `-t`: Specifies the image tag.
- `-f`: Specifies the Dockerfile to use.
- `.`: Refers to the build context, typically the root directory of your project.

---

## Step 3: Push the Frontend Docker Image

After building the image, push it to GHCR:

```bash
docker push ghcr.io/osalira/careconnected-frontend:v1.0
```

---

## Step 4: Build the Backend Docker Image

Execute the following command to build the backend image:

```bash
docker build -t ghcr.io/osalira/careconnected-backend:v1.0 -f Dockerfile.backend .
```

### Explanation:
- `-t`: Specifies the image tag.
- `-f`: Specifies the Dockerfile to use.
- `.`: Refers to the build context, typically the root directory of your project.

---

## Step 5: Push the Backend Docker Image

After building the image, push it to GHCR:

```bash
docker push ghcr.io/osalira/careconnected-backend:v1.0
```

---

## Step 6: Verify the Images on GHCR

To verify that the images have been pushed successfully:

1. Visit [GitHub Packages](https://github.com/settings/packages).
2. Locate the `careconnected-frontend` and `careconnected-backend` images under the `ghcr.io/osalira` namespace.

---

## Troubleshooting

1. **Authentication Issues**:
   - Ensure your Personal Access Token has the required permissions.
   - Re-authenticate using the Docker CLI if necessary.

2. **Build Errors**:
   - Ensure the `Dockerfile.frontend` and `Dockerfile.backend` are correctly configured.
   - Check for missing dependencies or incorrect configurations in the project.

3. **Push Errors**:
   - Verify that the image tag matches the one used in the `docker build` command.
   - Check your internet connection and GHCR access permissions.

---

## Conclusion

Following these steps ensures the CareConnectED web application's Docker images are built and pushed to GitHub Container Registry successfully. You can now deploy the application using the published Docker images.

