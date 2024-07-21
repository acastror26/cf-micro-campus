# Stage 1: Build the React app
FROM node:14 AS build

# Set the working directory
WORKDIR /usr/src/app

# Copy the package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application
COPY . .

# Build the React app
RUN npm run build

# Stage 2: Serve the React app using nginx
FROM nginx:alpine

# Copy the built React app from the previous stage
COPY --from=build /usr/src/app/build /usr/share/nginx/html

# Expose the port nginx will run on
EXPOSE 80

# Run nginx
CMD ["nginx", "-g", "daemon off;"]