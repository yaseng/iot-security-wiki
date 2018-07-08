# 网络

## 前言
本节主要讲述物联网在网络层协议的分析，包括数据抓包、分析、定位、修改、重放等方式。


## 抓取
在做协议分析之前，需要抓包，这里介绍几种抓包的方式。
### 路由器中

通过路由器抓包是最稳定有效的方式，推荐使用树莓派刷 openwrt ，然后外接 wifi 天线，不外接天线的话，wifi 信号质量和传输距离可能较差，有充分预算的也可以使用高配置的 Netgear 或 Linksys 路由器刷 openwrt 进行抓包，性能会更好。然后使用 tcpdump 抓包。
例如对某个摄像头一些通讯数据的抓包，抓取手机与设备之间的交互数据。

```c
tcpdump host 192.168.1.136 and  192.168.1.128  -i wlan0  -w  1.pcap
```

通过 ftp 传输回来，数据包为一些视频流和指令  。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/5b387f7ed43a7.jpg)

### 移动设备

当遇到使用了 ssl 的协议 例如 HTTPS ，抓包获取不到明文，这时可以通过如下方法进行抓包，例如 Android 下面伪造证书，然后 hook SSL Pinning ，也可以使用 Xposed 的 JustTrustMe 模块 ，然后配合 mitmproxy 抓包。对于一些较为复杂 、自定义的加密协议来说，hook 发包，收包来获取数据，会大大简化后续的分析流程。例如分析一个 Android app 与智能摄像头之间的通信，通信协议为 TCP ，需要 hook OutputStream write 函数 。需要注意的是不能 hook java.io.OutputStream 抽象类，而需要去 hook 具体实现类，这里使用跨平台的 Frida 工具来 hook。

hook 代码

```js
Java.perform(function() {

  console.log("[*] hook start...")
  h1 = Java.use("java.net.PlainSocketImpl$PlainSocketOutputStream");
  h1.write.overload('[B', 'int', 'int').implementation = function(a1, a2, a3) {

    console.log("[+] hook PlainSocketOutputStream:write(byte[],int,int)");
    console.log(a1, a2, a3);
    send('data:', new Uint8Array(a1));
    return this.write(a1, a2, a3);

  }

})
```

注入目标进程
frida  -H  192.168.1.128   -n  com.xxxx.xxxx   -l   tcpdump.js   --no-pause 

结果:
![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/5b3882c895003.jpg)

为了更方便的分析，修改数据，可以进一步的 hook APP 的交互的具体实现代码。例如通过 APP 对智能设备时间设置。

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/5b388656a6ecd.png)

逆向分析获取智能设备时间代码。

```java
private static DateTimeInfo getDateTimeServerEX(String strIP, int nPort, LoginHandle loginHandle, int nDeviceID) {
    OutputStream writer = null;
    InputStream reader = null;
    DateTimeInfo dateTimeHandler = new DateTimeInfo();
    dateTimeHandler.setnResult(ResultCode.RESULT_CODE_FAIL_SERVER_CONNECT_FAIL);
    System.out.println("get server IP:" + strIP + " Port: " + nPort);
    Socket sSocket = Functions.connectToServer(strIP, nPort, Defines.CMD_MR_WAIT);
    if (sSocket != null) {
        boolean isConnectOK;
        try {
            if (sSocket.isConnected()) {
                writer = sSocket.getOutputStream();
                reader = sSocket.getInputStream();
                isConnectOK = true;
                if (isConnectOK) {
                    Arrays.fill(buffer_EX, (byte) 0);  //数据包填充0 
                    Functions.IntToBytes((long) 315, buffer_EX, 0);  //获取时间的指令
                    Functions.IntToBytes((long) nDeviceID, buffer_EX, 4); //设备的id
                    buffer_EX[8] = (byte) 1;
                    Functions.IntToBytes(loginHandle.getlHandle(), buffer_EX, 9); //登陆标识
                    try {
                        writer.write(buffer_EX, 0, 256);  //发送数据
                        writer.flush();
                    } catch (IOException e) {

```

可以很清晰的看到一个指令的格式，各个部分的意义。hook 更多的类来获取更细节化的信息。例如 hook 获取时间和设置时间

```js
  h2= Java.use("com.xxx.sdk.setting.DeviceDateTimeSettingEX");
  h2.getDateTimeServerEX.implementation = function(a1,a2,a3,a4){

   console.log('[*] hook DeviceDateTimeSettingEX:getDateTimeServerEX');
   console.log(a1,a2,a3,a4);
   return  this.getDateTimeServerEX(a1,a2,a3,a4);

  }

 h2.setDateTimeServerEX.implementation = function(a1,a2,a3,a4,a5,a6,a7,a8,a9){

  console.log('[*] hook DeviceDateTimeSettingEX:setDateTimeServerEX');
  console.log(a1,a2,a3,a4,a5,a6,a7,a8,a9);
  return this.setDateTimeServerEX(a1,a2,a3,a4,a5,a6,a7,a8,a9);

 }
```

结果

![](https://img-1253984064.cos.ap-guangzhou.myqcloud.com/5b388950cb3de.jpg)


## 分析

常见的协议例如视频流，音频流的识别，以及自定义的协议的分析。

## 使用

对数据的分析，重放，修改 。
