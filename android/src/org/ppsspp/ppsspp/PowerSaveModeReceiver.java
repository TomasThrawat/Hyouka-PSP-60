package org.ppsspp.ppsspp;

import android.app.Activity;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.database.ContentObserver;
import android.net.Uri;
import android.os.PowerManager;
import android.provider.Settings;
import android.util.Log;

public class PowerSaveModeReceiver extends BroadcastReceiver {
	private static final String TAG = PowerSaveModeReceiver.class.getSimpleName();

	@Override
	public void onReceive(final Context context, final Intent intent) {
		sendPowerSaving(context);
	}

	public PowerSaveModeReceiver(final Activity activity) {
		IntentFilter filter = new IntentFilter();
		filter.addAction(Intent.ACTION_BATTERY_LOW);
		filter.addAction(Intent.ACTION_BATTERY_OKAY);
		filter.addAction(PowerManager.ACTION_POWER_SAVE_MODE_CHANGED);
		activity.registerReceiver(this, filter);

		activity.getContentResolver().registerContentObserver(Settings.System.CONTENT_URI, true, new ContentObserver(null) {
			@Override
			public void onChange(boolean selfChange, Uri uri) {
				super.onChange(selfChange, uri);
				String key = uri.getPath();
				if (key == null) return;
				key = key.substring(key.lastIndexOf("/") + 1);
				if (key.equals("user_powersaver_enable") || key.equals("psm_switch") || key.equals("powersaving_switch")) {
					sendPowerSaving(activity);
				}
			}
		});
		sendPowerSaving(activity);
	}

	public void destroy(final Context context) {
		context.unregisterReceiver(this);
	}

	protected void sendPowerSaving(final Context context) {
		if (!PpssppActivity.libraryLoaded) {
			Log.e(TAG, "Cannot send power saving: Library not loaded");
			return;
		}
		try {
			// Keep PSP emulation out of its internal power-saving/throttling path.
			// Android/device battery saver remains an OS-level control.
			NativeApp.sendMessageFromJava("core_powerSaving", "false");
		} catch (Exception e) {
			Log.e(TAG, "Exception in sendPowerSaving: " + e);
		}
	}
}
