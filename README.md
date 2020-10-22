
# Table of Contents

1.  [应用场景](#org184d501)
2.  [功能](#org45bc7f9)
3.  [使用方法](#org9c719fd)
    1.  [Windows](#org23ceb7f)
    2.  [MacOS](#org63f6e29):未经测试:
    3.  [Linux](#orgdc0379c)
        1.  [Linux下的安装过程](#org4f4a53a)
        2.  [Linux上的使用技巧](#org5aaf465)
4.  [程序解释](#org00f4e50)
5.  [可能出现的问题](#orgcc48091)
    1.  [为什么我输入不了密码？](#org1b474b6)
    2.  [我不在意安全，可以让我可以明文输入密码吗？](#orgebe6701)
    3.  [我看不懂英语怎么办？](#orgb0f762d)
6.  [待办 <code>[3/4]</code>](#org00062d2)
7.  [感谢](#orgd758685)



<a id="org184d501"></a>

# 应用场景

1.  懒人不想直接打开浏览器连网，想一键连
2.  玩树莓派但是没有下载图形界面版的系统，手机又没有多少流量。
3.  安装Archlinux或者Gentoo之类的Linux发行版的时候手机没有多少流量了。
4.  觉得一键登录校园网好玩


<a id="org45bc7f9"></a>

# 功能

1.  首次设置之后可以根据生成的配置文件自动登陆
2.  配置文件密码加密存储，（不过加密方法都写在源代码里面了，加密也只能防下小白吧）


<a id="org9c719fd"></a>

# 使用方法


<a id="org23ceb7f"></a>

## Windows

首先根安装python，可以自己百度如何安装。

安装完成之后在桌面按 `Windows+R` 打开运行，然后输入 `cmd` ，回车，然后在命令提示符中
输入：

`pip install requests`

等到又重新出现 `C:\>` 及类似的提示符，说明程序执行完毕，可以输入 `exit` 退出，也可以
直接点X退出命令提示符。

---

然后用文件管理器打开这个文件夹，然后在文件导航栏（就像浏览器的网址栏，是显示目前
的文件夹位置的地方，比如说 `D:\ > SourceCodes > Python` ）里面输入cmd或者
powershell回车，进入命令行。

Windows 的命令提示符长这样子：

    D:\SourceCodes\Python\csust-network-login>

大于号的左边是当前的目录，而右边就是我们输入命令的地方，下面我将命令提示符也写出
来了，为了方便表示，如果要用这个方法，只输入大于符号右边的东西就可以了。

如果是第一次使用，可以直接如下输入

    D:\SourceCodes\Python\csust-network-login> python .\log2network.py

如果想更改一下登陆的用户名或者密码，可以输入

    D:\SourceCodes\Python\csust-network-login> python .\log2network.py -n

也可以输入 -h 来获取帮助

    D:\SourceCodes\Python\csust-network-login> python .\log2network.py -h

---

上面的方法太过于麻烦，简单粗暴的方法:

1.  首次运行直接双击 `log.cmd` 运行，然后在按照提示输入学号与用户名
2.  之后运行直接双击 `log.cmd`
3.  如果需要方便一点的话，可以将 `log.cmd` 发送到桌面快捷方式，注意不能将
    `log.cmd` 复制或者移动到桌面，而是将其快捷方式发送到桌面，然后之后就双
    击这个快捷方式就可以了。如果不会的话可以百度如何发送快捷方式。
4.  <del>Windows有的可能没有显示后缀名，有的同学可能分不清哪个是 `.py` 哪个是 `.cmd` ，这</del>
    <del>样的话可以看图标，有一个python标志的是 `.py` 文件，图标主要是一个还是两个齿轮背
    景为一个白框的是 `.cmd` 文件</del>

    已经更名 `log2network.cmd` 为 `log.cmd`

5.  注意 `log.cmd` 与 `log2network.py` 要在同一个目录下，而且建议将这两个放到
    一个单独的文件夹下面而不是直接放在桌面上，因为程序会在当前目录下面生成2个文件。

如果输入错误或者想要更换号码，就把目录下面的 `loginData.json` 删除再双击运行。

程序会生成两个文件

-   loginData.json 配置文件，存储了学号与密码
-   login.log 是日志文件，记录了登陆的记录


<a id="org63f6e29"></a>

## MacOS     :未经测试:

没有用过MacOS，但是应该和Linux差不多，可以通过双击运行也可以直接命令行运行。

还是应该先安装python还有运行 `pip install requests`

打开终端，通过cd进入这个目录，这是一个Python程序，可以跨平台使用，所以使用方法和
windows一样。只不过windows中目录的斜杠是反斜杠，而MacOS与Linux里面的斜杠是正斜
杠，在 `右Shift` 的左边那个按键上面，例如下面这样：

    ~/csust-network-login $

但是其实都是一样的，我们要输入东西的区域是$符号右边，输入的内容和windows一样，只是将"\\"变成"/"。

也可以尝试一下双击(log2network.py)运行，参考上面说的windows平台上面的使用方法。


<a id="orgdc0379c"></a>

## Linux

用Linux的学弟学妹可以考虑看看源代码，然后写一个更好的让我用233。


<a id="org4f4a53a"></a>

### Linux下的安装过程

-   安装Python

    for archlinux:

        pacman -S python3 git

    for ubuntu:

        apt-get install python3 git

-   安装依赖

        pip install requests

-   获取源码

        git clone https://gitee.com/colawithsauce/csust-network-login.git

        # 如果想要切换到开发分支
        # cd csust-network-login && git checkout develop && cd ..

-   创建软连接

        # 如果 ~/.local/bin 不存在就创建
        if [ ! -d ~/.local/bin ]; then mkdir -p ~/.local/bin; fi

        # 如果 ~/.local/bin 不在PATH中就加入
        echo ${PATH} | grep ./local/bin || echo "export PATH = \${PATH}:~/.local/bin" | tee -a ~/.bashrc

        # 连接文件到目标
        ln -sf `pwd`/csust-network-login/log2network.py ~/.local/bin


<a id="org5aaf465"></a>

### Linux上的使用技巧

1.  保持自己在线

    虽然这个是一个待办事项，但是目前还没有用Python实现，可以用Shell暂时替代一下，方法是：

        while true; do log2network.py; sleep 10; done;

    每10秒钟尝试登陆一次

2.  如果想不通过删除配置文件的方法来换登陆账号

        log2network.py -n

    这是我预留的一个不通过配置文件登陆的方法，而且它还会问用户是否需要写入配置文件。


<a id="org00f4e50"></a>

# 程序解释

逻辑非常简单，就是获取账号密码然后登陆而已，就是有两个地方有一点麻烦：

1.  登录url的获取：

    虽然迷糊了好久，但是幸好有学长的代码可以借鉴: [学长的repo](https://github.com/linfangzhi/CSUST_network_auto_login)，我终于写出来了。

    登录的时候，网址可以看到是192.168.7.221，而后面还有一大堆东西，那些东西是登录
    的关键信息，必须和目前上网设备的信息一致，但是导航栏上面的网址并不是POST的网
    址，目标网址要按F12点Network，然后点登陆，打开出现的POST一栏，就可以看到这个
    url了。

    上面那段写了好久都没有写通顺，不如大家自己去上网登录窗口按F12，然后点Network，
    再点击登陆，看看POST请求的内容就清楚了。
2.  base64加密：

    python 的 base64 函数的输入参数与返回值都是bytes类型，而密码是str类型，而写入
    json文件的时候又需要是str类型，所以decode和encode非常多，让代码看上去有点丑。


<a id="orgcc48091"></a>

# 可能出现的问题


<a id="org1b474b6"></a>

## 为什么我输入不了密码？

为了安全（防止别人窥屏知道你的密码，或者甚至知道它的长度），所以我特意让密码输入
不回显，所以其实你是在输入的，只不过没有显示出来罢了。按照肌肉记忆输入完成然后回
车吧！


<a id="orgebe6701"></a>

## 我不在意安全，可以让我可以明文输入密码吗？

暂时还不能，而且也不打算支持。但是如果硬要明文输入应该可以采用在记事本上面写好然
后复制粘贴入终端的方法输入密码。

值得注意的是，好像Windows不能直接Ctrl-V粘贴，要右键然后点粘贴。不记得具体了，也
暂时没有办法验证，我一直在用Linux，好久没有用Windows了。。。


<a id="orgb0f762d"></a>

## 我看不懂英语怎么办？

因为我本来计划是在Linux的tty上面使用的，而终端没有办法用浏览器登录、显示中文也非
常麻烦，如果不打补丁的话中文会变成白方块。后面发现这个在桌面系统下面也比点鼠标要
方便，但是毕竟有的时候难免需要进入tty做事情，所以还是决定将语言更换为英文。

所以虽然第一版是中文输出与提示，但是后面经过考虑改成了英语提示，毕竟主要是给自己
用然后再去满足别人的需要。

如果实在看不懂的话，Student ID就是学号，Password就是密码，万一它显示[Y/n]就输入Y
然后回车（如果只是双击 `log.cmd` 运行是不会提示让你输入[Y/n]的），其它的输出都没有
必要看明白，它们作用只是让人知道程序现在运行到哪里了。


<a id="org00062d2"></a>

# [ ] 待办 <code>[3/4]</code>

-   [ ] 将其编译为可执行文件：

    我主要使用的是Linux操作系统，基本没有太多可能非常接触到有git还有python环境的
    Windows操作系统，所以这个待办可能会无限期推迟😅

    我早该想到的，为什么一定要在编译它的电脑上上传，我可以复制到我自己的电脑上面上
    传啊。明天就找舍友借一下电脑打包一下然后再复制到自己电脑上面上传。。。

-   <del>[ ] 调用系统API或者用python库控制系统根据配置自动连接校园网</del>

    <del>提升自动化程度，但是像第一个问题一样，没有接触到windows</del>

    -   Canceled: 因为如果增加这个功能的话，需要针对每台电脑配置网卡的参数，但是每台
        机器的网卡明显会是不同的，即使加上这个功能，它也只能在我电脑上运行。

-   <del>[ ] 登陆失败的时候返回更多信息：</del>

    <del>目前因为GET的回应只有HTML文件，服务器返回的账号不存在，密码错误等信息都是通过
    js加载的，所以只要找到一个得到那些js文件的执行结果的方法就可以解决这个问题了。</del>

    超过我目前的能力了，也许有空会挑战一下，但是我现在有更加重要的事情去做，所以坑
    了。

-   [X] 完善Linux相关的使用方法：

    我并没有用Linux的人就一定什么都懂的意思，因为我自己也在使用Linux。

    但是为什么第一版的Linux使用方法写成技术分享了呢？主要因为不想对同样的操作讲三
    遍。。。(因为单纯联网的话就是 `python log2network.py` 嘛，不同操作系统根本就没有
    什么不同，只不过为了双击运行，Windows用.cmd文件将这段调用的命令写下来了而已)

    所以之后有空了我打算重新写一下Linux部分的使用方法。

-   [X] 保证自己一直在线的功能：

    这个可能比较暴力， <del>表现为和女朋友抢校园网能永远不输</del> ，可以减少被不稳定的网卡折
    磨的痛苦。

    目前的思路是可以让电脑一直不断地对百度进行请求，如果没有回应了，就说明断连了，
    就调用登陆函数进行登陆即可。

-   [X] 将获取密码部分的代码也模块化：

    感觉现在代码的主逻辑还是不太干净，需要再减少一点东西保持干净。


<a id="orgd758685"></a>

# 感谢

[学长的repo](https://github.com/linfangzhi/CSUST_network_auto_login)
