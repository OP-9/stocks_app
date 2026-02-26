FROM node:20-slim
WORKDIR /app

# Install the tool to serve static files
RUN npm install -g serve

COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

EXPOSE 3000

# Points to 'dist' (for Vite) or 'build' (for CRA)
CMD ["serve", "-s", "dist", "-l", "3000"]