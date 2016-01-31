import rx
from rx import Observable, Observer
class MyObserver(Observer):
    def on_next(self, x):
        print("Got: %s" % x)
        
    def on_error(self, e):
        print("Got error: %s" % e)
        
    def on_completed(self):
        print("Sequence completed")

xs = Observable.from_iterable(range(10))
d = xs.subscribe(MyObserver())
