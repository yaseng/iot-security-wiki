##前言
这节开始介绍一些基础知识和工具。

## 芯片
### ROM 芯片
常见的 IOT 产品，一般采用嵌入式 linux 系统开发，对芯片分析主要目的之一就是获取到硬件系统的固件，从固件中分析可能存在的安全风险。
固件一般存储在 ROM 中，ROM 是只读存储器（Read-Only Memory）的简称，是一种只能读出事先所存数据的固态半导体存储器。其特性是一旦储存资料就无法再将之改变或删除。通常用在不需经常变更资料的电子或电脑系统中，并且资料不会因为电源关闭而消失。
常见的存储芯片按照存储读取方式和制作工艺不同，可以分为： ROM、PROM、EPROM、EEPROM、FLASH-ROM。
在大部分IOT产品中多采用 flash 芯片作为存储器，提取固件主要也是通过读取 flash 芯片。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image17.jpg)

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image18.jpg)

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image19.jpg)
### Flash芯片
FLASH ROM 属于真正的单电压芯片，在使用上很类似 EEPROM，因此，有些书籍上便把 FLASH ROM 作为 EEPROM 的一种。事实上，二者还是有差别的。FLASH ROM在擦除时，也要执行专用的刷新程序，但是在删除资料时，并非以 Byte 为基本单位，而是以 Sector（又称 Block）为最小单位，Sector 的大小随厂商的不同而有所不同；只有在写入时，才以 Byte 为最小单位写入；FLASH ROM 芯片的读和写操作都是在单电压下进行，不需跳线，只利用专用程序即可方便地修改其内容；FLASH ROM的存储容量普遍大于EEPROM，约为 512K 到至 8M KBit，由于大批量生产，价格也比较合适，很适合用来存放程序码，近年来已逐渐取代了 EEPROM，广泛用于主板的 BIOS ROM，也是 CIH 攻击的主要目标。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image20.jpg)

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image21.jpg)

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image22.jpg)

根据技术方式不同可分为： IIC EEPROM、SPI NorFlash 、CFI Flash、Parallel NandFlash、SPI NandFlash、eMMC Flash、USF2.0 等。
其中 SPI NorFlash 因为接口简单，使用的引脚少，易于连接，操作方便，并且可以在芯片上直接运行代码，其稳定性出色，传输速率高，在小容量时具有很高的性价比，这使其很适合应于嵌入式系统中作为 FLASH ROM，所以在市场的占用率非常高。
我们通常见到的 S25FL128、MX25L1605、W25Q64 等型号都是 SPI NorFlash，其常见的封装多为 SOP8，SOP16，WSON8，US0N8，QFN8、BGA24 等。
	  
![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image23.jpg)

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image24.jpg)
### 芯片印字
 一般 PCB 上有多块逻辑处理 IC，在多个 IC 芯片中，可以通过分析电路原理和查找芯片印字来确定具体的存储芯片。
 芯片上的丝印大多数情况会注明厂商和芯片型号，通过印字可以初步确定芯片类型，同时丝印层的文字也可以帮助我们来确定存储的格式和大小，常见的 W25 芯片的印字含义如下：
	   
![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image25.jpg)
## 编程器
读取Flash芯片，需要借助编程器，编程器又称烧录器、写入器、写码器，是专门用来对 IC 芯片进行读写、编程/烧录的仪器。并口多功能 BIOS 编程器，它可以对 EPROM（27系列芯片）、EEPROM（28系列芯片）、FLASH ROM（29、39、49系列芯片）及单片机、串行芯片等进行读写、编程，是一种性价比较高的编程器。
编程器种类多样，从功能简单的专用型到功能全面的全功能通用型都有，价格从几十元到上万元不等。
	   
