# Sample Dockerfile for Node.js Apps

# Use the official Node.js image as the base
FROM node:20.18.0

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json files to the working directory
COPY ["package.json", "package-lock.json*", "./"]

# Install production dependencies only
RUN npm install --production

# Copy the rest of your application code to the working directory
COPY . .

# Expose the application port
EXPOSE 8080

# Command to run the application
CMD [ "node", "front-end/server.js" ]
