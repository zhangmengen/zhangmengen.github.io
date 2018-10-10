# elasticsearch开机自启配置说明

## 注意：涉及到添加用户，可以看系统的用户列表

```查看用户信息
vim /etc/passwd
```

我有个elasticsearch用户 我想让它有读写 jdk文件夹的权限 应该切换到root账户下 用什么命令赋予elasticsearch权限 

```
chown -R elasticsearch:elasticsearch /usr/local/java/jdk
```

检查当前用户名称

```
who
```

#### 1.卸载系统自带的OpenJDK以及相关的java文件

①在命令窗口键入 ：	

```
java -version
```

可以看到系统自带openjdk版本信息

②在命令窗口键入： 

```
rpm -qa | grep java
```

命令说明：

rpm 　　管理套件    

-qa 　　使用询问模式，查询所有套件

grep　　查找文件里符合条件的字符串

java 　　查找包含java字符串的文件



以上文件中：

下面这几个可以删除

```
java-1.7.0-openjdk-1.7.0.111-2.6.7.8.el7.x86_64
java-1.8.0-openjdk-1.8.0.102-4.b14.el7.x86_64
java-1.8.0-openjdk-headless-1.8.0.102-4.b14.el7.x86_64
java-1.7.0-openjdk-headless-1.7.0.111-2.6.7.8.el7.x86_64
```

noarch文件可以不用删除 

```
python-javapackages-3.4.1-11.el7.noarch
tzdata-java-2016g-2.el7.noarch
javapackages-tools-3.4.1-11.el7.noarch
```

③在命令窗口键入 ：

```
rpm -e --nodeps java-1.7.0-openjdk-1.7.0.111-2.6.7.8.el7.x86_64
```

但是会出错，因为在普通用户sxd用户下，并没有操作这几个文件的权限。 

解决：

​	在命令窗口键入：

```
su root
```

进入root用户，可以有权限操作这几个文件。 



完整的删除文件的命令，在命令窗口键入： 

```
rpm -e --nodeps java-1.7.0-openjdk-1.7.0.111-2.6.7.8.el7.x86_64
rpm -e --nodeps java-1.8.0-openjdk-1.8.0.102-4.b14.el7.x86_64
rpm -e --nodeps java-1.8.0-openjdk-headless-1.8.0.102-4.b14.el7.x86_64
rpm -e --nodeps java-1.7.0-openjdk-headless-1.7.0.111-2.6.7.8.el7.x86_64
```

命令介绍：

rpm 　　　　管理套件  

-e　　　　　删除指定的套件

--nodeps　　不验证套件档的相互关联性



④检查是否已经删除成功

在命令窗口键入：

```
java -version
```

代表删除成功了。

⑤如果还没有删除，则用yum -y remove去删除他们 



#### 2.下载最新稳定JDK

**【注意】:JDK安装在哪个用户下，就是给哪个用户使用**

①下载地址为

　　当前最新版本下载地址：http://www.oracle.com/technetwork/java/javase/downloads/index.html

　　历史版本下载地址：　　http://www.oracle.com/technetwork/java/javase/archive-139210.html  

③下载完成后，将JDK压缩包  复制一份到/usr/local/src/作备份

键入命令：

```
cp jdk-8u181-linux-x64.tar.gz  /usr/local/src/
```

命令说明：

cp　　　　　　　　　　　　　　  复制文件或目录

jdk-8u181-linux-x64.tar.gz 　　　　文件名

/user/local/src　　　　　　　　　 要复制的目标目录



修改文件或者目录权限的先关操作说明：http://www.cnblogs.com/sxdcgaq8080/p/7498906.html

 

④修改JDK压缩文件的权限，然后再进行复制操作

在命令行键入：

```
chmod 755 jdk-8u181-linux-x64.tar.gz 
```

之后在键入： 

```
ls -al
```

可以看到效果：

文件名已经显示为绿色，行首也可以实际的看到权限 更改为：-rwxr-xr-x

注意：如果上面cp出现权限不够的问题，进行下面这一步。

⑤最终进入root用户下，进行复制操作

键入：

```
cp jdk-8u181-linux-x64.tar.gz  /usr/local/src/
```

#### 3.解压JDK

