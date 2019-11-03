set -a
source var/local/.euco.env

cd services/ui
npm install
npm run build

cd ../..
docker-compose up --build -d
