# Analytics de Logística Reversa

🇬🇧 [Read in English](README.md)

Visibilidade ponta a ponta da cadeia de pós-venda de uma operação de e-commerce: **devoluções, notas de crédito, recebimento de RMA, tickets de atendimento, cancelamentos, avarias e ressarcimento de transportadoras**, todos ligados por uma única chave, o número da entrega.

> Modelos semânticos Power BI / Fabric, dataflows, SQL (ERP) e Power Query (M).
> Tudo aqui é **sanitizado ou sintético**. Nenhuma empresa, cliente, parceiro ou pedido real foi incluído.

## O problema

Quando um pedido dá errado, a evidência está espalhada: o ERP conhece a nota de devolução e o crédito, o armazém sabe o que chegou fisicamente, o atendimento sabe o que o cliente ouviu, a transportadora deve um ressarcimento e o marketplace pode ou não ter reembolsado. Cada time via uma parte, então dinheiro ficava na mesa e ninguém sabia dizer *onde estava de fato um pedido em devolução*.

## A solução

O fluxo está no [README em inglês](README.md#the-solution).

- **Uma chave de ligação entre sistemas** – o número da entrega liga documentos do ERP, registros de RMA, tickets e repasses. Diferenças de espaços e formato entre sistemas são normalizadas no dataflow, e duplicidades são removidas pela chave composta (entrega, nota original).
- **Tipificação do crédito** – o ERP codifica o tipo de crédito (devolução, em trânsito, virtual); o dataflow traduz os códigos em status de negócio, distinguindo *devolução física*, *crédito virtual* e *devolução ainda em trânsito*.
- **Recebimento de RMA** – os registros do armazém trazem a última data de devolução, a transportadora de retorno e o valor da nota; combinados ao crédito, revelam dois vazamentos silenciosos: *recebido e não creditado* e *creditado e nunca recebido*.
- **Camada de atendimento** – data do primeiro ticket, status e prazos por entrega, fila de cancelamentos separando novos de encaminhados, e visão de reembolso/retratação.
- **Ressarcimento de transportadoras** – pedidos de ressarcimento, datas previstas e pagamentos por transportadora, para cobrar avarias e extravios no prazo.
- **Análise de avarias** – motivos e status do atendimento agrupados em uma visão de dano por entrega, incluindo transportadora de retorno e código de postagem.
- **Custo da devolução** – frete de retorno (documentos de frete), mão de obra de RMA e movimentações de estoque formam um custo por devolução, que alimenta o modelo de margem.

Atualização em camadas: os dataflows de origem rodam em agenda própria (de diária a semanal conforme a volatilidade do dado) e os modelos semânticos os consomem, de modo que um modelo pesado não trava um leve.

## Executar a implementação de referência

[`reference_implementation/return_stage.py`](reference_implementation/return_stage.py) mostra como a etapa de uma devolução é derivada dos fatos cruzados e quais etapas expõem dinheiro ou estoque à atenção de uma pessoa.

```bash
pip install pytest && pytest -q
```

## Decisões de projeto

- **Uma chave de negócio vale mais que muitos joins técnicos** – cada nova fonte só precisa expor o número da entrega.
- **Traduzir códigos do ERP uma vez, no dataflow** – os painéis falam a língua do negócio.
- **Expor os vazamentos silenciosos** – as duas divergências entre estado físico e financeiro são status de primeira classe.
- **Ritmos de atualização separados** – fontes voláteis atualizam com frequência; as lentas, não.

<!-- RESULTADOS: incluir depois (valor recuperado de transportadoras, devoluções sem crédito encontradas, tempo de tratativa, tickets no prazo). -->

## Autoria

Construído e mantido por [Bárbara Gomes](https://github.com/Barbarags) – Coordenadora de Dados e BI.
