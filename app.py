"""
Sistema de Análise de E-commerce - AULA PRÁTICA DE PYTHON
=========================================================
Este é um projeto educacional completo que demonstra:

🎯 CONCEITOS FUNDAMENTAIS:
- Estruturas de dados organizadas (listas, tuplas, dicionários)  
- CRUD básico em memória (Create, Read, Update, Delete)
- Relatórios (médias, rankings, filtros)
- Exportação para CSV
- Tratamento robusto de exceções
- Programação Orientada a Objetos
- Manipulação de arquivos
- Interface de usuário interativa

🏗️ ARQUITETURA:
- Classes especializadas para cada responsabilidade
- Separação clara entre dados, lógica e apresentação
- Reutilização de código através de métodos
- Tratamento de erros em todas as operações

📚 IDEAL PARA APRENDER:
- Lógica de programação avançada
- Estruturas de dados na prática
- Boas práticas de desenvolvimento
- Documentação e organização de código
"""

# ============================================================================
# IMPORTAÇÕES - Bibliotecas necessárias para o funcionamento do sistema
# ============================================================================

# Biblioteca para download de datasets do Kaggle
import kagglehub

# Biblioteca padrão do Python para operações com arquivos e diretórios
import os

# Biblioteca para leitura e escrita de arquivos CSV (Comma Separated Values)
import csv

# Biblioteca para trabalhar com dados em formato JSON (não usada no projeto atual)
import json

# Classe para trabalhar com datas e horários
from datetime import datetime

# Estruturas de dados especiais do Python:
# - defaultdict: dicionário que cria valores padrão automaticamente
# - Counter: contador automático para elementos
from collections import defaultdict, Counter

# Tipagens para melhor documentação e validação do código:
# - Dict: dicionário tipado
# - List: lista tipada
# - Tuple: tupla tipada
# - Optional: valor que pode ser None
# - Any: qualquer tipo de dado
from typing import Dict, List, Tuple, Optional, Any

# Biblioteca para controle do sistema (usado para sair do programa)
import sys


# ============================================================================
# CLASSE DATASTRUCTURE - Organização das Estruturas de Dados
# ============================================================================

class DataStructure:
    """
      Estruturas de Dados Organizadas
    
    Esta classe demonstra como organizar dados usando as estruturas corretas:
    - LISTAS: Para dados ordenados e pesquisáveis
    - DICIONÁRIOS: Para acesso rápido por chave
    - TUPLAS: Para dados imutáveis (que não mudam)
    - CONTADORES: Para estatísticas automáticas
    
    💡 CONCEITO: Cada estrutura tem seu propósito específico!
    """
    
    def __init__(self):
        """
        🏗️ CONSTRUTOR DA CLASSE
        
        Aqui inicializamos todas as estruturas de dados que vamos usar.
        O __init__ é chamado automaticamente quando criamos um objeto.
        """
        
        # ====================================================================
        # ESTRUTURAS PRINCIPAIS DE DADOS
        # ====================================================================
        
        # 📝 LISTA DE VENDAS:
        # - Por que lista? Porque precisamos manter a ordem das vendas
        # - Por que List[Dict[str, Any]]? Cada venda é um dicionário com dados
        # - Exemplo: [{'invoice_no': '001', 'total': 100.0}, {...}]
        self.vendas: List[Dict[str, Any]] = []
        
        # 📦 DICIONÁRIO DE PRODUTOS:
        # - Por que dicionário? Para buscar produtos rapidamente pelo código
        # - Estrutura: {'PROD001': {'description': 'Produto 1', 'vendas': 10}}
        # - Acesso rápido: O(1) vs O(n) em lista
        self.produtos: Dict[str, Dict[str, Any]] = {}
        
        # 👥 DICIONÁRIO DE CLIENTES:
        # - Similar aos produtos, mas indexado por ID do cliente
        # - Permite encontrar cliente instantaneamente
        self.clientes: Dict[str, Dict[str, Any]] = {}
        
        # 🌍 PAÍSES COM DEFAULTDICT:
        # - defaultdict(list) cria uma lista vazia automaticamente
        # - Evita erros de "key not found"
        # - Exemplo: se acessarmos paises['Brasil'], cria [] automaticamente
        self.paises: Dict[str, List[str]] = defaultdict(list)
        
        # ====================================================================
        # TUPLAS PARA METADADOS (DADOS IMUTÁVEIS)
        # ====================================================================
        
        # 📋 COLUNAS DO DATASET:
        # - Por que tupla? Porque as colunas NUNCA mudam!
        # - Tuplas são imutáveis, garantem que ninguém altere por engano
        # - Mais eficiente em memória que listas
        self.colunas_dataset: Tuple[str, ...] = (
            'InvoiceNo',    # Número da fatura
            'StockCode',    # Código do produto
            'Description',  # Descrição do produto
            'Quantity',     # Quantidade vendida
            'InvoiceDate',  # Data da venda
            'UnitPrice',    # Preço unitário
            'CustomerID',   # ID do cliente
            'Country'       # País da venda
        )
        
        # ====================================================================
        # CONTADORES PARA ESTATÍSTICAS AUTOMÁTICAS
        # ====================================================================
        
        # 📊 CONTADOR DE VENDAS POR PAÍS:
        # - Counter é um dicionário especial que conta automaticamente
        # - Exemplo: counter['Brasil'] += 1 conta mais uma venda no Brasil
        # - Método most_common() retorna os mais frequentes
        self.contador_vendas_pais = Counter()
        
        # 📈 CONTADOR DE PRODUTOS:
        # - Conta quantas vezes cada produto foi vendido
        # - Útil para rankings e estatísticas
        self.contador_produtos = Counter()
        
    def adicionar_venda(self, registro: Dict[str, Any]) -> bool:
        """
          Método para Adicionar Vendas
        
        Este método demonstra:
        - Validação de dados de entrada
        - Conversão segura de tipos
        - Tratamento de exceções
        - Atualização de múltiplas estruturas
        
        Args:
            registro: Dicionário com dados da venda do CSV
            
        Returns:
            bool: True se sucesso, False se erro
        """
        try:
            # ================================================================
            # ETAPA 1: VALIDAÇÃO DOS DADOS OBRIGATÓRIOS
            # ================================================================
            
            # 🔍 Por que validar?
            # - Evita dados corrompidos no sistema
            # - Falha rápida se dados essenciais estão ausentes
            # - .get() retorna None se chave não existir (seguro)
            
            if not registro.get('InvoiceNo') or not registro.get('StockCode'):
                # raise ValueError interrompe a execução e lança uma exceção
                # Será capturada pelo except abaixo
                raise ValueError("InvoiceNo e StockCode são obrigatórios")
            
            # ================================================================
            # ETAPA 2: CONVERSÃO SEGURA DE TIPOS
            # ================================================================
            
            # 🔄 Por que converter tipos?
            # - Dados do CSV vêm como string
            # - Precisamos de números para cálculos
            # - .get(chave, valor_padrão) evita erros se chave não existir
            
            venda = {
                # Strings: mantemos como texto
                'invoice_no': str(registro['InvoiceNo']),
                'stock_code': str(registro['StockCode']),
                'description': str(registro.get('Description', '')),  # '' se vazio
                
                # Números inteiros: int(float()) para lidar com "1.0"
                'quantity': int(float(registro.get('Quantity', 0))),
                
                # Datas: mantemos como string por simplicidade
                'invoice_date': str(registro.get('InvoiceDate', '')),
                
                # Números decimais: float() para preços
                'unit_price': float(registro.get('UnitPrice', 0)),
                
                # IDs: podem estar vazios, mantemos como string
                'customer_id': str(registro.get('CustomerID', '')),
                'country': str(registro.get('Country', '')),
                
                # Cálculo do total: quantidade × preço unitário
                'total': int(float(registro.get('Quantity', 0))) * float(registro.get('UnitPrice', 0))
            }
            
            # ================================================================
            # ETAPA 3: ADICIONAR À ESTRUTURA PRINCIPAL
            # ================================================================
            
            # 📝 Adicionar à lista de vendas
            # - append() adiciona ao final da lista
            # - Mantém ordem cronológica das vendas
            self.vendas.append(venda)
            
            # ================================================================
            # ETAPA 4: ATUALIZAR ESTRUTURAS AUXILIARES
            # ================================================================
            
            # 🔄 Por que atualizar outras estruturas?
            # - Mantém consistência dos dados
            # - Permite buscas rápidas por produto, cliente, país
            # - Atualiza estatísticas automaticamente
            
            self._atualizar_produto(venda)   # Atualiza dicionário de produtos
            self._atualizar_cliente(venda)   # Atualiza dicionário de clientes  
            self._atualizar_pais(venda)      # Atualiza dicionário de países
            
            return True  # ✅ Sucesso!
            
        except (ValueError, TypeError) as e:
            # ================================================================
            # TRATAMENTO DE EXCEÇÕES
            # ================================================================
            
            # 🚑 Por que capturar exceções?
            # - ValueError: dados inválidos (ex: string em campo numérico)
            # - TypeError: tipos incompatíveis
            # - Evita que o programa pare completamente
            
            print(f"Erro ao adicionar venda: {e}")
            return False  # ❌ Falhou!
    
    def _atualizar_produto(self, venda: Dict[str, Any]):
        """
          Método Privado para Atualizar Produtos
        
        O underscore (_) indica que é um método privado:
        - Só deve ser chamado internamente pela classe
        - Não faz parte da interface pública
        - Convenção Python para organização
        """
        
        # ================================================================
        # ETAPA 1: IDENTIFICAR O PRODUTO
        # ================================================================
        
        # Extrair o código do produto da venda atual
        stock_code = venda['stock_code']
        
        # ================================================================
        # ETAPA 2: VERIFICAR SE PRODUTO JÁ EXISTE
        # ================================================================
        
        # 🔍 Por que verificar?
        # - Primeira venda de um produto: criar entrada nova
        # - Vendas subsequentes: apenas atualizar totais
        
        if stock_code not in self.produtos:
            # 🆕 PRODUTO NOVO: criar entrada inicial
            self.produtos[stock_code] = {
                'description': venda['description'],  # Nome do produto
                'vendas_total': 0,                   # Contador de vendas
                'quantidade_total': 0,               # Soma das quantidades
                'receita_total': 0.0                 # Soma dos valores
            }
        
        # ================================================================
        # ETAPA 3: ATUALIZAR ESTATÍSTICAS DO PRODUTO
        # ================================================================
        
        # Referência ao produto no dicionário (para facilitar acesso)
        produto = self.produtos[stock_code]
        
        # 📊 Incrementar contadores:
        produto['vendas_total'] += 1                    # +1 venda
        produto['quantidade_total'] += venda['quantity'] # +quantidade vendida
        produto['receita_total'] += venda['total']      # +valor da venda
        
        # ================================================================
        # ETAPA 4: ATUALIZAR CONTADOR ESPECIAL
        # ================================================================
        
        # 🏆 Counter para rankings automáticos
        # - Usado para encontrar produtos mais vendidos rapidamente
        # - Counter.most_common() já ordena por quantidade
        self.contador_produtos[stock_code] += venda['quantity']
    
    def _atualizar_cliente(self, venda: Dict[str, Any]):
        """
          Atualizando Dados de Clientes
        
        Demonstra:
        - Validação de dados antes de processar
        - Criação condicional de registros
        - Acumulação de estatísticas por cliente
        """
        
        # ================================================================
        # ETAPA 1: EXTRAIR E VALIDAR ID DO CLIENTE
        # ================================================================
        
        customer_id = venda['customer_id']
        
        # 🔍 Por que validar customer_id?
        # - Nem todas as vendas têm cliente identificado
        # - Vendas anônimas ou à vista podem ter ID vazio
        # - Evita criar entradas desnecessárias no dicionário
        
        if customer_id and customer_id != '':
            # ============================================================
            # ETAPA 2: VERIFICAR SE CLIENTE JÁ EXISTE
            # ============================================================
            
            if customer_id not in self.clientes:
                # 🆕 CLIENTE NOVO: criar perfil inicial
                self.clientes[customer_id] = {
                    'pais': venda['country'],          # País do cliente
                    'compras_total': 0,                # Número de compras
                    'quantidade_total': 0,             # Total de itens comprados
                    'gasto_total': 0.0                 # Total gasto pelo cliente
                }
            
            # ============================================================
            # ETAPA 3: ATUALIZAR PERFIL DO CLIENTE
            # ============================================================
            
            # Referência ao cliente (mais fácil que repetir self.clientes[customer_id])
            cliente = self.clientes[customer_id]
            
            # 📊 Acumular estatísticas:
            cliente['compras_total'] += 1                    # +1 compra
            cliente['quantidade_total'] += venda['quantity'] # +itens comprados
            cliente['gasto_total'] += venda['total']         # +valor gasto
    
    def _atualizar_pais(self, venda: Dict[str, Any]):
        """
          Atualizando Dados por País
        
        Demonstra:
        - Uso do defaultdict para evitar erros
        - Múltiplas estruturas para diferentes propósitos
        - Eficiência de contadores automáticos
        """
        
        # ================================================================
        # ETAPA 1: EXTRAIR E VALIDAR PAÍS
        # ================================================================
        
        pais = venda['country']
        
        # 🌍 Por que validar país?
        # - Alguns registros podem ter país vazio
        # - Evita processamento desnecessário
        
        if pais:
            # ============================================================
            # ETAPA 2: ADICIONAR VENDA À LISTA DO PAÍS
            # ============================================================
            
            # 📝 Por que usar defaultdict(list)?
            # - Se país não existe, cria lista vazia automaticamente
            # - Sem defaultdict, precisaríamos: if pais not in self.paises: self.paises[pais] = []
            # - append() adiciona o número da fatura à lista do país
            self.paises[pais].append(venda['invoice_no'])
            
            # ============================================================
            # ETAPA 3: INCREMENTAR CONTADOR DO PAÍS
            # ============================================================
            
            # 📈 Por que usar Counter?
            # - Conta automaticamente vendas por país
            # - Counter[pais] += 1 incrementa o contador
            # - Método .most_common() já ordena por quantidade
            self.contador_vendas_pais[pais] += 1


