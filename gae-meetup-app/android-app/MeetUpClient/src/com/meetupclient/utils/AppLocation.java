package com.meetupclient.utils;

import android.app.Activity;
import android.content.Context;
import android.location.*;
import android.os.Bundle;

public class AppLocation {
	private LocationManager locationManager;
	private LocationListener locationListener;

	private Activity parentActivity;
	private Location lastLocation;

	public AppLocation(Activity parentActivity) {
		this.parentActivity = parentActivity;
	}

	public Location getLocation() {
		return lastLocation;
	}

	public void initialize() {
		// Acquire a reference to the system Location Manager
		locationManager = (LocationManager) parentActivity
				.getSystemService(Context.LOCATION_SERVICE);

		// Define a listener that responds to location updates
		locationListener = new LocationListener() {
			public void onLocationChanged(Location location) {
				lastLocation = location;
				AppUtils.showDialog(
						parentActivity,
						"Location: " + location.getLatitude() + " "
								+ location.getLongitude());
			}

			public void onStatusChanged(String provider, int status,
					Bundle extras) {
			}

			public void onProviderEnabled(String provider) {
			}

			public void onProviderDisabled(String provider) {
			}
		};

		/*
		 * Register the listener with the Location Manager to receive location
		 * updates
		 */
		locationManager.requestLocationUpdates(
				LocationManager.NETWORK_PROVIDER, (long) 0, 0.0f,
				locationListener);
	}

	public void cleanup() {
		if (locationListener != null && locationManager != null) {
			locationManager.removeUpdates(locationListener);	
		}		
		locationListener = null;
		lastLocation = null;
	}

}
