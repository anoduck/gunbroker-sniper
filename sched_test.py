#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sched
import time

scheduler = sched.scheduler(time.time, time.sleep)


def test(sec):
    scheduler.enterabs(sec, 1, print('Timer Stopped'))

sec = time.time
    
