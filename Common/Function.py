import sys,time
class Function:
    def count_down_exit(self, i = 10):
        print("系统将于" + str(i) + "秒后退出")
        i = int(i)
        # print(type(i))
        j = 0
        while j < i:
            print((i - j))
            j = j + 1
            time.sleep(1)
        sys.exit()
