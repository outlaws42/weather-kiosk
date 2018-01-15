#! /usr/bin/env python3

# -*- coding: utf-8 -*-
import inspect
class Mytest():
    def __init__(self):
        self.test2()
        self.test3()


    def test(self,type):
        source = inspect.stack()[1][3]
        if source == 'test2':
            print(type)
            print('This is called from ', source)
        else:
            print('This is called from ', source)
            print("this is test3")

    def test2(self):
        dog = self.test("I like this test")

    def test3(self):
        dog = self.test("I dont like this test")

if __name__ == '__main__':
    app = Mytest()
