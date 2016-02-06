import rx
from rx import Observable, Observer
import time
import datetime

xs = Observable.from_([1,2,3,4,5,6])
ys = xs.to_blocking()
zs = (x*x for x in ys if x > 3)
for x in zs:
    print(x)


class MyObserver(Observer):
    def on_next(self, x):
        print("Got: %s" % x)
        
    def on_error(self, e):
        print("Got error: %s" % e)
        
    def on_completed(self):
        print("Sequence completed")

xs = Observable.from_iterable(range(10))
d = xs.subscribe(MyObserver())