# ============================================================================
# CLASSE ECOMMERCECRUDE - Operações CRUD (Create, Read, Update, Delete)
# ============================================================================

class EcommerceCRUD:
    """
      Operações CRUD em Memória
    
    CRUD são as 4 operações básicas de qualquer sistema de dados:
    
    🆕 CREATE (Criar):
    - Adicionar novos registros ao sistema
    - Validar dados antes de inserir
    
    🔍 READ (Ler):
    - Buscar registros existentes
    - Filtrar por diferentes critérios
    - Listar todos os dados
    
    ✏️ UPDATE (Atualizar):
    - Modificar registros existentes
    - Manter consistência dos dados
    
    🗑️ DELETE (Deletar):
    - Remover registros do sistema
    - Confirmações de segurança
    
    💡 CONCEITO: Separação de Responsabilidades
    - Esta classe SÓ cuida das operações CRUD
    - Não se preocupa com interface ou relatórios
    - Reutilizável em diferentes contextos
    """
    
    def __init__(self, data_structure: DataStructure):
        """
        🏗️ CONSTRUTOR
        
        Recebe uma instância de DataStructure para trabalhar.
        Isso é chamado de "Composição" - uma classe usa outra.
        
        Args:
            data_structure: Objeto que contém todas as estruturas de dados
        """
        # Guardar referência para as estruturas de dados
        # Assim podemos acessar vendas, produtos, clientes, etc.
        self.data = data_structure
    
    # ========================================================================
    # 🆕 CREATE - CRIAR NOVOS REGISTROS
    # ========================================================================
    
    def criar_venda(self, dados_venda: Dict[str, Any]) -> bool:
        """
          Operação CREATE do CRUD
        
        Demonstra:
        - Delegação de responsabilidades
        - Tratamento de exceções em alto nível
        - Retorno consistente (bool)
        
        Args:
            dados_venda: Dicionário com dados da nova venda
            
        Returns:
            bool: True se criou com sucesso, False se falhou
        """
        try:
            # 🔄 DELEGAÇÃO:
            # - Esta classe não implementa a lógica de adição
            # - Delega para o método especializado em DataStructure
            # - Mantém responsabilidades separadas
            return self.data.adicionar_venda(dados_venda)
            
        except Exception as e:
            # 🚑 TRATAMENTO DE EXCEÇÃO EM ALTO NÍVEL:
            # - Captura qualquer erro não tratado pelos métodos internos
            # - Fornece feedback ao usuário
            # - Evita que o programa pare
            print(f"Erro ao criar venda: {e}")
            return False
    
    # ========================================================================
    # 🔍 READ - LER/BUSCAR REGISTROS EXISTENTES
    # ========================================================================
    
    def buscar_venda_por_invoice(self, invoice_no: str) -> Optional[Dict[str, Any]]:
        """
          Operação READ - Busca Por Chave Primária
        
        Demonstra:
        - Busca linear em lista (algoritmo O(n))
        - Uso de Optional para indicar "pode não encontrar"
        - Retorno None quando não encontra
        
        Args:
            invoice_no: Número da fatura para buscar
            
        Returns:
            Optional[Dict]: Venda encontrada ou None
        """
        try:
            # 🔄 BUSCA LINEAR:
            # - Percorre toda a lista de vendas
            # - Compara cada invoice_no com o buscado
            # - Para quando encontra o primeiro match
            
            for venda in self.data.vendas:
                if venda['invoice_no'] == invoice_no:
                    return venda  # ✅ Encontrou!
            
            # Se chegou aqui, não encontrou nada
            return None  # ❌ Não encontrado
            
        except Exception as e:
            # 🚑 SEGURANÇA: sempre tratar erros em operações de busca
            print(f"Erro ao buscar venda: {e}")
            return None
    
    def buscar_vendas_por_produto(self, stock_code: str) -> List[Dict[str, Any]]:
        """
          Busca com Filtro - List Comprehension
        
        Demonstra:
        - List comprehension (sintaxe compacta do Python)
        - Filtro por critério específico
        - Retorno de lista (pode ter 0, 1 ou N resultados)
        
        Args:
            stock_code: Código do produto para filtrar
            
        Returns:
            List[Dict]: Lista de vendas do produto (pode estar vazia)
        """
        try:
            # 📜 LIST COMPREHENSION EXPLICADA:
            # Sintaxe: [expressão for item in lista if condição]
            # 
            # Equivale a:
            # resultado = []
            # for venda in self.data.vendas:
            #     if venda['stock_code'] == stock_code:
            #         resultado.append(venda)
            # return resultado
            
            return [venda for venda in self.data.vendas if venda['stock_code'] == stock_code]
            
        except Exception as e:
            print(f"Erro ao buscar vendas por produto: {e}")
            return []  # Lista vazia em caso de erro
    
    def buscar_vendas_por_pais(self, pais: str) -> List[Dict[str, Any]]:
        """
          Busca com Comparação Case-Insensitive
        
        Demonstra:
        - Comparação ignorando maiúsculas/minúsculas
        - Método .lower() para normalizar strings
        - Busca mais amigável ao usuário
        
        Args:
            pais: Nome do país (ex: "brasil", "Brasil", "BRASIL")
            
        Returns:
            List[Dict]: Vendas do país (qualquer capitalização)
        """
        try:
            # 🔤 COMPARAÇÃO CASE-INSENSITIVE:
            # - .lower() converte para minúsculas
            # - "Brasil".lower() == "brasil".lower() é True
            # - Usuário pode digitar "brasil", "Brasil" ou "BRASIL"
            
            return [venda for venda in self.data.vendas 
                   if venda['country'].lower() == pais.lower()]
                   
        except Exception as e:
            print(f"Erro ao buscar vendas por país: {e}")
            return []
    
    # ========================================================================
    # ✏️ UPDATE - ATUALIZAR REGISTROS EXISTENTES
    # ========================================================================
    
    def atualizar_venda(self, invoice_no: str, novos_dados: Dict[str, Any]) -> bool:
        """
          Operação UPDATE do CRUD
        
        Demonstra:
        - Busca com enumerate() para obter índice
        - Validação de campos permitidos (segurança)
        - Recalculo automático de campos derivados
        - Atualização parcial (só campos fornecidos)
        
        Args:
            invoice_no: Identificador da venda
            novos_dados: Dicionário com campos a atualizar
            
        Returns:
            bool: True se atualizou, False se não encontrou
        """
        try:
            # 🔢 ENUMERATE PARA OBTER ÍNDICE:
            # - enumerate(lista) retorna (index, item)
            # - Precisamos do índice para atualizar a posição correta
            
            for i, venda in enumerate(self.data.vendas):
                if venda['invoice_no'] == invoice_no:
                    
                    # ============================================================
                    # SEGURANÇA: Só PERMITIR CAMPOS ESPECÍFICOS
                    # ============================================================
                    
                    # 🔒 Por que restringir campos?
                    # - Evita modificação acidental de dados críticos
                    # - invoice_no nunca deve mudar (chave primária)
                    # - customer_id e country são dados históricos
                    
                    campos_permitidos = ['quantity', 'unit_price', 'description']
                    
                    for campo in campos_permitidos:
                        if campo in novos_dados:
                            # Atualizar apenas se campo foi fornecido
                            venda[campo] = novos_dados[campo]
                    
                    # ============================================================
                    # RECALCULAR CAMPOS DERIVADOS
                    # ============================================================
                    
                    # 📊 Por que recalcular?
                    # - Total depende de quantity e unit_price
                    # - Se qualquer um mudou, total deve ser atualizado
                    # - Mantém consistência dos dados
                    
                    venda['total'] = venda['quantity'] * venda['unit_price']
                    
                    return True  # ✅ Atualizou com sucesso
            
            return False  # ❌ Não encontrou a venda
            
        except Exception as e:
            print(f"Erro ao atualizar venda: {e}")
            return False
    
    # ========================================================================
    # 🗑️ DELETE - REMOVER REGISTROS
    # ========================================================================
    
    def deletar_venda(self, invoice_no: str) -> bool:
        """
          Operação DELETE do CRUD
        
        Demonstra:
        - Busca com enumerate() para deleção segura
        - Uso de del para remover item de lista
        - Deleção por índice (mais eficiente)
        
        ⚠️ ATENÇÃO: Esta operação é irreversível!
        
        Args:
            invoice_no: Identificador da venda a deletar
            
        Returns:
            bool: True se deletou, False se não encontrou
        """
        try:
            # 🔍 BUSCAR VENDA A DELETAR:
            for i, venda in enumerate(self.data.vendas):
                if venda['invoice_no'] == invoice_no:
                    
                    # ========================================================
                    # DELEÇÃO SEGURA POR ÍNDICE
                    # ========================================================
                    
                    # 🗑️ Por que del por índice?
                    # - del lista[index] é mais eficiente
                    # - lista.remove(item) precisa buscar o item novamente
                    # - Já temos o índice do enumerate()
                    
                    del self.data.vendas[i]
                    
                    return True  # ✅ Deletou com sucesso
            
            return False  # ❌ Não encontrou para deletar
            
        except Exception as e:
            print(f"Erro ao deletar venda: {e}")
            return False
    
    def listar_todas_vendas(self) -> List[Dict[str, Any]]:
        """
          Operação READ - Listar Todos
        
        Demonstra:
        - Acesso direto à estrutura de dados
        - Retorno de referência (não cópia)
        - Método simples mas essencial
        
        Returns:
            List[Dict]: Todas as vendas do sistema
        """
        # 📝 RETORNO DIRETO:
        # - Retorna a lista original (não uma cópia)
        # - Mais eficiente em memória
        # - Cuidado: modificações na lista retornada afetam os dados originais
        
        return self.data.vendas


