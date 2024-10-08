# Osciloscópio Serial

*Osciloscópio Serial* é um software desenvolvido em Python para funcionar em conjunto com o Arduino. Ele permite a leitura de múltiplos sinais analógicos e a análise em tempo real das suas características, como frequência, Vrms e Vpp. O software também ajusta automaticamente as escalas de tempo e amplitude dos gráficos, facilitando a visualização dos sinais.

![Interface do programa](image\osciloscopio.jpeg)

## Funcionalidades

- *Leitura simultânea de vários sinais*: o Arduino envia os valores lidos dos pinos analógicos via comunicação serial. Cada valor de sinal é separado por espaços na mensagem (exemplo: 0.5 0.1 0.7).
- *Análise automática dos sinais*: o programa calcula automaticamente a frequência, Vrms (tensão eficaz) e Vpp (tensão de pico a pico) para cada sinal recebido.
- *Ajuste automático de escalas*: as escalas de tempo e amplitude dos sinais exibidos no gráfico são ajustadas automaticamente.
- *Detecção automática da placa*: ao iniciar o programa, ele detecta automaticamente a placa Arduino conectada à porta USB. Se não houver uma placa conectada, o software aguardará até que uma seja conectada.

## Requisitos

O projeto depende de algumas bibliotecas Python que estão listadas no arquivo requirements.txt. Certifique-se de instalar todas as dependências antes de executar o programa.

### Instalação das dependências

Para instalar as dependências, execute o seguinte comando:

```bash
pip install -r requirements.txt
```

### Como usar

1. Certifique-se de que o Arduino esteja configurado para enviar os valores dos pinos analógicos via comunicação serial.

2. Conecte a placa Arduino a uma porta USB do computador.

3. Execute o programa Python.

4. O programa detectará automaticamente a placa e começará a receber os sinais.

5. Para o cálculo correto da frequência, certifique-se de que a frequência de amostragem configurada no Arduino é a mesma informada ao software.

### Código Arduino

Há um exemplo de código para realizar a leitura de 3 sinais simultâneos utilizando diferentes pinos do Arduino como entrada. [app\arduino\example.ino](app\arduino\example.ino)

### Exemplo de mensagem recebida

A cada amostra de sinal coletada, o Arduino deverá enviar os valores separados por espaço em uma mensagem via serial, por exemplo:

```bash
0.5 0.1 0.7
```

O software irá processar os sinais formados pelos valores enviados pelas sucessivas mensagens, calculando suas respectivas frequências, Vrms e Vpp.

### Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
