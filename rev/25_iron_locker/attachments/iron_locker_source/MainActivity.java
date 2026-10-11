package enit.ironlocker;

import android.app.Activity;
import android.os.Bundle;
import android.webkit.WebSettings;
import android.webkit.WebView;

public final class MainActivity extends Activity {
    @Override
    public void onCreate(Bundle state) {
        super.onCreate(state);
        WebView view = new WebView(this);
        WebSettings settings = view.getSettings();
        settings.setJavaScriptEnabled(true);
        view.addJavascriptInterface(new LockerBridge(), "IronLocker");
        view.loadUrl("file:///android_asset/index.html");
        setContentView(view);
    }
}
