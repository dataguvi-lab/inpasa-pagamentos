import pandas as pd
from fpdf import FPDF
from wrapper import DataWrapper
from git import Repo

# 1. Buscar os dados
data = DataWrapper.get_reports_pagamentos()
date_venc = DataWrapper.get_data_venc()
df = pd.DataFrame(data)

# Assumindo que você tem um método para executar a query
group_gef_data = DataWrapper.get_group_gef() # Substitua pelo método correto
df_group_gef = pd.DataFrame(group_gef_data)

# NOVA CONSULTA: Buscar dados agrupados por empenho
group_empenho_data = DataWrapper.get_group_empenho() # Método para executar QUERY_GROUP_EMPENHO
df_group_empenho = pd.DataFrame(group_empenho_data)

# 2. Tratar dados detalhados
df[["manual", "eletronico"]] = df[["manual", "eletronico"]].fillna("")
df["manual_calc"] = pd.to_numeric(df["manual"], errors="coerce").fillna(0.0)
df["eletronico_calc"] = pd.to_numeric(df["eletronico"], errors="coerce").fillna(0.0)
df["total"] = df["manual_calc"] + df["eletronico_calc"]

# 2.1. Tratar dados agrupados por G.E.F.
df_group_gef[["manual", "eletronico"]] = df_group_gef[["manual", "eletronico"]].fillna(0.0)
df_group_gef["manual_calc"] = pd.to_numeric(df_group_gef["manual"], errors="coerce").fillna(0.0)
df_group_gef["eletronico_calc"] = pd.to_numeric(df_group_gef["eletronico"], errors="coerce").fillna(0.0)
df_group_gef["total"] = df_group_gef["manual_calc"] + df_group_gef["eletronico_calc"]

# 2.2. Tratar dados agrupados por empenho
df_group_empenho[["manual", "eletronico"]] = df_group_empenho[["manual", "eletronico"]].fillna(0.0)
df_group_empenho["manual_calc"] = pd.to_numeric(df_group_empenho["manual"], errors="coerce").fillna(0.0)
df_group_empenho["eletronico_calc"] = pd.to_numeric(df_group_empenho["eletronico"], errors="coerce").fillna(0.0)
df_group_empenho["total"] = df_group_empenho["manual_calc"] + df_group_empenho["eletronico_calc"]

# 3. Totais
total_manual = df["manual_calc"].sum()
total_eletronico = df["eletronico_calc"].sum()
total_geral = df["total"].sum()

# 4. Layout PDF
col_widths = [70, 50, 26, 26, 26]
col_names = ["Fornecedor", "G.E.F.", "Eletrônico", "Manual", "Total"]
x_inicio = (210 - sum(col_widths)) / 2

# Layout para tabela de G.E.F.
col_widths_gef = [80, 40, 40, 40]
col_names_gef = ["G.E.F.", "Eletrônico", "Manual", "Total"]
x_inicio_gef = (210 - sum(col_widths_gef)) / 2

# Layout para tabela de Empenho
col_widths_empenho = [50, 50, 35, 35, 35]
col_names_empenho = ["Empenho", "G.E.F.", "Eletrônico", "Manual", "Total"]
x_inicio_empenho = (210 - sum(col_widths_empenho)) / 2