# ============================================================================
# CLASSE RELATORIOSANALYTICS - Geração de Relatórios e Estatísticas
# ============================================================================

class RelatoriosAnalytics:
    """
      Análise de Dados e Relatórios
    
    Esta classe demonstra conceitos avançados de análise:
    
    📊 MÉDIAS E ESTATÍSTICAS:
    - Cálculos matemáticos com dados reais
    - Agregações e totalizações
    - Indicação de performance do negócio
    
    🏆 RANKINGS:
    - Ordenação de dados por critérios
    - Identificação de tops performers
    - Uso de algoritmos de ordenação
    
    🔍 FILTROS:
    - Seleção de dados por critérios
    - Segmentação de informações
    - Análise focada em subconjuntos
    
    📈 RELATÓRIOS DETALHADOS:
    - Combinação de múltiplas estatísticas
    - Visão holística dos dados
    - Suporte à tomada de decisão
    
    💡 PRINCÍPIO: Single Responsibility
    - Focada apenas em análises e relatórios
    - Não modifica dados, apenas consulta
    - Reaproveitável para diferentes visualizações
    """
    
    def __init__(self, data_structure: DataStructure):
        """
        🏗️ CONSTRUTOR
        
        Recebe as estruturas de dados para análise.
        Mantém separação entre dados e análise.
        """
        self.data = data_structure
    
    def calcular_medias(self) -> Dict[str, float]:
        """
          Cálculos Estatísticos Fundamentais
        
        Demonstra:
        - Validação antes de cálculos (evita divisão por zero)
        - Função sum() com generator expression
        - Agregações múltiplas de uma única passada
        - Retorno estruturado em dicionário
        
        Returns:
            Dict[str, float]: Métricas calculadas do negócio
        """
        try:
            # ================================================================
            # VALIDAÇÃO INICIAL
            # ================================================================
            
            # 🚑 Por que validar primeiro?
            # - Evita divisão por zero
            # - Retorna resultado consistente (dict vazio)
            # - Falha rápida se não há dados
            
            if not self.data.vendas:
                return {}  # Sem dados, sem cálculos
            
            # ================================================================
            # CÁLCULOS DE AGREGAÇÃO
            # ================================================================
            
            # 🔢 Contar total de vendas (base para todas as médias)
            total_vendas = len(self.data.vendas)
            
            # 💰 SOMA DE VALORES com Generator Expression:
            # sum(expressão for item in lista) é eficiente em memória
            # Não cria lista temporária, processa item por item
            soma_valores = sum(venda['total'] for venda in self.data.vendas)
            
            # 📦 Soma de quantidades vendidas
            soma_quantidades = sum(venda['quantity'] for venda in self.data.vendas)
            
            # ================================================================
            # RETORNO ESTRUTURADO
            # ================================================================
            
            # 📈 Por que retornar dicionário?
            # - Auto-documenta cada métrica
            # - Fácil de acessar: resultado['receita_total']
            # - Extensível (fácil adicionar novas métricas)
            
            return {
                # Média de receita por venda individual
                'receita_media_por_venda': soma_valores / total_vendas,
                
                # Média de itens por venda
                'quantidade_media_por_venda': soma_quantidades / total_vendas,
                
                # Preço médio dos produtos (recalculado para demonstração)
                'preco_medio_unitario': sum(venda['unit_price'] for venda in self.data.vendas) / total_vendas,
                
                # Totais absolutos (não são médias, mas úteis no contexto)
                'receita_total': soma_valores,
                'total_vendas': total_vendas
            }
            
        except Exception as e:
            # 🚑 Segurança: sempre tratar erros em cálculos
            print(f"Erro ao calcular médias: {e}")
            return {}  # Retorno consistente mesmo com erro
    
    def ranking_produtos_mais_vendidos(self, top_n: int = 10) -> List[Tuple[str, Dict[str, Any]]]:
        """
          Algoritmo de Ordenação e Rankings
        
        Demonstra:
        - Função sorted() para ordenação personalizada
        - Lambda functions para critérios de ordenação
        - Slicing de listas para limitar resultados
        - Trabalho com tuplas como retorno
        
        Args:
            top_n: Quantos produtos incluir no ranking (padrão 10)
            
        Returns:
            List[Tuple]: Lista de tuplas (stock_code, dados_produto)
        """
        try:
            # ================================================================
            # ALGORITMO DE ORDENAÇÃO PERSONALIZADA
            # ================================================================
            
            # 🔄 SORTED() COM KEY PERSONALIZADA:
            # - sorted() não modifica o dicionário original
            # - .items() retorna tuplas (chave, valor)
            # - lambda x: x[1]['quantidade_total'] define critério
            # - reverse=True para ordem decrescente (maior primeiro)
            
            produtos_ordenados = sorted(
                self.data.produtos.items(),  # Lista de tuplas (stock_code, dados)
                
                # 🎯 LAMBDA FUNCTION EXPLICADA:
                # x = (stock_code, dados_produto)
                # x[0] = stock_code (string)
                # x[1] = dados_produto (dicionário)
                # x[1]['quantidade_total'] = critério de ordenação
                key=lambda x: x[1]['quantidade_total'],
                
                reverse=True  # Decrescente: maior quantidade primeiro
            )
            
            # ================================================================
            # SLICING PARA LIMITAR RESULTADOS
            # ================================================================
            
            # 🔢 [:top_n] = pega os primeiros top_n elementos
            # Exemplo: [:5] pega os 5 primeiros
            # Se lista tem menos elementos, retorna todos
            
            return produtos_ordenados[:top_n]
            
        except Exception as e:
            print(f"Erro ao gerar ranking de produtos: {e}")
            return []  # Lista vazia em caso de erro
    
    def ranking_paises_por_vendas(self, top_n: int = 10) -> List[Tuple[str, int]]:
        """Gera ranking dos países por número de vendas"""
        try:
            return self.data.contador_vendas_pais.most_common(top_n)
        except Exception as e:
            print(f"Erro ao gerar ranking de países: {e}")
            return []
    
    def filtrar_vendas_por_valor(self, valor_minimo: float = 0, valor_maximo: float = float('inf')) -> List[Dict[str, Any]]:
        """Filtra vendas por faixa de valor"""
        try:
            return [
                venda for venda in self.data.vendas 
                if valor_minimo <= venda['total'] <= valor_maximo
            ]
        except Exception as e:
            print(f"Erro ao filtrar vendas por valor: {e}")
            return []
    
    def relatorio_por_pais(self, pais: str) -> Dict[str, Any]:
        """Gera relatório detalhado por país"""
        try:
            vendas_pais = [venda for venda in self.data.vendas if venda['country'].lower() == pais.lower()]
            
            if not vendas_pais:
                return {'erro': f'Nenhuma venda encontrada para {pais}'}
            
            receita_total = sum(venda['total'] for venda in vendas_pais)
            quantidade_total = sum(venda['quantity'] for venda in vendas_pais)
            
            produtos_unicos = set(venda['stock_code'] for venda in vendas_pais)
            clientes_unicos = set(venda['customer_id'] for venda in vendas_pais if venda['customer_id'])
            
            return {
                'pais': pais,
                'total_vendas': len(vendas_pais),
                'receita_total': receita_total,
                'quantidade_total': quantidade_total,
                'receita_media': receita_total / len(vendas_pais),
                'produtos_unicos': len(produtos_unicos),
                'clientes_unicos': len(clientes_unicos)
            }
        except Exception as e:
            print(f"Erro ao gerar relatório por país: {e}")
            return {'erro': str(e)}


