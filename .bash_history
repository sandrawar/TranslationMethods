docker --version
cd /mnt/c/src/github/sandrawar/TranslationMethods/moses-smtnlp
docker --version
docker build -t moses-smt .
sudo usermod -aG docker $USER
docker run hello-world
