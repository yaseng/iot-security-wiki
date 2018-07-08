# 串口调试
## 前言

上节介绍了关于通过编程器直接读取芯片获取固件用来静态分析的一点思路，本篇将介绍通过 UART 串口来直接与机器交互，通过串口输出输入信息，做动态调试。
通用异步收发传输器（Universal Asynchronous Receiver/Transmitter)，通常称作 UART ，是一种异步收发传输器，是电脑硬件的一部分。它将要传输的资料在串行通信与并行通信之间加以转换。作为把并行输入信号转成串行输出信号的芯片， UART 通常被集成于其他通讯接口的连结上。
对于物联网硬件的串口调试，多数情况下指的就是通过 UART 串口进行数据通讯， 但是我们经常搞不清楚它和COM口的区别,  以及 RS232, TTL 等关系,             实际上 UART 、COM 指的物理接口形式(硬件), 而 TTL、RS-232 是指的电平标准(电信号).
 UART 有4个pin（VCC, GND , RX, TX）, 用的TTL电平， 低电平为0(0V)、高电平为1（3.3V或以上）， UART 串口的 RXD、TXD 等一般直接与处理器芯片的引脚相连，而RS232串口的 RXD、TXD 等一般需要经过电平转换(通常由 Max232 等芯片进行电平转换)才能接到处理器芯片的引脚上，否则这么高的电压很可能会把芯片烧坏。
 在调试的时候, 多数情况下我们只引出 rx、tx、 GND 即可，但是 UART 的数据要传到电脑上分析就要匹配电脑的接口，通常我们电脑使用接口有COM口和USB口（最终在电脑上是一个虚拟的COM口），但是要想连上这两种接口都要需要进行硬件接口转换和电平转换。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image32.jpg)

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image33.jpg)

##  UART 串口调试
 UART 调试第一步需要先找到对应的四个PIN，在通电情况下，VCC 口可以不要接，判断 GND , RX, TX 三个引脚是调试的关键，找四个引脚可以先看 PCB上的印字。
![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image65.jpg)

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image66.jpg)

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image67.jpg)

但多数厂商在量产前会去掉用于调试的串口印字，如果找不到对应引脚的印字，就需要先分析 PCB 的结构，一般 PCB 上有3、4 、5个并排或相距不远的焊点或通孔，就有可能是 UART 调试串口。
![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image68.jpg)

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image69.jpg)

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image70.jpg)

但 PCB 上可能存在多个这样的焊点或通孔，从多个口中找出真正的调试串口，就需要借助到万用表。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image101.jpg)

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image102.jpg)

万用表找串口首先需要找到 GND 口，就是接地口，在疑似串口的焊点处，通过测量电势差，可以判断出 GND 口，通过连接焊点和输入负极，如果电势为0，就可能是 GND 口，如果电势为最大值，例如 3.6V、5V 等，就可能是 VCC 口。然后通过 UART 转换器对应的4个口，引出导线，并设置好串口输出环境后，就可以依次尝试。也可以通过短接其中的两口，如果机器重启，就可以判断这两口为VCC和 GND 。
需要注意的是，在 TTL 电平模式下，UART 转换接口上的 RX、TX 口与上位设备，也就是 PCB 上的 UART 口的RX和TX是需要反接的。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image71.jpg)

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image72.jpg)

### 案例一：调试某智能摄像头
通过万用表测量电势差之后，在靠近 CPU 的地方有三个通孔，有可能是 UART 串口，用导线连接之后，设置波特率为 115200。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image73.jpg)

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image35.jpg)

用 SecureCRT 连接串口，给机器通上电之后，串口立马输出了启动信息，并可以执行命令，说明串口正确，如果遇到无法输入的情况，首先检查接线是否松动，然后在 SecureCRT 中的， Session Options -> Connection -> Serial -> Flow Control，将原先选中的 RTS/CTS 取消掉，这是因为如果选中了 RTS/CTS ，则硬件上要有对应接口，软件上实现对应协议，才能实现此流控制。如果串口输出为乱码，则需要切换波特率，直至输出正常。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image74.jpg)

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image75.jpg)

### 案例二：调试某路由器
在靠近cpu的地方有四个通孔，测量电势差后，利用导线探针，确定了三个 PIN，连接转换器。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image76.jpg)

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image77.jpg)

串口中输出调试信息，因波特率设置问题，初始输出为乱码，改为 38400 即可正常输出。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image78.jpg)
### 案例三：调试某路由器
在 PCB 上有四个焊点，先测量电势差，分出 GND 和VCC，在利用焊枪分别焊上导线，连接转换接口，测试出 TX 和 RX 口。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image79.jpg)

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image80.jpg)

设置波特率为57600，串口输出正确，并可执行命令。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image81.jpg)
### 案例四：调试某路由器
在 PCB 一侧有5个通孔，并标注有 UART -0字样，通电后，测试各口电势差，确实 GND 和 VCC 后，连接转换接口，并测试出 RX 和 TX 口。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image82.jpg)

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image83.jpg)

设置波特率为 57600，串口输出正确，并可执行命令。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image84.jpg)

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image85.jpg)

通过本地架设的 tftp 服务器，并在串口输入命令，开启相关服务，就可以通过 tftp 与机器传输文件。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image86.jpg)

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image87.jpg)
### 案例五：调试某无线数据终端
拆开正面压板，发现 PCB 上标注有印字，利用 PCB 夹具和探针，引出 RX 和 TX 口，连接转换器，因该无线终端串口电压不超过 1.7V，焊接容易造成信号衰减，因此采用夹具。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image88.jpg)

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image89.jpg)
因串口输出信息过多，影响输入和输出结果，因此采用串口调试助手，设置波特率为 115200，输入命令并发送，可以成功执行。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image90.jpg)

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image91.jpg)

### 案例六：调试某无线数据终端

拆解机器，该型机器采用多块电路板层级设计，其主要处理芯片位于顶部，拆解时注意走线位置，防止拉坏接线口，在 PCB 上有 UART 的 PIN 口印字，给每一个 PIN 口焊上导线，连接转换器。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image122.jpg)

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image123.jpg)

设置波特率为 921600，连接串口，用 root 账号登陆，密码为空，成功进入系统，执行命令。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image124.jpg)

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image125.jpg)