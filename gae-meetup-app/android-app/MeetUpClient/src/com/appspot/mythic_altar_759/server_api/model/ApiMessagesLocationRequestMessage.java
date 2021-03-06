/*
 * Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
 * in compliance with the License. You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software distributed under the License
 * is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
 * or implied. See the License for the specific language governing permissions and limitations under
 * the License.
 */
/*
 * This code was generated by https://code.google.com/p/google-apis-client-generator/
 * (build: 2014-11-17 18:43:33 UTC)
 * on 2014-12-31 at 16:50:48 UTC 
 * Modify at your own risk.
 */

package com.appspot.mythic_altar_759.server_api.model;

/**
 * Model definition for ApiMessagesLocationRequestMessage.
 *
 * <p> This is the Java data model class that specifies how to parse/serialize into the JSON that is
 * transmitted over HTTP when working with the server_api. For a detailed explanation see:
 * <a href="http://code.google.com/p/google-http-java-client/wiki/JSON">http://code.google.com/p/google-http-java-client/wiki/JSON</a>
 * </p>
 *
 * @author Google, Inc.
 */
@SuppressWarnings("javadoc")
public final class ApiMessagesLocationRequestMessage extends com.google.api.client.json.GenericJson {

  /**
   * The value may be {@code null}.
   */
  @com.google.api.client.util.Key("device_id")
  private java.lang.String deviceId;

  /**
   * The value may be {@code null}.
   */
  @com.google.api.client.util.Key
  private java.lang.Double latitude;

  /**
   * The value may be {@code null}.
   */
  @com.google.api.client.util.Key
  private java.lang.Double longitude;

  /**
   * The value may be {@code null}.
   */
  @com.google.api.client.util.Key("user_id")
  private java.lang.String userId;

  /**
   * @return value or {@code null} for none
   */
  public java.lang.String getDeviceId() {
    return deviceId;
  }

  /**
   * @param deviceId deviceId or {@code null} for none
   */
  public ApiMessagesLocationRequestMessage setDeviceId(java.lang.String deviceId) {
    this.deviceId = deviceId;
    return this;
  }

  /**
   * @return value or {@code null} for none
   */
  public java.lang.Double getLatitude() {
    return latitude;
  }

  /**
   * @param latitude latitude or {@code null} for none
   */
  public ApiMessagesLocationRequestMessage setLatitude(java.lang.Double latitude) {
    this.latitude = latitude;
    return this;
  }

  /**
   * @return value or {@code null} for none
   */
  public java.lang.Double getLongitude() {
    return longitude;
  }

  /**
   * @param longitude longitude or {@code null} for none
   */
  public ApiMessagesLocationRequestMessage setLongitude(java.lang.Double longitude) {
    this.longitude = longitude;
    return this;
  }

  /**
   * @return value or {@code null} for none
   */
  public java.lang.String getUserId() {
    return userId;
  }

  /**
   * @param userId userId or {@code null} for none
   */
  public ApiMessagesLocationRequestMessage setUserId(java.lang.String userId) {
    this.userId = userId;
    return this;
  }

  @Override
  public ApiMessagesLocationRequestMessage set(String fieldName, Object value) {
    return (ApiMessagesLocationRequestMessage) super.set(fieldName, value);
  }

  @Override
  public ApiMessagesLocationRequestMessage clone() {
    return (ApiMessagesLocationRequestMessage) super.clone();
  }

}
