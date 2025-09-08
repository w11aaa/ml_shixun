import importlib


def excutefun(modulename, functionname, parammap):
    try:
        className = modulename.split('.')[-1]

        className = className[0].upper() + className[1:]

        # 动态导入模块
        try:
            module = importlib.import_module(modulename)
        except ImportError:
            raise ImportError(f"Module '{modulename}' not found")

        # 获取类对象
        try:
            classObj = getattr(module, className)
        except AttributeError:
            raise AttributeError(f"Class '{className}' not found in module '{modulename}'")

        # 获取方法
        try:
            method = getattr(classObj, functionname)
        except AttributeError:
            raise AttributeError(f"Function '{functionname}' not found in class '{className}'")

        # 调用函数
        try:
            return method(parammap)
        except Exception as e:
            raise RuntimeError(f"Error executing {functionname}: {str(e)}")

    except Exception as e:
        print(f"Error: {str(e)}")
        raise  # 重新抛出异常供上层处理
        return str(e)


def excutefun2(modulename, functionname, parammap):
    className = modulename.split('.')[-1]
    # 动态地导入模块
    module = importlib.import_module(modulename)
    # 方法1：使用split()分割
    classObj = getattr(module, className)

    method = getattr(classObj, functionname)

    if method is None:
        raise AttributeError(f"Module '{modulename}' has no function '{functionname}'")
    # 调用函数，并传递参数
    result = method(parammap)
    return result


# 调用函数
"""
result = excutefun("com.module1", "fun1", "AAA","BBB")

print(result)
"""
