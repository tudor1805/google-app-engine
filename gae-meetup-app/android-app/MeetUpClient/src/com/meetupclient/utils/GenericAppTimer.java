package com.meetupclient.utils;

import java.util.*;

public class GenericAppTimer {
	private final Timer timer;

	public GenericAppTimer(TimerTask callback, int secInterval) {
		this.timer = new Timer();
		int msInterval = secInterval * 1000;
		timer.schedule(callback, msInterval, msInterval);
	}

	public void stop() {
		timer.cancel();
	}
}