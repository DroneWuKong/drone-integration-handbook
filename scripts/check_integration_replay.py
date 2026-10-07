#!/usr/bin/env python3
"""Software fixture only: two read-only observers; no network or device writes."""
import json

class Observer:
    def __init__(self):self.sample=None;self.rejected=0
    def accept(self,sample):
        if self.sample and sample['session']==self.sample['session'] and sample['sequence']<=self.sample['sequence']:
            self.rejected+=1;return
        self.sample=dict(sample)
    def state(self,now):
        if not self.sample:return 'unknown'
        age=now-self.sample['received_monotonic']
        return 'future-invalid' if age<0 else 'stale' if age>2 else 'fresh'

def run():
    observers=[Observer(),Observer()]
    fixture=[({'session':'boot-a','sequence':2,'received_monotonic':1.0},1.5,'fresh'),
             ({'session':'boot-a','sequence':1,'received_monotonic':1.2},4.0,'stale'),
             ({'session':'boot-b','sequence':0,'received_monotonic':5.0},5.5,'fresh'),
             ({'session':'boot-b','sequence':1,'received_monotonic':8.0},7.0,'future-invalid')]
    results=[]
    for sample,now,expected in fixture:
        for observer in observers:observer.accept(sample)
        actual=[observer.state(now) for observer in observers]
        assert actual==[expected,expected],(sample,actual,expected)
        results.append({'fixture':sample,'observed_monotonic':now,'states':actual})
    assert [o.rejected for o in observers]==[1,1]
    return {'evidence_category':'software-tested','transport':'local fixture','observers':2,'command_authority':False,'cases':results,'hardware_acceptance':False}
if __name__=='__main__':print(json.dumps(run(),indent=2))
