我初步实现了通过客户的形式（cat 一个json参数文件到一个sh，再将结果重定向到一个json文件中）。
https://github.com/sheltont/fortiapi


由于我现在的限制：没有写权限，D90上没有虚墙的概念，所以仅仅处于概念展示，实现了一个列出所有策略的命令。文件说明：

因为列出policy不需要输入参数，default_empty.json就是个占位符，空的json数据。
list_firewall_policy.sh 一个shell命令，调用python代码实现功能。我在命令中写死了fortinet IP地址用户登录信息等。
firewall_policies.json这个是输出的结果，包括所有的策略。
Fgt.py, fos_api.py在厂家提供的例子基础上修改。fgt.py就是实现了FGT class，fos_api.py是客户需要交互的。使用命令 python fos_api.py –h可以查看所有支持的命令行参数。

FortiGate REST API command line wrapper


optional arguments:
  -h, --help     show this help message and exit
  -U USERNAME    Fortigate username
  -P PASSWORD    the password of the user
  -H HOST        Fortigate Host IP address
  -X ACTION      Action to be executed
  -O OBJECT      Object to be manipulated
  -p PORT        Fortigate HTTPS listening port
  -d VDOM        Fortigate VDOM
  -a PARAMS      Optional command parameters
  -v, --verbose  Logging option