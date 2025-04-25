civitai提供的models api不适合去浏览模型，因为是基于cursor检索数据，你只能根据给定的next cursor和对应的url进行前后页面跳转。

可是这样的话为何我不去使用civitai官网去浏览模型文件呢？这样更有效率啊。

如果我想下载什么模型我可以通过一个web插件实现这样的功能，比如一键添加下载任务什么的。

这是个非常好的主意。

![[Screenshot 2025-03-15 003235.png]]

下载按钮是一个< a >元素，而且下载按钮的xpath都是一致的：

```html
/html/body/div[1]/div/div/div/div/div/main/div[2]/div/div[3]/div[1]/div/div[1]/div[1]/div[1]/a
```

只需要定位这个按钮的位置，然后获取其api link地址就可以了。

![[Pasted image 20250315005420.png]]

但是要注意：如果有些处于Early Access的模型没有用buzz买下的话是不会显示链接的，不过就算有链接也无法正常下载，服务器会查询用户账户是否已经购买某个model。

![[Pasted image 20250315005557.png]]

