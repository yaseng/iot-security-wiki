# 远程调试

## 前言
在通过串口调试嵌入式设备时，每次需要通过接线和 USB 转换器连接才能进行，对设备操作的话，存在一定的不便，并且会占用电脑的 USB 口，接线也会造成一定的不稳定，因此可以通过串口命令开启 telnet 或者 ssh 服务，远程登陆设备。通过系统命令、程序的输出以及 gdb 进行 远程调试，提高调试的便捷性。

## 调试案例

### 某路由器溢出漏洞调试

在 2.3.1 章节中对漏洞进行静态分析，现在来动态调试。

基本函数结构分析结束后，使用 gdbserver 附加到 goahead 进程进行远程调试，验证我们的猜测是否正确。
telnet 连上路由器并使用 gdbserver 附加到 goahead 进程进行调试。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/5b390e8f8bc7d.png)

使用 ida 远程链接之后在 sub_457ebc 入口出下断点，f9 键开始运行，brupsuit 发送 poc 之后断在了 sub_457ebc 函数处。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/5b390e96f181b.png)

单步查看 websGetVar 的返回值 0x48d4a8 处的值正是我们发送的poc。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/5b391147c2521.png)

运行至 bs_setmanpwd 查看参数如下,a0 的值为格式化之后的 json 对象的指针，a1 的值为当前栈帧中一个长度为 400 字节的缓冲区的指针。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/5b390ea6a2580.png)

继续运行，查看 nvram_bufget 的返回值v0为我们传入的 routepwd 字段的值。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/5b390eae51d41.png)

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/5b390eb587d58.png)

继续向下，fprintf 格式化字符串，a0 为当前栈帧上一个长度为 200 字节的字符串的地址。
![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/5b390ebe75750.png)

可以看到此处并没有对 nvram_bufget 获取到的值进行长度验证就格式化到缓冲区上造成了缓冲区溢出。
![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/5b390ec7ab081.png)

继续向下可以看到 bl_do_system 把刚才格式化好的字符串当作指令执行了，因此此处对 “chpasswd admin %s” 进行截断之后可以追加任意命令且以管理员权限执行。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/5b390ecfa87b2.png)

继续向下执行到“lw $ra,0x2a0+ra($sp)”之后，ra的值被覆盖成 0x61616161 ，我们在此处劫持了函数的返回地址，经过计算此处距离缓冲区起始地址为 618 个字节，至此可以执行任意代码。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/5b390ed82ba62.png)



### 某摄像头远程调试

在对某个摄像头进行漏洞分析时需要调试 recorder 进程。

```c
[root@xxx /tmp]$ ftpget   192.168.1.111   gdbserver-7.7.1-armel-eabi5-v1-sysv
[root@xxx /tmp]$ chmod   777   gdbserver-7.7.1-armel-eabi5-v1-sysv
[root@xxx /tmp]$  ./gdbserver-7.7.1-armel-eabi5-v1-sysv  :9999  --attach  2394
Attached; pid = 2394
Listening on port 9999
```

直接附加上去之后，本地 arm-none-eabi-gdb 连接，下断点，提示:Cannot access memory at address 0xb695de04 发现内存地址不可读，查看发现已经变为僵尸进程，又新起了一个。

```c
[root@xxx ~]$ ps   |  grep  re
    2 root       0:00 [kthreadd]
 2394 root       0:24 [recorder]
 2651 root       0:02 recorder
```

猜测应该有另外一个守护进程，附加的时候会停止程序，查看进程

```c
494 root 0:01 /mvs/apps/as9ipcwatchdog /mnt/mtd
```

直接 kill 掉发现摄像头不能正常使用，看来这个进程还有一些其他的功能，不能直接 kill，只能去掉对目标进程的守护功能，载入 ida
字符串搜索 recorder 。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/5b388c1a6b58f.jpg)

直接替换掉 recorder 即可，例如替换为相同长度的 aaaaaaaa 。 

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/5b388c79eea01.jpg)

为了方便，可以把原程序修改，然后重刷进去，具体可以参考后面 2.6 章节，这里不涉及到硬件修改，简单的把守护进程放到可写目录。
目前的调试流程为:
1. 修改 as9ipcwatchdog，替换所有的 recorder 
2. 停止 as9ipcwatchdog，recorder 。
3. 下载 as9ipcwatchdog 到tmp目录，启动  as9ipcwatchdog 。
3. 启动 recorder
4. APP 端删除当前的设备，重新搜索添加 。
5. 断点调试


```c
(gdb) target  remote 192.168.1.136:9999
Remote debugging using 192.168.1.136:9999
warning: No executable has been specified and target does not support
determining executable automatically.  Try using the "file" command.
0xb69d3e04 in ?? ()
(gdb) x  /5i  $pc
=> 0xb69d3e04:    mov    r7, r0
   0xb69d3e08:    mov    r0, r12
   0xb69d3e0c:    bl    0xb6a19b74
   0xb69d3e10:    mov    r0, r7
   0xb69d3e14:    pop    {r7, lr}
```

此时已经可以正常调试，同样以修改设备的时间来做测试，在 Linux 操作时间函数 stime 下断点 。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/5b388d5a744d5.jpg)

点击保存

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/5b388656a6ecd.png)

```c
(gdb) b *0x0000D3DC
Breakpoint 1 at 0xd3dc
(gdb) info  b
Num     Type           Disp Enb Address    What
1       breakpoint     keep y   0x0000d3dc
(gdb) c
Continuing.
[New Thread 1925.2202]
[New Thread 1925.2201]
[Switching to Thread 1925.2202]

Thread 28 "" hit Breakpoint 1, 0x0000d3dc in ?? ()
```

成功断点，可以做一些后续的漏洞分析。

