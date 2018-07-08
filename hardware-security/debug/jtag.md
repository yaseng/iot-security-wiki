# JTAG调试
## 前言
JTAG(Joint Test Action Group；联合测试工作组)是一种国际标准测试协议（IEEE 1149.1兼容），主要用于芯片内部测试。现在多数的高级器件都支持 JTAG 协议，如 DSP、FPGA 器件等。标准的 JTAG 接口是4线：TMS、TCK、TDI、TDO，分别为模式选择、时钟、数据输入和数据输出线,另外 ARM 还提供了 SWD 的调试接口，比 JTAG 所需要的线更少，高速模式下更稳稳定，部分厂商如TI，还支持2线制 JTAG 协议进行调试，称为 SBW 接口。
常见支持上述协议进行调试和仿真的设备如：Jlink、Ulink、ST-link 和 MSP430 仿真器等,jtag 既支持在线调试，又能直接获取固件，对于芯片的调试和分析是非常具有帮助的。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/688535e77168b873/5b2d380d4a5f7.jpg)

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/872bc42054768e0f/5b35314ac5b6f.jpg)

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/872bc42054768e0f/5b35314fe28a8.jpg)

## 接口定义
 JTAG有 10pin 的、14pin 的和 20pin 的，尽管引脚数和引脚的排列顺序不同，但是其中有一些引脚是一样的，各个引脚的定义如下。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/872bc42054768e0f/5b3532c0a4b4a.png)

### 引脚定义
Test Clock Input (TCK) -----强制要求1
TCK 在 IEEE1149.1 标准里是强制要求的。TCK 为 TAP 的操作提供了一个独立的、基本的时钟信号，TAP 的所有操作都是通过这个时钟信号来驱动的。

Test Mode Selection Input (TMS) -----强制要求2
TMS 信号在 TCK 的上升沿有效。TMS 在 IEEE1149.1 标准里是强制要求的。TMS信号用来控制 TAP 状态机的转换。通过TMS信号，可以控制 TAP 在不同的状态间相互转换。

Test Data Input (TDI) -----强制要求3
TDI 在 IEEE1149.1 标准里是强制要求的。TDI 是数据输入的接口。所有要输入到特定寄存器的数据都是通过 TDI 接口一位一位串行输入的（由 TCK 驱动）。

Test Data Output (TDO) -----强制要求4
TDO在IEEE1149.1标准里是强制要求的。TDO 是数据输出的接口。所有要从特定的寄存器中输出的数据都是通过 TDO 接口一位一位串行输出的（由 TCK 驱动）。

Test Reset Input (TRST) ----可选项1
这个信号接口在 IEEE 1149.1 标准里是可选的，并不是强制要求的。TRST 可以用来对 TAPController 进行复位（初始化）。因为通过TMS也可以对TAP Controll 进行复位（初始化）。所以有四线 JTAG 与五线 JTAG 之分。

 (VTREF) -----强制要求5
接口信号电平参考电压一般直接连接 Vsupply 。这个可以用来确定 ARM 的 JTAG 接口使用的逻辑电平（比如3.3V还是5.0V）

Return Test Clock ( RTCK) ----可选项2
可选项，由目标端反馈给仿真器的时钟信号,用来同步 TCK 信号的产生,不使用时直接接地。

System Reset ( nSRST)----可选项3
与目标板上的系统复位信号相连,可以直接对目标系统复位。同时可以检测目标系统的复位情况，为了防止误触发应在目标端加上适当的上拉电阻。

USER IN：用户自定义输入。可以接到一个 IO 上，用来接受上位机的控制。

USER OUT：用户自定义输出。可以接到一个 IO 上，用来向上位机的反馈一个状态

由于 JTAG 经常使用排线连接，为了增强抗干扰能力，在每条信号线间加上地线就出现了这种 20 针的接口。但事实上，RTCK、USER IN、USER OUT 一般都不使用，于是还有一种14针的接口。
### SWD 引脚定义
VRef：目标板参考电压信号。用于检查目标板是否供电，直接与目标板 VDD 联，并不向外输出电压；
GND：公共地信号；
SWDIO：串行数据输入输出，作为仿真信号的双向数据信号线，建议上拉；
SWCLK：串行时钟输入，作为仿真信号的时钟信号线，建议下拉；
SWO：串行数据输出引脚，CPU 调试接口可通过 SWO 引脚输出一些调试信息。该引脚是可选的；
RESET：仿真器输出至目标 CPU 的系统复位信号。
虽然RESET是可选的信号，但一般都建议接上，使得仿真器能够在连接器件前对器件进行复位，以获得较理想的初始状态，便于后续调试操作。

