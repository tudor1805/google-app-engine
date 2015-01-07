package com.meetupclient.utils;

import android.app.Activity;
import android.app.AlertDialog;
import android.widget.Toast;

public class AppUtils {

	public static void showMessage(Activity act, String message) {
		AlertDialog.Builder builder = new AlertDialog.Builder(act);
		builder.setTitle("Information").setMessage(message)
				.setIcon(android.R.drawable.ic_dialog_alert).show();
	}
	
	public static void showDialog(Activity act, String message) {
		Toast.makeText(act.getApplicationContext(), message, Toast.LENGTH_SHORT).show();
	}

}