①将/home/centos/jdk-8u181-linux-x64.tar.gz文件拷贝一份到/usr/local/java

命令行键入:

```
cp jdk-8u181-linux-x64.tar.gz /usr/local/java
```

在命令窗口键入： 

```
tar jdk-8u181-linux-x64.tar.gz
```

命令介绍：

tar　　　　　　备份文件

-zxvf　　　　　

-z　　　　　　 　　　　　　　　  通过gzip指令处理备份文件

-x　　　　　　　　　　　　　　   从备份文件中还原文件

-v　　　　　　　　　　　　　　   显示指令执行过程

-f　　　　　　 　　　　　　　　   指定备份文件

jdk-8u181-linux-x64.tar.gz　　　　文件名

③删除JDK压缩包

在命令行键入：

```
rm -f jdk-8u181-linux-x64.tar.gz
```

命令解释：

rm　　　　删除文件或目录

-f　　　　  强制删除文件或目录

#### 4.配置JDK环境变量

①编辑全局变量

在命令行键入：

```
vim /etc/profile
```

命令说明：

vim　　　　　　文本编辑

/etc/profile　　　全局变量文件进入文本编辑状态下，光标走到文件最后一行，键盘按下： 

```
i
```

进入插入状态：

在文本的最后一行粘贴如下：

注意JAVA_HOME=/usr/java/jdk-8u181-linux-x64  就是你自己的目录

```
# 配置环境变量
#java environment
#JAVA_HOME=/usr/java/jdk1.8.0_181
#JRE_HOME=$JAVA_HOME/jre
 
#PATH=$PATH:$JAVA_HOME/bin:/sbin:/usr/bin:/usr/sbin
#CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar
#export JAVA_HOME
#export JRE_HOME
#export PATH
#export CLASSPATH
```

【注】：CentOS6上面的是JAVAHOME，CentOS7是{JAVA_HOME} 

键盘： 

```退出编辑模式
ESC

shift+q
```

键盘： 

```
qw！
```

写入并强制退出。

如果不管用可以键盘：

```
x
```

一个意思，都是保存并退出的意思。 

-----------------------------------------------------------------------------------------------------------------------------------

##### 注意：这一步可以设置也可以不用设置

我没有用这一步

#### 5.让刚刚设置的环境变量生效并检查是否安装成功

①让刚刚设置的环境变量生效

 键入：

```
source /etc/profile
```

②检查是否配置成功

键入：

```
java -version
```

返回：

java version "1.8.0_181"
Java(TM) SE Runtime Environment (build 1.8.0_181-b13)
Java HotSpot(TM) 64-Bit Server VM (build 25.181-b13, mixed mode)

安装成功！

如果没有返回上面的结果：说明java未配置到/usr/bin目录下

解决方法：添加软连接

```
ln -s /usr/local/java/jdk1.8.0_181/bin/java /usr/bin/java
```

再次执行java -version ,就没有问题了

## 接下来正式开始配置elasticsearch开机自启的功能

### 一、将解压的jdk包迁移到/usr/local/java/目录下

```
mv jdk1.8.0_181/ /usr/local/java/
```

如果没有Java目录，可以建一个

```
mkdir /usr/local/java
```

### 二、编辑elasticsearch开机自启脚本文件

1.最近搭建了一个elasticsearch服务，其中机器重启而ES服务没有重启是问题，就有下面的脚本

首先，将/etc/init.d目录下的elasticsearch文件备份

```备份elasticsearch开机自启文件
 cd /etc/init.d/
 
mv elasticsearch elasticsearch.backup
```

编辑es开机自启脚本文件

```
vim /etc/init.d/elasticsearch
```

```
#!/bin/sh
#chkconfig: 2345 80 05
#description: es
 
export JAVA_HOME=/usr/local/java/jdk1.8.0_181
export JAVA_BIN=/usr/bin
export PATH=$PATH:$JAVA_HOME/bin
export CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar
export JAVA_HOME JAVA_BIN PATH CLASSPATH

case $1 in
start)
#下面的“<<!”是切换用户后，待执行的命令，执行完后使用“!”来进行结束
    su elasticsearch<<!
    cd /usr/share/elasticsearch
    ./bin/elasticsearch -d
exit
!
#上面的“!”是以上面的对应起来，并且顶格放置，这是语法
    echo "es startup" #将该行替换成你自己的服务启动命令
    ;;
stop)
    es_pid=`ps aux|grep elasticsearch | grep -v 'grep elasticsearch' | awk '{print $2}'`#注意这个号“`”
    kill -9 $es_pid
    echo "es stopup" #将该行替换成你自己的服务启动命令
    ;;