# ============================================================================
# CLASSE EXPORTADORCSV - Exportação de Dados para Arquivos
# ============================================================================

class ExportadorCSV:
    """
      Manipulação de Arquivos e Exportação de Dados
    
    Esta classe demonstra conceitos fundamentais:
    
    📁 MANIPULAÇÃO DE ARQUIVOS:
    - Abertura e fechamento de arquivos
    - Context managers (with statement)
    - Encoding para caracteres especiais
    
    📊 FORMATO CSV:
    - Comma Separated Values (padrão universal)
    - Compatível com Excel, Google Sheets, etc.
    - Fácil de importar em outras ferramentas
    
    🔄 TRANSFORMAÇÃO DE DADOS:
    - Conversão de estruturas Python para CSV
    - Padronização de formatos
    - Tratamento de caracteres especiais
    
    🛠️ BIBLIOTECA CSV:
    - DictWriter para escrita estruturada
    - Geração automática de cabeçalhos
    - Escapamento automático de caracteres especiais
    

    """
    
    def __init__(self, data_structure: DataStructure):
        """
        🏗️ CONSTRUTOR
        
        Mantém referência aos dados para exportação.
        Separar exportação em classe própria é boa prática.
        """
        self.data = data_structure
    
    def exportar_vendas(self, nome_arquivo: str = 'vendas_export.csv') -> bool:
        """
          Exportação de Dados para CSV
        
        Demonstra:
        - Context manager (with statement)
        - Parâmetros de abertura de arquivo
        - Uso da biblioteca CSV do Python
        - Geração automática de cabeçalhos
        - Validação antes da exportação
        
        Args:
            nome_arquivo: Nome do arquivo CSV a criar
            
        Returns:
            bool: True se exportou com sucesso
        """
        try:
            # ================================================================
            # CONTEXT MANAGER - ABERTURA SEGURA DE ARQUIVO
            # ================================================================
            
            # 🔒 WITH STATEMENT:
            # - Garante fechamento automático do arquivo
            # - Mesmo se der erro, arquivo será fechado
            # - Equivale a: arquivo = open(...); try: ... finally: arquivo.close()
            
            with open(nome_arquivo, 'w', newline='', encoding='utf-8') as arquivo:
                #     ╰────────────────────────────────────────┐
                # 📄 PARÂMETROS DE ABERTURA EXPLICADOS:
                # - 'w': write mode (sobrescreve arquivo existente)
                # - newline='': evita linhas em branco extras no CSV
                # - encoding='utf-8': suporte a acentos e caracteres especiais
                
                # ============================================================
                # VALIDAÇÃO ANTES DE EXPORTAR
                # ============================================================
                
                if not self.data.vendas:
                    print("Nenhuma venda para exportar")
                    return False
                
                # ============================================================
                # CONFIGURAÇÃO DO DICTWRITER
                # ============================================================
                
                # 📝 FIELDNAMES AUTOMÁTICOS:
                # - Pega chaves do primeiro dicionário
                # - Assume que todos têm as mesmas chaves
                # - Cria colunas automaticamente
                fieldnames = self.data.vendas[0].keys()
                
                # 📊 DICTWRITER:
                # - Especializado em escrever dicionários como CSV
                # - Converte automaticamente valores para string
                # - Trata escaping de caracteres especiais
                writer = csv.DictWriter(arquivo, fieldnames=fieldnames)
                
                # ============================================================
                # ESCRITA DOS DADOS
                # ============================================================
                
                # 🏷️ Escrever cabeçalho (nomes das colunas)
                writer.writeheader()
                
                # 📝 Escrever todas as linhas de dados
                # writerows() escreve lista de dicionários de uma vez
                writer.writerows(self.data.vendas)
                
                # ============================================================
                # CONFIRMAÇÃO DE SUCESSO
                # ============================================================
                
                print(f"Vendas exportadas com sucesso para {nome_arquivo}")
                return True
                
        except Exception as e:
            # 🚑 Tratar erros de arquivo (permissão, espaço, etc.)
            print(f"Erro ao exportar vendas: {e}")
            return False
    
    def exportar_relatorio_produtos(self, nome_arquivo: str = 'produtos_relatorio.csv') -> bool:
        """Exporta relatório de produtos para CSV"""
        try:
            with open(nome_arquivo, 'w', newline='', encoding='utf-8') as arquivo:
                fieldnames = ['stock_code', 'description', 'vendas_total', 'quantidade_total', 'receita_total']
                writer = csv.DictWriter(arquivo, fieldnames=fieldnames)
                writer.writeheader()
                
                for stock_code, dados in self.data.produtos.items():
                    row = {'stock_code': stock_code, **dados}
                    writer.writerow(row)
                
                print(f"Relatório de produtos exportado para {nome_arquivo}")
                return True
                
        except Exception as e:
            print(f"Erro ao exportar relatório de produtos: {e}")
            return False
    
    def exportar_relatorio_paises(self, nome_arquivo: str = 'paises_relatorio.csv') -> bool:
        """Exporta relatório de países para CSV"""
        try:
            with open(nome_arquivo, 'w', newline='', encoding='utf-8') as arquivo:
                fieldnames = ['pais', 'total_vendas']
                writer = csv.DictWriter(arquivo, fieldnames=fieldnames)
                writer.writeheader()
                
                for pais, total in self.data.contador_vendas_pais.items():
                    writer.writerow({'pais': pais, 'total_vendas': total})
                
                print(f"Relatório de países exportado para {nome_arquivo}")
                return True
                
        except Exception as e:
            print(f"Erro ao exportar relatório de países: {e}")
            return False


