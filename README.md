# Drive-Through Restaurant P2P


## Execução dos testes

### Execução normal com os scripts fornecidos pelos docentes

simulação:
```console
$ python3 simulation.py
```
cliente:
```console
$ python3 client.py
```

cliente implementado pelo grupo:
```console
$ python3 our_client.py
```

### Script bash para executar cada entidade de forma aleatória com um espaçamento temporal

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


### Script bash para executar vários clientes


```console
$ ./init.sh <script to run> <number of clients>
```
```console
Usage:
$ ./init.sh client.py 10
```

### Script bash para intercalar duas versões da classe RingNode em toda a simulação

```console
$ ./switch_to_v2.sh <import file to substitute> <import file to add>
```

```console
Usage:
$ ./switch_to_v2.sh RingNode_v2 RingNode
```

### Script bash para terminar toda a simulação

```console
$ ./kill_all_simulations.sh 
```


## Authors

* **Mário Antunes** - [mariolpantunes](https://github.com/mariolpantunes)
* **Pedro Escaleira**
* **Rafael Simões**

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

