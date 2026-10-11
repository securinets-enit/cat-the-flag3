package enit.ironlocker;

import android.webkit.JavascriptInterface;

public final class LockerBridge {
    static {
        System.loadLibrary("ironlocker");
    }

    @JavascriptInterface
    public long create(String text) {
        return nativeCreate(text.getBytes());
    }

    @JavascriptInterface
    public long createBytes(byte[] bytes) {
        return nativeCreate(bytes);
    }

    @JavascriptInterface
    public void remove(long handle) {
        nativeRemove(handle);
    }

    @JavascriptInterface
    public byte[] read(long handle) {
        return nativeRead(handle);
    }

    private static native long nativeCreate(byte[] bytes);
    private static native void nativeRemove(long handle);
    private static native byte[] nativeRead(long handle);
}
