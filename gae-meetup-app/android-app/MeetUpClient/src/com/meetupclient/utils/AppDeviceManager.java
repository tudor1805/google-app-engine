package com.meetupclient.utils;

import android.app.Activity;
import android.content.Context;
import android.provider.Settings.Secure;
import android.telephony.TelephonyManager;

public class AppDeviceManager {

	/*
	 * Retrieve the Android Device Id Note that this is not 100% accurate !!!
	 * Source:
	 * http://stackoverflow.com/questions/2785485/is-there-a-unique-android
	 * -device-id
	 */
	public static String getDeviceId(Activity activity) {
		String uuid = Secure.getString(activity.getApplicationContext()
				.getContentResolver(), Secure.ANDROID_ID);
		return uuid;
	}

	/* Retrieve the Telephone Device Id */
	public static String getTelephoneId(Activity activity) {
		TelephonyManager tManager = (TelephonyManager) activity
				.getSystemService(Context.TELEPHONY_SERVICE);
		String uuid = tManager.getDeviceId();
		return uuid;
	}
}
