# POO-Exame_Especial
Este repositório contêm os arquivos referentes à entrega do Exame Especial da disciplina de Programação Orientada a Objetos.  
O Exame Especial é uma simulação de um mercado, desenvolvido em Python, utilizando conceitos da programação orientada a objetos e modularização.  

## Modo de uso:
O projeto deve ser executado utiliando o comando:  
`python online_market\run.py`  
O diretório onde o comando é executado deve também conter a pasta `data/`.  

Foi disponibilizado no diretório uma base de dados de exemplo para a execução do programa.  
No entanto, caso queira criar um nova base de dados vazia, o arquivo `database.json` pode ser excluído, e então, antes de executar `run.py` deve se utilizar o comando:  
`python online_market\setup.py`  
Note que o diretório onde o comando de setup é executado também deve conter a pasta `data/`.

## Diagrama UML de Classes
O diagrama UML de classes do projeto foi criado utilizando a ferramenta PlantUML.  

No diagrama, é possível observar os conceitos de programação orientada a objetos, como interfaces, classes abstratas, herança, encapsulamento, etc.  
Também está representado como o código foi modularizado em diferentes packages, e como as diferentes classes dos diferentes pacotes se relacionam e interagem.

![Diagrama UML de Classes](https://github.com/Brugger-UFMG/POO-Exame_Especial/blob/3c586b680561176c375cbda6064b2d4b01035fe9/docs/online_market.png)
