# install vnc viewer (for server) 
sudo apt-get update
sudo apt-get install vnc4server
vncserver
sudo apt-get install x-window-system-core
sudo apt-get install gdm
sudo apt-get install ubuntu-desktop
sudo apt-get install gnome-panel gnome-settings-daemon metacity nautilus gnome-terminal
sudo vim ~/.vnc/xstartup
vncserver -kill :1
vncserver :1
> source
> http://dblab.xmu.edu.cn/blog/1998-2/
# install java8 from oracle * 3
```
sudo add-apt-repository ppa:webupd8team/java
sudo apt-get update
sudo apt-get install oracle-java8-installer
// setup JAVA_HOME and jRE_HOME
cat >> /etc/environment <<EOL
JAVA_HOME=/usr/lib/jvm/java-8-oracle
JRE_HOME=/usr/lib/jvm/java-8-oracle/jre
EOL
```
> 
https://tecadmin.net/install-oracle-java-8-ubuntu-via-ppa/
> https://www.digitalocean.com/community/tutorials/how-to-install-java-with-apt-get-on-ubuntu-16-04
# install google chrome
```
cd Desktop
sudo mkdir Download
cd Download
sudo wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

sudo apt-get install fonts-liberation libxss1 xdg-utils //install dependencies
sudo dpkg -i google-chrome-stable_current_amd64.deb
```
# install spark-2.4.0-bin-hadoop2.7
From: http://spark.apache.org/downloads.html
```
tar -xf spark-2.4.0-bin-hadoop2.7.tgz
sudo mv spark-2.4.0-bin-hadoop2.7.tgz
```
the spark is now in `~/spark`
# configuration
https://medium.com/ymedialabs-innovation/apache-spark-on-a-multi-node-cluster-b75967c8cb2b
change hostnames of nodes in cluster to master, slave01, slave02
ssh from master to slave can be done with non-root user
## On cluster edit spark-env.sh
```
$ cd /usr/local/spark/conf
$ cp spark-env.sh.template spark-env.sh


$ sudo vim spark-env.sh
//append the following:
export SPARK_MASTER_HOST='<MASTER-IP>'
export JAVA_HOME=<Path_of_JAVA_installation>
```
## On cluster edit file slaves
Add Workers
Edit the configuration file slaves in (/usr/local/spark/conf).
```
$ sudo vim slaves
// And add the following entries.

master
slave01
slave02
```
## Start Spark Cluster
To start the spark cluster, run the following command on master.
```
$ cd /usr/local/spark
$ ./sbin/start-all.sh
```
To stop the spark cluster, run the following command on master.
```
$ cd /usr/local/spark
$ ./sbin/stop-all.sh
```
Check whether services have been started
To check daemons on master and slaves, use the following command.
```
$ jps
```
## Spark Web UI
Browse the Spark UI to know about worker nodes, running application, cluster resources.
```
Spark Master UI
http://<MASTER-IP>:8080/
Spark Application UI
http://<MASTER_IP>:4040/
```
## Use Jupyter in ubuntu
In terminal:
```
jupyter notebook
```