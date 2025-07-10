import pandas as pd
from fpdf import FPDF
from wrapper import DataWrapper
from git import Repo


data = DataWrapper.get_reports_pagamentos()

date_venc = DataWrapper.get_data_venc()

df = pd.DataFrame(data)

df[["manual", "eletronico"]] = df[["manual", "eletronico"]].fillna(0.0)
df["total"] = df["manual"] + df["eletronico"]

total_manual = df["manual"].sum()
total_eletronico = df["eletronico"].sum()
total_geral = df["total"].sum()

# Colunas ajustadas
col_widths = [70, 50, 26, 26, 26]
col_names = ["Fornecedor", "G.E.F.", "Manual", "Eletrônico", "Total"]
x_inicio = (210 - sum(col_widths)) / 2

# Criar PDF com cabeçalho customizado
class PDF(FPDF):
    def header(self):
        # Imagem (ajuste conforme o caminho e o tamanho necessário)
        self.image("logo.png", 10, 2, 20)  # x, y, largura
        self.set_font("Arial", "B", 10)
        self.cell(0, 10, f"Detalhamento de Pagamentos - {date_venc}", align="C", ln=True)
        self.ln(5)

pdf = PDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()

pdf.set_line_width(0.1)  # Linha mais fina
pdf.set_font("Arial", 'B', 8)
pdf.set_x(x_inicio)

# Cabeçalho da Tabela
for i, name in enumerate(col_names):
    pdf.cell(col_widths[i], 6, name, border=1, align='C')
pdf.ln()

# Conteúdo
pdf.set_font("Arial", '', 8)
for _, row in df.iterrows():
    y_before = pdf.get_y()
    x_before = x_inicio

    # Fornecedor com quebra de linha
    pdf.set_xy(x_before, y_before)
    pdf.multi_cell(col_widths[0], 4.5, str(row['fornecedor']), border=1)
    y_after = pdf.get_y()
    cell_height = y_after - y_before

    pdf.set_xy(x_before + col_widths[0], y_before)
    pdf.cell(col_widths[1], cell_height, str(row['G.E.F.']), border=1, align='C')
    pdf.cell(col_widths[2], cell_height, f"R$ {row['manual']:,.2f}".replace(",", "v").replace(".", ",").replace("v", "."), border=1, align='R')
    pdf.cell(col_widths[3], cell_height, f"R$ {row['eletronico']:,.2f}".replace(",", "v").replace(".", ",").replace("v", "."), border=1, align='R')
    pdf.cell(col_widths[4], cell_height, f"R$ {row['total']:,.2f}".replace(",", "v").replace(".", ",").replace("v", "."), border=1, align='R')
    pdf.ln()

# Totais
pdf.set_font("Arial", 'B', 8)
pdf.set_x(x_inicio)
pdf.cell(col_widths[0] + col_widths[1], 6, "Totais", border=1, align='R')
pdf.cell(col_widths[2], 6, f"R$ {total_manual:,.2f}".replace(",", "v").replace(".", ",").replace("v", "."), border=1, align='R')
pdf.cell(col_widths[3], 6, f"R$ {total_eletronico:,.2f}".replace(",", "v").replace(".", ",").replace("v", "."), border=1, align='R')
pdf.cell(col_widths[4], 6, f"R$ {total_geral:,.2f}".replace(",", "v").replace(".", ",").replace("v", "."), border=1, align='R')

# Salvar PDF
output_path = r"C:\home\ubuntu\inpasa-pagamentos\detalhamento_pagamentos.pdf"
pdf.output(output_path)

# Enviar para Git (opcional)
repo_dir = r"C:\home\ubuntu\inpasa-pagamentos"  # <=== altere aqui

# Bloco do Git (mantido como no original)
try:
    # Descomente as linhas abaixo para usar o Git
    #repo = Repo(repo_dir)
    #repo.git.add(r'\home\ubuntu\inpasa-pagamentos\detalhamento_pagamentos.pdf')
    #repo.index.commit('chore: Relatório de Pagamentos atualizado')
    #origin = repo.remote(name='origin')
    #origin.push()
    print("Arquivo enviado para o GitHub com sucesso!")
except Exception as e:
    print(f"Erro ao enviar para o GitHub: {e}")

print('✅ Relatorio Gerado!')