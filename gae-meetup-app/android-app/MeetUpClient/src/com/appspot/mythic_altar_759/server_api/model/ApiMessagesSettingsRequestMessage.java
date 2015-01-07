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
 * Model definition for ApiMessagesSettingsRequestMessage.
 *
 * <p> This is the Java data model class that specifies how to parse/serialize into the JSON that is
 * transmitted over HTTP when working with the server_api. For a detailed explanation see:
 * <a href="http://code.google.com/p/google-http-java-client/wiki/JSON">http://code.google.com/p/google-http-java-client/wiki/JSON</a>
 * </p>
 *
 * @author Google, Inc.
 */
@SuppressWarnings("javadoc")
public final class ApiMessagesSettingsRequestMessage extends com.google.api.client.json.GenericJson {

  /**
   * The value may be {@code null}.
   */
  @com.google.api.client.util.Key("device_id")
  private java.lang.String deviceId;

  /**
   * The value may be {@code null}.
   */
  @com.google.api.client.util.Key("is_visible")
  private java.lang.Boolean isVisible;

  /**
   * The value may be {@code null}.
   */
  @com.google.api.client.util.Key("search_radius") @com.google.api.client.json.JsonString
  private java.lang.Long searchRadius;

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
  public ApiMessagesSettingsRequestMessage setDeviceId(java.lang.String deviceId) {
    this.deviceId = deviceId;
    return this;
  }

  /**
   * @return value or {@code null} for none
   */
  public java.lang.Boolean getIsVisible() {
    return isVisible;
  }

  /**
   * @param isVisible isVisible or {@code null} for none
   */
  public ApiMessagesSettingsRequestMessage setIsVisible(java.lang.Boolean isVisible) {
    this.isVisible = isVisible;
    return this;
  }

  /**
   * @return value or {@code null} for none
   */
  public java.lang.Long getSearchRadius() {
    return searchRadius;
  }

  /**
   * @param searchRadius searchRadius or {@code null} for none
   */
  public ApiMessagesSettingsRequestMessage setSearchRadius(java.lang.Long searchRadius) {
    this.searchRadius = searchRadius;
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
  public ApiMessagesSettingsRequestMessage setUserId(java.lang.String userId) {
    this.userId = userId;
    return this;
  }

  @Override
  public ApiMessagesSettingsRequestMessage set(String fieldName, Object value) {
    return (ApiMessagesSettingsRequestMessage) super.set(fieldName, value);
  }

  @Override
  public ApiMessagesSettingsRequestMessage clone() {
    return (ApiMessagesSettingsRequestMessage) super.clone();
  }

}
