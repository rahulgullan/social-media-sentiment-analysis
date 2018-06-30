# Configuration
## Open Terminal and type following commands to create a Virtual Environment 
cd ~  
sudo apt-get install python-virtualenv  
sudo apt-get install python-pip  
mkdir flask-application  
cd flask-application  
virtualenv flask-env  
source flask-env/bin/activate  
pip install Flask  
pip install sklearn  
pip install pandas  
pip install numpy  

Copy all files and folders inside flask-application/flask-env/bin folder  

## How to run program
open terminal  
cd flask-application  
source flask-env/bin/activate  
cd flask-env/bin  
python sentiment.py  
open url in the browser
