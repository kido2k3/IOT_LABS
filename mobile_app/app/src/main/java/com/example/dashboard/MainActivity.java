package com.example.dashboard;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.util.Log;
import android.widget.TextView;

import com.github.angads25.toggle.interfaces.OnToggledListener;
import com.github.angads25.toggle.model.ToggleableView;
import com.github.angads25.toggle.widget.LabeledSwitch;

import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttCallbackExtended;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;

import java.nio.charset.Charset;

public class MainActivity extends AppCompatActivity {

    MQTTHelper connection;
    TextView txtTemp, txtHumid;
    LabeledSwitch btnLed, btnPump;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        //text
        txtTemp = findViewById(R.id.txtTemperature);
        txtHumid = findViewById(R.id.txtHumidity);
        //button
        btnLed = findViewById(R.id.btnLED);
        btnLed.setOnToggledListener(new OnToggledListener() {
            @Override
            public void onSwitched(ToggleableView toggleableView, boolean isOn) {
                if(isOn==true){
                    sendDataMQTT("kido2k3/feeds/iot-led","1");
                }else{
                    sendDataMQTT("kido2k3/feeds/iot-led","0");
                }
            }
        });
        btnPump = findViewById(R.id.btnPump);
        btnPump.setOnToggledListener(new OnToggledListener() {
            @Override
            public void onSwitched(ToggleableView toggleableView, boolean isOn) {
                if(isOn==true){
                    sendDataMQTT("kido2k3/feeds/iot-pump","1");
                }else{
                    sendDataMQTT("kido2k3/feeds/iot-pump","0");
                }
            }
        });
        startMQTT();
    }
    public void startMQTT(){
        connection = new MQTTHelper(this);
        connection.setCallback(new MqttCallbackExtended() {
            @Override
            public void connectComplete(boolean reconnect, String serverURI) {

            }

            @Override
            public void connectionLost(Throwable cause) {

            }

            @Override
            public void messageArrived(String topic, MqttMessage message) throws Exception {
                Log.d("TEST", topic+"---"+message.toString());
                if(topic.contains("iot-temperature")){
                    txtTemp.setText(message.toString()+"℃");
                }else if(topic.contains("iot-humidity")){
                    txtHumid.setText(message.toString()+"%");
                } else if(topic.contains("iot-led")){
                    if(message.toString().equals("1")){
                        btnLed.setOn(true);
                    }else{
                        btnLed.setOn(false);
                    }
                } else if(topic.contains("iot-pump")){
                    if(message.toString().equals("1")){
                        btnPump.setOn(true);
                    }else{
                        btnPump.setOn(false);
                    }
                }
            }

            @Override
            public void deliveryComplete(IMqttDeliveryToken token) {

            }
        });
    }
    public void sendDataMQTT(String topic, String value){
        MqttMessage msg = new MqttMessage();
        msg.setId(1234);
        msg.setQos(0);
        msg.setRetained(false);

        byte[] b = value.getBytes(Charset.forName("UTF-8"));
        msg.setPayload(b);

        try {
            connection.mqttAndroidClient.publish(topic, msg);
        }catch (MqttException e){
        }
    }
}