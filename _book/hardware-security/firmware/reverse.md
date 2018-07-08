# 固件逆向

## 前言

对固件的一些逆向思路，通过几个具体的案例。

## 单片机
相对于嵌入式设备的逆向，单片机的逆向纯属于体力活，需要根据芯片定义的每个 IO 口，配合电路和外部模块进行分析、调试。逐步确定每一个分支的功能，逻辑等，是非常繁琐和复杂的工作。
这里使用 MSP430 系列芯片作为逆向分析的案例，其他的单片机也类似。

### 基础知识

#### MSP430 开发基础

Know it then hack it ，在对一个单片机芯片做逆向分析以及漏洞挖掘时，需要熟悉单片机开发和底层的工作原理，以 MSP430G2553 为例，简单介绍下有关单片机开发的基础知识。

##### 芯片特性
德州仪器  (TI) MSP430G2x13 和 MSP430G2x53 系列是超低功耗混合信号微控制器，具有内置的 16 位定时器、多达 24 个支持触摸感测的 I/O 引脚、一个通用型模拟比较器以及采用通用串行通信接口的内置通信能力。 此外，MSP430G2x53 系列成员还具有一个 10 位模数 (A/D) 转换器。 典型应用包括低成本传感器系统，此类系统负责捕获模拟信号、将之转换为数字值、随后对数据进行处理以进行显示或传送至主机系统。

##### 程序基础

MSP430 单片机的程序设计可以使用汇编语言，也可以使用 c 语言 ，无论汇编还是 c 语言，都需要掌握 MSP430 微处理器的结构、原理、接口等才可以进行软件与硬件的设计。
MSP430  系列采用的是“冯-诺依曼”结构，ROM、RAM 在同一地址空间，使用一组地址数据总线。中央处理单元采用了精简的、高透明的、高效率的正交设计，它包括一个 16 位 ALU（算术逻辑运算单元），16 个寄存器，一个指令控制单元，16 个寄存器中有 4 个为特殊用途，扮演重要角色，分别是：程序计数器、堆栈指针、状态寄存器、常数发生器。程序流程通过程序计数器控制，而程序执行的现场状态体现在程序状态字中。


##### 开发环境

德州仪器  (TI) 官方提供免费版本的开发软件 CCS，采用 eclipse+plugs+compiler 的组合开发平台，
CCS 平台自由度较高，可以更了解芯片的细节部分，比如启动过程 cstart ，中断的跳转方式，如何把中断向量表放置到 RAM 中，如何把函数拷贝到 RAM 中执行等等，IAR Embedded Workbench 是另一款收费的专业的 IDE 工具，集成度比较高，使用很方便，提供给用户的很多的友好的功能，对程序下载调试支持更友好，目前 IAR 已经更新至 7.X 版本，但建议使用 5.3 或 5.6 版本，功能更为稳定，这里使用 IAR 作为开发调试的环境。

##### 工作原理

目前市场上使用的单片机种类繁杂，包括 C51、AVR、MSP430、STM32、PIC 等等，其硬件架构虽不尽相同，但基本原理一致，最小单元都是 CMOS 管，通过逻辑运算，操作 IO 口输出不同数字电平信号，实现对外部模块的控制和通信。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/5b3c6b725a2d1.jpg)

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/5b3c6ecd492db.jpg)

内部大多会有 CPU、RAM、ROM、时钟晶振、总线接口、串行接口、寄存器、 ADC 等功能模块。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/5b3c6ee9d3650.png)

单片机程序执行原理基本一致，单片机自动完成赋予它的任务的过程，也就是单片机执行程序的过程，即一条条执行指令的过程，所谓指令就是把要求单片机执行的各种操作用的命令的形式写下来，这一系列指令的集合就成为程序，程序需要预先存放在具有存储功能的部件——存储器中，烧写程序的过程就是把程序代码转为为二进制，然后根据二进制数值不同，转为高低电平信号，改变存储器中晶体管的状态，程序就被固化在了存储器中。存储器由许多存储单元（基本结构为浮栅晶体管）组成，指令就存放在这些单元里，单元里的指令取出并执行就像大楼房的每个房间的被分配到了唯一一个房间号一样，每一个存储单元也必须被分配到唯一的地址号，该地址号称为存储单元的地址，这样只要知道了存储单元的地址，就可以找到这个存储单元，其中存储的指令就可以被取出，然后再被执行。

