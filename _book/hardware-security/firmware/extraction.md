## 前言
上节初步介绍一些硬件基础知识和分析硬件所需要的基本工具，本篇将讲述利用编程器直接读取芯片固件的方法。
为了读取 Flash 芯片的内容，有以下两种常用方式：

1、直接将导线连接到芯片的引脚，在通过飞线连接编程器，进行在线读取固件；

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image34.jpg)


2、把芯片拆焊下来，通过烧录座编程器，离线读取固件。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/dce974d6b8fae7f6/20180606_154759.jpg)

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/5b2d35d6e7f9a.png)

## 飞线法读取
通过夹具夹住芯片引脚，然后连接编程器读取芯片内容，通过编程器连接芯片需要注意引脚的顺序，在 IC 芯片上都会有一个小点，大多数情况下，小点对应的引脚即为芯片的第一脚，而连接编程器的导线也需要插入编程器上相应的引脚。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image36.jpg)
### 案例一：读取中控 F7 门禁固件
拆掉门禁外壳，通过电路图和芯片印字分析，在主板上有一颗 FM25F04A 存储芯片，通过夹具连接芯片到编程器，在通过专用编程器软件，对该芯片进行读取。 

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image37.jpg)

连接完成，确定引脚接线正确后，打开编程器对应软件，通过智能识别芯片ID，即可开始读取固件工作。
如无法识别，可根据印字说明，尝试类似的型号，一般情况下兼容。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image38.jpg)

点击读取，即可开始固件提取，成功之后会保存为 BIN 格式文件，打开即可看到 16 进制的内容，为下一步分析提供基础。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image39.jpg)

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image40.jpg)
### 案例二：读取某智能摄像头固件
拆掉摄像头外壳，通过分析 PCB 上的各个 IC，找到 Flash 存储芯片。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image41.jpg)

在显微镜下，可以看到是一颗 25L64 型号的 Flash 芯片。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image118.jpg)

用夹具连接各引脚，并和编程器连接，进行固件读取。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image42.jpg)

识别到芯片型号为 GD25Q64，点击读取，读取完毕后按照提示保存到文件。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image43.jpg)

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image44.jpg)

打开保存的 BIN 文件或者查看缓冲区，即可看到固件内容。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image45.jpg)

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image46.jpg)

在Ubuntu中，用binwalk解包固件，做进一步分析。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image116.jpg)

### 案例三：读取某智能摄像头固件
打开外壳，在PCB背面发现一颗 Flash 存储芯片

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image47.jpg)

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image48.jpg)

通过显微镜发现芯片型号为 25L128。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image120.jpg)

连接编程器读取固件并保存。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image49.jpg)

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image50.jpg)
### 案例四：读取某路由器固件
打开外壳，发现 PCB 上有一颗 Flash 存储器，但厂商出于安全考虑，把芯片印字涂抹掉了。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image52.jpg)

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image119.jpg)

在不知道芯片型号的情况下，我们连接该芯片，让编程器去尝试读取。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image51.jpg)

通过智能识别，发现编程器无法识别出具体型号，而因为 Flash 存储芯片的种类多样，通过查找又无法获得该路由器的具体参数，这时我们通过 UART 串口，读取出 UBOOT 启动信息，串口输出里面发现了该芯片型号为  W25Q128BV。（下一篇将会重点介绍关于串口调试的方法）

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image54.jpg)

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image53.jpg)

在编程器中选择该型号，成功提取出固件。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image55.jpg)

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image56.jpg)

用 binwalk 解包固件。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image115.jpg)

### 案例五：读取某智能电饭锅固件
拆掉外壳，背面嵌有一块 PCB，反面是 WIFI 处理芯片，正面为存储器，连接编程器。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image57.jpg)

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image58.jpg)

通过印字分析为25芯片，存储大小为 2M 字节，尝试该型号芯片，成功读取固件。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image59.jpg)

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image60.jpg)

### 案例六：读取某网络监控摄像机固件
在 PCB 上找到一块 25L128 型号的 Flash 存储芯片。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image62.jpg)

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image121.jpg)

通过夹具连接编程器。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image61.jpg)

识别到芯片为 MX25L128，选择其中一种，成功提取固件。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image63.jpg)

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image64.jpg)

用binwalk解包固件内容。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image117.jpg)
## 拆焊芯片读取固件
一般情况下，对于 TSOP8 封装的闪存芯片，可以用上述方法来读取，但可能存在在线读取成功率不高或数据丢失的情况，对于更多引脚和封装格式的芯片，飞线的难度更高，有一定锡焊基础的建议采用拆焊芯片，用烧录座离线读取的方法。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/20180628165648.jpg)

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/20180628165631.jpg)

热风枪设置在适合的温度，吹下芯片，周围的元件可以用铝箔或锡箔纸适当保护。

拆下的闪存芯片放在烧录座上，在连接编程器进行读写，芯片放置的引脚方向要注意对齐编程器和烧录座的第一脚。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/20180628165637.jpg)

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/20180628165659.png)

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/20180628165651.png)

读取完成，用点焊法把芯片焊上焊盘即可。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/20180628165634.jpg)

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/20180628171222.jpg)

更多芯片焊接修改操作请参考 2.4.2 硬件修改一节

## jtag提取固件
### 拆焊芯片
首先用热风枪拆下智能锁主控芯片，该单片机型号为：Stm32F103R6。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/872bc42054768e0f/5b3522b3bcebf.jpg)

### 烧录座连接Jlink
芯片第一脚对齐烧录座第一脚，然后把 Jlink 插入烧录座引出的 JTAG 接口。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/872bc42054768e0f/5b352394427b3.jpg)

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/872bc42054768e0f/5b3523a551154.jpg)

### 读取固件
电脑上安装好 Jlink 驱动，打开 J-Flash 客户端，设置好参数，主要在配置栏选择正确的芯片型号，然后点击连接，在点击 Target->Read Back->Entire trip 即可读写固件。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/872bc42054768e0f/5b3524c6c08bb.jpg)

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/872bc42054768e0f/5b3524ced11a4.jpg)

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/872bc42054768e0f/5b3524d65ced7.jpg)

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/872bc42054768e0f/5b3524db79b3c.jpg)

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/872bc42054768e0f/5b3524f327ac3.jpg)