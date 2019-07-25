# docker run -p 5678:5678 --rm -it $(docker build -q .)
docker build -t=tor-py .
docker run -p 5678:5678 tor-py