单片机程序通常是顺序执行的，所以程序中的指令也是一条条顺序存放的，单片机在执行程序时要能把这些指令一条条取出并加以执行，必须有一个部件能追踪指令所在的地址，这一部件就是程序计数器 PC（包含在 CPU 中），在开始执行程序时，给 PC 赋以程序中第一条指令所在的地址，然后取得每一条要执行的命令，PC 在中的内容就会自动增加，增加量由本条指令长度决定，可能是 1 、2 或 3 ，以指向下一条指令的起始地址，保证指令顺序执行。 

通过 IAR 的仿真调试，可知CPU初始会进行复位操作，然后把复位向量数据作为 PC 寄存器的值 ，在执行 IAR 编译器定义的程序入口点 __program_start 函数，其又被编译器定义为 cstart_begin 函数，后面紧跟着的是 cstart_call_main 函数，此函数才会去调用 main 函数 ，因此在一般的逆向过程中， 只需要从 main 入口函数开始分析。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/5b3c736724390.png)

编程大多基于 c 或汇编语言，对于不同的单片机，首先需要通过芯片型号查找官方数据手册，里面官方会有详细的介绍，包括功能模块、引脚定义、寄存器、ROM、RAM、时序图等信息，参考官方说明，对单片机开发入门具有帮助。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/5b3c6f0e97f49.png)

##### 实例分析

下面是一个简单控制 LED 闪烁的程序 ：

```c
#include <msp430g2553.h>

//IO口初始化
void Port_Init()
{
    P1DIR|= 0x40; // P1^6配置为输出
    P1OUT|= 0x40; // P1输出0100 0000
}

//看门狗初始化
void WDT_Init()
{
   WDTCTL = WDTPW + WDTHOLD; //关闭看门狗
}

int main( void )
{
    WDT_Init();
    Port_Init();
    while (1)
    {
       __delay_cycles(500000); // 系统延时 500 000 机器周期
       P1OUT ^= 0x40; // 循环异或实现LED闪烁
    }
}
```

硬件连线图如下 ：

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/5b3c726566d9d.png)

电路原理图如下 ：

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/5b3c72bc170e6.png)

程序首先定义 P1 口寄存器，初始化为输出状态，寄存器为8位数据，然后在 while 循环改变 IO 输出状态，通过高低电片的循环延时变化，使 LED 闪烁，详细说明如下：

- WDTCTL = WDTPW + WDTHOLD; //MSP430 的看门狗默认是打开的，如果在程序开始不关闭，程序执行到一定时间就会自动复位，那样程序就无法正常执行
- P1DIR |= 0x40; //PxDIR,Px 口方向寄存器，为 0 端口配置为输入（默认），为 1 端口配置为输入，P1.6 口配置为输出
- P1OUT |= 0x40; // 配置IO口寄存器，PxOUT,Px 口输出寄存器（输入、输出两种模式），当 IO 口配置为输出模式时：0 输出低电平、1 输出高电平，当 IO 口配置为输入模式并且置高/置低使能时：0置低、1置高，P1输出 0100 0000，此时 P1.6 口为高电平，点亮 LED 灯。
- __delay_cycles(500000); // IAR编译器内联的精准延时函数，此芯片默认设置时钟主频为1M，即每个机器周期为 1us，500000即为执行500000个机器周期的时间，延时500毫秒，实际开发中，可以根据如下代码，设置主频然后换算成毫秒来计时

	```c
	#define CPU_F ((double)1000000)   设置主频晶振1MHZ
	#define delay_ms(x) __delay_cycles((long)(CPU_F*(double)x/1000.0))
	```

- P1OUT ^=0x40; //P1 异或输出 0000 0000  ，熄灭 LED 灯，再次循环，异或输出 0100 0000 点亮 LED，循环实现闪烁功能。

#### MSP430 逆向基础

使用上面 LED 闪烁程序来做案例，通过调试查看源代码和二进制还有汇编指令一一对应的关系。

- main 函数

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/5b3c96380df63.png)

- 其他函数

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/5b3c9638bf0d5.png)

走边为源代码，右边红色圈为hex文件的地址，蓝色圈为二进制字节码，绿色圈为对应的汇编代码，通过一一对比可以正向看出 MSP430 编码怎么编译成固件，需要注意几个点：
1. 关闭看门狗，芯片工作时必须的操作，这是一个宏定义值，因此可以用于定位入口函数。
2. __delay_cycles的参数为需要执行的机器周期个数，IAR根据该参数编译为需要执行对应机器周期数量的汇编指令 。 

##### 初步分析

