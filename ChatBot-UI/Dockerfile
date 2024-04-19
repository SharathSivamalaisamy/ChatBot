# Use the official Node.js base image
FROM node:14

# In some network environments, access to the internet is routed through a proxy server. When building Docker images or running containers, tools like apt-get or pip may need to download packages from the internet. If your network requires the use of a proxy server to access the internet, you need to configure the Docker container accordingly.
# Define environment variable
ENV HTTP_PROXY=http://proxy-in.its.hpecorp.net:443
ENV HTTPS_PROXY=http://proxy-in.its.hpecorp.net:443
ENV http_proxy=http://proxy-in.its.hpecorp.net:443
ENV https_proxy=http://proxy-in.its.hpecorp.net:443

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the React app
RUN npm run build

# Expose the port the React app runs on
EXPOSE 3000

# Command to run the React app
CMD ["npm", "start"]
