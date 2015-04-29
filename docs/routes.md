_Ideias iniciais para rotas. Passar para wiki depois..._

### Catadores

#### /catadores
Interface de filtros.
* __GET__ -> Lista com todos os catadores
* /catadores/?material="slug_material"
* /catadores/?position="slug_bairro"
* /catadores/?lat="lat"&lon="lon"
* /catadores/?google_maps_q="google_maps_q"
* /catadores/?actor="actor"


#### /catador
Interface para o Profile dos Catadores
* __GET__ -> Detalhes de um catador especifico.
* __POST__ ou __PUT__ -> Atualiza os dados de um catador.
* __DELETE__ -> Apagar um catador.


### Material

#### /materials
* __GET__ -> Obter lista de materiais
* __POST__ -> Adicionar um material

#### /material
* __GET__ -> Obter detalhes de um material
* __POST__ ou __PUT__ -> Atualizar um material
* __DELETE__ -> Apagar um material
