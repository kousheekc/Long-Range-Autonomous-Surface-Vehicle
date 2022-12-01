#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
#include <QMC5883LCompass.h>
#include <Servo.h>

#define CE_PIN   9
#define CSN_PIN 10
#define RUDDER_PIN 6
#define THROTTLE_PIN 7
#define MODE_PIN 8 
#define CELL1_PIN A3
#define CELL2_PIN A2
#define CELL3_PIN A1

const byte my_address[5] = {'R','x','A','A','A'};

RF24 radio(CE_PIN, CSN_PIN);
QMC5883LCompass compass;
Servo right_esc;
Servo left_esc;


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
int mode = 0;
int left_motor_speed = 1000;
int right_motor_speed = 1000;

void setup()
{
  Serial.begin(9600);
  Serial.println("Autonomous Surface Vehicle Telemetry Stream");

  radio.begin();
  radio.setDataRate(RF24_250KBPS);
  radio.openReadingPipe(1, my_address);
  radio.enableAckPayload();
  radio.startListening();
  radio.writeAckPayload(1, &t_data, sizeof(t_data));

  compass.init();

  pinMode(RUDDER_PIN, INPUT);
  pinMode(THROTTLE_PIN, INPUT);
  pinMode(MODE_PIN, INPUT);
  pinMode(CELL1_PIN, INPUT);
  pinMode(CELL2_PIN, INPUT);
  pinMode(CELL3_PIN, INPUT);

  Serial.println("[INFO]\tArming motors");
  right_esc.attach(2);
  left_esc.attach(5);
  right_esc.writeMicroseconds(left_motor_speed);
  left_esc.writeMicroseconds(right_motor_speed);
  delay(2000);
  Serial.println("[INFO]\tMotors are armed");
}

void loop()
{
  get_control_data();
  if (new_data == true)
  {
    print_control_data();
    new_data = false;
  }

  int mode = get_mode();
  if (mode == 0)
  {
    // Manual
    int throttle = get_throttle();
    int rudder = get_rudder();

    left_motor_speed = get_left_speed_manual(throttle, rudder);
    right_motor_speed = get_right_speed_manual(throttle, rudder);
    
    left_esc.writeMicroseconds(left_motor_speed);
    right_esc.writeMicroseconds(right_motor_speed);
  }
  else
  {
    // Auto
    if (c_data.start == 1)
    {
      int current_heading = get_heading();
      int desired_heading = c_data.desired_heading;
      int error = get_error(current_heading, desired_heading);

      left_motor_speed = get_left_speed_auto(c_data, error);
      right_motor_speed = get_right_speed_auto(c_data, error);
      
      left_esc.writeMicroseconds(left_motor_speed);
      right_esc.writeMicroseconds(right_motor_speed);
    }
  }
}

void get_control_data()
{
  if (radio.available())
  {
    radio.read(&c_data, sizeof(c_data));
    update_telemetry_data();
    radio.writeAckPayload(1, &t_data, sizeof(t_data));
    
    Serial.println();
    Serial.println();
    print_telemetry_data();
    new_data = true;
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

void update_telemetry_data()
{
  t_data.mode = get_mode();
  t_data.throttle = get_throttle();
  t_data.rudder = get_rudder();
  t_data.left_motor_speed = get_left_motor_speed();
  t_data.right_motor_speed = get_right_motor_speed();
  t_data.current_heading = get_heading();
  t_data.lat = get_lat();
  t_data.lon = get_lon();
  t_data.cell1 = get_cell_voltage(0);
  t_data.cell2 = get_cell_voltage(1);
  t_data.cell3 = get_cell_voltage(2);
}

int get_mode()
{
  int mode_val = pulseIn(MODE_PIN, HIGH);
  if (mode_val > 1500)
  {
    return 1;
  }
  else
  {
    return 0;
  }
}

int get_throttle()
{
  return pulseIn(THROTTLE_PIN, HIGH);
}

int get_rudder()
{
  return pulseIn(RUDDER_PIN, HIGH);
}

int get_left_motor_speed()
{
  return left_motor_speed;
}

int get_right_motor_speed()
{
  return right_motor_speed;
}

int get_heading()
{
  compass.read();
  return compass.getAzimuth();
}

float get_lat()
{
  return 1.0;
}

float get_lon()
{
  return 1.0;
}

float get_cell_voltage(int cell_num)
{
  float cells[3];
  
  int cell1_val = analogRead(CELL1_PIN);
  int cell2_val = analogRead(CELL2_PIN);
  int cell3_val = analogRead(CELL3_PIN);
  
  float v1 = cell1_val * (5.0 / 1023.0);
  float v2 = cell2_val * (5.0 / 1023.0);
  float v3 = cell3_val * (5.0 / 1023.0);
  
  v1 *= 1;
  v2 *= 2;
  v3 *= 3;

  cells[2] = v3 - v2;
  cells[1] = v2 - v1;
  cells[0] = v1;
  
  return cells[cell_num];
}

int get_left_speed_manual(int throttle, int rudder)
{
  return throttle + ((rudder - 1500) / 2);
}

int get_right_speed_manual(int throttle, int rudder)
{
  return throttle - ((rudder - 1500) / 2);
}

int get_left_speed_auto(struct control_data c_data, int error)
{
  int left_speed = c_data.cruise_speed + (c_data.kp * error);
  if (left_speed > c_data.max_speed)
  {
    left_speed = c_data.max_speed; 
  }
  if (left_speed < 1000)
  {
    left_speed = 1000;
  }
  return left_speed;
}

int get_right_speed_auto(struct control_data c_data, int error)
{
  int right_speed = c_data.cruise_speed - (c_data.kp * error);
  if (right_speed > c_data.max_speed)
  {
    right_speed = c_data.max_speed; 
  }
  if (right_speed < 1000)
  {
    right_speed = 1000;
  }
  return right_speed;
}

int get_error(int current, int desired) {
  int error;
  if (current == desired) {
    error = 0;
  }
  else if (current < desired) {
    error = desired - current;
  }
  else if (current > desired) {
    error = desired - current;
    if (error < -180) {
      error = error + 360;
    }
  }
  return error;
}