![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image26.jpg)

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image27.jpg)

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image28.jpg)
## 通信协议
串口通信指串口按位（bit）发送和接收字节。尽管比按字节（byte）的并行通信慢，但是串口可以在使用一根线发送数据的同时用另一根线接收数据。在串口通信中，常用的协议包括 RS-232、 RS-422 和RS-485。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image29.jpg)

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image30.jpg)

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image31.jpg)
### RS-232
通信方式允许简单连接三线：Tx、Rx和地线。但是对于数据传输，双方必须对数据定时采用使用相同的波特率。
###  RS-422 
 RS-422 标准全称是“平衡电压数字接口电路的电气特性”，在 RS232 后推出，使用 TTL 差动电平表示逻辑，就是两根的电压差表示逻辑，RS422 定义为全双工的，所以最少要4根通信线（一般额外地多一根地线）。
 ### RS-485
 RS485是一个定义平衡数字多点系统中的驱动器和接收器的电气特性的标准，RS-485与 RS-422 的区别在于RS-485为半双工通信方式， RS-422 为全双工方式。 RS-422 用两对平衡差分信号线分别用于发送和接收，所以采用 RS-422 接口通信时最少需要4根线。RS-485 只用一对平衡差分信号线，不能同时发送和接收，最少只需两根连线。
 ### SPI
 spi是串行外设接口（Serial Peripheral Interface）的缩写。SPI是一种高速的，全双工，同步的通信总线，并且在芯片的管脚上只占用四根线，节约了芯片的管脚，同时为 PCB 的布局上节省空间，提供方便，正是出于这种简单易用的特性，如今越来越多的芯片集成了这种通信协议，比如 AT91RM9200。
 ### I2C
 I2C 即Inter-Integrated Circuit(集成电路总线），这种总线类型是由飞利浦半导体公司在八十年代初设计出来的一种简单、双向、二线制、同步串行总线，主要是用来连接整体电路(ICS) ，IIC  是一种多向控制总线，也就是说多个芯片可以连接到同一总线结构下，同时每个芯片都可以作为实时数据传输的控制源。这种方式简化了信号传输总线接口。
## 信号分析
### 示波器分析
示波器是一种用途十分广泛的电子测量仪器。它能把肉眼看不见的电信号变换成看得见的图像，便于人们研究各种电现象的变化过程。示波器利用狭窄的、由高速电子组成的电子束，打在涂有荧光物质的屏面上，就可产生细小的光点（这是传统的模拟示波器的工作原理）。在被测信号的作用下，电子束就好像一支笔的笔尖，可以在屏面上描绘出被测信号的瞬时值的变化曲线。利用示波器能观察各种不同信号幅度随时间变化的波形曲线，还可以用它测试各种不同的电量，如电压、电流、频率、相位差、调幅度等等。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/IMG_3237.jpg)

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/IMG_3239.jpg)

通过分析电路结构，找到待测的引脚和信号源，分析其信号变化和具体的信号形式,得到模拟信号和经过外部AD转换信号的波形图。

### 逻辑分析仪
逻辑分析仪是分析数字系统逻辑关系的仪器。逻辑分析仪是属于数据域测试[2]仪器中的一种总线分析仪，即以总线（多线）概念为基础，同时对多条数据线上的数据流进行观察和测试的仪器，这种仪器对复杂的数字系统的测试和分析十分有效。逻辑分析仪是利用时钟从测试设备上采集和显示数字信号的仪器，最主要作用在于时序判定。由于逻辑分析仪不像示波器那样有许多电压等级，通常只显示两个电压（逻辑 1 和 0 ），因此设定了参考电压后，逻辑分析仪将被测信号通过比较器进行判定，高于参考电压者为 High ,低于参考电压者为 Low，在 High 与 Low 之间形成数字波形。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/5b34d5b3314fe.jpg)

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/5b34d8d59bfb5.png)

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/5b34d5c7b5319.jpg)

通过连接待测设备的接口，分析其中通信数据，通过协议转码，可以得到具体的16进制数据。
## 设备拆解
对于一台未接触过的机器，拆解首先需要观察其外部结构，是否存在暴露的螺丝孔，如果没有，一般可能隐藏在贴纸或橡胶垫下面，可以用手感受是否存在空洞，部分机器采用卡榫结构，只要找对方向，用一字螺丝刀或撬片，从缝隙中就可以撬开，拆解设备唯一的要诀就是胆大心细。部分常用工具如下：

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image104.jpg)

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/5b2d3ac1a60b9.jpg)

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/5b2d3ac7644b8.jpg)

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/5b2d3ad527734.jpg)

维修组合套装，用来拆装各类螺丝，PCB 夹用来拔出排线，热风枪和焊台用来拆焊各类元器件和芯片，BGA 焊台用于拆焊 BGA 封装的芯片。
## 常见物联网智能设备

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image105.jpg)

共享充电宝，采用 gprs 模块配合物联卡与云端通信。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image106.jpg)

蓝牙挂锁，通过蓝牙芯片与手机配对通信，
蓝牙控制电机驱动，使卡锁运转。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image107.jpg)

共享充电宝，采用 GSM 模块加蓝牙模块控制通信。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image108.jpg)

智能锁，WIFI 芯片加蓝牙芯片配合控制，外接指纹识别传感器。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image109.jpg)

智能摄像头，采用 WIFI 芯片通信，外接音频、视频处理模块。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image110.jpg)

网络摄像机，采用网卡芯片，配合多口输出输入视频信号模块。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image111.jpg)

智能路由器，高容量内存搭配智能 OS。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image112.jpg)

智能家居控制终端，高性能 WIFI 收发中继控制。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image113.jpg)

智能保险柜，采用 WIFI 芯片控制加指纹识别传感器。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/image114.jpg)

无线终端，采用 4G 模块和 WIFI 芯片，做便携式 WIFI 终端。