# 5. Classe PDF com cabeçalho apenas na primeira página
class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.data_venc = date_venc['data_maxima'].iloc[0] if not date_venc.empty else "N/A"
        
    def header(self):
        # Cabeçalho completo apenas na primeira página
        if self.page_no() == 1:
            # Background sutil para o cabeçalho
            self.set_fill_color(248, 249, 250)  # Cinza muito claro
            self.rect(0, 0, 210, 25, 'F')
            
            # Logo posicionada à esquerda
            try:
                self.image("logo.png", x=12, y=5, w=60, h=15)  # Ajustado tamanho e posição
            except:
                # Se não encontrar o logo, cria um placeholder minimalista
                self.set_fill_color(230, 230, 230)
                self.rect(12, 6, 18, 13, 'F')
                self.set_font("Arial", "B", 8)
                self.set_text_color(120, 120, 120)
                self.text(15, 14, "LOGO")
            
            # Título principal - posicionado após o logo
            self.set_font("Arial", "B", 14)
            self.set_text_color(51, 51, 51)  # Cinza escuro
            self.set_xy(80, 7)
            self.cell(0, 8, "Detalhamento de Pagamentos", ln=True)
            
            # Subtítulo
            self.set_font("Arial", "", 10)
            self.set_text_color(102, 102, 102)  # Cinza médio
            self.set_xy(80, 14)
            self.cell(0, 6, f"Aprovações Pendentes - {self.data_venc}", ln=True)
            
            # Linha sutil de separação
            self.set_draw_color(220, 220, 220)
            self.set_line_width(0.3)
            self.line(10, 24, 200, 24)
            
            # Reset das cores para o conteúdo
            self.set_text_color(0, 0, 0)
            self.set_draw_color(0, 0, 0)
            
            # Espaço após o cabeçalho
            self.ln(8)
        else:
            # Nas demais páginas, apenas um pequeno espaço no topo
            self.ln(5)
        
    def footer(self):
        # Posicionar a 15mm do final da página
        self.set_y(-15)
        
        # Linha sutil acima do rodapé
        self.set_draw_color(220, 220, 220)
        self.set_line_width(0.3)
        self.line(10, self.get_y() - 2, 200, self.get_y() - 2)
        
        # Número da página com design minimalista
        self.set_font('Arial', '', 8)
        self.set_text_color(102, 102, 102)
        self.cell(0, 10, f'Página {self.page_no()}/{{nb}}', align='C')
        
        # Reset da cor
        self.set_text_color(0, 0, 0)
        
    def add_table_header(self):
        """Adiciona o cabeçalho da tabela com design aprimorado"""
        # Background sutil para o cabeçalho da tabela
        self.set_fill_color(245, 246, 247)
        
        self.set_font("Arial", '', 9)
        self.set_text_color(51, 51, 51)
        self.set_x(x_inicio)
        
        for i, name in enumerate(col_names):
            self.cell(col_widths[i], 8, name, border=1, align='C', fill=True)
        
        # Reset das cores
        self.set_text_color(0, 0, 0)
        self.set_fill_color(255, 255, 255)
        self.ln()

    def add_gef_table_header(self):
        """Adiciona o cabeçalho da tabela de G.E.F."""
        # Background sutil para o cabeçalho da tabela
        self.set_fill_color(245, 246, 247)
        
        self.set_font("Arial", '', 9)
        self.set_text_color(51, 51, 51)
        self.set_x(x_inicio_gef)
        
        for i, name in enumerate(col_names_gef):
            self.cell(col_widths_gef[i], 8, name, border=1, align='C', fill=True)
        
        # Reset das cores
        self.set_text_color(0, 0, 0)
        self.set_fill_color(255, 255, 255)
        self.ln()

    def add_empenho_table_header(self):
        """Adiciona o cabeçalho da tabela de Empenho"""
        # Background sutil para o cabeçalho da tabela
        self.set_fill_color(245, 246, 247)
        
        self.set_font("Arial", '', 9)
        self.set_text_color(51, 51, 51)
        self.set_x(x_inicio_empenho)
        
        for i, name in enumerate(col_names_empenho):
            self.cell(col_widths_empenho[i], 8, name, border=1, align='C', fill=True)
        
        # Reset das cores
        self.set_text_color(0, 0, 0)
        self.set_fill_color(255, 255, 255)
        self.ln()

    def add_section_title(self, title):
        """Adiciona um título de seção"""
        self.ln(3)
        self.set_font("Arial", "B", 11)
        self.set_text_color(51, 51, 51)
        self.cell(0, 8, title, ln=True)
        self.set_text_color(0, 0, 0)
        self.ln(2)

# 6. Criar e configurar o PDF
pdf = PDF()
pdf.alias_nb_pages()  # Para mostrar total de páginas no rodapé
pdf.set_auto_page_break(auto=True, margin=20)  # Margem maior para o rodapé
pdf.add_page()
pdf.set_line_width(0.1)

# 7. Seção 1: Detalhamento por Fornecedor
pdf.add_section_title("DETALHAMENTO POR FORNECEDOR")
pdf.add_table_header()