# ============================================================================
# CLASSE ECOMMERCESYSTEM - Sistema Principal (Orquestrador)
# ============================================================================

class EcommerceSystem:
    """
      Padrão de Arquitetura - Facade e Composition
    
    Esta é a classe principal que demonstra:
    
    🏢 PADRÃO FACADE:
    - Interface simples para sistema complexo
    - Esconde complexidade das classes internas
    - Ponto único de acesso para funcionalidades
    
    🔧 COMPOSIÇÃO:
    - Usa outras classes como componentes
    - Cada classe tem responsabilidade específica
    - Sistema modular e manutenível
    
    💬 INTERFACE DE USUÁRIO:
    - Menus interativos
    - Validações de entrada
    - Feedback claro ao usuário
    
    🔄 FLUXO DE CONTROLE:
    - Coordena operações entre classes
    - Gerencia estado da aplicação
    - Trata exceções de alto nível
    
    💡 BENEFÍCIOS:
    - Código organizado e legível
    - Fácil manutenção e extensão
    - Reutilização de componentes
    - Testabilidade individual
    """
    
    def __init__(self):
        """
        🏗️ CONSTRUTOR - Inicialização do Sistema
        
        Demonstra:
        - Composição de objetos
        - Injeção de dependência manual
        - Estado inicial da aplicação
        """
        
        # ================================================================
        # INICIALIZAÇÃO DOS COMPONENTES
        # ================================================================
        
        # 📁 ESTRUTURA DE DADOS (componente central)
        self.data_structure = DataStructure()
        
        # 🔧 INJEÇÃO DE DEPENDÊNCIA:
        # - Todas as classes recebem a mesma instância de DataStructure
        # - Garante consistência entre componentes
        # - Compartilha os mesmos dados
        
        # 🔍 CRUD (operações básicas)
        self.crud = EcommerceCRUD(self.data_structure)
        
        # 📈 RELATÓRIOS (analíticas)
        self.relatorios = RelatoriosAnalytics(self.data_structure)
        
        # 💾 EXPORTADOR (arquivos)
        self.exportador = ExportadorCSV(self.data_structure)
        
        # ================================================================
        # CONTROLE DE ESTADO
        # ================================================================
        
        # 📊 FLAG DE CONTROLE:
        # - Impede operações sem dados carregados
        # - Melhora experiência do usuário
        # - Evita erros e confusão
        self.dataset_carregado = False
    
    def carregar_dataset_kaggle(self) -> bool:
        """
          Integração com APIs Externas e Processamento de Dados
        
        Demonstra:
        - Uso de bibliotecas de terceiros (kagglehub)
        - Manipulação de caminhos de arquivos
        - Leitura de CSV com DictReader
        - Processamento em lote com feedback
        - Tratamento de diferentes tipos de erro
        
        Returns:
            bool: True se carregou com sucesso
        """
        try:
            print("🔄 Carregando dataset do Kaggle...")
            
            # ================================================================
            # DOWNLOAD DO DATASET VIA API
            # ================================================================
            
            # 🌎 INTEGRAÇÃO COM KAGGLE:
            # - kagglehub é biblioteca oficial do Kaggle
            # - Faz download automático do dataset
            # - Retorna caminho onde salvou os arquivos
            caminho_dos_arquivos = kagglehub.dataset_download("carrie1/ecommerce-data")
            
            # ================================================================
            # EXPLORAÇÃO DOS ARQUIVOS BAIXADOS
            # ================================================================
            
            # 📁 LISTAR ARQUIVOS:
            print(f"📁 Arquivos encontrados em: {caminho_dos_arquivos}")
            arquivos = os.listdir(caminho_dos_arquivos)
            for arquivo in arquivos:
                print(f"   - {arquivo}")
            
            # ================================================================
            # CONSTRUÇÃO DO CAMINHO DO ARQUIVO
            # ================================================================
            
            # 🛤️ OS.PATH.JOIN:
            # - Une caminhos de forma compatível com o SO
            # - Evita problemas de portabilidade
            caminho_csv = os.path.join(caminho_dos_arquivos, "data.csv")
            
            # 🔍 VERIFICAÇÃO DE EXISTÊNCIA:
            if not os.path.exists(caminho_csv):
                raise FileNotFoundError(f"Arquivo data.csv não encontrado em {caminho_dos_arquivos}")
            
            print(f"📊 Carregando dados de: {caminho_csv}")
            
            # ================================================================
            # ABERTURA DO ARQUIVO CSV COM ENCODING LATIN-1
            # ================================================================
            
            # 💡 ENCODING LATIN-1:
            # - ISO-8859-1 (Europa Ocidental)
            # - Suporta caracteres especiais como £ (libra esterlina)
            # - Padrão para datasets de e-commerce britânicos
            # - Resolve o erro 'utf-8' codec can't decode byte 0xa3
            
            print("🔧 Abrindo arquivo com encoding latin-1...")
            arquivo_csv = open(caminho_csv, mode='r', encoding='latin-1')
            print("✅ Arquivo aberto com sucesso!")
            
            # ================================================================
            # PROCESSAMENTO DO ARQUIVO
            # ================================================================
            
            try:
                leitor_csv = csv.DictReader(arquivo_csv)
                
                # 📋 MOSTRAR ESTRUTURA DOS DADOS
                print("📋 Colunas encontradas:")
                for coluna in leitor_csv.fieldnames:
                    print(f"   - {coluna}")
                
                # ============================================================
                # PROCESSAMENTO EM LOTE COM FEEDBACK
                # ============================================================
                
                # 📈 CONTADORES PARA ESTATÍSTICAS:
                registros_carregados = 0
                registros_com_erro = 0
                registros_encoding_erro = 0  # Novo contador para erros de encoding
                
                # 🔄 PROCESSAMENTO LINHA POR LINHA COM TRATAMENTO DE ERRO:
                for numero_linha, registro in enumerate(leitor_csv, start=2):  # start=2 (cabeçalho = linha 1)
                    try:
                        # Tentar adicionar cada registro
                        if self.data_structure.adicionar_venda(registro):
                            registros_carregados += 1
                        else:
                            registros_com_erro += 1
                            
                    except UnicodeDecodeError as e:
                        # 🚨 ERRO DE ENCODING EM LINHA ESPECÍFICA:
                        # - Alguns caracteres podem ainda causar problemas
                        # - Registra erro mas continua processamento
                        registros_encoding_erro += 1
                        print(f"⚠️ Erro de encoding na linha {numero_linha}: {e}")
                        continue
                        
                    except Exception as e:
                        # 🚨 OUTROS ERROS DE PROCESSAMENTO:
                        registros_com_erro += 1
                        if registros_com_erro <= 5:  # Mostrar apenas primeiros 5 erros
                            print(f"⚠️ Erro na linha {numero_linha}: {e}")
                        continue
                    
                    # 📈 FEEDBACK DE PROGRESSO:
                    # - A cada 50.000 registros, mostra progresso
                    # - Usuário sabe que sistema não travou
                    # - Útil para datasets grandes
                    if registros_carregados % 50000 == 0 and registros_carregados > 0:
                        print(f"   ✅ {registros_carregados} registros carregados...")
                
                # ============================================================
                # RELATÓRIO FINAL DE CARREGAMENTO COM ENCODING
                # ============================================================
                
                print(f"✅ Dataset carregado com sucesso!")
                print(f"   🎯 Encoding usado: latin-1")
                print(f"   📈 Total de vendas: {registros_carregados}")
                print(f"   📦 Total de produtos: {len(self.data_structure.produtos)}")
                print(f"   👥 Total de clientes: {len(self.data_structure.clientes)}")
                print(f"   🌍 Total de países: {len(self.data_structure.paises)}")
                
                # ⚠️ RELATÓRIO DE PROBLEMAS:
                if registros_com_erro > 0:
                    print(f"   ⚠️  Registros com erro de dados: {registros_com_erro}")
                if registros_encoding_erro > 0:
                    print(f"   🔤 Registros com erro de encoding: {registros_encoding_erro}")
                

                print(f"   📖 Isso é comum em dados de países que usam caracteres especiais como £")
                print(f"   🌍 Latin-1 resolve problemas com símbolos monetários europeus")
                
                # ============================================================
                # ATUALIZAR ESTADO DO SISTEMA
                # ============================================================
                
                self.dataset_carregado = True
                return True
                
            except Exception as e:
                # 🚨 ERRO DURANTE PROCESSAMENTO:
                print(f"❌ Erro durante processamento: {e}")
                return False
                
            finally:
                # ============================================================
                # LIMPEZA: FECHAR ARQUIVO SEMPRE
                # ============================================================
                
                # 🧹 FINALLY sempre executa:
                # - Mesmo se der erro, arquivo será fechado
                # - Evita vazamentos de recursos
                # - Boa prática de programação
                if arquivo_csv:
                    arquivo_csv.close()
                    print("🔒 Arquivo fechado com segurança")
                
        except FileNotFoundError as e:
            # 📁 Erro específico de arquivo
            print(f"❌ Arquivo não encontrado: {e}")
            return False
        except Exception as e:
            # 🚑 Qualquer outro erro
            print(f"❌ Erro ao carregar dataset: {e}")
            return False
    
    def mostrar_menu_principal(self):
        """Mostra o menu principal do sistema"""
        print("\n" + "="*60)
        print("🛒 SISTEMA DE ANÁLISE DE E-COMMERCE")
        print("="*60)
        print("1. 📊 Carregar Dataset do Kaggle")
        print("2. 🔍 Operações CRUD")
        print("3. 📈 Relatórios e Análises")
        print("4. 💾 Exportar Dados (CSV)")
        print("5. 📋 Visualizar Dados")
        print("0. 🚪 Sair")
        print("="*60)
    
    def menu_crud(self):
        """Menu para operações CRUD"""
        while True:
            print("\n" + "-"*40)
            print("🔍 OPERAÇÕES CRUD")
            print("-"*40)
            print("1. ➕ Criar Nova Venda")
            print("2. 🔎 Buscar Venda")
            print("3. ✏️  Atualizar Venda")
            print("4. 🗑️  Deletar Venda")
            print("5. 📋 Listar Todas Vendas")
            print("0. ⬅️  Voltar")
            print("-"*40)
            
            opcao = input("Digite sua opção: ").strip()
            
            if opcao == '1':
                self._criar_nova_venda()
            elif opcao == '2':
                self._buscar_venda()
            elif opcao == '3':
                self._atualizar_venda()
            elif opcao == '4':
                self._deletar_venda()
            elif opcao == '5':
                self._listar_vendas()
            elif opcao == '0':
                break
            else:
                print("❌ Opção inválida!")
    
    def _criar_nova_venda(self):
        """Interface para criar nova venda"""
        try:
            print("\n➕ CRIAR NOVA VENDA")
            print("-" * 30)
            
            dados_venda = {}
            dados_venda['InvoiceNo'] = input("Número da Fatura: ")
            dados_venda['StockCode'] = input("Código do Produto: ")
            dados_venda['Description'] = input("Descrição: ")
            dados_venda['Quantity'] = input("Quantidade: ")
            dados_venda['UnitPrice'] = input("Preço Unitário: ")
            dados_venda['CustomerID'] = input("ID do Cliente: ")
            dados_venda['Country'] = input("País: ")
            dados_venda['InvoiceDate'] = datetime.now().strftime("%m/%d/%Y %H:%M")
            
            if self.crud.criar_venda(dados_venda):
                print("✅ Venda criada com sucesso!")
            else:
                print("❌ Erro ao criar venda!")
                
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    def _buscar_venda(self):
        """Interface para buscar venda"""
        try:
            invoice_no = input("Digite o número da fatura: ")
            venda = self.crud.buscar_venda_por_invoice(invoice_no)
            
            if venda:
                print("\n✅ Venda encontrada:")
                self._exibir_venda(venda)
            else:
                print("❌ Venda não encontrada!")
                
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    def _atualizar_venda(self):
        """Interface para atualizar venda"""
        try:
            invoice_no = input("Digite o número da fatura para atualizar: ")
            venda = self.crud.buscar_venda_por_invoice(invoice_no)
            
            if not venda:
                print("❌ Venda não encontrada!")
                return
            
            print("\n📝 Venda atual:")
            self._exibir_venda(venda)
            
            print("\n✏️ Digite os novos valores (Enter para manter atual):")
            novos_dados = {}
            
            novo_qty = input(f"Quantidade atual ({venda['quantity']}): ")
            if novo_qty.strip():
                novos_dados['quantity'] = int(novo_qty)
            
            novo_price = input(f"Preço atual ({venda['unit_price']}): ")
            if novo_price.strip():
                novos_dados['unit_price'] = float(novo_price)
            
            nova_desc = input(f"Descrição atual ({venda['description']}): ")
            if nova_desc.strip():
                novos_dados['description'] = nova_desc
            
            if novos_dados and self.crud.atualizar_venda(invoice_no, novos_dados):
                print("✅ Venda atualizada com sucesso!")
            else:
                print("❌ Nenhuma alteração realizada!")
                
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    def _deletar_venda(self):
        """Interface para deletar venda"""
        try:
            invoice_no = input("Digite o número da fatura para deletar: ")
            venda = self.crud.buscar_venda_por_invoice(invoice_no)
            
            if not venda:
                print("❌ Venda não encontrada!")
                return
            
            print("\n🗑️ Venda a ser deletada:")
            self._exibir_venda(venda)
            
            confirmacao = input("\n⚠️ Confirma a exclusão? (s/N): ").lower()
            if confirmacao == 's':
                if self.crud.deletar_venda(invoice_no):
                    print("✅ Venda deletada com sucesso!")
                else:
                    print("❌ Erro ao deletar venda!")
            else:
                print("❌ Operação cancelada!")
                
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    def _listar_vendas(self):
        """Interface para listar vendas"""
        try:
            vendas = self.crud.listar_todas_vendas()
            
            if not vendas:
                print("❌ Nenhuma venda encontrada!")
                return
            
            print(f"\n📋 Total de vendas: {len(vendas)}")
            
            # Opção de paginação
            pagina = 0
            itens_por_pagina = 10
            
            while True:
                inicio = pagina * itens_por_pagina
                fim = inicio + itens_por_pagina
                vendas_pagina = vendas[inicio:fim]
                
                if not vendas_pagina:
                    print("❌ Fim da lista!")
                    break
                
                print(f"\n📄 Página {pagina + 1} (itens {inicio + 1}-{min(fim, len(vendas))} de {len(vendas)}):")
                print("-" * 80)
                
                for venda in vendas_pagina:
                    print(f"🧾 {venda['invoice_no']} | {venda['stock_code']} | "
                          f"{venda['description'][:30]}... | Qtd: {venda['quantity']} | "
                          f"Total: R$ {venda['total']:.2f}")
                
                if fim >= len(vendas):
                    break
                
                continuar = input("\n➡️ Próxima página? (s/N): ").lower()
                if continuar != 's':
                    break
                
                pagina += 1
                
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    def _exibir_venda(self, venda: Dict[str, Any]):
        """Exibe uma venda formatada"""
        print("-" * 50)
        print(f"🧾 Fatura: {venda['invoice_no']}")
        print(f"📦 Produto: {venda['stock_code']} - {venda['description']}")
        print(f"📊 Quantidade: {venda['quantity']}")
        print(f"💰 Preço Unitário: R$ {venda['unit_price']:.2f}")
        print(f"💳 Total: R$ {venda['total']:.2f}")
        print(f"👤 Cliente: {venda['customer_id']}")
        print(f"🌍 País: {venda['country']}")
        print(f"📅 Data: {venda['invoice_date']}")
        print("-" * 50)
    
    def menu_relatorios(self):
        """Menu para relatórios e análises"""
        while True:
            print("\n" + "-"*40)
            print("📈 RELATÓRIOS E ANÁLISES")
            print("-"*40)
            print("1. 📊 Médias Gerais")
            print("2. 🏆 Ranking Produtos Mais Vendidos")
            print("3. 🌍 Ranking Países por Vendas")
            print("4. 💰 Filtrar por Faixa de Valor")
            print("5. 🇧🇷 Relatório por País")
            print("0. ⬅️ Voltar")
            print("-"*40)
            
            opcao = input("Digite sua opção: ").strip()
            
            if opcao == '1':
                self._mostrar_medias()
            elif opcao == '2':
                self._mostrar_ranking_produtos()
            elif opcao == '3':
                self._mostrar_ranking_paises()
            elif opcao == '4':
                self._filtrar_por_valor()
            elif opcao == '5':
                self._relatorio_por_pais()
            elif opcao == '0':
                break
            else:
                print("❌ Opção inválida!")
    
    def _mostrar_medias(self):
        """Mostra médias gerais do sistema"""
        try:
            if not self.dataset_carregado:
                print("❌ Carregue o dataset primeiro!")
                return
            
            medias = self.relatorios.calcular_medias()
            
            if not medias:
                print("❌ Nenhum dado disponível!")
                return
            
            print("\n📊 MÉDIAS GERAIS")
            print("=" * 50)
            print(f"💰 Receita Total: R$ {medias['receita_total']:,.2f}")
            print(f"🛒 Total de Vendas: {medias['total_vendas']:,}")
            print(f"📈 Receita Média por Venda: R$ {medias['receita_media_por_venda']:.2f}")
            print(f"📦 Quantidade Média por Venda: {medias['quantidade_media_por_venda']:.2f}")
            print(f"💵 Preço Médio Unitário: R$ {medias['preco_medio_unitario']:.2f}")
            print("=" * 50)
            
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    def _mostrar_ranking_produtos(self):
        """Mostra ranking de produtos mais vendidos"""
        try:
            if not self.dataset_carregado:
                print("❌ Carregue o dataset primeiro!")
                return
            
            top_n = int(input("Quantos produtos mostrar (padrão 10): ") or "10")
            ranking = self.relatorios.ranking_produtos_mais_vendidos(top_n)
            
            if not ranking:
                print("❌ Nenhum produto encontrado!")
                return
            
            print(f"\n🏆 TOP {top_n} PRODUTOS MAIS VENDIDOS")
            print("=" * 80)
            
            for i, (stock_code, dados) in enumerate(ranking, 1):
                print(f"{i:2d}. 📦 {stock_code}")
                print(f"     📝 {dados['description'][:50]}...")
                print(f"     📊 Qtd Vendida: {dados['quantidade_total']:,}")
                print(f"     💰 Receita: R$ {dados['receita_total']:,.2f}")
                print(f"     🛒 Nº Vendas: {dados['vendas_total']:,}")
                print("-" * 80)
                
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    def _mostrar_ranking_paises(self):
        """Mostra ranking de países por vendas"""
        try:
            if not self.dataset_carregado:
                print("❌ Carregue o dataset primeiro!")
                return
            
            top_n = int(input("Quantos países mostrar (padrão 10): ") or "10")
            ranking = self.relatorios.ranking_paises_por_vendas(top_n)
            
            if not ranking:
                print("❌ Nenhum país encontrado!")
                return
            
            print(f"\n🌍 TOP {top_n} PAÍSES POR VENDAS")
            print("=" * 50)
            
            for i, (pais, total_vendas) in enumerate(ranking, 1):
                print(f"{i:2d}. 🏳️ {pais:<20} | 🛒 {total_vendas:,} vendas")
            
            print("=" * 50)
                
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    def _filtrar_por_valor(self):
        """Filtra vendas por faixa de valor"""
        try:
            if not self.dataset_carregado:
                print("❌ Carregue o dataset primeiro!")
                return
            
            valor_min = float(input("Valor mínimo (0): ") or "0")
            valor_max = float(input("Valor máximo (sem limite): ") or "inf")
            
            vendas_filtradas = self.relatorios.filtrar_vendas_por_valor(valor_min, valor_max)
            
            if not vendas_filtradas:
                print("❌ Nenhuma venda encontrada nesta faixa!")
                return
            
            print(f"\n💰 VENDAS ENTRE R$ {valor_min:.2f} E R$ {valor_max:.2f}")
            print("=" * 80)
            print(f"📊 Total encontrado: {len(vendas_filtradas)} vendas")
            
            receita_total = sum(venda['total'] for venda in vendas_filtradas)
            print(f"💰 Receita Total: R$ {receita_total:,.2f}")
            print(f"📈 Receita Média: R$ {receita_total / len(vendas_filtradas):.2f}")
            
            # Mostrar algumas vendas
            mostrar_detalhes = input("\n🔍 Mostrar vendas detalhadas? (s/N): ").lower()
            if mostrar_detalhes == 's':
                for i, venda in enumerate(vendas_filtradas[:20]):  # Máximo 20
                    print(f"\n{i+1}. 🧾 {venda['invoice_no']} | {venda['stock_code']} | "
                          f"Total: R$ {venda['total']:.2f}")
                
                if len(vendas_filtradas) > 20:
                    print(f"\n... e mais {len(vendas_filtradas) - 20} vendas")
                
        except ValueError:
            print("❌ Valor inválido!")
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    def _relatorio_por_pais(self):
        """Gera relatório detalhado por país"""
        try:
            if not self.dataset_carregado:
                print("❌ Carregue o dataset primeiro!")
                return
            
            pais = input("Digite o nome do país: ").strip()
            if not pais:
                print("❌ Nome do país é obrigatório!")
                return
            
            relatorio = self.relatorios.relatorio_por_pais(pais)
            
            if 'erro' in relatorio:
                print(f"❌ {relatorio['erro']}")
                return
            
            print(f"\n🇧🇷 RELATÓRIO - {relatorio['pais'].upper()}")
            print("=" * 60)
            print(f"🛒 Total de Vendas: {relatorio['total_vendas']:,}")
            print(f"💰 Receita Total: R$ {relatorio['receita_total']:,.2f}")
            print(f"📦 Quantidade Total: {relatorio['quantidade_total']:,}")
            print(f"📈 Receita Média: R$ {relatorio['receita_media']:.2f}")
            print(f"🎯 Produtos Únicos: {relatorio['produtos_unicos']:,}")
            print(f"👥 Clientes Únicos: {relatorio['clientes_unicos']:,}")
            print("=" * 60)
                
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    def menu_exportacao(self):
        """Menu para exportação de dados"""
        while True:
            print("\n" + "-"*40)
            print("💾 EXPORTAR DADOS (CSV)")
            print("-"*40)
            print("1. 📊 Exportar Todas as Vendas")
            print("2. 📦 Exportar Relatório de Produtos")
            print("3. 🌍 Exportar Relatório de Países")
            print("0. ⬅️ Voltar")
            print("-"*40)
            
            opcao = input("Digite sua opção: ").strip()
            
            if opcao == '1':
                nome_arquivo = input("Nome do arquivo (vendas_export.csv): ") or "vendas_export.csv"
                self.exportador.exportar_vendas(nome_arquivo)
            elif opcao == '2':
                nome_arquivo = input("Nome do arquivo (produtos_relatorio.csv): ") or "produtos_relatorio.csv"
                self.exportador.exportar_relatorio_produtos(nome_arquivo)
            elif opcao == '3':
                nome_arquivo = input("Nome do arquivo (paises_relatorio.csv): ") or "paises_relatorio.csv"
                self.exportador.exportar_relatorio_paises(nome_arquivo)
            elif opcao == '0':
                break
            else:
                print("❌ Opção inválida!")
    
    def menu_visualizacao(self):
        """Menu para visualização de dados"""
        while True:
            print("\n" + "-"*40)
            print("📋 VISUALIZAR DADOS")
            print("-"*40)
            print("1. 📈 Estatísticas Gerais")
            print("2. 📦 Lista de Produtos")
            print("3. 👥 Lista de Clientes")
            print("4. 🌍 Lista de Países")
            print("5. 🔍 Buscar por Produto")
            print("6. 🔍 Buscar por País")
            print("0. ⬅️ Voltar")
            print("-"*40)
            
            opcao = input("Digite sua opção: ").strip()
            
            if opcao == '1':
                self._mostrar_estatisticas_gerais()
            elif opcao == '2':
                self._listar_produtos()
            elif opcao == '3':
                self._listar_clientes()
            elif opcao == '4':
                self._listar_paises()
            elif opcao == '5':
                self._buscar_por_produto()
            elif opcao == '6':
                self._buscar_por_pais()
            elif opcao == '0':
                break
            else:
                print("❌ Opção inválida!")
    
    def _mostrar_estatisticas_gerais(self):
        """Mostra estatísticas gerais do sistema"""
        if not self.dataset_carregado:
            print("❌ Carregue o dataset primeiro!")
            return
        
        print("\n📈 ESTATÍSTICAS GERAIS")
        print("=" * 50)
        print(f"🛒 Total de Vendas: {len(self.data_structure.vendas):,}")
        print(f"📦 Total de Produtos: {len(self.data_structure.produtos):,}")
        print(f"👥 Total de Clientes: {len(self.data_structure.clientes):,}")
        print(f"🌍 Total de Países: {len(self.data_structure.paises):,}")
        print("=" * 50)
    
    def _listar_produtos(self):
        """Lista produtos cadastrados"""
        if not self.data_structure.produtos:
            print("❌ Nenhum produto encontrado!")
            return
        
        produtos = list(self.data_structure.produtos.items())
        pagina = 0
        itens_por_pagina = 10
        
        while True:
            inicio = pagina * itens_por_pagina
            fim = inicio + itens_por_pagina
            produtos_pagina = produtos[inicio:fim]
            
            if not produtos_pagina:
                print("❌ Fim da lista!")
                break
            
            print(f"\n📦 PRODUTOS - Página {pagina + 1}")
            print("-" * 80)
            
            for stock_code, dados in produtos_pagina:
                print(f"🏷️ {stock_code} | {dados['description'][:40]}...")
                print(f"   📊 Vendas: {dados['vendas_total']} | "
                      f"Qtd: {dados['quantidade_total']} | "
                      f"Receita: R$ {dados['receita_total']:.2f}")
                print("-" * 80)
            
            if fim >= len(produtos):
                break
            
            continuar = input("\n➡️ Próxima página? (s/N): ").lower()
            if continuar != 's':
                break
            
            pagina += 1
    
    def _listar_clientes(self):
        """Lista clientes cadastrados"""
        if not self.data_structure.clientes:
            print("❌ Nenhum cliente encontrado!")
            return
        
        print(f"\n👥 CLIENTES ({len(self.data_structure.clientes)} total)")
        print("-" * 80)
        
        # Mostrar os 20 primeiros clientes
        for i, (customer_id, dados) in enumerate(list(self.data_structure.clientes.items())[:20]):
            print(f"👤 {customer_id} | {dados['pais']} | "
                  f"Compras: {dados['compras_total']} | "
                  f"Gasto: R$ {dados['gasto_total']:.2f}")
        
        if len(self.data_structure.clientes) > 20:
            print(f"\n... e mais {len(self.data_structure.clientes) - 20} clientes")
    
    def _listar_paises(self):
        """Lista países cadastrados"""
        if not self.data_structure.paises:
            print("❌ Nenhum país encontrado!")
            return
        
        print(f"\n🌍 PAÍSES ({len(self.data_structure.paises)} total)")
        print("-" * 50)
        
        for pais, vendas in self.data_structure.paises.items():
            total_vendas = len(vendas)
            print(f"🏳️ {pais:<30} | 🛒 {total_vendas:,} vendas")
    
    def _buscar_por_produto(self):
        """Busca vendas por produto"""
        try:
            stock_code = input("Digite o código do produto: ").strip()
            if not stock_code:
                print("❌ Código do produto é obrigatório!")
                return
            
            vendas = self.crud.buscar_vendas_por_produto(stock_code)
            
            if not vendas:
                print("❌ Nenhuma venda encontrada para este produto!")
                return
            
            # Informações do produto
            if stock_code in self.data_structure.produtos:
                produto = self.data_structure.produtos[stock_code]
                print(f"\n📦 PRODUTO: {stock_code}")
                print(f"📝 Descrição: {produto['description']}")
                print(f"📊 Total de Vendas: {len(vendas)}")
                print(f"🔢 Quantidade Total: {produto['quantidade_total']}")
                print(f"💰 Receita Total: R$ {produto['receita_total']:.2f}")
                print("-" * 60)
            
            # Mostrar algumas vendas
            for i, venda in enumerate(vendas[:10]):  # Máximo 10
                print(f"{i+1}. 🧾 {venda['invoice_no']} | "
                      f"Qtd: {venda['quantity']} | "
                      f"Total: R$ {venda['total']:.2f} | "
                      f"{venda['country']}")
            
            if len(vendas) > 10:
                print(f"\n... e mais {len(vendas) - 10} vendas")
                
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    def _buscar_por_pais(self):
        """Busca vendas por país"""
        try:
            pais = input("Digite o nome do país: ").strip()
            if not pais:
                print("❌ Nome do país é obrigatório!")
                return
            
            vendas = self.crud.buscar_vendas_por_pais(pais)
            
            if not vendas:
                print("❌ Nenhuma venda encontrada para este país!")
                return
            
            print(f"\n🌍 VENDAS EM {pais.upper()}")
            print(f"📊 Total de Vendas: {len(vendas)}")
            
            receita_total = sum(venda['total'] for venda in vendas)
            print(f"💰 Receita Total: R$ {receita_total:,.2f}")
            print("-" * 60)
            
            # Mostrar algumas vendas
            for i, venda in enumerate(vendas[:10]):  # Máximo 10
                print(f"{i+1}. 🧾 {venda['invoice_no']} | "
                      f"{venda['stock_code']} | "
                      f"Total: R$ {venda['total']:.2f}")
            
            if len(vendas) > 10:
                print(f"\n... e mais {len(vendas) - 10} vendas")
                
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    def executar(self):
        """
          Loop Principal de Aplicação (Event Loop)
        
        Demonstra:
        - Loop infinito controlado
        - Tratamento de entrada do usuário
        - Estrutura de menu interativo
        - Validação de estado (dataset carregado)
        - Tratamento de interrupções (Ctrl+C)
        - Recuperação graceful de erros
        """
        # ================================================================
        # MENSAGEM DE BOAS-VINDAS
        # ================================================================
        
        print("🎉 Bem-vindo ao Sistema de Análise de E-commerce!")
        
        # ================================================================
        # LOOP PRINCIPAL DA APLICAÇÃO
        # ================================================================
        
        # 🔄 WHILE TRUE - Loop Infinito Controlado:
        # - Continua até usuário escolher sair (break)
        # - Permite navegação contínua pelos menus
        # - Retorna ao menu principal após cada operação
        
        while True:
            try:
                # ============================================================
                # APRESENTAÇÃO DO MENU E CAPTURA DA OPÇÃO
                # ============================================================
                
                self.mostrar_menu_principal()
                
                # 📝 INPUT COM LIMPEZA:
                # - .strip() remove espaços em branco das bordas
                # - Evita erros por espaços acidentais
                opcao = input("\nDigite sua opção: ").strip()
                
                # ============================================================
                # ROTEAMENTO DE OPÇÕES (DISPATCHER PATTERN)
                # ============================================================
                
                if opcao == '1':
                    # 📊 CARREGAR DADOS:
                    # - Única opção que não precisa de dataset
                    # - Ponto de entrada do sistema
                    self.carregar_dataset_kaggle()
                    
                elif opcao == '2':
                    # 🔍 OPERAÇÕES CRUD:
                    if self.dataset_carregado:
                        self.menu_crud()
                    else:
                        print("❌ É necessário carregar o dataset primeiro!")
                        
                elif opcao == '3':
                    # 📈 RELATÓRIOS:
                    if self.dataset_carregado:
                        self.menu_relatorios()
                    else:
                        print("❌ É necessário carregar o dataset primeiro!")
                        
                elif opcao == '4':
                    # 💾 EXPORTAÇÃO:
                    if self.dataset_carregado:
                        self.menu_exportacao()
                    else:
                        print("❌ É necessário carregar o dataset primeiro!")
                        
                elif opcao == '5':
                    # 📋 VISUALIZAÇÃO:
                    if self.dataset_carregado:
                        self.menu_visualizacao()
                    else:
                        print("❌ É necessário carregar o dataset primeiro!")
                        
                elif opcao == '0':
                    # 🚪 SAÍDA CONTROLADA:
                    print("👋 Obrigado por usar o sistema!")
                    break  # Sai do loop while, encerrando o programa
                    
                else:
                    # ❌ VALIDAÇÃO DE ENTRADA:
                    print("❌ Opção inválida!")
                
            except KeyboardInterrupt:
                # ================================================================
                # TRATAMENTO DE INTERRUPÇÃO (CTRL+C)
                # ================================================================
                
                # ⚡ KEYBOARD INTERRUPT:
                # - Usuário pressionou Ctrl+C
                # - Encerração forçada mas controlada
                # - Mensagem amigável em vez de erro críptico
                
                print("\n\n👋 Sistema encerrado pelo usuário!")
                break
                
            except Exception as e:
                # ================================================================
                # RECUPERAÇÃO GRACEFUL DE ERROS
                # ================================================================
                
                # 🚑 TRATAMENTO DE ERROS INESPERADOS:
                # - Mostra o erro para depuração
                # - NÃO encerra o programa
                # - Volta ao menu principal
                # - Sistema continua operável
                
                print(f"❌ Erro inesperado: {e}")
                print("ℹ️ O sistema continuará funcionando...")


