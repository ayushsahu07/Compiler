FROM node:18

# Install required compilers and tools
RUN apt-get update && apt-get install -y \
    python3 \
    default-jdk \
    gcc \
    g++ \
    build-essential

# Set the working directory
WORKDIR /app

# Copy package.json and install dependencies
COPY package.json .
RUN npm install

# Copy the rest of the application
COPY . .

# Expose the port
EXPOSE 3000

# Start the application
CMD ["npm", "start"]