
# House_Rocket_Insight_Project

<i>If you want to read about this project in English, [click here](https://github.com/felipefvasconcelos/House_Rocket_Insight_Project/blob/main/README.md).</i>

Neste repositório eu utilizo conceitos básicos de Python para fornecer insights sobre o negócio imobiliário em King County (EUA), baseado em dados públicos. <br>

Toda informação abaixo é fictícia.

## 1. Problema do Negócio

O modelo de negócio da House Rocket é basciamente comprar e vender propriedades utilizando a tecnologia para maximar sua receita. O grande desafio é encontrar as melhores oportunidades de negócio no mercado imobilário, baseado nos muitos atributos de cada propriedade.

Portanto, as principais perguntas que este projeto visa responder são:
  * Quais propriedades a House Rocket deve comprar?
  * Por quanto elas devem ser vendidas?
  * Quando elas devem ser vendidas?
  * Qual é o lucro esperado?<br>

## 2. Premissas do Negócio

* Quando uma propriedade é comprada e vendida mais de uma vez dentro do período de tempo do dataset (2014-2015), é gerado uma linha duplicada. Somente as informações mais recentes serão mantidas e o restante das duplicadas serão removidas.
* Inconsistências entre os atributos das propriedades são considerados como erro de entrada. Linhas com essas inconsistências serão removidas.
* Propriedades recomendadas para compra devem ter 'condition' maior ou igual a 3 e preço menor do que a mediana de preços das propriedades na mesma região.
* O preço das propriedades são afetadas por sasonalidade de acordo com as estações do ano apenas.
* A recomendação do preço de venda de cada propriedade será:
  * O preço da compra mais 30%, se o preço da compra for menor do que a mediana dos preços na região em estação do ano específica.
  * O preço da compra mais 10%, se o preço da compra for maior do que a mediana dos preços na região em estação do ano específica.
* Estações do ano:
  * Primavera começa em Março e termina em Maio.
  * Verão começa em Junho e termina em Agosto.
  * Outuno começa em Setembro e termina em Novembro.
  * Inverno começa em Dezembro e termina em Fevereiro.

## 3. Dados

Os dados usados neste projeto podem ser encontrados em:<br>
https://www.kaggle.com/harlfoxem/housesalesprediction/discussion/207885
<br><br>
A tabela abaixo lista cada atributo das propriedades e sua respectiva definição:<br>
<details><summary>Clique aqui para ver a tabela de atributos</summary><br>
  
Atributo | Definição
------------ | -------------
|id | ID único de cada propriedade disponível|
|date | Data em que a propriedade estava disponível|
|price | Preço de venda de cada propriedade|
|bedrooms | Número de quartos|
|bathrooms | Número de banheiros, onde .5 conta como banheiro com sanitário mas sem chuveiro, e .75 conta como banheiro que tem uma pia, um sanitário e um chuveiro ou banheira|
|sqft_living | Area interior dos apartamentos em pés quadrados|
|sqft_lot | Area do terreno em pés quadrados|
|floors | Número de andares|
|waterfront | Indica se propriedade tem vistá para água ou não|
|view | Index de 0 a 4 de quão boa é a vista da propriedade|
|condition | Index de 1 a 5 sobre a condição da propriedade|
|grade | Index de 1 a 13, onde 1-3 construição e design pobres, 4-10 construição e design medianos, e 11-13 construição e design alto padrão|
|sqft_above | Area do interior das propriedades que está acima do nível do solo em pés quadrados|
|sqft_basement | Area do interior das propriedades que está abaixo do nível do solo em pés quadrados|
|yr_built | Ano em que a propriedade foi construída|
|yr_renovated | Ano da última renovação da propriedade|
|zipcode | Código postal da região onde a propriedade está localizada|
|lat | Latitude|
|long | Longitude|
|sqft_living15 | Area espaço interior para os 15 vizinhos mais próximos em pés quadrados|
|sqft_lot15 | Area dos lotes dos 15 vizinhos mais próximos em pés quadrados|
</details>

## 4. Estratégia de Solução

1. Entendimento do modelo e do problema do negócio;
2. Coletar dados do Kaggle;
3. Processar dados;
4. Limpar dados;
5. Explorar dados;
6. Responder questões do negócio (seção 1);
7. Publicar [dashboard](https://house-rocket-insights-db.herokuapp.com/);
8. Validar hipóteses;
9. Providenciar insights relevantes.

## 5. Ferramentas

* Python 3.10.2
* Jupyter Notebook
* Pycharm

## 6. Resultados do Negócio

Baseado nos critérios estabelecidos anteriormente, existem 10.500 propriedade que devem ser compradas de um total de 21.421.<br>
Se as recomendações de venda forem seguiras, os resultados esperados são:
* Valor máximo investido: $ 4,078,617,894.0
* Lucro Mínimo Esperado: $ 694,433,672.2
* Lucro Máximo Esperado: $ 839,540,926.8
<br><br>
Informações sobre qual propriedade deve ser comprada e quando vender podem ser encontradas no [dashboard](https://house-rocket-insights-db.herokuapp.com/) online.

## 7. Insights Mais Relevantes do Negócio

1. Propriedades com 'condition' igual a 4 são as mais lucrativas, seguida pelas propriedades com 'condition' igual a 3 e 5.<br><br>
<img src="https://github.com/felipefvasconcelos/House_Rocket_Insight_Project/blob/main/assets/hipotesis_8.JPG" width="700" height="400"><br><br>
2. A maioria das propriedades (58%) ficaram disponíveis para venda durante o verão e primavera.<br><br>
<img src="https://github.com/felipefvasconcelos/House_Rocket_Insight_Project/blob/main/assets/hipotesis_9.JPG" width="800" height="400"><br><br>
3. 50% das propriedades recomendades para compra estão dentro de raio de 15km do lago<br><br>
<img src="https://github.com/felipefvasconcelos/House_Rocket_Insight_Project/blob/main/assets/hipotesis_10.JPG" width="700" height="400"><br><br>

## 8. Conclusão

O objetivo deste projeto era de aplicar conceitos básicos de Python para resolver um hipotético problema de negócio de uma empresa fictícia (House Rocket). Após seguir as etapas da estratégia de solução, e considerando as premissas do negócio feitas, foi possível classificar cada propriedade com um recomendação "compra" ou "não compra". Além disso, para àquelas propriedades recomendads para serem compradas, foi sugerido um preço de venda e a melhor estação do ano para venda de cada uma delas. Finalmente, foi gerado um dashboard online para visualizar todas as recomendações feitas durante o desenvolvimento deste projeto.
<br><br>

---
## Referências:
* Dataset House Sales in King County (USA) em [Kaggle](https://www.kaggle.com/harlfoxem/housesalesprediction)
* Definição dos atributos em [Kaggle discussion](https://www.kaggle.com/harlfoxem/housesalesprediction/discussion/207885)
* Python do Zero ao DS aulas no [Youtube](https://www.youtube.com/watch?v=1xXK_z9M6yk&list=PLZlkyCIi8bMprZgBsFopRQMG_Kj1IA1WG&ab_channel=SejaUmDataScientist)
* Blog [Seja um Data Scientist](https://sejaumdatascientist.com/os-5-projetos-de-data-science-que-fara-o-recrutador-olhar-para-voce/)