现在假设我们不知道源码，只有 hex 文件和电路图，参考芯片的手册《MSP430G2553 用户指南》和《MSP430 汇编指令集》 。我们使用 ida 来一一逆向分析固件 ， 
载入ida，处理器选择 MSP430 。 

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/5b3cad0587669.png)

可以看到有四个函数，这里有些函数地址会和之前调试的不一样，根据看门狗 mov.w   #5A80h, &120h 指令可以确定 sub_C038 为关闭看门狗函数， 按 n 重命名此函数 ，按 x 查看交叉引用可以回溯到  main 函数里面，可以确定 sub_C00C 为程序的入口。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/5b3cadeed7449.png)

整个固件程序结构

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/5b3cadf68b002.png)



#### 自动化分析

对比之前和 IAR 调试界面，发现 ida 里面一些寄存器地址例如 P1OUT ，WDTCTL 不能自动显示出来，而是具体的偏移 21h ， 120h ，为了方便分析，可以写一个的idaPython 脚本来自动化注释，读取 msp430g2553.h  宏定义替换。

```c
......
#define P1IN_               (0x0020u)  /* Port 1 Input */
READ_ONLY DEFC( P1IN           , P1IN_)
#define P1OUT_              (0x0021u)  /* Port 1 Output */
DEFC(   P1OUT             , P1OUT_)
#define P1DIR_              (0x0022u)  /* Port 1 Direction */
DEFC(   P1DIR             , P1DIR_)
......
#define WDTCTL_             (0x0120u)  /* Watchdog Timer Control */
DEFW(   WDTCTL            , WDTCTL_)
......
```

Python脚本，也可以从附件文件夹 [/scripts/2.3.2/msp430_auto_comment.py](/_assets/scripts/2.3.2/msp430_auto_comment.py) 获取。

```python
from idaapi import *

file = open("msp430g2553.h",'r')
lines = file.readlines()
funcs = Functions()
for f in funcs:
	for i in FuncItems(f):
		try:
			if idc.GetOpnd(i,0)[0]=='&':
				for line in lines:
					if line.find(idc.GetOpnd(i,0)[1:].replace('h','',1)) != -1:
						line.expandtabs()
						words = line.split(' ')
						MakeComm(i,words[1][:-1])
						break
			if idc.GetOpnd(i,1)[0]=='&':
				for line in lines:
					if line.find(idc.GetOpnd(i,1)[1:].replace('h','',1)) != -1:
						line.expandtabs()
						words = line.split(' ')
						MakeComm(i,words[1][:-1])
						break
		except :
			continue
```
在某固件中执行脚本，可以自动把地址对应的寄存器自动注释出来，大大方便之后的逆向。 

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/5b3cadf68b2a1.png)

##### 逆向结果

回到 main 函数，继续根据流程逐步分析 ，调用 sub_C02A ，这个函数有两个指令。

```
bis.b   #40h, &22h      ; P1DIR  配置P1.6口配置为输出口
bis.b   #40h, &21h      ; P1OUT  P1 ，配合电路图分析即为高电平，LED 灯亮 。
```

猜测此函数功能为一些 io 口的初始化，添加备注和修改函数名称。继续后面为一个循环结构。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/5b3cbe7837d7f.png)

根据 ida 结构显示为两个循环嵌套，外面一个死循环，嵌套一个 loc_C01C 条件循环，根据指令操作和上下关联推断其为延时功能：

```c
mov.w    #E846 ， R15 // 0xE846 移入R15寄存器，耗时2个机器周期
nop // 空指令占位，耗时1个机器周期
mov.w    #0x1 ， R14 // 0x1 移入R14寄存器，设置为R15寄存器的最高位，耗时1个机器周期
add.w    #0xFFFF , R15 // 0xFFFF 移入R15寄存器，因数值超过16位，需要进位，同时SR寄存器N状态位置1，C状态位置为1，耗时1个机器周期
addc.w    #0xFFFF , R14 // 0xFFFF 加上 C 状态位的值，移入R14寄存器，因数值超过16位，需要进位，C状态位置保持为1，耗时1个机器周期
jc  0xC0IC  //根据进位位的值也就是C状态位的值判断是否跳转至 0xC0IC ，当循环完所有周期，C状态位复位为0，结束循环，耗时2个机器周期。
```

loc_C01C 执行需要4个机器周期，初始置位赋值需要8个机器周期，即可推算出整个循环需要 0x1e846*4 + 8 = 500000 个机器周期，配合上之前定义的时钟主频 1M hz，推算出总延时长为 0.5 s ，然后执行下面的语句。