# ============================================================================
# FUNÇÃO PRINCIPAL E PONTO DE ENTRADA
# ============================================================================

def main():
    """
      Função Principal e Tratamento de Erros Globais
    
    Demonstra:
    - Ponto de entrada estruturado
    - Tratamento de exceções em nível de aplicação
    - Saída controlada do programa
    - Separação entre lógica e execução
    """
    try:
        # ================================================================
        # INICIALIZAÇÃO DO SISTEMA
        # ================================================================
        
        # 🚀 INSTANCIAÇÃO:
        # - Cria o sistema principal
        # - Todos os componentes são inicializados automaticamente
        # - Estado inicial limpo e consistente
        sistema = EcommerceSystem()
        
        # 🎨 EXECUÇÃO DA INTERFACE:
        # - Delega controle para o sistema
        # - Loop principal de interação com usuário
        # - Menus, validações, operações
        sistema.executar()
        
    except Exception as e:
        # ================================================================
        # TRATAMENTO DE ERROS FATAIS
        # ================================================================
        
        # 🚑 CAPTURA DE ÚNIMA INSTÂNCIA:
        # - Erros que não foram tratados em lugar nenhum
        # - Problemas de inicialização do sistema
        # - Falhas críticas de infraestrutura
        
        print(f"❌ Erro fatal: {e}")
        
        # 🚪 SAÍDA CONTROLADA:
        # - sys.exit(1) indica erro para o sistema operacional
        # - Código 1 = erro | Código 0 = sucesso
        # - Útil para scripts e automação
        sys.exit(1)


# ============================================================================
# PONTO DE ENTRADA DO PROGRAMA
# ============================================================================

if __name__ == "__main__":
    """
      Condição de Execução Principal
    
    __name__ == "__main__" significa:
    - Este arquivo está sendo executado diretamente (python app.py)
    - Não está sendo importado como módulo
    
    💡 UTILIDADE:
    - Permite reutilizar código como biblioteca
    - import app não executa o sistema automaticamente
    - from app import EcommerceSystem funciona sem efeitos colaterais
    
    🎯 PADRÃO PYTHON:
    - Convenção universal em Python
    - Boa prática de desenvolvimento
    - Facilita testes e reutilização
    """
    main()  # Chama a função principal

