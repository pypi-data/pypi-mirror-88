## fasttest_selenium
### Demo
https://github.com/Jodeee/fasttestSeleniumDemo

- 浏览器相关Action
```
module: selenium
skip: false
description: 浏览器相关操作
steps:
  # 打开URL
  - openUrl('https://www.baidu.com')
  # 获取浏览器名字
  - ${getName} = $.getName()
  # 窗口最大化
  - maxWindow()
  # 窗口最小化
  - minWindow()
  # 全屏窗口
  - fullscreenWindow()
  # 设置窗口大小
  - setWindowSize(2000,1500)
  # 设置窗口位置
  - setWindowPosition(10,30)
  # 获取窗口大小
  - ${w_size} = $.getWindowSize()
  # 获取窗口位置
  - ${w_position} = $.getWindowPosition()
  
  - click('xpath=//*[@id="s-top-left"]/a[1]')
  # 获取当前窗口句柄
  - ${handle} = $.getCurrentWindowHandle()
  # 获取所有窗口句柄
  - ${all_handle} = $.getWindowHandles()
  - for ${handle} in ${all_handle}:
      # 切换窗口句柄
      - switchToWindow(${handle})
      - ${title} = $.getTitle()
      - if ${title} == '百度新闻——海量中文资讯平台':
          - break

  # 获取当前窗口标题
  - ${title} = $.getTitle()
  # 获取当前窗口url
  - ${current_url} = $.getCurrentUrl()

  - click('xpath=//*[@id="channel-all"]/div/ul/li[2]')
  - click('xpath=//*[@id="channel-all"]/div/ul/li[3]')
  # 后退
  - back()
  # 前进
  - forward()
  # 刷新
  - refresh()
```
- 键盘鼠标相关Action
```
module: selenium
skip: false
description: action相关
steps:
  - openUrl('https://www.baidu.com')
  # 检查元素
  - check('id=su')
  # 单击元素
  - click('id=su')
  # 右击元素
  - contextClick('id=su')
  # 双击元素
  - doubleClick('class=hot-refresh-text')
  # 按住鼠标左键
  - holdClick('class=hot-refresh-text')

  # 鼠标拖放
  - click('xpath=//*[@id="s-top-left"]/a[1]')
  - ${all_handle} = $.getWindowHandles()
  - switchToWindow(${all_handle}[-1])
  - dragDrop('xpath=//*[@id="sbox"]/tbody/tr/td[1]/div[1]/a/img','id=s_btn_wr')
   # 拖动元素到某个位置
  - dragDropByOffset('xpath=//*[@id="sbox"]/tbody/tr/td[1]/div[1]/a/img',10,10)
  - switchToWindow(${all_handle}[0])
  # 鼠标从当前位置移动到某个坐标
  - moveByOffset(10,10)
  # 鼠标移动到某个元素上
  - moveToElement('xpath=//*[@id="hotsearch-content-wrapper"]/li[1]/a/span[2]')
  # 移动到距某个元素(左上角坐标)多少距离的位置
  - moveToElementWithOffset('xpath=//*[@id="hotsearch-content-wrapper"]/li[1]/a/span[2]',10,20)
  # 输入
  - sendKeys('name=wd','te')
  - sendKeys('name=wd','Keys.COMMAND', 'v')
  # 清除
  - clear('name=wd')
  # 截图
  - ${screenshot} = $.saveScreenshot('id=su', 'test.png')
  # 执行JS
  - ${js} = "window.open('http://www.taobao.com')"
  - executeScript(${js})
```
- cookies相关Action
```
module: selenium
skip: false
description: cookies相关
steps:
  - openUrl('https://www.baidu.com')
  # 获取所有cookies
  - ${cookies} = $.getCookies()
  # 获取指定cookie
  - ${cookie} = $.getCookie('BAIDUID')
  # 删除指定cookie
  - deleteCookie('BAIDUID')
  # 删除所有cookie
  - deleteAllCookies()
  # 添加指定cookie
  - ${add_cookie} = {'name':'ADDCOOKIE','value':'123adc'}
  - addCookie(${add_cookie})
  - ${cookies} = $.getCookies()

```
- 元素相关Action
```
module: selenium
skip: false
description: 元素相关操作
steps:
  - openUrl('https://www.baidu.com')
  # 获取单个元素 id|name|class|tag_name|link_text|partial_link_text|xpath|css_selector
  - ${element_id} = $.getElement('id=su')
  - ${element_name} = $.getElement('name=f')
  - ${element_class} = $.getElement('class=s_ipt')
  - ${element_tag_name} = $.getElement('tag_name=form')
  - ${element_link_text} = $.getElement('link_text=新闻')
  - ${element_partial_link_text} = $.getElement('partial_link_text=新')
  - ${element_xpath} = $.getElement('xpath=//*[@id="su"]')
  - ${element_css_selector} = $.getElement('css_selector=[name="wd"]')

   # 获取一组元素
  - ${elements_class} = $.getElements('class=title-content-title')

  # 判断元素是否选中
  - ${is_selected} = $.isSelected(${element_id})
  # 判断元素是否显示
  - ${is_displayed} = $.isDisplayed(${element_id})
  # 判断元素是否可使用
  - ${is_enabled} = $.isEnabled(${element_id})

  # 获取元素大小
  - ${size} = $.getSize(${element_id})
  # 获取元素坐标
  - ${location} = $.getLocation(${element_id})
  # 获取元素位置大小
  - ${rect} = $.getRect(${element_id})

  # 获取元素tag
  - ${tag_name} = $.getTagName(${element_id})
  # 获取元素文案
  - ${text} = $.getText(${element_id})
  # 获取元素属性
  - ${attribute} = $.getAttribute(${element_id}, 'value')
  # 获取元素css
  - ${css} = $.getCssProperty(${element_id}, 'height')
```
- 通用Action
```
module: common
skip: false
description: 公共关键字
steps:
  # 科学运算
  - ${test1} = $.id(1+2*3)
  - ${test2} = $.id('test'+' '+'common')
  # 设置全局变量
  - setVar('test3', True)
  # 获取全局变量
  - ${test3} = $.getVar('test3')
  # 休眠
  - sleep(5)

  - openUrl('https://www.baidu.com')
  - ${elements} = $.getElements('class=title-content-title')
  # 获取数组长度
  - ${len} = $.getLen(${elements})
  # while 循环
  - while ${len}:
      - ${len} = $.id(${len}-1)
      - ${element} = ${elements}[${len}]
      - ${text} = $.getText(${element})
      - if ${len} == 3:
          - assert ${len} == 3
        elif ${text} == '美国将对更多中国公民实施签证限制':
          - break
        else:
          - sleep(1)
  # for 循环
  - click('xpath=//*[@id="s-top-left"]/a[1]')
  - ${all_handle} = $.getWindowHandles()
  - for ${handle} in ${all_handle}:
      - switchToWindow(${handle})
      - ${title} = $.getTitle()
      - if ${title} == '百度新闻——海量中文资讯平台':
          - break

  # call 公共方法
  - call common_action(${elements}[0])

  # 用脚本无返回值-调用selenium api完成复杂动作
  - keyDown(${elements}[0], '这是一条测试数据')
  - sendKeys('name=wd','Keys.COMMAND', 'v')

  # 调用脚本有返回值
  - ${text} = getText('这是一条测试数据')

```
### 已完成功能
- selenium 90%的Action支持
- 可拓展的公共方法和公共函数
- 高度还原steps的报告输出
### 待完成功能
- 数据类型优化：支持自定义复杂数据结构
- 启动项优化：支持其他浏览器以及启动参数配置
- 结果报告优化：支持图片放大