# 8. Conteúdo da tabela detalhada
pdf.set_font("Arial", '', 8)
for _, row in df.iterrows():
    # Verificar se precisa de nova página
    if pdf.get_y() > 250:  # Próximo da margem inferior
        pdf.add_page()
        pdf.add_table_header()  # Recriar cabeçalho da tabela na nova página
    
    y_before = pdf.get_y()
    x_before = x_inicio

    pdf.set_xy(x_before, y_before)
    pdf.multi_cell(col_widths[0], 4.5, str(row['fornecedor']), border=1)
    y_after = pdf.get_y()
    cell_height = y_after - y_before

    pdf.set_xy(x_before + col_widths[0], y_before)
    pdf.cell(col_widths[1], cell_height, str(row['G.E.F.']), border=1, align='C')

    # Formatando 'eletronico' com segurança
    try:
        val_eletronico = f"R$ {float(row['eletronico']):,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")
    except (ValueError, TypeError):
        val_eletronico = ""
    pdf.cell(col_widths[2], cell_height, val_eletronico, border=1, align='R')

    # Formatando 'manual' com segurança
    try:
        val_manual = f"R$ {float(row['manual']):,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")
    except (ValueError, TypeError):
        val_manual = ""
    pdf.cell(col_widths[3], cell_height, val_manual, border=1, align='R')

    # Formatando 'total'
    val_total = f"R$ {row['total']:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")
    pdf.cell(col_widths[4], cell_height, val_total, border=1, align='R')

    pdf.ln()

# 9. Verificar se os totais cabem na página atual
if pdf.get_y() > 250:
    pdf.add_page()

# 10. Totais da seção detalhada
pdf.ln(2)
pdf.set_font("Arial", 'B', 8)
pdf.set_x(x_inicio)
pdf.cell(col_widths[0] + col_widths[1], 6, "Totais", border=1, align='R')

val_total_eletronico = f"R$ {total_eletronico:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")
val_total_manual = f"R$ {total_manual:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")
val_total_geral = f"R$ {total_geral:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")

pdf.cell(col_widths[2], 6, val_total_eletronico, border=1, align='R')
pdf.cell(col_widths[3], 6, val_total_manual, border=1, align='R')
pdf.cell(col_widths[4], 6, val_total_geral, border=1, align='R')

# 11. Seção 2: Resumo por G.E.F.
pdf.ln(8)
pdf.add_section_title("RESUMO POR G.E.F.")

# Verificar se precisa de nova página para a seção G.E.F.
if pdf.get_y() > 200:  # Deixar espaço suficiente para a nova seção
    pdf.add_page()
    pdf.add_section_title("RESUMO POR G.E.F.")

pdf.add_gef_table_header()

# 12. Conteúdo da tabela de G.E.F.
pdf.set_font("Arial", '', 8)
for _, row in df_group_gef.iterrows():
    # Verificar se precisa de nova página
    if pdf.get_y() > 250:
        pdf.add_page()
        pdf.add_gef_table_header()
    
    pdf.set_x(x_inicio_gef)
    
    # G.E.F.
    pdf.cell(col_widths_gef[0], 6, str(row['G.E.F.']), border=1, align='L')
    
    # Eletrônico
    try:
        val_eletronico = f"R$ {float(row['eletronico']):,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")
    except (ValueError, TypeError):
        val_eletronico = "R$ 0,00"
    pdf.cell(col_widths_gef[1], 6, val_eletronico, border=1, align='R')
    
    # Manual
    try:
        val_manual = f"R$ {float(row['manual']):,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")
    except (ValueError, TypeError):
        val_manual = "R$ 0,00"
    pdf.cell(col_widths_gef[2], 6, val_manual, border=1, align='R')
    
    # Total
    val_total = f"R$ {row['total']:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")
    pdf.cell(col_widths_gef[3], 6, val_total, border=1, align='R')
    
    pdf.ln()

# 13. Totais da seção G.E.F.
pdf.ln(2)
pdf.set_font("Arial", 'B', 8)
pdf.set_x(x_inicio_gef)

# Calculando totais da seção G.E.F.
total_gef_eletronico = df_group_gef["eletronico_calc"].sum()
total_gef_manual = df_group_gef["manual_calc"].sum()
total_gef_geral = df_group_gef["total"].sum()

pdf.cell(col_widths_gef[0], 6, "TOTAL GERAL", border=1, align='R')

