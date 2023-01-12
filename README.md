# Projeto James Bauer (Investidor de imóveis ficticio)

Este projeto é sobre um investidor fictício que tem como obejtivo comprar imóveis na cidade de Nova York e depois loca-los pela plataforma Airbnb.

Juntamente com a conclusão final de quais tipos de imóveis e bairros onde são recomendados para compra, foi fornecido para o time de negócios 5 hipósteses para que possa gerar insights.

O projeto foi disponibilizado para visualização através da ferramenta Streamlit, que permite que o time de negócio acesse do seu computador pessoal, tablet ou smarthphone.

Link para visualização:  https://rafapires07-james-bauer--streamlit-airbnb-2019-dashboard-cyjdpy.streamlit.app

## Questão do negócio:

O investidor James Bauer gostaria de diversificar seus negócios e começar a investir em imóveis. Ele definiu que compraria imóveis na cidade de Nova York, nos Estados Unidos. Por ser um dos locais mais caros para se viver no País, ele acredita que obterá um retorno satisfatório de seus investimentos caso loque imóveis na cidade.

Como planeja-se inicialmente locar os imóveis adquiridos, ele definiu que irá utilizar a plataforma Airbnb para esse fim. Para realizar o estudo foi fornecida a base de dados referente aos imóveis da Airbnb em Nova York em 2019. O estudo tem como objetivo a escolha das regiões onde há maior locação, maiores preços e maior rentabilidade da cidade de Nova York, pois ele acredita que essas características irão ajudá-lo a recuperar o dinheiro investido na aquisição desses imóveis mais rapidamente.

## Premissas do projeto

Para a execução deste projeto algumas premissas foram adotadas, sendo elas:

*Foram retirados os imóveis com rentabilidade maior que 29794.06, uma vez que estaremos considerando que esses imóveis possuem características muito específicas e que seriam difíceis ou impossíveis de replicar, atrapalhando a análise dos melhores bairros e tipo de imóveis a serem comprados.
r'''
            $$ 𝑟𝑒𝑛𝑡𝑎𝑏𝑖𝑙𝑖ty = \frac{𝑝𝑟𝑖𝑐𝑒 * (𝑚𝑖𝑛𝑖𝑚𝑢𝑚\_𝑛𝑖𝑔ℎ𝑡𝑠 + 1) *  n𝑢𝑚𝑏𝑒𝑟\_𝑜𝑓\_𝑟𝑒𝑣𝑖𝑒𝑤𝑠}{ \sqrt{𝑎𝑣𝑎𝑖𝑙𝑎𝑏𝑖𝑙𝑖𝑡𝑦_365}} $$)
            ''')

## 6. Resultado financeiro

O objetivo desse projeto é fornecer uma lista de imóveis com opções de compra e venda, para obtenção do __lucro máximo__ que poderá ser obtido se todas as sugestões ocorrerem. O resultado financeiro apresentado representa o lucro máximo que pode ser obtido utilizando as recomendações informadas.

| __Número de imóveis__ | __Custo total__ | __Receita de vendas__ | __Lucro (profit)__ |
| ----------------- | ----------------- | ----------------- | ----------------- |
| 10.642 | R$ 4.079.586.744,00 | R$ 4.766.745.551,20 | R$ 687.158.807,20 |


## 6. Conclusão

O objetivo deste projeto é prover para o time de negócio informações suficientes para uma melhor tomada de decisões. Sendo assim, este projeto cumpriu sua função.
