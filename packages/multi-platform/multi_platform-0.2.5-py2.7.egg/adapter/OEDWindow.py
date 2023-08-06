# -*- coding: UTF-8 -*-

import time
from oed_native_lib.OEDWindow import OEDWindow
from adapter.Element import MtControl
from testbase.conf import settings
from testbase import logger
from testbase import TestCase
from testbase.util import ThreadGroupLocal
import testbase
from tuia.exceptions import ControlAmbiguousError


class OEDXWindow(OEDWindow):
    '''
    跨平台 Window类
    '''

    def __init__(self, OEDApp, **kwds):
        OEDWindow.__init__(self, OEDApp, **kwds)

    def updateLocator(self, locators):
        if settings.PLATFORM == "Android" or settings.PLATFORM == "h5":
            super(OEDXWindow, self).update_locator(locators)
        else:
            super(OEDXWindow, self).updateLocator(locators)

    def wait_for_exist(self, timeout=10, interval=0.5):
        if settings.PLATFORM == "h5":
            self.Activity = "com.tencent.mobileqq.activity.QQBrowserActivity"
        try:
            return super(OEDXWindow, self).wait_for_exist(timeout, interval)
        except Exception:
            return False

    def click_screen(self, width_ratio=0.5, height_ratio=0.5):
        self.wait_for_exist(timeout=5, interval=0.5)
        if settings.PLATFORM == "Android":
            screen_width, screen_height = self.device.screen_size  # 获取屏幕宽度、高度
            self.device.run_shell_cmd('input tap %d %d' % (
                screen_width * width_ratio, screen_height * height_ratio))
        if settings.PLATFORM == "iOS":
            self._device.click(x=width_ratio, y=height_ratio)

    def double_click_screen(self, width_ratio=0.5, height_ratio=0.5):
        self.wait_for_exist(timeout=5, interval=0.5)
        if settings.PLATFORM == "Android":
            screen_width, screen_height = self.device.screen_size  # 获取屏幕宽度、高度
            self.device.run_shell_cmd('input tap %d %d' % (
                screen_width * width_ratio, screen_height * height_ratio))
            self.device.run_shell_cmd('input tap %d %d' % (
                screen_width * width_ratio, screen_height * height_ratio))
        if settings.PLATFORM == "iOS":
            self._device.click(x=width_ratio, y=height_ratio)
            self._device.click(x=width_ratio, y=height_ratio)

    def triple_click_screen(self, width_ratio=0.5, height_ratio=0.5):
        self.wait_for_exist(timeout=5, interval=0.5)
        if settings.PLATFORM == "Android":
            screen_width, screen_height = self.device.screen_size  # 获取屏幕宽度、高度
            self.device.run_shell_cmd('input tap %d %d' % (
                screen_width * width_ratio, screen_height * height_ratio))
            self.device.run_shell_cmd('input tap %d %d' % (
                screen_width * width_ratio, screen_height * height_ratio))
            self.device.run_shell_cmd('input tap %d %d' % (
                screen_width * width_ratio, screen_height * height_ratio))
        if settings.PLATFORM == "iOS":
            self._device.click(x=width_ratio, y=height_ratio)
            self._device.click(x=width_ratio, y=height_ratio)
            self._device.click(x=width_ratio, y=height_ratio)

    def touch_skip(self, timeout=30, interval=0.5):
        logger.info("跳过")
        time0 = time.time()
        self.add_control('跳过')
        while time.time() - time0 < timeout:
            if self.Controls['跳过'].wait_for_exist(timeout=5, interval=0.5):
                logger.info("点击跳过")
                self.Controls['跳过'].click()
                return True
            time.sleep(interval)
        logger.info("跳过不存在")

    def touch_skip_select(self, timeout=2, interval=0.5):
        logger.info("跳过选择学院")
        time0 = time.time()
        while time.time() - time0 < timeout:
            if self.Controls['跳过选择学院'].exist():
                logger("点击跳过选择学院")
                self.Controls['跳过选择学院'].click()
                return True
            time.sleep(interval)
        logger.info("选择学院不存在")

    def click_confirm(self, timeout=5, interval=0.5):
        logger.info("点击确认")
        time0 = time.time()
        self.add_control("确认")
        while time.time() - time0 < timeout:
            if self.Controls['确认'].exist():
                self.Controls['确认'].click()
                return True
            time.sleep(interval)
        logger.info("确认不存在")

    def click_cancel(self, timeout=10, interval=0.5):
        """
        点击取消
        """
        time0 = time.time()
        self.add_control("取消")
        while time.time() - time0 < timeout:
            if self.Controls['取消'].exist():
                self.Controls['取消'].click()
                return True
            time.sleep(interval)

    def click_defined_element(self, name, search_page=5):
        """
        在页面查找Métis控件并点击，当前页面找不到就翻到下一页
        需在相应xml中添加对应name(TODO自动更新adapter)
        """
        self.wait_for_exist(timeout=5, interval=2)
        self.Controls[name].wait_for_exist(timeout=5, interval=0.5)
        for _ in range(search_page):
            if self.Controls[name].exist():
                self.Controls[name].click()
                return
            self._app.swipe_pagedown()
        self.Controls[name].show_uitree()
        raise Exception("未找到元素 %s" % name)

    def verify_element_existence(self, name, search_page=1):
        """
        在页面查找Métis控件，默认为当前页，可翻页查找
        """
        self.wait_for_exist(timeout=5, interval=2)
        self.Controls[name].wait_for_exist(timeout=5, interval=0.5)
        for _ in range(search_page):
            if self.Controls[name].exist():
                return True
            self._app.swipe_pagedown()
        return False

    def show_uitree(self):
        '''打印窗口的UI树
        '''
        self.updateLocator({"Mt": {'type': MtControl, 'root': self}})
        self.Controls['Mt'].show_uitree()

    def add_control(self, name):
        '''仅限新增临时control，无需在xml中添加
        '''
        if name not in self._locators.keys():
            self.updateLocator({name: {'type': MtControl, 'root': self}})

    def click_first_of_repeat_control(self, control):
        try:
            self.add_control(control)
            self.click_defined_element(control)
        except ControlAmbiguousError:
            logger.info("重复控件，点击第一个")
            self.updateLocator({control + "-0": {'type': MtControl, 'root': self, 'name': control, 'instance': 0}})
            self.click_defined_element(control + "-0")

    def click_last_of_repeat_control(self, control):
        try:
            self.add_control(control)
            self.click_defined_element(control)
        except ControlAmbiguousError:
            logger.info("重复控件，点击最后一个")
            control_names = self.get_all_control_names()
            logger.info("control_names: %s" % control_names)
            count = control_names.count(control)
            instance_num = "-%d" % (count - 1)
            self.updateLocator(
                {control + instance_num: {'type': MtControl, 'root': self, 'name': control, 'instance': count - 1}})
            self.click_defined_element(control + "-0")

    def click_any_of_repeat_control(self, control, number=0):
        try:
            self.add_control(control)
            self.click_defined_element(control)
        except ControlAmbiguousError:
            logger.info("重复控件，点击第 %d" %number)
            control_names = self.get_all_control_names()
            logger.info("control_names: %s" % control_names)
            instance_num = "-%d" % number
            self.updateLocator(
                {control + instance_num: {'type': MtControl, 'root': self, 'name': control, 'instance': number}})
            self.click_defined_element(control + "-0")

    def swipe_pagedown(self):
        logger.info("翻到下一页")
        self._app.swipe_pagedown()

    def swipe_pageup(self):
        logger.info("翻到上一页")
        self._app.swipe_pageup()

    def swipe_to_visible(self, control, page=5):
        self.add_control(control)
        for _ in range(page):
            if self.Controls[control].exist():
                logger.info("Find %s" % control)
                return
            else:
                self.swipe_pagedown()
        logger.info("Not find %s in %s pages" % (control, page))

    def swipe_screen_oriented(self, x, y, direction, count=1):
        '''沿固定方向滑动屏幕
        :param x， y: 滑动点起点位置（屏幕百分比 0-1）
        :param direction: 滑动方向 (left, right, top, bottom)
        :param count:     次数
        '''
        logger.info("向%s方向滑动" % direction)
        self._app.swipe_screen_oriented(x, y, direction, count=1)

    def get_all_control_names(self):
        self.add_control("controls")
        uitree = self.Controls['controls'].get_uitree()
        control_names = ' | '.join(uitree.keys())
        return control_names

    def get_control_names_in_window(self, x0=0, y0=0, x1=1, y1=1):
        '''获取坐标范围内的控件
        x0, y0 左上坐标
        x1, y1 右下坐标
        '''
        self.add_control("controls")
        width, height = self.device.screen_size
        px0, py0 = x0 * width, y0 * height
        px1, py1 = x1 * width, y1 * height
        control_names = []
        uitree = self.Controls['controls'].get_uitree()
        for name, rect in uitree.items():
            if px0 < rect['Left'] + 0.5 * rect['Width'] < px1 and \
                    py0 < rect['Top'] + 0.5 * rect['Height'] < py1:
                control_names.append(name)
        return control_names

    def get_control_name_by_partial(self, partial, option):
        self.add_control('controls')
        uitree = self.Controls['controls'].get_uitree()
        for name in uitree.keys():
            if option == 'startswith':
                if name.startswith(partial):
                    return name
            elif option == 'endswith':
                if name.endswith(partial):
                    return name
            else:
                if partial in name:
                    return name
        logger.info("当前页面没有包含 %s 的控件" % partial)
        logger.info("All controls: %s" % (self.get_all_control_names()))

    def take_screen_shot(self, info="获取当前页面截图"):
        testcase = ThreadGroupLocal().testcase
        testcase.take_screen_shot(self._app, info)
