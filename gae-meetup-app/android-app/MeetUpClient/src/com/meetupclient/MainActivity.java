package com.meetupclient;

import java.util.*;

import com.google.android.gms.common.ConnectionResult;
import com.google.android.gms.common.GooglePlayServicesUtil;
import com.google.android.gms.common.api.*;
import com.google.android.gms.common.api.GoogleApiClient.*;
import com.google.android.gms.maps.*;
import com.google.android.gms.maps.model.*;
import com.google.android.gms.plus.*;
import com.google.android.gms.plus.People.LoadPeopleResult;
import com.google.android.gms.plus.model.people.*;
import com.meetupclient.utils.AppDeviceManager;
import com.meetupclient.utils.AppLocation;
import com.meetupclient.utils.AppUtils;
import com.meetupclient.utils.GenericAppTimer;

import android.app.*;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.IntentSender.SendIntentException;

import android.location.Location;
import android.location.LocationManager;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.support.v4.app.FragmentActivity;
import android.util.Log;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.*;

public class MainActivity extends FragmentActivity implements
		ConnectionCallbacks, OnConnectionFailedListener,
		ResultCallback<People.LoadPeopleResult> {

	// Tag under which we are going to log messages
	private static final String TAG = "android-meetup";

	private AppFacade appFacade = new AppFacade();
	private AppLocation appLocation = new AppLocation(this);
	private GenericAppTimer appLocTimer = null;
	private GenericAppTimer appQueryTimer = null;
	private Activity thisActivity = this;

	private MapFragment mapFragment;
	private TextView mStatusTextfield;

	/* ============== GooglePlus API =============== */

	public String connectionStatus = "Signed Out";

	/**
	 * A flag indicating that a PendingIntent is in progress and prevents us
	 * from starting further intents.
	 */
	private boolean mIntentInProgress;
	public boolean mResolveOnFail = true;
	private boolean mSignInClicked;
	private ConnectionResult mConnectionResult;
	private static final int RC_SIGN_IN = 0;

	// GoogleApiClient wraps our service connection to Google Play services and
	// provides access to the users sign in state and Google's APIs.
	private GoogleApiClient mGoogleApiClient;
	private ArrayList<String> mCirclesList = new ArrayList<>();
	private ArrayList<String> mTestCirclesList = new ArrayList<>();
	private Map<String, String> mFriendsMap = new HashMap<>();
	private Person currentUser;

	private void showGPSDisabledAlertToUser() {
		AlertDialog.Builder alertDialogBuilder = new AlertDialog.Builder(this);
		alertDialogBuilder
				.setMessage(
						"GPS is disabled in your device. Would you like to enable it?")
				.setCancelable(false)
				.setPositiveButton("Goto Settings Page To Enable GPS",
						new DialogInterface.OnClickListener() {
							public void onClick(DialogInterface dialog, int id) {
								Intent callGPSSettingIntent = new Intent(
										android.provider.Settings.ACTION_LOCATION_SOURCE_SETTINGS);
								startActivity(callGPSSettingIntent);
							}
						});
		alertDialogBuilder.setNegativeButton("Cancel",
				new DialogInterface.OnClickListener() {
					public void onClick(DialogInterface dialog, int id) {
						dialog.cancel();
					}
				});
		AlertDialog alert = alertDialogBuilder.create();
		alert.show();
	}

	private void checkIfGpsEnabled() {
		LocationManager locationManager = (LocationManager) getSystemService(LOCATION_SERVICE);

		if (locationManager.isProviderEnabled(LocationManager.GPS_PROVIDER)) {
			Toast.makeText(this, "GPS is Enabled in your devide",
					Toast.LENGTH_SHORT).show();
		} else {
			showGPSDisabledAlertToUser();
		}
	}

	/*
	 * private void showNetworkDisabledAlertToUser() { AlertDialog.Builder
	 * alertDialogBuilder = new AlertDialog.Builder(this);
	 * alertDialogBuilder.setMessage(
	 * "Network access is disabled in your device. Disabling app")
	 * .setCancelable(false); AlertDialog alert = alertDialogBuilder.create();
	 * alert.show(); }
	 */

	private void hideApp() {
		Intent intent = new Intent(Intent.ACTION_MAIN);
		intent.addCategory(Intent.CATEGORY_HOME);
		intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
		startActivity(intent);
	}

	private void checkIfNetworkIsEnabled() {
		ConnectivityManager connectivityManager = (ConnectivityManager) getSystemService(Context.CONNECTIVITY_SERVICE);
		NetworkInfo activeNetworkInfo = connectivityManager
				.getActiveNetworkInfo();

		if (activeNetworkInfo == null || !activeNetworkInfo.isConnected()) {
			// showNetworkDisabledAlertToUser();
			hideApp();
		}
	}

	private void initializeMenuBar() {
		/*
		 * Source:
		 * http://stackoverflow.com/questions/16141824/two-spinner-menu-items
		 * -in-actionbar-width
		 */
		ArrayAdapter<CharSequence> adapter = ArrayAdapter.createFromResource(
				this, R.array.discovery_radius_array,
				android.R.layout.simple_spinner_item);

		final ActionBar actionBar = getActionBar();
		actionBar.setCustomView(R.layout.actionbar_item);
		actionBar.setDisplayShowTitleEnabled(false);
		actionBar.setDisplayShowCustomEnabled(true);
		actionBar.setDisplayUseLogoEnabled(false);
		actionBar.setDisplayShowHomeEnabled(false);

		Spinner discoveryRadiusSpinner = (Spinner) findViewById(R.id.spinner_discoveryRadius);
		discoveryRadiusSpinner.setAdapter(adapter);

		discoveryRadiusSpinner
				.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
					public void onItemSelected(AdapterView<?> adapterView,
							View view, int i, long l) {
						syncAppSettings();
					}

					public void onNothingSelected(AdapterView<?> adapterView) {
						return;
					}
				});

		CheckBox visibleCheckBox = (CheckBox) findViewById(R.id.checkbox_visibility);
		visibleCheckBox.setOnClickListener(new OnClickListener() {
			@Override
			public void onClick(View v) {
				syncAppSettings();
				AppUtils.showDialog(thisActivity, "Conn Status: "
						+ connectionStatus);
			}
		});
	}

	private void syncAppSettings() {
		final CheckBox visibleCheckBox = (CheckBox) findViewById(R.id.checkbox_visibility);
		final Spinner discoveryRadiusSpinner = (Spinner) findViewById(R.id.spinner_discoveryRadius);
		try {
			boolean isVisible = visibleCheckBox.isChecked();
			String radiusText = discoveryRadiusSpinner.getSelectedItem()
					.toString();
			long selectedRadius = Long.parseLong(radiusText.split(" ")[0]);

			if (currentUser == null) {
				// Error
				return;
			}
			appFacade.updateSettingsAsync(currentUser.getId(),
					AppDeviceManager.getDeviceId(thisActivity), selectedRadius,
					isVisible);

			// AppUtils.showDialog(this, "Visible: " + isVisible + " Radius: "
			// + selectedRadius);
		} catch (Exception ex) {
			ex.printStackTrace();
		}
	}

	private void updateLocation() {
		final Location currentLocation = appLocation.getLocation();

		if (currentLocation != null) {
			// Map needs to be updated from main thread
			Handler handler = new Handler(Looper.getMainLooper());
			handler.post(new Runnable() {

				@Override
				public void run() {
					CameraUpdate center = CameraUpdateFactory
							.newLatLng(new LatLng(
									currentLocation.getLatitude(),
									currentLocation.getLongitude()));
					CameraUpdate zoom = CameraUpdateFactory
							.zoomTo(AppConfig.MAP_ZOOM);

					mapFragment.getMap().moveCamera(center);
					mapFragment.getMap().animateCamera(zoom);

					mapFragment.getMap().clear();
					mapFragment.getMap().addMarker(
							new MarkerOptions()
									.position(
											new LatLng(currentLocation
													.getLatitude(),
													currentLocation
															.getLongitude()))
									.title("Me")
									.icon(BitmapDescriptorFactory
											.defaultMarker(100)));
				}
			});

			if (currentUser != null) {
				appFacade.updateLocation(currentUser.getId(),
						AppDeviceManager.getDeviceId(thisActivity),
						currentLocation.getLatitude(),
						currentLocation.getLongitude());
			}
		}
	}

	private void queryNearFriends() {
		if (currentUser == null)
			return;

		Map<String, LatLng> mapNearFriends = appFacade.queryNearFriends(
				currentUser.getId(),
				AppDeviceManager.getDeviceId(thisActivity), mTestCirclesList);
		// mCirclesList);

		if (mapNearFriends != null) {
			for (String friend_id : mapNearFriends.keySet()) {
				String friend_nickname = mFriendsMap.get(friend_id);
				if (friend_nickname == null) {
					friend_nickname = friend_id;
				}
				final String friendDisplayName = friend_nickname;
				final LatLng position = mapNearFriends.get(friend_id);

				Handler handler = new Handler(Looper.getMainLooper());
				handler.post(new Runnable() {

					@Override
					public void run() {
						mapFragment.getMap().addMarker(
								new MarkerOptions()
										.position(
												new LatLng(position.latitude,
														position.longitude))
										.title(friendDisplayName)
										.icon(BitmapDescriptorFactory
												.defaultMarker(50)));
					}
				});
			}
		}

	}

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);

		initializeMenuBar();

		mGoogleApiClient = new GoogleApiClient.Builder(thisActivity)
				.addConnectionCallbacks(this)
				.addOnConnectionFailedListener(this)
				.addApi(Plus.API, Plus.PlusOptions.builder().build())
				.addScope(Plus.SCOPE_PLUS_LOGIN).build();

		mapFragment = (MapFragment) getFragmentManager().findFragmentById(
				R.id.map);

		mStatusTextfield = (TextView) findViewById(R.id.textView_status);

		mTestCirclesList.add("test_user1");
		mTestCirclesList.add("test_user2");
		mTestCirclesList.add("test_user3");
		mTestCirclesList.add("test_user4");
		mTestCirclesList.add("test_user5");
		mTestCirclesList.add("test_user6");
		mTestCirclesList.add("test_user7");
		mTestCirclesList.add("test_user8");
		mTestCirclesList.add("test_user9");
		mTestCirclesList.add("test_user10");
		mTestCirclesList.add("test_user11");
		mTestCirclesList.add("test_user12");
		mTestCirclesList.add("test_user13");
	}

	@Override
	public void onDestroy() {
		super.onDestroy();
		mGoogleApiClient = null;

	}

	protected void onPause() {
		super.onPause();
	}

	protected void onResume() {
		super.onPause();
	}

	protected void onStart() {
		super.onStart();

		checkIfGpsEnabled();
		checkIfNetworkIsEnabled();

		appLocation.initialize();

		appLocTimer = new GenericAppTimer(new TimerTask() {
			@Override
			public void run() {
				updateLocation();
			}
		}, AppConfig.LOCATION_UPDATE_INTERVAL);

		appQueryTimer = new GenericAppTimer(new TimerTask() {
			@Override
			public void run() {
				queryNearFriends();
			}
		}, AppConfig.LOCATION_QUERY_INTERVAL);

		if (!mGoogleApiClient.isConnected()) {
			mGoogleApiClient.connect();
		}

		mGoogleApiClient.connect();
		mSignInClicked = true;
		signInWithGplus();
		syncAppSettings();
	}

	protected void onStop() {
		super.onStop();
		if (mGoogleApiClient != null && mGoogleApiClient.isConnected()) {
			Plus.AccountApi.clearDefaultAccount(mGoogleApiClient);
			mGoogleApiClient.disconnect();
		}

		connectionStatus = getResources().getString(R.string.status_signed_out);
		mStatusTextfield.setText(connectionStatus);

		if (appQueryTimer != null)
			appQueryTimer.stop();

		if (appLocTimer != null)
			appLocTimer.stop();

		if (appLocation != null)
			appLocation.cleanup();
	}

	/**
	 * onConnected is called when our Activity successfully connects to Google
	 * Play services. onConnected indicates that an account was selected on the
	 * device, that the selected account has granted any requested permissions
	 * to our app and that we were able to establish a service connection to
	 * Google Play services.
	 */
	@Override
	public void onConnected(Bundle connectionHint) {
		// Reaching onConnected means we consider the user signed in.
		currentUser = Plus.PeopleApi.getCurrentPerson(mGoogleApiClient);
		connectionStatus = getResources().getString(R.string.signed_in_as,
				currentUser.getDisplayName());
		mStatusTextfield.setText(connectionStatus);

		// Retrieve a list with the user's friends
		Plus.PeopleApi.loadVisible(mGoogleApiClient, null).setResultCallback(
				this);
	}

	@Override
	public void onConnectionSuspended(int cause) {
		/*
		 * The connection to Google Play services was lost for some reason. We
		 * call connect() to attempt to re-establish the connection or get a
		 * ConnectionResult that we can attempt to resolve.
		 */
		mGoogleApiClient.connect();
	}

	@Override
	protected void onActivityResult(int requestCode, int responseCode,
			Intent data) {
		if (requestCode == RC_SIGN_IN) {
			if (responseCode != RESULT_OK) {
				mSignInClicked = false;
			}

			mIntentInProgress = false;

			if (!mGoogleApiClient.isConnecting()) {
				mGoogleApiClient.connect();
			}
		}
	}

	/**
	 * Sign-in into google
	 * */
	private void signInWithGplus() {
		if (!mGoogleApiClient.isConnecting()) {
			mSignInClicked = true;
			resolveSignInError();
		}
	}

	/**
	 * onConnectionFailed is called when our Activity could not connect to
	 * Google Play services. onConnectionFailed indicates that the user needs to
	 * select an account, grant permissions or resolve an error in order to sign
	 * in.
	 */
	@Override
	public void onConnectionFailed(ConnectionResult result) {
		if (!result.hasResolution()) {
			GooglePlayServicesUtil.getErrorDialog(result.getErrorCode(), this,
					0).show();
			return;
		}

		if (!mIntentInProgress) {
			// Store the ConnectionResult for later usage
			mConnectionResult = result;

			if (mSignInClicked) {
				/*
				 * The user has already clicked 'sign-in' so we attempt to
				 * resolve all errors until the user is signed in, or they
				 * cancel.
				 */
				resolveSignInError();
			}
		}
	}

	/**
	 * Method to resolve any signin errors
	 * */
	private void resolveSignInError() {
		if (mConnectionResult.hasResolution()) {
			try {
				mIntentInProgress = true;
				mConnectionResult.startResolutionForResult(thisActivity,
						RC_SIGN_IN);
			} catch (SendIntentException e) {
				mIntentInProgress = false;
				mGoogleApiClient.connect();
			}
		}
	}

	@Override
	public void onResult(LoadPeopleResult peopleData) {
		if (peopleData.getStatus().getStatusCode() == CommonStatusCodes.SUCCESS) {
			mCirclesList.clear();
			PersonBuffer personBuffer = peopleData.getPersonBuffer();
			try {
				int count = personBuffer.getCount();
				for (int i = 0; i < count; i++) {
					mFriendsMap.put(personBuffer.get(i).getId(), personBuffer
							.get(i).getDisplayName());
					mCirclesList.add(personBuffer.get(i).getId());
				}
			} finally {
				personBuffer.close();
			}

		} else {
			Log.e(TAG,
					"Error requesting visible circles: "
							+ peopleData.getStatus());
		}

		// AppUtils.showDialog(this, "Friends: " + mCirclesList + "");
	}
}
