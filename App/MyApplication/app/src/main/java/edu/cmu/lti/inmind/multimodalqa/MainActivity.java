package edu.cmu.lti.inmind.multimodalqa;

import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.webkit.WebView;
import android.webkit.WebViewClient;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        WebView webView = (WebView)findViewById(R.id.webView);
        webView.getSettings().setJavaScriptEnabled(true);
        //webView.loadUrl("http://holbox.lti.cs.cmu.edu:16000/index.html");
        webView.loadUrl("http://192.168.1.45:5000");
        webView.setWebViewClient(new WebViewClient());
    }
}