### 对应关系
20、14、10pin JTAG 的引脚名称与序号对应关系
![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/872bc42054768e0f/5b352e3d3ff72.png)

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/872bc42054768e0f/5b352e5ea9dc2.png)

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/872bc42054768e0f/5b352e6a43af4.png)

值得注意的是，不同的 IC 公司会自己定义自家产品专属的 Jtag 头，来下载或调试程序。
需要说明的是，上述 Jtag 头的管脚名称是对 IC 而言的。例如 TDI 脚，表示该脚应该与 IC 上的 TDI 脚相连，而不是表示数据从该脚进入 download cable。
实际上10针的只需要接4根线，4号是自连回路，不需要接，1，2接的都是1管脚，而8，10接的是 GND，也可以不接。
## JTAG提取固件
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

## 预留接口调试
如果PCB上保留了厂商在研发过程中预留的 JTAG 接口，可直接通过飞线的方式，连上对应的引脚进行调试。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/872bc42054768e0f/5b3533c4f41a8.jpg)

## 直连芯片 JTAG 引脚调试
大部分厂商在生产环节会去掉外部引出的 JTAG 接口，因为多数量产芯片的封装格式，直接飞线难度较大，因此可以采用探针台直连芯片引脚进行调试。
在研究的某款智能锁，拆解发现采用的是 MSP432G2553 作为主控，下图红框位置。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/6d1723e1cd5f9f23/20180614_161604.jpg)

该款智能锁利用手机 app 产生开锁音频信号，进过外部 AD 转换后传输至芯片中进行解密开锁处理，厂商在生产过程中比较注重安全意识，PC 上的没有保留调试接口，进一步分析的话，需要对芯片进行固件提取和在线调试。
### 芯片分析
查TI官方手册，MSP432G2553 芯片引脚定义如下，其支持四线 JTAG 和两线 SBW 的调试接口，随采用两线制 SBW 接口作为调试方式，其 16 引脚为 SBWTDIO 口，17脚为 SBWTCK 脚。
![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/6d1723e1cd5f9f23/20180614170114.jpg)

### 连接引脚
两线制 SBW 对应 MSP430 仿真器上的14线排针接口，分别为 16 脚 SBWTDIO 口连仿真器第一脚 TDO，17脚 SBWTCK 连第7脚 TCK，最后需要连接 GND 脚，即芯片的第 20 脚连仿真器第9口，两线制 SBW 同时需要外部电源供电，仿真器接口定义如下图。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/6d1723e1cd5f9f23/medish.jpg)

按照引脚说明，开始在探针台上连接引脚，需要注意 JTAG 和 SBW 调试，对连线的长度有严格要求，超过 20 厘米信号会大幅衰减，造成无法调试，因此在探针上利用夹子和铜导线缩小接线距离。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/6d1723e1cd5f9f23/20180612_190034.jpg)

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/6d1723e1cd5f9f23/20180612_190040.jpg)

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/6d1723e1cd5f9f23/20180612_190045.jpg)

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/6d1723e1cd5f9f23/20180612_190130.jpg)

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/6d1723e1cd5f9f23/20180612_190136.jpg)

### 在线调试 
连接上仿真器，启动 msp430-gdbproxy。
msp430-gdb 远程连接
target remote  192.168.1.196:2000

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/6d1723e1cd5f9f23/15300767804938.jpg)


### 固件提取

仿真器环境配置好，然后打开Lite FET-Pro430，选择好芯片型号后，点击 read 即可读取固件，提取的固件分为 txt 和 hex 两种格式，也可以利用接口自己进行在线调试。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/6d1723e1cd5f9f23/20180612190327.png)

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/6d1723e1cd5f9f23/20180615160857.png)

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/6d1723e1cd5f9f23/20180615160905.png)
