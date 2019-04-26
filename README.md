# Drive-Through Restaurant P2P

## Várias possibilidades de execução
### Execução normal dos scripts fornecidos pelos docentes

- simulação:
```console
$ python3 simulation.py
```
- cliente:
```console
$ python3 client.py
```

- cliente implementado pelo grupo:
```console
$ python3 our_client.py
```

### Script bash para executar cada entidade de forma aleatória com um espaçamento temporal
 - O intervalo em segundos é o intervalo entre o inicio de execução entre cada entidade
```console
$ ./simulation_init.py <Interval in seconds>
```
```console
Usage:
$ ./simulation_init.py 10
```

### Script bash para testar a versão 2 do ring node, selecionando aleatoriamente 1 processo para ser terminado, tendo um tempo de "sleep" entre cada termino de processo.

```console
$ ./simulation_v2_init.py <Number of iterations> <Time between process kills ( in seconds ) >
```
```console
Usage:
$ ./simulation_v2_init.py 5 3
```


### Script bash para executar vários clientes ao mesmo tempo


```console
$ ./init.sh <script to run> <number of clients>
```
```console
Usage:
$ ./init.sh client.py 10
```

### Script bash para mudar a versão do RingNode usada em cada entidade

```console
$ ./switch_to_v2.sh <import file to substitute> <import file to add>
```

```console
Usage:
$ ./switch_to_v2.sh RingNode_v2 RingNode
```

## Authors

* [**Mário Antunes**](https://github.com/mariolpantunes)
* [**Pedro Escaleira**](https://github.com/oEscal)
* [**Rafael Simões**](https://github.com/Rafaelyot)