```c
xor.b   #40h, &21h      ;  P1OUT寄存器的值与0x40异或， P1.6口输出寄存器第7位的值， 循环异或，输出高低电平，实现闪烁功能。
```

根据上述分析，结合电路和硬件，本程序通过对IO口寄存器值的循环异或，输出高低电平，再通过每次延时500毫秒，实现控制 LED 闪烁功能。

完整逆向结果：

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/5b23e9d8cbb91.png)

### 某智能锁

再来看一个实际的例子，对一个基于 MSP430 芯片的电子锁逆向分析，该款电子密码锁板载 MSP430F149 单片机，基本功能是当输入正确密码时，单片机会输出一个信号，使电机转动 实现开锁动作。

#### 提取固件

通过之后的 2.5.2 章节 SBW 协议提取 hex 格式的固件。
 
####  电路分析

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/5b3afe34d24b6.png)

查看电路结构，发现在 P2.0 到 P2.3 口布线连接至 TC1508S 型号的芯片上，查芯片手册得知 TC1508S 是双通道内置功率 MOS 全桥驱动芯片。该芯片主要实现驱动直流电机进行正反转、前进后退等功能。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/5b3afdf529f7e.png)

ULN2003 输出管脚连至一个双极性的直流电机上，用于控制电机正反转等动作，由此可知在代码中会初始化P2.0-P2.3 IO口，并在密码正确的情况下，输出控制信号，参考 TC1508S 的逻辑真值表：

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/5b3afe1e2ad60.png)


#### 逆向分析

载入 ida ，运行 msp430_auto_comment.py 自动加上注释 ，确定 main 函数，从 main 开始分析整个固件流程。
根据之前的电路分析，可以初步得出P2.0-P2.3 IO 口来控制电机芯片的，也就是要开关锁的关键 。
初步逆向分析结果：

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/5b3cad0587345.png)

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/5b3cad0587ac1.png)

由于篇幅有限，对智能锁的详细逆向分析及其攻防可以看后续的章节 。

## 嵌入式

嵌入式设备的逆向和传统二进制一样差不多，注意架构就行，这里使用路由器的 web 服务器漏洞逆向来做案例。

### 某路由器漏洞分析

某路由器存在溢出漏洞，测试 poc 如下，来静态逆向分析漏洞。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/5b390e96f181b.png)

从poc中可以得知，路由器上的 web 服务器在处理 /goform/set_manpwd 请求时出现了问题，导致在未进行用户校验的情况下，通过 routepwd 字段可以更改管理员密码，且能崩溃 web 服务器。

提取路由器中的固件，使用 binwalk 解压固件，在 /bin 目录下可以得到路由器的 web服务器的二进制文件 goahead。使用 file 命令查看 goahead 的信息如下：

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/5b390d6b2a969.png)

可以看到目标平台是 mips32 位，LSB 字段表明是小端序，指令集为 mips32 rel2。
使用 ida 对 goahead 进行静态分析，在 strings 窗口中直接搜索 set_manpwd ，得到两处字符串。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/5b390e34d34ae.png)

分别查看交叉引用得到 0x46c558 处的字符串在 sub_457ebc 中被引用两次，

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/5b39100b3120a.png)

0x46b6b4 处的字符串在 formDefineCGIjson 中被引用了一次。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/5b3910574ca57.png)

查看 formDefineCGIjson 中的引用位置发现 websFormDefine 的第二个参数被置为 sub_457ebc 的指针。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/5b391068d0fae.png)

推断 sub_457ebc 为主要处理 set_manpwd 的函数，进入sub_457ebc 函数发现主要有以下函数调用：
获取 routepwd 的值，该字段正是可以更改密码和命令执行的字段，

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/5b390e6acf933.png)

将传入的参数格式化成 json 对象并传入 bs_setmanpwd 函数，同时传入的还有当前栈帧的字符串地址，对 bs_setmanpwd 函数分析之后发现是一个来自 libshare.so 的库函数，且对我们的漏洞并无重大影响

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/5b390e7d89d76.png)

对 http 请求进行回复并删除 json 对象。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/5b3910db68c51.png)

获取 password 并使用 password 格式化字符串 “chpasswd.sh admin %s”,可以看出此条命令应该和修改管理员密码有关，继续向下发现 bl_do_system 函数的参数为刚才格式化好的字符串，推测此处应该是修改密码并进行命令执行的地方。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/5b390e87c11a9.png)


