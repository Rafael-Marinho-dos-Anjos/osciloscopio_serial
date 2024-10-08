// Período da frequência de cada leitura em us (1000000 / frequencia)
// Para uma frequencia de 1kHZ: interval = 1000000 / 1000 = 1000
int interval = 1000;
unsigned long elapsed_time;

// Definição dos pinos analógicos
const int pinA0 = A0;
const int pinA1 = A1;
const int pinA2 = A2;

// Variável para armazenar o valor lido de cada pino
int valorA0;
int valorA1;
int valorA2;

void setup() {
  // Inicializa a comunicação serial
  Serial.begin(9600);

  // Configura os pinos como entrada (opcional, já que pinos analógicos são inputs por padrão)
  pinMode(pinA0, INPUT);
  pinMode(pinA1, INPUT);
  pinMode(pinA2, INPUT);
}

void loop() {
  // Inicio da leitura
  elapsed_time = micros();
  
  // Leitura dos valores dos pinos analógicos
  valorA0 = analogRead(pinA0);
  valorA1 = analogRead(pinA1);
  valorA2 = analogRead(pinA2);

  // Converte os valores lidos para tensões
  float tensaoA0 = valorA0 * (5.0 / 1023.0);
  float tensaoA1 = valorA1 * (5.0 / 1023.0);
  float tensaoA2 = valorA2 * (5.0 / 1023.0);

  // Envia os valores lidos pela serial separados por espaços
  Serial.print(tensaoA0);
  Serial.print(" ");
  Serial.print(tensaoA1);
  Serial.print(" ");
  Serial.println(tensaoA2);

  // Tempo decorrido durante a leitura
  elapsed_time = micros() - elapsed_time;

  // Pequeno atraso para manter a frequência de leitura
  delayMicroseconds(interval - elapsed_time); 
}