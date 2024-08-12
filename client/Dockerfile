FROM node:20-alpine

WORKDIR /code

COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application files
COPY . .

EXPOSE 3000

CMD [ "npm", "run", "dev"]