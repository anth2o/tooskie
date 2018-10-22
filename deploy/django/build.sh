# install git
# create ssh key
# pull git project

sudo yum update -y
sudo yum install git

git clone git@gitlab.com:antoineh/tooskie.git
cd tooskie
git pull origin dev
git checkout dev


sudo yum install python36.x86_64
sudo easy_install-3.6 pip
pip3 install --user -r requirements.txt 

sudo yum install make automake gcc gcc-c++ kernel-devel -y 
sudo yum install nginx -y