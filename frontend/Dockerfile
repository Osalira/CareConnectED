# frontend/Dockerfile

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

# Want to help us make this template better? Share your feedback here: https://forms.gle/ybq9Krt8jtBL3iCk7


# ARG NODE_VERSION=20.9.0

# FROM node:${NODE_VERSION}-alpine

# Use a Node.js base image
FROM node:18-bullseye

# Set the working directory
WORKDIR /app
# WORKDIR /usr/src/app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application files
COPY . .

# Expose the Vite development server port
# for dev
# EXPOSE 5173

# # Run the Vite dev server
# for dev
# CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
RUN npm run build

CMD ["npx", "serve", "-s", "dist", "-l", "3000"]