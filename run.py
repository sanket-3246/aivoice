import multiprocessing
import subprocess



def startJarvis():
        # Code for process 1
        print("Process 1 is running.")
        from main import start
        start()
    

def listenHotword():
        # Code for process 2j
        print("Process 2 is running.")
        from engine.features import hotword
        hotword()
if __name__ == '__main__':
        p1 = multiprocessing.Process(target=startJarvis)
        p2 = multiprocessing.Process(target=listenHotword)
        p1.start()
        import os

        batch_file = os.path.join(os.path.dirname(__file__), "device.bat")
        subprocess.call(batch_file, shell=True)

        p2.start()
        p1.join()

        if p2.is_alive():
            p2.terminate()
            p2.join()

        print("system stop")  