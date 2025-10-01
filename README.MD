# Sistema de Análise de E-commerce

Sistema completo de análise de dados de vendas online desenvolvido como projeto da disciplina **Lógica de Programação II** da ADA Tech.

## ✨ Funcionalidades

- **📊 Carregamento automático** de dataset do Kaggle
- **🔍 CRUD completo** em memória (Create, Read, Update, Delete)
- **📈 Relatórios e análises** (médias, rankings, filtros)
- **💾 Exportação CSV** de dados e relatórios
- **⚠️ Tratamento robusto** de exceções

## 🚀 Como usar

```bash
# Instalar dependência
pip install kagglehub

# Executar sistema
python app.py
```

## 🏗️ Arquitetura

### Classes principais
- **`DataStructure`**: Organiza dados em estruturas adequadas
- **`EcommerceCRUD`**: Operações CRUD completas
- **`RelatoriosAnalytics`**: Relatórios e análises
- **`ExportadorCSV`**: Exportação de arquivos
- **`EcommerceSystem`**: Interface principal

### Estruturas de dados
- **Listas**: Vendas ordenadas e indexadas
- **Dicionários**: Acesso rápido por chave (produtos, clientes)
- **Tuplas**: Metadados imutáveis (colunas)
- **Contadores**: Estatísticas automáticas

## � Operações CRUD

```python
# Criar nova venda
sistema.crud.criar_venda(dados_venda)

# Buscar venda por fatura
venda = sistema.crud.buscar_venda_por_invoice('123456')

# Atualizar venda existente
sistema.crud.atualizar_venda('123456', novos_dados)

# Deletar venda
sistema.crud.deletar_venda('123456')
```

## 📊 Relatórios disponíveis

- Médias gerais (receita, quantidade, preços)
- Ranking de produtos mais vendidos
- Ranking de países por vendas
- Filtros por faixa de valor
- Análise detalhada por país

## 📁 Estrutura do projeto

```
LMS_ADA/
├── app.py                    # Sistema principal
├── README.MD                 # Esta documentação
└── documentacao/
    ├── Dataset_Projeto_Análise_Inicial_pandas_&_kagglehub.ipynb
    ├── Paleta_Cores.pdf
    └── Projeto_Lógica de Programação_II.pdf
```

## ✅ Requisitos atendidos

- [x] Estruturas de dados organizadas (listas, tuplas, dicionários)
- [x] CRUD básico em memória
- [x] Relatórios e análises completas
- [x] Exportação CSV
- [x] Tratamento de exceções

---

**ADA Tech - Lógica de Programação II | Outubro 2025**