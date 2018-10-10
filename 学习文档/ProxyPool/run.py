from proxypool.scheduler import Scheduler
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')  # 标准输出流 改成 utf-8编码


def main():
    try:
        s = Scheduler()
        s.run()
    except:
        main()


if __name__ == '__main__':
    main()
