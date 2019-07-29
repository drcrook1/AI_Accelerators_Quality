docker stop ai_acc
docker rm ai_acc
cd WebApp
docker build -t ai_acc .
cd ..
docker run --name ai_acc -p 80:80 ai_acc