restart)
    es_pid=`ps aux|grep elasticsearch | grep -v 'grep elasticsearch' | awk '{print $2}'` #“grep -v”过滤掉本身的执行命令，获取准确的pid
    kill -9 $es_pid
    echo "es stopup" #将该行替换成你自己的服务启动命令
    su elasticsearch<<!
    cd /usr/share/elasticsearch
    ./bin/elasticsearch -d
!
    echo "es startup" #将该行替换成你自己的服务启动命令
    ;;
*)
    echo "start|stop|restart" #将该行替换成你自己的服务启动命令
    ;;
esac
```

保存退出

保存为elasticsearch，放在/etc/init.d下面,并执行下面命令赋予执行权限

```给文件添加可读可写可执行权限
chmod 777 elasticsearch
```

最后在/etc/init.d下执行

```
chkconfig --add elasticsearch
```

将elasticsearch添加到服务器。

chkconfig简单详解连接：https://blog.csdn.net/lanyang123456/article/details/54695567

2.将/usr/share下的elasticsearch文件更改用户权限，

```
chown -R elasticsearch:elasticsearch /usr/share/elasticsearch
```

原因：elasticsearch一般不能以root用户身份运行，需要切换到普通用户

切换用户：

```
su elasticsearch
```

注意：如果切换不成功

```
vim /etc/passwd
```

```
将：
elasticsearch:x:995:991:elasticsearch user:/home/elasticsearch:/sbin/nologin
改为：
elasticsearch:x:995:991:elasticsearch user:/home/elasticsearch/bin/bash
```

这样在切换用户就能成功了。

在elasticsearch用户下后台运行elasticsearch看是否成功

```
cd /usr/share/elasticsearch
./bin/elasticsearch -d
```

##### 注意：现在因为添加了自启动配置文件，所以原来在root用户下的启动命令发生改变

```elasticsearch启动，停止，重启命令
service elasticsearch start/stop/restart   
```

该命令操作的是/etc/init.d目录下的elasticsearch文件，其控制的是安装目录下的elasticsearch启动，现在init.d目录下的elasticsearch文件被我们用自己的elasticsearch文件所代替，在使用

```
service elasticsearch start/stop/restart
```

该命令时，它会首先找到/etc/elasticsearch文件，会报错

而只能用下面的命令启动不会报错：

```
systemctl /start/stop/status elasticsearch
```

该命令操作的是配置文件下的elasticsearch文件，即：/etc/elasticsearch/elasticsearch.yml

如果elasticsearch没有启动起来，报以下错误：

```
ERROR: [1] bootstrap checks failed
[1]: max file descriptors [65535] for elasticsearch process is too low, increase to at least [65536]
```

解决方法：

```
vim /etc/security/limits.conf 修改或新增
```

```
* soft nofile 65536
* hard nofile 131072
* soft nproc 2048
* hard nproc 4096

备注：* 代表Linux所有用户名称（比如 hadoop）

后面设置的nproc实际上设置多线程，以防止再报用户最大可创建线程数太小的故障。

保存、退出、重新登录才可生效

重新使用SSH登录，再次启动elasticsearch即可。

```

如果输入以下命令：

```
systemctl status elasticsearch
```

显示elasticsearch状态为dead，elasticsearch.service为disabled禁用状态，说明elasticsearch被禁止开机自启。执行以下命令：

```
systemctl enable elasticsearch.service
```

相关服务器开机自启知识参考链接：https://blog.csdn.net/qq_34829953/article/details/73752719

##### 另外

还要更改/etc/sysconfig/elasticsearch文件

```
vim /etc/sysconfig/elasticsearch
```

```
将：
#JAVA_HOME=
改为：
JAVA_HOME=/usr/local/java/jdk1.8.0_181
```

