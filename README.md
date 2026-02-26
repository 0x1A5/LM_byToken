# LM_byToken (Launch Minecraft by Token / 通过Token启动正版Minecraft)
此工具可以获取您的Minecraft正版登录Token并启动Minecraft。<br>
## 什么是 Minecraft 访问令牌？
Minecraft 正版验证Token用于验证您是否为正版验证。

例如，除了官方的 Minecraft 启动器启动 Minecraft Java 版本外，您还可以通过命令行启动游戏。

在命令行启动参数中，minecraft 验证令牌就是其中之一。

也就是说，您可以在**没有**启动器的情况下启动**正版**Minecraft。

## 如何使用这个工具？
- 下载仓库的zip压缩包并解压。
### 配置参数
> 在解压后的`src`文件夹中的`tokens.json`文件为此工具所需参数的存储文件。

以下是其内容即填写格式：
```json
{
    "user": [
        {
            "name": "<您的Minecraft档案名>",
            "uuid": "<您的Minecraft UUID>",
            "acc_token": "<您的登录token>",
            "ref_token": "<您的刷新token>"
        }
    ],
    "gameVersions": [
        "<您要启动的游戏版本，如1.20.4>，可以有多个值，程序会请求选择"
        ],
    "Dirs": {
        "versionDir": "<您要启动的Minecraft版本文件夹所在的目录>",
        "assetsDir": "<您的assets文件夹所在的目录>",
        "javaDir": "<您用于启动Minecraft的java.exe文件所在的目录>"
    }
}
```
- 其中，`user`参数中的`name`为您的Minecraft档案名；`uuid`为您的Minecraft账号的uuid，**不包含"-"连字符**，可在[这里](https://mcuuid.net)查询。
- 其中，`acc_token`参数为您的Minecraft登录token而非Microsoft登录token；`ref_token`参数为您的Microsoft刷新token，若您不知道您的登录token，可以直接留空。
- `gameVersions`参数为您要启动的Minecraft版本（名称），这一参数为您的版本文件夹所在的目录，或您的Minecraft`.jar`文件的名称，不包含".jar"。
- `Dirs`参数中为此工具需要（或启动Minecraft需要）的文件路径，以下是获取方法及示例。

**gameDir**
> 在您的Minecraft游戏目录下（或第三方启动器如PCL、HMCL根目录下），找到`.minecraft`文件夹，并打开`.minecraft/versions`文件夹，
> 即您现在所在的目录中存在字符串".minecraft/versions"，在`versions`文件夹下，若您下载过任意版本的Minecraft，您会在这个文件夹下
> 看到一些文件夹，这些文件夹的名称就是您所下的游戏版本。
> 请直接复制版本文件夹所在的路径（即`(省略号)../.minecraft/versions`），并粘贴至`versionDir`的参数中。

**gameVersions**
> 停留在`versions`文件夹内，假如您下载过Minecraft，此时您会看到一个或一个以上的文件夹，复制您要启动的版本对应的版本文件夹名称，并粘贴到`gameVersions`参数内，需以英文双引号包围，如有多个版本，可以使用英文逗号分离。

**assetsDir**
> 返回至`.minecraft`文件夹，不出意外的话，您会看到一个名为`assets`文件夹（其与`versions`在同一目录下），请直接复制您当前所在的目录路径，
>并粘贴至`tokens.json`的`assetsDir`参数中。

**javaDir**
> 本参数为启动Minecraft所使用的`java.exe`文件所在目录（路径不包含"java.exe"），若您未手动下载过java，可以在第三方启动器（如PCL、HMCL）
> 的设置中找到`java.exe`文件所在的目录，复制它至`tokens.json`的`javaDir`参数中。

不出意外的话，您现在的`tokens.json`内容应该大致为以下内容（`gameVersions`中的版本可能不一样）：
```json
{
    "user": [
        {
            "name": "YIJANG",
            "uuid": "a86efb5f12654efdb5fc94a6ce98d62d",
            "acc_token": "",
            "ref_token": ""
        },
        {
            "name": "<您的第二个账号名>",
            "uuid": "<您的第二个账号名的UUID>",
            "acc_token": "",
            "ref_token": ""
        }
    ],
    "gameVersions": [
        "1.21.1",
        "1.21.10",
        "1.21.1-Fabric 0.16.10",
        "1.2.1",
        "b1.8"
    ],
    "Dirs": {
        "versionDir": "E:/Minecraft/.minecraft/versions",
        "assetsDir": "E:/Minecraft/.minecraft",
        "javaDir": "E:/java22/bin"
    }
}
```

### 启动工具
使用python启动根目录下的`main.py`文件，如果您之前的token留空，工具会请求登录（添加新的账号时，也仅需将所有token留空，会自动请求登录），打开网址并登录相对应的Microsoft账号，之后页面会跳转至一个显示`您不应该访问这个页面`的页面，请快速地查看现在浏览器显示的网址并复制它，它应该大致为以下格式：
```
https://login.live.com/oauth20_desktop.srf?code=......&lc=2052
或
https://login.live.com/oauth20_desktop.srf?code=......
```
请将此时的网址**直接**复制到命令行，不出意外的话，工具会启动Minecraft，并使用您刚刚登录的Microsoft账号登录Minecraft。

### 进阶操作
> 在解压后的`src`文件夹中的`options.json`文件为此工具的配置文件。

以下是其**默认内容**：
```json
{
    "gettoken_thenSaveToken": true,
    "gettoken_thenLaunch": true,
    "gettoken_thenEchotoken": false,
    "launch_thenRefreshToken": false,
    "always_refreshToken": true,
    "launch_thenCleanbat": false
}
```
- 其中，`true`和`false`为各个参数有且仅有的两个参数选项，分别表示“开”和“关”，代表其对应的选项的开关状态。
- 其中，`gettoken_thenSaveToken`参数代表“获取token后保存token”，即任何情况下（包括第一次登录、刷新token等）获取的token是否保存至`tokens.json`文件（覆盖原有token）。
- 其中，`gettoken_thenLaunch`参数代表“获取token后启动Minecraft”，即启动工具后第一次获取token（也许是登录，也许是刷新）后是否启动Minecraft。
- 其中，`gettoken_thenEchotoken`参数代表“获取token后输出token”，即任何情况下（包括第一次登录、刷新token等）获取的token是否输出token。
- 其中，`launch_thenRefreshToken`参数代表“启动Minecraft后是否刷新token”。
- 其中，`always_refreshToken`参数代表“启动工具后是否直接刷新token”。
- 其中，`launch_thenCleanbat`参数代表“启动Minecraft后是否清空`Launch.bat`文件”。
