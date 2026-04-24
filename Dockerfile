FROM node:20-bullseye

WORKDIR /app

RUN npm install -g hexo-cli

COPY package*.json ./
RUN npm install

RUN echo "this file is from image build" > /app/from-image.txt

CMD ["bash"]
