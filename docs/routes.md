_Ideias iniciais para rotas. Passar para wiki depois..._


->>>>> <DONE> CARROCEIRO <DONE> <<<<<<-

#### /carroceiro/id/

Interface para o Profile dos Catadores

* __GET__ -> Detalhes de um carroceiro especifico.
* __PUT__ -> Atualiza os dados de um carroceiro.
* __DELETE__ -> Apagar um carroceiro.


#### /carroceiro/

Lista de carroceiros, para listar todos ou incluir novos.

* __GET__ -> Detalhes de um carroceiro especifico.
* __POST__ -> Adiciona um novo carroceiro.


->>>> TODO <<<<- (Discutir como vai ficar or argumentos e CRUD)

### Carroceiros filtros

Interface de filtros.
* __GET__ -> Lista com todos os catadores
* /catadores/?material="slug_material"
* /catadores/?position="slug_bairro"
* /catadores/?lat="lat"&lon="lon"
* /catadores/?google_maps_q="google_maps_q"
* /catadores/?actor="actor"

### Material

#### /materials
* __GET__ -> Obter lista de materiais
* __POST__ -> Adicionar um material

#### /material
* __GET__ -> Obter detalhes de um material
* __POST__ ou __PUT__ -> Atualizar um material
* __DELETE__ -> Apagar um material
