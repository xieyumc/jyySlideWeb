# feature🚀
可以尝试访问在线[demo](http://slide.yuyu.pub/public/)，直接编写查看效果👀

![realtime-converter.gif](staticfiles/img/realtime-converter.gif)
> 实时转换：左边输入markdown，右边可以实时看到生成的效果

<br><br>

![auto-save.png](staticfiles/img/auto-save.png)
> 自动保存：编辑幻灯片时每分钟都会自动保存一次，并且在关闭窗口，返回主页时都会自动保存

<br><br>


![auto-title.jpg](staticfiles/img/auto-title.jpg)
> 自动读取标题：幻灯片的标题会自动从文章中读取，由第一个#标题决定

<br><br>


![auto-upload-img.gif](staticfiles/img/auto-upload-img.gif)
> 快捷插入图片：可以直接拖拽或者ctrl+v粘贴图片到编辑器中，图片会自动上传到服务器，生成的链接会自动转换成markdown格式，插入到编辑器中

<br><br>


![img.png](staticfiles/img/public-mode.png)
> 公开分享幻灯片：幻灯片默认需要密码才能访问，也可以设置成公开的来分享，在公开模式下幻灯片是只读的


# 快速安装

## 使用docker安装

在仓库根目录下载：

- [docker-compose.yml](docker-compose.yml)
- [db.sqlite3](db.sqlite3)

然后在本地创建一个`media`文件夹，这个文件夹是存放上传图片用的

此时，你的目录结构应该是这样的：

```
├── docker-compose.yml
├── db.sqlite3
└── media
    └── xxx.img
```

然后运行：

```bash
docker-compose up
```

项目会运行在本地10001端口，并且借助watchtower，会自动更新容器

## 从源码安装

- 下载源码

- 切换到项目根目录

- `pip install -r requirements.txt`

- `daphne -p 10001 jyy_slide_web.asgi:application`

项目会运行在本地10001端口


# 快速上手

## 访问主页和修改密码
安装好项目后，访问`http://localhost:10001/` 即可访问主页

默认账号是`admin`，密码是`admin@django`

若需要修改密码，请访问`http://localhost:10001/admin/` 然后点击右上角的`Change password`

## 编写幻灯片
访问`http://localhost:10001/` ，点击`新建幻灯片`

![index.png](staticfiles/img/index.png)

可以看到我已经写好了两张教程幻灯片，基础语法可以直接配合幻灯片内容进行学习

## 分享幻灯片
每张幻灯片创建时默认都是上锁的（左上角的锁）

![slide-lock.png](staticfiles/img/slide-lock.png)

如果需要分享幻灯片，可以点击左上角锁的按钮，这个幻灯片就会变成公开幻灯片

然后访问`http://localhost:10001/public/` 即可看到所有公开的幻灯片，这个界面不需要密码也可以访问

在这个公开模式下，幻灯片是只读的，

可以被实时编辑预览，但是编辑的内容不会保存到数据库。

同时，上传图片功能也会被禁用（防止服务器被大量图片上传攻击）

![img.png](staticfiles/img/public-mode.png)


# 感谢🙏

本项目的灵感来源为南京大学的[jyy老师](https://jyywiki.cn)

本项目基于[jyyslide-md](https://github.com/zweix123/jyyslide-md)开发，感谢大佬已经把转换逻辑完善了，本人只是做了一些微小的工作
