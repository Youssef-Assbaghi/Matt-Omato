#include <Servo.h>
Servo servo1; //servo de la base
Servo servo2; //servo del brazo
Servo servo3; //servo del antebrazo
Servo servo4; //servo de la muñequilla
Servo servo5; //servo de giro de pinza
Servo servo6; //servo de apertura/cierre de pinza
//Definicion de variables de la cinematica inversa
const float pi=3.1415;
//coordenadas de la pinza del robot
float x;
float y;
float z;
float b=185; //longitud de brazo mm
float ab=138; //longitud de antebrazo mm
float m=172; //longitud de muñequilla mm
float H=85; //altura de base mm
float cabGrados; //angulo de cabeceo en grados
float cabRAD; //angulo de cabeceo en radianes
float Axis1; //Giro de la base en RAD
float Axis2; //Giro del brazo en RAD
float Axis3; //Giro del antebrazo en RAD
float Axis4; //Giro de la muñequilla en RAD
float Axis5; //Giro de la pinza en grados
float Pinza; //Pinza en grados
float Axis1Grados; //Giro de la base en Grados
float Axis2Grados; //Giro del brazo en Grados
float Axis3Grados; //Giro del antebrazo en Grados
float Axis4Grados; //Giro de la muñequilla en Grados
float M;
float xprima;
float yprima;
float Afx;
float Afy;
float A;
float B;
float Hip;
float alfa;
float beta;
float gamma;
void PosicionCero()
{
//Ajustar valores de servos de posición home
servo1.write(90);
servo2.write(145);
servo3.write(0);
servo4.write(0);
servo5.write(90);
servo6.write(70); // pinza cerrada 70º
// pinza abierta 110º
}
void setup() {
	Serial.begin(9600);
	// asignacion de servos a pines y centrar servos
	servo1.attach(9);
	servo1.write(home_servo1);
	servo2.attach(10);
	servo2.write(home_servo2);
	servo3.attach(11);
	servo3.write(home_servo3);
	servo4.attach(3);
	servo4.write(home_servo4);
	servo5.attach(5);
	servo5.write(home_servo5);
	servo6.attach(6);
	servo6.write(home_servo6);
}
void loop()
{
// Datos a donde col·locar el robot:
// x=100mm Y=100mm Z=100mm cabeceopinza=0º
// Giropinza=90º Pinza=110 (cerrada)
x=100;
y= 100;
z= 200;
cabGrados=0;
Axis5=90; // giro de la pinza es directo
Pinza=110;
cabRAD=cabGrados*pi/180; //angulo cabeceo en rad.
Axis1=atan2(y,x);
M=sqrt(pow(x,2)+pow(y,2));
xprima=M;
yprima=z;
Afx=cos(cabRAD)*m;
B=xprima-Afx;
Afy=sin(cabRAD)*m;
A=yprima+Afy-H;
Hip=sqrt(pow(A,2)+pow(B,2));
alfa=atan2(A,B);
beta=acos((pow(b,2)-pow(ab,2)+pow(Hip,2))/(2*b*Hip));
Axis2=alfa+beta;
gamma=acos((pow(b,2)+pow(ab,2)-pow(Hip,2))/(2*b*ab));
Axis3=gamma;
Axis4=2*pi-cabRAD-Axis2-Axis3;
Axis1Grados=Axis1*180/pi; //Giro base en Grados
Axis2Grados=90-Axis2*180/pi; //Giro brazo en Grados
Axis3Grados=180-Axis3*180/pi; //Giro antebrazo grados
Axis4Grados=180-Axis4*180/pi; //Giro muñequilla grados
servo1.write(Axis1Grados);
servo2.write(Axis2Grados);
servo3.write(Axis3Grados);
servo4.write(Axis4Grados);
servo5.write(Axis5);
servo6.write(Pinza);
Serial.println("Ejes:");
Serial.print("Axis1 en grados: ");
Serial.println(Axis1Grados);
Serial.print("Axis2 en grados: ");
Serial.println(Axis2Grados);
Serial.print("Axis3 en grados: ");
Serial.println(Axis3Grados);
Serial.print("Axis4 en grados: ");
Serial.println(Axis4Grados);
Serial.print("giro de la pinza en grados: ");
Serial.println(Axis5);
Serial.print("Cierre o apertura de la pinza: ");
Serial.println(Pinza);
}