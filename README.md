# Spring-Cloud-Function-SpEL-poc-and-exp

影响版本:

3.0.0.RELEASE <= Spring Cloud Function <= 3.2.2


Spring-cloud-function RCE  POC and  EXP:

运行漏洞环境:
java -jar demo-0.0.1-SNAPSHOT.jar

用法:
运行python spring-rec.python

输入url，进行检测，检测到漏洞后，输入监听的ip和端口直接用nc进行反弹shell，即可。
反弹shell需要nc

![image](https://github.com/XUANCUN/Spring-Cloud-Function-SpEL-poc-and-exp/raw/main/2022-03-31_091503.png)
