class reflect:
    #反射调用函数，传入param是list
    def reflect(self,module,function,param):
        dd = __import__(module, fromlist=True)
        tager_func = getattr(dd, function)
        if (len(param) > 0):
            result = tager_func(*param)#使用*list将list转为可传递参数
        else:
            result = tager_func()
        return  result
