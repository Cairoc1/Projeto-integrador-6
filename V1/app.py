import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import requests
from datetime import datetime
import threading
import json
import re

class AgroTechApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🌱 AgroTech - Seletor Inteligente de Sementes")
        self.root.geometry("1100x750")
        self.root.configure(bg="#f0fdf4")
        
        # API Key
        self.API_KEY = "01cff47d321d789bd5933fe3bfe1c7db"
        
        # Banco de dados EXPANDIDO de sementes
        self.BANCO_SEMENTES = {
            "tomate": [
                {
                    "nome": "Tomate Cereja",
                    "clima_ideal": {"min_temp": 18, "max_temp": 28},
                    "detalhes": "Ideal para climas amenos, produz frutos doces e pequenos. Perfeito para saladas.",
                    "irrigacao": "Moderada - 2-3 vezes por semana",
                    "epoca": "Primavera/Verão",
                    "performance": "95% em condições ideais",
                    "sol": "Pleno sol",
                    "ciclo": "75-90 dias",
                    "dificuldade": "Fácil"
                },
                {
                    "nome": "Tomate Italiano",
                    "clima_ideal": {"min_temp": 20, "max_temp": 30},
                    "detalhes": "Perfeito para molhos, adapta-se bem ao calor. Frutos carnudos.",
                    "irrigacao": "Frequente - 3-4 vezes por semana",
                    "epoca": "Verão",
                    "performance": "90% em climas quentes",
                    "sol": "Pleno sol",
                    "ciclo": "80-100 dias",
                    "dificuldade": "Médio"
                },
                {
                    "nome": "Tomate Santa Cruz",
                    "clima_ideal": {"min_temp": 15, "max_temp": 25},
                    "detalhes": "Tradicional brasileiro, versátil e produtivo. Ideal para mesas.",
                    "irrigacao": "Moderada - 2 vezes por semana",
                    "epoca": "Ano todo em estufa",
                    "performance": "85% em diversas condições",
                    "sol": "Meia sombra a pleno sol",
                    "ciclo": "90-110 dias",
                    "dificuldade": "Fácil"
                },
                {
                    "nome": "Tomate Débora",
                    "clima_ideal": {"min_temp": 16, "max_temp": 26},
                    "detalhes": "Resistente a doenças, alto rendimento. Frutos firmes.",
                    "irrigacao": "Moderada - 2-3 vezes por semana",
                    "epoca": "Primavera/Outono",
                    "performance": "88% em solo fértil",
                    "sol": "Pleno sol",
                    "ciclo": "85-95 dias",
                    "dificuldade": "Médio"
                }
            ],
            "alface": [
                {
                    "nome": "Alface Crespa",
                    "clima_ideal": {"min_temp": 10, "max_temp": 22},
                    "detalhes": "Folhas frisadas e crocantes, ideal para climas amenos.",
                    "irrigacao": "Frequente - solo sempre úmido",
                    "epoca": "Outono/Inverno",
                    "performance": "98% em climas frios",
                    "sol": "Meia sombra",
                    "ciclo": "45-60 dias",
                    "dificuldade": "Fácil"
                },
                {
                    "nome": "Alface Americana",
                    "clima_ideal": {"min_temp": 12, "max_temp": 24},
                    "detalhes": "Folhas macias e cabeça compacta. Ideal para sanduíches.",
                    "irrigacao": "Frequente - regas diárias em calor",
                    "epoca": "Inverno/Primavera",
                    "performance": "92% com irrigação constante",
                    "sol": "Meia sombra",
                    "ciclo": "55-70 dias",
                    "dificuldade": "Médio"
                },
                {
                    "nome": "Alface Roxa",
                    "clima_ideal": {"min_temp": 14, "max_temp": 26},
                    "detalhes": "Rica em antioxidantes, cor vibrante. Tolera mais calor.",
                    "irrigacao": "Moderada - 3-4 vezes por semana",
                    "epoca": "Primavera/Verão",
                    "performance": "85% em climas variados",
                    "sol": "Meia sombra a pleno sol",
                    "ciclo": "50-65 dias",
                    "dificuldade": "Fácil"
                }
            ],
            "cenoura": [
                {
                    "nome": "Cenoura Brasília",
                    "clima_ideal": {"min_temp": 8, "max_temp": 25},
                    "detalhes": "Raiz cilíndrica e lisa, adaptada ao clima tropical.",
                    "irrigacao": "Moderada - evitar encharcamento",
                    "epoca": "Outono/Inverno/Primavera",
                    "performance": "92% em solo arenoso",
                    "sol": "Pleno sol",
                    "ciclo": "85-100 dias",
                    "dificuldade": "Médio"
                },
                {
                    "nome": "Cenoura Nantes",
                    "clima_ideal": {"min_temp": 10, "max_temp": 22},
                    "detalhes": "Sabor adocicado, textura macia. Ideal para consumo fresco.",
                    "irrigacao": "Moderada - solo bem drenado",
                    "epoca": "Inverno/Primavera",
                    "performance": "90% em clima ameno",
                    "sol": "Pleno sol",
                    "ciclo": "70-80 dias",
                    "dificuldade": "Fácil"
                }
            ],
            "feijão": [
                {
                    "nome": "Feijão Carioca",
                    "clima_ideal": {"min_temp": 18, "max_temp": 30},
                    "detalhes": "Tradicional brasileiro, grão rajado. Alta produtividade.",
                    "irrigacao": "Moderada - 2 vezes por semana",
                    "epoca": "Primavera/Verão",
                    "performance": "95% em clima tropical",
                    "sol": "Pleno sol",
                    "ciclo": "75-90 dias",
                    "dificuldade": "Fácil"
                },
                {
                    "nome": "Feijão Preto",
                    "clima_ideal": {"min_temp": 20, "max_temp": 32},
                    "detalhes": "Grão popular no sul do Brasil. Rico em proteínas.",
                    "irrigacao": "Moderada - tolera seca",
                    "epoca": "Verão",
                    "performance": "88% em clima quente",
                    "sol": "Pleno sol",
                    "ciclo": "85-100 dias",
                    "dificuldade": "Fácil"
                }
            ],
            "milho": [
                {
                    "nome": "Milho Verde",
                    "clima_ideal": {"min_temp": 22, "max_temp": 35},
                    "detalhes": "Ideal para consumo fresco. Espigas doces e macias.",
                    "irrigacao": "Frequente - precisa de muita água",
                    "epoca": "Primavera/Verão",
                    "performance": "90% em solo fértil",
                    "sol": "Pleno sol",
                    "ciclo": "80-100 dias",
                    "dificuldade": "Médio"
                },
                {
                    "nome": "Milho Pipoca",
                    "clima_ideal": {"min_temp": 20, "max_temp": 32},
                    "detalhes": "Grãos pequenos e duros, ideais para estourar.",
                    "irrigacao": "Moderada - 2-3 vezes por semana",
                    "epoca": "Verão",
                    "performance": "85% em clima seco",
                    "sol": "Pleno sol",
                    "ciclo": "95-110 dias",
                    "dificuldade": "Médio"
                }
            ],
            "couve": [
                {
                    "nome": "Couve Manteiga",
                    "clima_ideal": {"min_temp": 15, "max_temp": 25},
                    "detalhes": "Folhas largas e macias. Tradicional na culinária brasileira.",
                    "irrigacao": "Frequente - solo úmido",
                    "epoca": "Ano todo",
                    "performance": "95% em clima ameno",
                    "sol": "Meia sombra a pleno sol",
                    "ciclo": "60-80 dias",
                    "dificuldade": "Fácil"
                }
            ],
            "repolho": [
                {
                    "nome": "Repolho Verde",
                    "clima_ideal": {"min_temp": 12, "max_temp": 22},
                    "detalhes": "Cabeça compacta, folhas firmes. Ideal para saladas.",
                    "irrigacao": "Frequente - solo sempre úmido",
                    "epoca": "Outono/Inverno",
                    "performance": "90% em clima frio",
                    "sol": "Pleno sol",
                    "ciclo": "70-90 dias",
                    "dificuldade": "Médio"
                }
            ],
            "beterraba": [
                {
                    "nome": "Beterraba Early Wonder",
                    "clima_ideal": {"min_temp": 10, "max_temp": 24},
                    "detalhes": "Raiz redonda e vermelha intensa. Ciclo rápido.",
                    "irrigacao": "Moderada - solo bem drenado",
                    "epoca": "Outono/Inverno/Primavera",
                    "performance": "88% em solo profundo",
                    "sol": "Pleno sol",
                    "ciclo": "55-65 dias",
                    "dificuldade": "Fácil"
                }
            ],
            "pepino": [
                {
                    "nome": "Pepino Aodai",
                    "clima_ideal": {"min_temp": 20, "max_temp": 32},
                    "detalhes": "Frutos médios, casca fina. Ideal para saladas.",
                    "irrigacao": "Frequente - muita água",
                    "epoca": "Primavera/Verão",
                    "performance": "92% em clima quente",
                    "sol": "Pleno sol",
                    "ciclo": "50-60 dias",
                    "dificuldade": "Médio"
                }
            ],
            "abobrinha": [
                {
                    "nome": "Abobrinha Italiana",
                    "clima_ideal": {"min_temp": 18, "max_temp": 30},
                    "detalhes": "Frutos cilíndricos e tenros. Alta produtividade.",
                    "irrigacao": "Frequente - solo úmido",
                    "epoca": "Primavera/Verão",
                    "performance": "90% em solo rico",
                    "sol": "Pleno sol",
                    "ciclo": "45-55 dias",
                    "dificuldade": "Fácil"
                }
            ],
            "pimentão": [
                {
                    "nome": "Pimentão Amarelo",
                    "clima_ideal": {"min_temp": 20, "max_temp": 30},
                    "detalhes": "Frutos doces e coloridos. Rico em vitamina C.",
                    "irrigacao": "Moderada - 3 vezes por semana",
                    "epoca": "Primavera/Verão",
                    "performance": "85% em clima quente",
                    "sol": "Pleno sol",
                    "ciclo": "80-100 dias",
                    "dificuldade": "Médio"
                }
            ],
            "berinjela": [
                {
                    "nome": "Berinjela Comprida",
                    "clima_ideal": {"min_temp": 22, "max_temp": 32},
                    "detalhes": "Frutos roxos longos. Ideal para assar e cozinhar.",
                    "irrigacao": "Moderada - tolera seca",
                    "epoca": "Verão",
                    "performance": "88% em clima tropical",
                    "sol": "Pleno sol",
                    "ciclo": "85-100 dias",
                    "dificuldade": "Médio"
                }
            ],
            "cebola": [
                {
                    "nome": "Cebola Baia Periforme",
                    "clima_ideal": {"min_temp": 12, "max_temp": 25},
                    "detalhes": "Bulbo arredondado, sabor suave. Boa conservação.",
                    "irrigacao": "Moderada - reduzir na colheita",
                    "epoca": "Outono/Inverno",
                    "performance": "90% em solo arenoso",
                    "sol": "Pleno sol",
                    "ciclo": "120-150 dias",
                    "dificuldade": "Médio"
                }
            ],
            "alho": [
                {
                    "nome": "Alho Nobre",
                    "clima_ideal": {"min_temp": 8, "max_temp": 20},
                    "detalhes": "Bulbo com dentes grandes. Sabor intenso.",
                    "irrigacao": "Moderada - pouco no final",
                    "epoca": "Outono/Inverno",
                    "performance": "85% em clima frio",
                    "sol": "Pleno sol",
                    "ciclo": "120-140 dias",
                    "dificuldade": "Médio"
                }
            ],
            "batata": [
                {
                    "nome": "Batata Asterix",
                    "clima_ideal": {"min_temp": 15, "max_temp": 25},
                    "detalhes": "Ideal para fritar e cozinhar. Resistente a doenças.",
                    "irrigacao": "Moderada - evitar excesso",
                    "epoca": "Inverno/Primavera",
                    "performance": "92% em solo bem drenado",
                    "sol": "Pleno sol",
                    "ciclo": "100-120 dias",
                    "dificuldade": "Médio"
                }
            ],
            "morango": [
                {
                    "nome": "Morango Oso Grande",
                    "clima_ideal": {"min_temp": 10, "max_temp": 25},
                    "detalhes": "Frutos grandes e doces. Produz o ano todo em estufa.",
                    "irrigacao": "Frequente - gotejamento ideal",
                    "epoca": "Outono/Primavera",
                    "performance": "88% em solo ácido",
                    "sol": "Pleno sol",
                    "ciclo": "90-120 dias",
                    "dificuldade": "Alta"
                }
            ]
        }
        
        self.setup_ui()
    
    def setup_ui(self):
        # Header
        header_frame = tk.Frame(self.root, bg="#10b981", height=100)
        header_frame.pack(fill=tk.X, padx=20, pady=10)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="🌱 AgroTech", 
                              font=("Arial", 24, "bold"), 
                              bg="#10b981", fg="white")
        title_label.pack(pady=20)
        
        subtitle_label = tk.Label(header_frame, 
                                 text="Seletor Inteligente de Sementes - Cultivando o Futuro", 
                                 font=("Arial", 12), 
                                 bg="#10b981", fg="white")
        subtitle_label.pack()
        
        # Main Container
        main_container = tk.Frame(self.root, bg="#f0fdf4")
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Left Frame - Inputs
        left_frame = tk.Frame(main_container, bg="white", relief=tk.RAISED, bd=2)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Form Title
        form_title = tk.Label(left_frame, text="📋 Informações do Plantio", 
                             font=("Arial", 14, "bold"), 
                             bg="white", fg="#1f2937")
        form_title.pack(pady=20)
        
        # Cultura Input
        cultura_frame = tk.Frame(left_frame, bg="white")
        cultura_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(cultura_frame, text="🌿 O que você quer plantar?", 
                font=("Arial", 10, "bold"), bg="white").pack(anchor=tk.W)
        
        self.cultura_var = tk.StringVar()
        culturas = list(self.BANCO_SEMENTES.keys())
        cultura_combo = ttk.Combobox(cultura_frame, 
                                    textvariable=self.cultura_var,
                                    values=culturas,
                                    font=("Arial", 11),
                                    state="readonly")
        cultura_combo.pack(fill=tk.X, pady=5)
        cultura_combo.set("tomate")
        
        # Localização Input
        local_frame = tk.Frame(left_frame, bg="white")
        local_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(local_frame, text="📍 Sua localização", 
                font=("Arial", 10, "bold"), bg="white").pack(anchor=tk.W)
        
        self.local_var = tk.StringVar()
        local_entry = tk.Entry(local_frame, 
                              textvariable=self.local_var,
                              font=("Arial", 11),
                              relief=tk.SOLID,
                              bd=1)
        local_entry.pack(fill=tk.X, pady=5)
        local_entry.insert(0, "São Paulo")
        
        # Sugestões de cidades
        cidades_frame = tk.Frame(left_frame, bg="white")
        cidades_frame.pack(fill=tk.X, padx=20, pady=5)
        
        tk.Label(cidades_frame, text="🏙️ Cidades sugeridas:", 
                font=("Arial", 9, "bold"), bg="white").pack(anchor=tk.W)
        
        cidades_btn_frame = tk.Frame(cidades_frame, bg="white")
        cidades_btn_frame.pack(fill=tk.X, pady=5)
        
        cidades = ["São Paulo", "Rio de Janeiro", "Belo Horizonte", "Brasília", 
                  "Curitiba", "Porto Alegre", "Salvador", "Fortaleza"]
        
        for i, cidade in enumerate(cidades):
            btn = tk.Button(cidades_btn_frame, text=cidade, 
                          font=("Arial", 8),
                          command=lambda c=cidade: self.local_var.set(c),
                          relief=tk.GROOVE,
                          bg="#e5e7eb")
            btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        # Search Button
        search_btn = tk.Button(left_frame, 
                              text="🔍 Buscar Recomendações", 
                              font=("Arial", 12, "bold"),
                              bg="#3b82f6",
                              fg="white",
                              relief=tk.FLAT,
                              command=self.buscar_recomendacoes,
                              cursor="hand2")
        search_btn.pack(fill=tk.X, padx=20, pady=20)
        
        # Progress Bar
        self.progress = ttk.Progressbar(left_frame, mode='indeterminate')
        self.progress.pack(fill=tk.X, padx=20, pady=5)
        
        # Right Frame - Results
        self.right_frame = tk.Frame(main_container, bg="#f8fafc")
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Results Notebook (Abas)
        self.notebook = ttk.Notebook(self.right_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Clima Tab
        self.clima_tab = tk.Frame(self.notebook, bg="#f8fafc")
        self.notebook.add(self.clima_tab, text="🌤️ Condições Climáticas")
        
        # Recomendações Tab
        self.recomendacoes_tab = tk.Frame(self.notebook, bg="#f8fafc")
        self.notebook.add(self.recomendacoes_tab, text="🌿 Recomendações")
        
        # Dicas Tab
        self.dicas_tab = tk.Frame(self.notebook, bg="#f8fafc")
        self.notebook.add(self.dicas_tab, text="💡 Dicas de Plantio")
        
        # Status Bar
        self.status_var = tk.StringVar(value="Pronto para buscar...")
        status_bar = tk.Label(self.root, textvariable=self.status_var,
                             relief=tk.SUNKEN, anchor=tk.W, bg="#e5e7eb")
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def buscar_recomendacoes(self):
        cultura = self.cultura_var.get()
        localizacao = self.local_var.get().strip()
        
        if not cultura or not localizacao:
            messagebox.showwarning("Atenção", "Preencha todos os campos!")
            return
        
        # Limpar caracteres especiais e formatar
        localizacao = self.formatar_localizacao(localizacao)
        
        # Iniciar loading
        self.progress.start()
        self.status_var.set(f"Buscando clima para {localizacao}...")
        
        # Executar em thread separada
        thread = threading.Thread(target=self.processar_busca, 
                                 args=(cultura, localizacao))
        thread.daemon = True
        thread.start()
    
    def formatar_localizacao(self, localizacao):
        """Formata a localização para a API"""
        # Remover caracteres especiais e múltiplos espaços
        localizacao = re.sub(r'[^\w\s,]', '', localizacao)
        localizacao = re.sub(r'\s+', ' ', localizacao).strip()
        
        # Se não tem vírgula, assumir que é só cidade
        if ',' not in localizacao:
            # Adicionar país para melhor precisão
            localizacao += ",BR"  # Brasil como padrão
        
        return localizacao.title()
    
    def processar_busca(self, cultura, localizacao):
        try:
            # Buscar dados climáticos
            condicoes = self.get_clima_real(localizacao)
            
            if 'error' in condicoes:
                self.root.after(0, lambda: self.mostrar_erro(condicoes['error']))
                return
            
            # Buscar recomendações
            recomendacoes = self.get_variedades_sementes(cultura, condicoes)
            
            # Buscar dicas
            dicas = self.get_dicas_plantio(cultura, condicoes)
            
            # Atualizar interface
            self.root.after(0, lambda: self.mostrar_resultados(
                cultura, localizacao, condicoes, recomendacoes, dicas
            ))
            
        except Exception as e:
            self.root.after(0, lambda: self.mostrar_erro(f"Erro inesperado: {str(e)}"))
    
    def get_clima_real(self, localizacao):
        """Consulta a API OpenWeatherMap com tratamento melhorado de erros"""
        try:
            # Primeiro tentar geocoding direto
            geocoding_url = f"http://api.openweathermap.org/geo/1.0/direct?q={localizacao}&limit=1&appid={self.API_KEY}"
            
            response_geo = requests.get(geocoding_url, timeout=15)
            
            if response_geo.status_code != 200:
                return {"error": f"Erro na API: {response_geo.status_code}"}
            
            geo_data = response_geo.json()

            if not geo_data:
                # Tentar sem o país se falhou
                cidade_base = localizacao.split(',')[0].strip()
                geocoding_url = f"http://api.openweathermap.org/geo/1.0/direct?q={cidade_base}&limit=1&appid={self.API_KEY}"
                response_geo = requests.get(geocoding_url, timeout=15)
                geo_data = response_geo.json()
                
                if not geo_data:
                    return {"error": f"📍 Cidade '{localizacao}' não encontrada. Tente: 'São Paulo' ou 'Rio de Janeiro, BR'"}

            lat = geo_data[0]['lat']
            lon = geo_data[0]['lon']
            nome_cidade = geo_data[0].get('name', localizacao.split(',')[0])
            pais = geo_data[0].get('country', 'BR')

            # Buscar dados climáticos
            weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={self.API_KEY}&units=metric&lang=pt_br"
            
            response_weather = requests.get(weather_url, timeout=15)
            
            if response_weather.status_code != 200:
                return {"error": "Erro ao obter dados climáticos"}

            weather_data = response_weather.json()

            # Extrair dados
            temperatura = weather_data['main']['temp']
            temp_min = weather_data['main']['temp_min']
            temp_max = weather_data['main']['temp_max']
            descricao_clima = weather_data['weather'][0]['description'].title()
            umidade = weather_data['main']['humidity']
            vento = weather_data['wind']['speed']
            pressao = weather_data['main']['pressure']

            return {
                "temperatura": f"{temperatura:.1f}°C",
                "temp_min": f"{temp_min:.1f}°C",
                "temp_max": f"{temp_max:.1f}°C",
                "pluviosidade": descricao_clima,
                "umidade": f"{umidade}%",
                "vento": f"{vento} m/s",
                "pressao": f"{pressao} hPa",
                "cidade": nome_cidade,
                "pais": pais,
                "atualizacao": datetime.now().strftime("%d/%m/%Y %H:%M")
            }

        except requests.exceptions.Timeout:
            return {"error": "⏰ Tempo de conexão esgotado. Verifique sua internet."}
        except requests.exceptions.ConnectionError:
            return {"error": "🌐 Sem conexão com a internet. Verifique sua rede."}
        except requests.exceptions.RequestException as e:
            return {"error": f"🔧 Erro na requisição: {str(e)}"}
        except Exception as e:
            return {"error": f"❌ Erro inesperado: {str(e)}"}
    
    def get_variedades_sementes(self, cultura, condicoes_locais):
        """Sistema inteligente de recomendação"""
        if 'error' in condicoes_locais:
            return []
            
        cultura = cultura.lower().strip()
        
        try:
            temp_str = condicoes_locais.get('temperatura', '20°C')
            temp_celsius = float(temp_str.replace("°C", "").strip())
        except:
            temp_celsius = 20  # Valor padrão se houver erro
        
        # Busca no banco de sementes
        variedades = self.BANCO_SEMENTES.get(cultura, [])
        
        if not variedades:
            return [{
                "nome": f"Cultura '{cultura}' Não Encontrada",
                "detalhes": f"Tente: {', '.join(list(self.BANCO_SEMENTES.keys())[:3])}...",
                "irrigacao": "-",
                "epoca": "-",
                "performance": "-",
                "sol": "-",
                "ciclo": "-",
                "dificuldade": "-",
                "score": 0
            }]

        # Calcula score para cada variedade
        recomendacoes_com_score = []
        for variedade in variedades:
            try:
                temp_ideal_min = variedade['clima_ideal']['min_temp']
                temp_ideal_max = variedade['clima_ideal']['max_temp']
                
                # Calcula score de compatibilidade (0-100)
                if temp_ideal_min <= temp_celsius <= temp_ideal_max:
                    score = 100 - (abs(temp_celsius - (temp_ideal_min + temp_ideal_max)/2) * 2)
                elif temp_celsius < temp_ideal_min:
                    score = max(0, 100 - (temp_ideal_min - temp_celsius) * 5)
                else:
                    score = max(0, 100 - (temp_celsius - temp_ideal_max) * 5)
                
                variedade_com_score = variedade.copy()
                variedade_com_score['score'] = max(0, min(100, int(score)))
                recomendacoes_com_score.append(variedade_com_score)
            except:
                # Se houver erro no cálculo, dá score padrão
                variedade_com_score = variedade.copy()
                variedade_com_score['score'] = 50
                recomendacoes_com_score.append(variedade_com_score)

        # Ordena por score e retorna as melhores
        recomendacoes_com_score.sort(key=lambda x: x['score'], reverse=True)
        return recomendacoes_com_score[:4]  # Retorna até 4 melhores
    
    def get_dicas_plantio(self, cultura, condicoes_locais):
        """Fornece dicas personalizadas"""
        if 'error' in condicoes_locais:
            return ["⚠️ Não foi possível obter dicas específicas devido a erro no clima"]
            
        dicas = []
        
        try:
            temp_str = condicoes_locais.get('temperatura', '20°C')
            temp_celsius = float(temp_str.replace("°C", "").strip())
            umidade = int(condicoes_locais.get('umidade', '50%').replace('%', '').strip())
        except:
            temp_celsius = 20
            umidade = 50
        
        # Dicas baseadas na temperatura
        if temp_celsius > 30:
            dicas.append("🌡️ Cuidado com o calor: Regue no início da manhã ou final da tarde")
            dicas.append("☀️ Proteja as plantas com sombreamento parcial")
        elif temp_celsius > 25:
            dicas.append("🌤️ Clima quente ideal: Boa época para crescimento")
        elif temp_celsius < 10:
            dicas.append("❄️ Proteja do frio: Use estufa ou cobertura térmica")
            dicas.append("⏰ Reduza regas: O solo demora mais para secar no frio")
        elif temp_celsius < 15:
            dicas.append("🍂 Clima frio: Plantas de inverno se desenvolvem melhor")
        
        # Dicas baseadas na umidade
        if umidade < 40:
            dicas.append("💧 Umidade baixa: Aumente a frequência de regas")
            dicas.append("🌫️ Considere pulverizar água nas folhas pela manhã")
        elif umidade > 80:
            dicas.append("🌧️ Umidade alta: Cuidado com fungos - evite regar à noite")
            dicas.append("🍄 Use fungicida natural como prevenção")
        
        # Dicas baseadas na previsão
        if "chuva" in condicoes_locais.get('pluviosidade', '').lower():
            dicas.append("☔ Previsão de chuva: Suspenda a irrigação hoje")
            dicas.append("🌱 Aproveite para fazer adubação foliar")
        elif "sol" in condicoes_locais.get('pluviosidade', '').lower():
            dicas.append("☀️ Dia de sol: Ideal para fotossíntese e crescimento")
        
        # Dicas específicas por cultura
        cultura_lower = cultura.lower()
        if "tomate" in cultura_lower:
            dicas.append("🍅 Para tomates: Tutoramento é essencial para melhor produção")
            dicas.append("🌿 Retire os brotos laterais (ladrões) regularmente")
        elif "alface" in cultura_lower:
            dicas.append("🥬 Para alface: Colha pela manhã para maior crocância")
            dicas.append("💧 Mantenha o solo sempre úmido mas não encharcado")
        elif "cenoura" in cultura_lower:
            dicas.append("🥕 Para cenouras: Solo arenoso e profundo é ideal")
            dicas.append("🌱 Desbaste as mudinhas para dar espaço às raízes")
        elif "feijão" in cultura_lower:
            dicas.append("🫘 Para feijão: Plante em local com boa circulação de ar")
        elif "milho" in cultura_lower:
            dicas.append("🌽 Para milho: Plante em blocos para melhor polinização")
        
        # Dica geral se não tiver muitas
        if len(dicas) < 3:
            dicas.append("🌱 Verifique a acidez do solo periodicamente")
            dicas.append("💚 Rotação de culturas previne doenças")
        
        return dicas
    
    def mostrar_resultados(self, cultura, localizacao, condicoes, recomendacoes, dicas):
        self.progress.stop()
        self.status_var.set("Busca concluída!")
        
        self.atualizar_aba_clima(condicoes)
        self.atualizar_aba_recomendacoes(cultura, recomendacoes)
        self.atualizar_aba_dicas(dicas)
        
        messagebox.showinfo("Sucesso", f"Recomendações encontradas para {cultura} em {condicoes['cidade']}!")
    
    def atualizar_aba_clima(self, condicoes):
        for widget in self.clima_tab.winfo_children():
            widget.destroy()
        
        canvas = tk.Canvas(self.clima_tab, bg="#f8fafc")
        scrollbar = ttk.Scrollbar(self.clima_tab, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Card do clima
        clima_card = tk.Frame(scrollable_frame, bg="white", relief=tk.RAISED, bd=1)
        clima_card.pack(fill=tk.X, padx=10, pady=10)
        
        header_frame = tk.Frame(clima_card, bg="#3b82f6")
        header_frame.pack(fill=tk.X)
        
        tk.Label(header_frame, text=f"🌤️ Clima em {condicoes['cidade']}, {condicoes['pais']}", 
                font=("Arial", 16, "bold"), bg="#3b82f6", fg="white").pack(pady=10)
        
        content_frame = tk.Frame(clima_card, bg="white")
        content_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # Temperatura principal
        temp_frame = tk.Frame(content_frame, bg="white")
        temp_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(temp_frame, text=condicoes['temperatura'], 
                font=("Arial", 32, "bold"), bg="white").pack(side=tk.LEFT)
        
        tk.Label(temp_frame, text=condicoes['pluviosidade'], 
                font=("Arial", 14), bg="white", fg="#6b7280").pack(side=tk.LEFT, padx=20)
        
        # Informações detalhadas
        info_frame = tk.Frame(content_frame, bg="white")
        info_frame.pack(fill=tk.X)
        
        infos = [
            ("📊 Mín/Máx", f"{condicoes['temp_min']} / {condicoes['temp_max']}"),
            ("💧 Umidade", condicoes['umidade']),
            ("🌬️ Vento", condicoes['vento']),
            ("🕐 Atualização", condicoes['atualizacao'])
        ]
        
        for i, (label, value) in enumerate(infos):
            frame = tk.Frame(info_frame, bg="white")
            frame.grid(row=i//2, column=i%2, sticky="w", padx=10, pady=5)
            tk.Label(frame, text=label, font=("Arial", 10, "bold"), bg="white").pack(anchor="w")
            tk.Label(frame, text=value, font=("Arial", 10), bg="white", fg="#6b7280").pack(anchor="w")
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def atualizar_aba_recomendacoes(self, cultura, recomendacoes):
        for widget in self.recomendacoes_tab.winfo_children():
            widget.destroy()
        
        titulo = tk.Label(self.recomendacoes_tab, 
                         text=f"🌿 Recomendações para {cultura.title()}",
                         font=("Arial", 16, "bold"), 
                         bg="#f8fafc")
        titulo.pack(pady=10)
        
        canvas = tk.Canvas(self.recomendacoes_tab, bg="#f8fafc")
        scrollbar = ttk.Scrollbar(self.recomendacoes_tab, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        for variedade in recomendacoes:
            self.criar_card_variedade(scrollable_frame, variedade)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def criar_card_variedade(self, parent, variedade):
        score = variedade['score']
        if score >= 80:
            color = "#10b981"  # Verde
        elif score >= 60:
            color = "#f59e0b"  # Amarelo
        else:
            color = "#ef4444"  # Vermelho
        
        card = tk.Frame(parent, bg="white", relief=tk.RAISED, bd=1)
        card.pack(fill=tk.X, padx=10, pady=5)
        
        header = tk.Frame(card, bg=color)
        header.pack(fill=tk.X)
        
        tk.Label(header, text=variedade['nome'], 
                font=("Arial", 14, "bold"), bg=color, fg="white").pack(side=tk.LEFT, padx=10, pady=5)
        
        tk.Label(header, text=f"{score}% Compatível", 
                font=("Arial", 12, "bold"), bg=color, fg="white").pack(side=tk.RIGHT, padx=10, pady=5)
        
        content = tk.Frame(card, bg="white")
        content.pack(fill=tk.X, padx=15, pady=10)
        
        tk.Label(content, text=variedade['detalhes'], 
                font=("Arial", 10), bg="white", wraplength=600, justify=tk.LEFT).pack(anchor="w")
        
        details_frame = tk.Frame(content, bg="white")
        details_frame.pack(fill=tk.X, pady=10)
        
        detalhes = [
            ("💧 Irrigação:", variedade['irrigacao']),
            ("📅 Época:", variedade['epoca']),
            ("☀️ Sol:", variedade['sol']),
            ("⏱️ Ciclo:", variedade['ciclo']),
            ("📊 Performance:", variedade['performance']),
            ("🎯 Dificuldade:", variedade['dificuldade'])
        ]
        
        for i, (label, value) in enumerate(detalhes):
            if i % 2 == 0:
                row_frame = tk.Frame(details_frame, bg="white")
                row_frame.pack(fill=tk.X)
            
            item_frame = tk.Frame(row_frame, bg="white")
            item_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=2)
            
            tk.Label(item_frame, text=label, font=("Arial", 9, "bold"), bg="white").pack(anchor="w")
            tk.Label(item_frame, text=value, font=("Arial", 9), bg="white", fg="#6b7280").pack(anchor="w")
    
    def atualizar_aba_dicas(self, dicas):
        for widget in self.dicas_tab.winfo_children():
            widget.destroy()
        
        titulo = tk.Label(self.dicas_tab, 
                         text="💡 Dicas de Plantio Personalizadas",
                         font=("Arial", 16, "bold"), 
                         bg="#f8fafc")
        titulo.pack(pady=10)
        
        if not dicas:
            tk.Label(self.dicas_tab, text="Nenhuma dica específica para as condições atuais.",
                    font=("Arial", 12), bg="#f8fafc").pack(pady=20)
            return
        
        canvas = tk.Canvas(self.dicas_tab, bg="#f8fafc")
        scrollbar = ttk.Scrollbar(self.dicas_tab, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        for i, dica in enumerate(dicas):
            card = tk.Frame(scrollable_frame, bg="#fff3cd", relief=tk.RAISED, bd=1)
            card.pack(fill=tk.X, padx=10, pady=5)
            
            tk.Label(card, text=f"💡 {dica}", font=("Arial", 11), 
                    bg="#fff3cd", fg="#856404", wraplength=600, justify=tk.LEFT).pack(padx=15, pady=10)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def mostrar_erro(self, mensagem):
        self.progress.stop()
        self.status_var.set("Erro na busca")
        messagebox.showerror("Erro", mensagem)

def main():
    try:
        root = tk.Tk()
        app = AgroTechApp(root)
        root.mainloop()
    except Exception as e:
        print(f"Erro ao iniciar aplicação: {e}")
        input("Pressione Enter para sair...")

if __name__ == "__main__":
    print("🌱 Iniciando AgroTech...")
    print("📋 Culturas disponíveis: tomate, alface, cenoura, feijão, milho, couve, repolho, beterraba, pepino, abobrinha, pimentão, berinjela, cebola, alho, batata, morango")
    main()