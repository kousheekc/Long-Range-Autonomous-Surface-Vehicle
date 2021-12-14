#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

#define CE_PIN 9
#define CSN_PIN 10

const byte boat_address[5] = {'R','x','A','A','A'};

RF24 radio(CE_PIN, CSN_PIN);

struct control_data
{
  int start;
  int max_speed;
  int cruise_speed;
  int desired_heading;
  float kp;
  float ki;
  float kd;
};

struct telemetry_data
{
  int mode;
  int throttle;
  int rudder;
  int left_motor_speed;
  int right_motor_speed;
  int current_heading;
  float lat;
  float lon;
  float cell1;
  float cell2;
  float cell3;
};

struct control_data c_data;
struct telemetry_data t_data;

bool new_data = false;

unsigned long current_millis;
unsigned long prev_millis;
unsigned long telemetry_request_interval = 500;

void setup() 
{
  Serial.begin(9600);
  Serial.println("Autonomous Surface Vehicle Telemetry Stream");

  radio.begin();
  radio.setDataRate(RF24_250KBPS);
  radio.enableAckPayload();
  radio.setRetries(5,5);
  radio.openWritingPipe(boat_address);

  c_data.start = 0;
  c_data.max_speed = 1500;
  c_data.cruise_speed = 1000;
  c_data.desired_heading = 90;
  c_data.kp = 5;
  c_data.ki = 0;
  c_data.kd = 0;
}

void loop()
{
  current_millis = millis();
  if (current_millis - prev_millis >= telemetry_request_interval) 
  {
      send_signal();  
      prev_millis = millis();
  }
  if (new_data == true)
  {
    print_telemetry_data();
    new_data = false;
  }
  if (Serial.available() > 0)
  {
    String data = Serial.readStringUntil('\n');
    char command_signal = data[0];
    switch (command_signal)
    {
      case 's':
        Serial.println("[INFO]\tEnabling auto mode");
        c_data.start = 1;
        break;
      case 'S':
        Serial.println("[INFO]\tDisabling auto mode");
        c_data.start = 0;
        break;
      case 'm':
        Serial.print("[INFO]\tSetting max speed to: ");
        c_data.max_speed = data.substring(1).toInt();
        Serial.println(c_data.max_speed);
        break;
      case 'c':
        Serial.print("[INFO]\tSetting cruise speed to: ");
        c_data.cruise_speed = data.substring(1).toInt();
        Serial.println(c_data.cruise_speed);
        break;
      case 'h':
        Serial.print("[INFO]\tSetting heading to: ");
        c_data.desired_heading = data.substring(1).toInt();
        Serial.println(c_data.desired_heading);
        break;
      case 'p':
        Serial.print("[INFO]\tSetting kp to: ");
        c_data.kp = data.substring(1).toFloat();
        Serial.println(c_data.kp);
        break;
      case 'i':
        Serial.print("[INFO]\tSetting ki to: ");
        c_data.ki = data.substring(1).toFloat();
        Serial.println(c_data.ki);
        break;
      case 'd':
        Serial.print("[INFO]\tSetting kd to: ");
        c_data.kd = data.substring(1).toFloat();
        Serial.println(c_data.kd);
        break;
    }
  }
}

void send_signal()
{
  bool write_result = radio.write(&c_data, sizeof(c_data));
//  Serial.println();
//  Serial.println();
//  print_control_data();
  
  if (write_result)
  {
    if (radio.isAckPayloadAvailable())
    {
      radio.read(&t_data, sizeof(t_data));
      new_data = true;
    }
    else 
    {
      Serial.println("[ERROR]\tAcknowledge received but no data ");
    }
//    update_control_signal();
  }
  else 
  {
    Serial.println("[ERROR]\tTransmitting Control Signal Failed");
  }
}

void print_control_data()
{
  Serial.print("[CONTROL]\t");
  Serial.print(c_data.start);
  Serial.print("\t");
  Serial.print(c_data.max_speed);
  Serial.print("\t");
  Serial.print(c_data.cruise_speed);
  Serial.print("\t");
  Serial.print(c_data.desired_heading);
  Serial.print("\t");
  Serial.print(c_data.kp);
  Serial.print("\t");
  Serial.print(c_data.ki);
  Serial.print("\t");
  Serial.print(c_data.kd);
  Serial.println("\t");
}

void print_telemetry_data()
{
  Serial.print("[TELEMETRY]\t");
  Serial.print(t_data.mode);
  Serial.print("\t");
  Serial.print(t_data.throttle);
  Serial.print("\t");
  Serial.print(t_data.rudder);
  Serial.print("\t");
  Serial.print(t_data.left_motor_speed);
  Serial.print("\t");
  Serial.print(t_data.right_motor_speed);
  Serial.print("\t");
  Serial.print(t_data.current_heading);
  Serial.print("\t");
  Serial.print(t_data.lat);
  Serial.print("\t");
  Serial.print(t_data.lon);
  Serial.print("\t");
  Serial.print(t_data.cell1);
  Serial.print("\t");
  Serial.print(t_data.cell2);
  Serial.print("\t");
  Serial.print(t_data.cell3);
  Serial.println("\t");
}

void update_control_signal()
{
  return;
}
