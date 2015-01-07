package com.meetupclient;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import android.util.Log;

import com.appspot.mythic_altar_759.server_api.ServerApi;
import com.appspot.mythic_altar_759.server_api.model.*;
import com.google.android.gms.maps.model.LatLng;
import com.google.api.client.extensions.android.http.AndroidHttp;
import com.google.api.client.json.gson.GsonFactory;

public class AppFacade {

	private ServerApi getService() {
		ServerApi.Builder builder = new ServerApi.Builder(
				AndroidHttp.newCompatibleTransport(), new GsonFactory(), null);
		return builder.build();
	}

	private ApiMessagesSettingsRequestMessage formatSettingsRequest(
			String userId, String deviceId, Long searchRadius, Boolean isVisible) {

		ApiMessagesSettingsRequestMessage msg = new ApiMessagesSettingsRequestMessage();

		msg.setUserId(userId);
		msg.setDeviceId(deviceId);
		msg.setSearchRadius(searchRadius);
		msg.setIsVisible(isVisible);

		return msg;
	}

	private ApiMessagesLocationRequestMessage formatLocationRequest(
			String userId, String deviceId, Double latitude, Double longitude) {
		ApiMessagesLocationRequestMessage msg = new ApiMessagesLocationRequestMessage();

		msg.setUserId(userId);
		msg.setDeviceId(deviceId);
		msg.setLatitude(latitude);
		msg.setLongitude(longitude);

		return msg;
	}

	private ApiMessagesQueryRequestMessage formatQueryRequest(String userId,
			String deviceId, List<String> friends) {
		ApiMessagesQueryRequestMessage msg = new ApiMessagesQueryRequestMessage();

		msg.setUserId(userId);
		msg.setDeviceId(deviceId);
		msg.setUserFriendIds(friends);

		return msg;
	}

	// ==== Public Api ====

	public void updateSettingsAsync(String userId, String deviceId,
			Long searchRadius, Boolean isVisible) {

		final ServerApi service = getService();

		try {
			final ApiMessagesSettingsRequestMessage msg = formatSettingsRequest(
					userId, deviceId, searchRadius, isVisible);

			new Thread(new Runnable() {
				@Override
				public void run() {
					try {
						service.updateSettings(msg).execute();
					} catch (IOException e) {
						e.printStackTrace();
					}
				}
			}).start();

		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	public void updateLocation(String userId, String deviceId, Double latitude,
			Double longitude) {

		ServerApi service = getService();

		try {
			ApiMessagesLocationRequestMessage msg = formatLocationRequest(
					userId, deviceId, latitude, longitude);

			service.updateLocation(msg).execute();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	public Map<String, LatLng> queryNearFriends(String userId, String deviceId,
			ArrayList<String> friends) {
		ServerApi service = getService();

		try {
			Map<String, LatLng> mapNearFriends = new HashMap<>();

			ApiMessagesQueryRequestMessage msg = formatQueryRequest(userId,
					deviceId, friends);

			ApiMessagesQueryResponseMessage response = service
					.queryNearFriends(msg).execute();

			List<ApiMessagesFriendLocation> nearFriends = response
					.getNearFriends();

			if (nearFriends != null) {
				for (ApiMessagesFriendLocation friend : nearFriends) {
					Log.v("blabla", friend.getUserFriendId() + " " + friend.getLatitude() + " " +friend.getLongitude());
					mapNearFriends.put(friend.getUserFriendId(), new LatLng(
							friend.getLatitude(), friend.getLongitude()));
				}
			}

			return mapNearFriends;
		} catch (IOException e) {
			e.printStackTrace();
		}

		return null;
	}

}