val_total_gef_eletronico = f"R$ {total_gef_eletronico:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")
val_total_gef_manual = f"R$ {total_gef_manual:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")
val_total_gef_geral = f"R$ {total_gef_geral:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")

pdf.cell(col_widths_gef[1], 6, val_total_gef_eletronico, border=1, align='R')
pdf.cell(col_widths_gef[2], 6, val_total_gef_manual, border=1, align='R')
pdf.cell(col_widths_gef[3], 6, val_total_gef_geral, border=1, align='R')

# 14. NOVA SEÇÃO: Resumo por Empenho
pdf.ln(8)
pdf.add_section_title("RESUMO POR EMPENHO")

# Verificar se precisa de nova página para a seção Empenho
if pdf.get_y() > 180:  # Deixar espaço suficiente para a nova seção
    pdf.add_page()
    pdf.add_section_title("RESUMO POR EMPENHO")

pdf.add_empenho_table_header()

# 15. Conteúdo da tabela de Empenho
pdf.set_font("Arial", '', 8)
for _, row in df_group_empenho.iterrows():
    # Verificar se precisa de nova página
    if pdf.get_y() > 250:
        pdf.add_page()
        pdf.add_empenho_table_header()
    
    pdf.set_x(x_inicio_empenho)
    
    # Empenho (truncar se muito longo)
    empenho_text = str(row['empenho'])[:20] + "..." if len(str(row['empenho'])) > 20 else str(row['empenho'])
    pdf.cell(col_widths_empenho[0], 6, empenho_text, border=1, align='L')
    
    # G.E.F. (truncar se muito longo)
    gef_text = str(row['G.E.F.'])[:20] + "..." if len(str(row['G.E.F.'])) > 20 else str(row['G.E.F.'])
    pdf.cell(col_widths_empenho[1], 6, gef_text, border=1, align='L')
    
    # Eletrônico
    try:
        val_eletronico = f"R$ {float(row['eletronico']):,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")
    except (ValueError, TypeError):
        val_eletronico = "R$ 0,00"
    pdf.cell(col_widths_empenho[2], 6, val_eletronico, border=1, align='R')
    
    # Manual
    try:
        val_manual = f"R$ {float(row['manual']):,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")
    except (ValueError, TypeError):
        val_manual = "R$ 0,00"
    pdf.cell(col_widths_empenho[3], 6, val_manual, border=1, align='R')
    
    # Total
    val_total = f"R$ {row['total']:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")
    pdf.cell(col_widths_empenho[4], 6, val_total, border=1, align='R')
    
    pdf.ln()

# 16. Totais da seção Empenho
pdf.ln(2)
pdf.set_font("Arial", 'B', 8)
pdf.set_x(x_inicio_empenho)

# Calculando totais da seção Empenho
total_empenho_eletronico = df_group_empenho["eletronico_calc"].sum()
total_empenho_manual = df_group_empenho["manual_calc"].sum()
total_empenho_geral = df_group_empenho["total"].sum()

pdf.cell(col_widths_empenho[0] + col_widths_empenho[1], 6, "TOTAL GERAL", border=1, align='R')

val_total_empenho_eletronico = f"R$ {total_empenho_eletronico:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")
val_total_empenho_manual = f"R$ {total_empenho_manual:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")
val_total_empenho_geral = f"R$ {total_empenho_geral:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")

pdf.cell(col_widths_empenho[2], 6, val_total_empenho_eletronico, border=1, align='R')
pdf.cell(col_widths_empenho[3], 6, val_total_empenho_manual, border=1, align='R')
pdf.cell(col_widths_empenho[4], 6, val_total_empenho_geral, border=1, align='R')

# 17. Salvar PDF
output_path = r"\home\ubuntu\inpasa-pagamentos\detalhamento_pagamentos.pdf"
pdf.output(output_path)

# 18. Enviar para o Git (opcional)
repo_dir = r"\home\ubuntu\inpasa-pagamentos"
try:
    # Descomente para usar
    repo = Repo(repo_dir)
    repo.git.add(r'detalhamento_pagamentos.pdf')
    repo.index.commit('chore: Relatório de Pagamentos atualizado')
    repo.remote(name='origin').push()
    print("Arquivo enviado para o GitHub com sucesso!")
except Exception as e:
    print(f"Erro ao enviar para o GitHub: {e}")

print('✅ Relatório Gerado!')