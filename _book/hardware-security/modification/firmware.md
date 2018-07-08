# 软改

## 前言

某些情况下，单纯针对硬件层面的修改可能无法满足需求时，就需要在固件层面进行修改，如通过修改智能摄像头固件中的密码，绕过厂商在串口调试时的密码验证；如修改家用电视机主板固件中的用户信息，解决开机故障问题，如修改路由器固件，使低版本固件兼容高版本硬件，本章将用实例，展示固件修改的具体方式和思路。

## 嵌入式设备
对于嵌入式系统的固件，查看其文件系统，解压，找到对应的文件，直接修改，修改之后重打包刷入即可。例如对某个摄像头 root 密码的修改。

### 摄像头固件修改

拿到固件 BIN 之后，使用 binwalk 解包

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/5b23e73cde014.png)

发现有多个 squashfs 文件系统，且解包后对应的文件系统根目录只有一个，其他几个是不完全的目录，猜测第一个 squashfs 对应文件系统根目录。将第一个 squashfs 文件系统从固件中 dump 出来，然后使用 unsquashfs 工具解压

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/5b23e9d8cbb9b.png)

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/5b23ea5f7ae5f.png)

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/5b23ea74b401e.png)

在当前工作目录中多出一个 squashfs-root 文件夹，内容正是根文件系统

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/5b23eb58bc587.png)

查看 etc/shadow

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/5b23ebddc4948.png)

将root账户的密码字段置空后保存，然后使用 mksquashfs 工具打包，压缩格式选用和 second.bin 相同的压缩格式，blocksize 设置为和 second.bin 相同的131072 bytes，将所有文件的所有者使用 -all-root 参数设置为 root，-nopad 指定不要进行4k对齐

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/5b23ee02b2d66.png)

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/5b23eee21ff88.png)

由于重打包之后的文件系统比原文件系统要小，所以要对 newrootfs.bin 末尾进行填充

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/5b23ef9ccdab9.png)

填充之后的 newrootfs.bin 和 second.bin 大小相同。然后将 first.bin,newrootfs.bin,three.bin 按顺序拼接成新的固件

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/5b23f0ebd1fc0.png)

可以看到修改之后的固件和原固件大小相同，文件结构也相同，配合之前的体外分离硬改，刷入固件之后开机，root 用户已经可以无密码登录。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/858ffghe3564/5b3263dc9f57a.jpg)

如果要对 elf 文件的修改，可以参考之前的 2.3.2 固件逆向，2.5.3 远程调试章节，二进制逆向分析，修改对应的指令，字符串来完成程序修改。然后在重新打包回去。


## 单片机
对于无操作系统的单片机固件，需要通过逆向出来，再来修改逻辑或字符串。