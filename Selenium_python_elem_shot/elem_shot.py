# encoding=utf-8

from selenium import webdriver
from PIL import Image
import time

wd = webdriver.Chrome()
wd.get("https://developer.mozilla.org/zh-CN/")
wd.maximize_window()

'''
我分别在页面的上中下取了三个元素用于验证
'''
shot_items = ("登录", "MDN Web 文档", "推广 MDN")

for index, item in enumerate(shot_items, start=1):
    elem = wd.find_element_by_link_text(item)
    '''
    print(elem.is_displayed())
    print(elem.rect)
    print(elem.location_once_scrolled_into_view)
    '''

    '''
    我对 location_once_scrolled_into_view 的理解：
    只要可以展示元素全部（暂不讨论宽高超过可视范围的情况），那么滚动最小距离
    使其贴边，如果在最后一屏，很有可能x, y值大于0
    如果 top = 0 说明可以滚动最小距离，贴到边缘。
    如果 top > 0 那么说明要滚动整个页面的高度。
    '''
    
    left = elem.location_once_scrolled_into_view['x']
    top = elem.location_once_scrolled_into_view['y']
    right = elem.size['width'] + left
    height = elem.size['height'] + top
    
    '''
    elem.rect 返回的是元素在页面中的位置
    '''
    
    js = "document.documentElement.scrollTop={}".format(elem.rect['y'])
    wd.execute_script(js)
    time.sleep(2)
    
    wd.save_screenshot(r'./{}.png'.format(index))
    
    im = Image.open(r'./{}.png'.format(index))
    im2 = im.crop((left, top, right, height))
    im2.save(r'./cropped_{}.png'.format(index))

wd.close()
wd.quit()
