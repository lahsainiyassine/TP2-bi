import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            return  # Page de garde sans en-tete ni pied de page

        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#4A5568"))

        # En-tete
        self.drawString(45, A4[1] - 32, "Master TEE - S3 | Business Intelligence | Projet : Alimentation Data Warehouse")
        self.drawRightString(A4[0] - 45, A4[1] - 32, "LAHSAINI Yassine")
        self.setStrokeColor(colors.HexColor("#CBD5E0"))
        self.setLineWidth(0.5)
        self.line(45, A4[1] - 38, A4[0] - 45, A4[1] - 38)

        # Pied de page
        self.line(45, 40, A4[0] - 45, 40)
        self.drawString(45, 28, "Universite Cadi Ayyad - ENS Marrakech | Enseignante : Pr. Oumaima STITINI")
        page_str = f"Page {self._pageNumber} sur {page_count}"
        self.drawRightString(A4[0] - 45, 28, page_str)
        self.restoreState()

def build_pdf():
    pdf_path = r'c:\Users\pc\OneDrive\Bureau\ETL\Rapport_Projet_BI_LAHSAINI_Yassine.pdf'
    img_dir = r'c:\Users\pc\OneDrive\Bureau\ETL\images'

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        leftMargin=45,
        rightMargin=45,
        topMargin=48,
        bottomMargin=48
    )

    styles = getSampleStyleSheet()

    primary_color = colors.HexColor("#1A365D")   # Bleu marine profond
    secondary_color = colors.HexColor("#2B6CB0") # Bleu acier
    dark_neutral = colors.HexColor("#2D3748")    # Gris anthracite
    light_bg = colors.HexColor("#F7FAFC")        # Gris perle fond tableau

    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=25,
        textColor=primary_color,
        alignment=1
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11.5,
        leading=16,
        textColor=secondary_color,
        alignment=1
    )

    meta_style = ParagraphStyle(
        'CoverMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=15,
        textColor=dark_neutral,
        alignment=1
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=primary_color,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=secondary_color,
        spaceBefore=6,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=dark_neutral,
        spaceAfter=4
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=dark_neutral,
        leftIndent=12,
        spaceAfter=2.5
    )

    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor("#1A202C")
    )

    caption_style = ParagraphStyle(
        'Caption_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#4A5568"),
        alignment=1,
        spaceBefore=3,
        spaceAfter=6
    )

    th_style = ParagraphStyle(
        'TableHeader_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white
    )

    story = []

    # ==========================================
    # PAGE 1 : PAGE DE GARDE ACADEMIQUE
    # ==========================================
    story.append(Spacer(1, 20))
    story.append(Paragraph("UNIVERSITE CADI AYYAD", meta_style))
    story.append(Paragraph("ECOLE NORMALE SUPERIEURE DE MARRAKECH", meta_style))
    story.append(Paragraph("Departement d'Informatique et Technologies Educatives", meta_style))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="80%", thickness=1.5, color=primary_color, spaceAfter=18, spaceBefore=4))

    story.append(Paragraph("Master Technologie Educative Emergente (TEE)", subtitle_style))
    story.append(Paragraph("Semestre 3 - Annee Universitaire 2026-2027", subtitle_style))
    story.append(Spacer(1, 18))

    story.append(Paragraph("RAPPORT DE PROJET BUSINESS INTELLIGENCE", ParagraphStyle('SubSub', parent=subtitle_style, fontSize=11, leading=14, fontName='Helvetica-Bold', textColor=secondary_color)))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Conception et Alimentation d'un Data Warehouse Decisionnel avec Talaxie Open Studio et MySQL", title_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Integration Multi-Sources (Excel, CSV, XML), Deduplication par tUnite/tUniqRow et Modelisation en Etoile", subtitle_style))
    story.append(Spacer(1, 22))

    story.append(HRFlowable(width="60%", thickness=0.8, color=colors.HexColor("#CBD5E0"), spaceAfter=22, spaceBefore=4))

    info_data = [
        [Paragraph("<b>Etudiant auteur :</b>", body_style), Paragraph("<b>LAHSAINI Yassine</b>", body_style)],
        [Paragraph("<b>Filiere universitaire :</b>", body_style), Paragraph("Master TEE (Technologie Educative Emergente)", body_style)],
        [Paragraph("<b>Module de formation :</b>", body_style), Paragraph("Business Intelligence & Data Warehousing", body_style)],
        [Paragraph("<b>Enseignante responsable :</b>", body_style), Paragraph("Pr. Oumaima STITINI", body_style)],
        [Paragraph("<b>Plateformes et Outils :</b>", body_style), Paragraph("Talaxie Open Studio for Data Integration (v8.9), MySQL / MariaDB, Microsoft Power BI", body_style)],
        [Paragraph("<b>Depot GitHub :</b>", body_style), Paragraph("https://github.com/lahsainiyassine/TP2-bi", body_style)],
        [Paragraph("<b>Date de remise :</b>", body_style), Paragraph("Novembre 2026", body_style)]
    ]
    info_table = Table(info_data, colWidths=[150, 320])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), light_bg),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E0")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(info_table)
    story.append(PageBreak())

    # ==========================================
    # PAGE 2 : CONTEXTE ET MODELISATION MULTIDIMENSIONNELLE
    # ==========================================
    story.append(Paragraph("1. Contexte Metier, Enjeux et Architecture Multidimensionnelle", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=8, spaceBefore=2))

    story.append(Paragraph("1.1 Contexte et Enjeux Metier", h2_style))
    story.append(Paragraph(
        "Dans le cadre des activites d'une societe de distribution commerciale, les informations operationnelles sont fragmentees entre de multiples systemes heterogenes : les comptes clients, le catalogue des articles, les points de vente physiques et les transactions de caisse reposent sur des formats disparates (classeurs Excel, fichiers plats CSV et fichiers hierarchiques XML).",
        body_style
    ))
    story.append(Paragraph(
        "Cette fragmentation empeche toute vision globale et consolidation analytique. L'objectif consiste a construire un Data Warehouse unifie (<b>dwh_ventes</b>) sous MySQL, structure en <b>schema en etoile</b> et alimente par des flux ETL robustes avec <b>Talaxie Open Studio</b>.",
        body_style
    ))

    story.append(Paragraph("1.2 Justification du Schema en Etoile", h2_style))
    story.append(Paragraph(
        "Le schema en etoile a ete retenu pour ses performances de requetage et sa simplicite d'utilisation par les analystes decisionnels :",
        body_style
    ))
    story.append(Paragraph("- <b>Jointures directes et performantes :</b> Une seule jointure relie la table de faits centrale a chacune des dimensions, garantissant un temps de reponse optimal sur de grands volumes.", bullet_style))
    story.append(Paragraph("- <b>Cles de substitution (Surrogate Keys) :</b> Chaque dimension possede une cle artificielle entiere (ex. <code>id_client_sk</code>, <code>id_produit_sk</code>) de type INTEGER, insensible aux mutations des codes metier sources.", bullet_style))
    story.append(Paragraph("- <b>Securisation de l'integrite referentielle :</b> Une ligne artificielle par defaut (cle = 1 : C_INCONNU, P_INCONNU, M_INCONNU) est presente dans chaque dimension. Lors du chargement des ventes, toute transaction orpheline est redirigee vers cette cle 1, eliminant les erreurs de contrainte etrangere.", bullet_style))

    story.append(Spacer(1, 2))
    story.append(Paragraph("1.3 Cartographie des Fichiers Sources", h2_style))
    sources_data = [
        [Paragraph("<b>Fichier Source</b>", body_style), Paragraph("<b>Format</b>", body_style), Paragraph("<b>Role et Contenu Metier</b>", body_style)],
        [Paragraph("clients_base_50.xlsx<br/>clients_online_50.csv<br/>clients_fidelite_50.xml", body_style), Paragraph("Excel (.xlsx)<br/>CSV (virgule)<br/>XML (boucle XPath)", body_style), Paragraph("Donnees signaletiques clients (id, nom, prenom, ville, date inscription), adresses email et segments web, et programme fidelite (points, type de carte).", body_style)],
        [Paragraph("produits_catalogue.xlsx<br/>produits_fournisseurs.csv", body_style), Paragraph("Excel (.xlsx)<br/>CSV (virgule)", body_style), Paragraph("Catalogue articles (code, libelle, categorie, marque, prix d'achat, prix de vente) et donnees logistiques (fournisseur, pays origine, delai, cout transport).", body_style)],
        [Paragraph("magasins_localisation (2).csv<br/>magasins_ventes (1).xlsx", body_style), Paragraph("CSV (virgule)<br/>Excel (.xlsx)", body_style), Paragraph("Coordonnees geographiques des boutiques (code, nom, ville, region, pays) et donnees d'exploitation commerciale (surface m2, date ouverture, effectif, CA annuel).", body_style)],
        [Paragraph("ventes_synthese.xlsx", body_style), Paragraph("Excel (.xlsx)", body_style), Paragraph("Transactions commerciales de vente (id_vente, id_client_source, id_produit_source, id_magasin_source, date_vente, quantite, prix, montant, paiement).", body_style)]
    ]
    t_sources = Table(sources_data, colWidths=[130, 95, 280])
    t_sources.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), primary_color),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, light_bg])
    ]))
    story.append(t_sources)
    story.append(PageBreak())

    # ==========================================
    # PAGE 3 : DICTIONNAIRE DWH ET REFERENTIEL TALAXIE
    # ==========================================
    story.append(Paragraph("2. Dictionnaire du Data Warehouse et Pattern Architectural", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=8, spaceBefore=2))

    story.append(Paragraph("2.1 Dictionnaire des Tables du Data Warehouse (dwh_ventes)", h2_style))
    dwh_data = [
        [Paragraph("<b>Table</b>", body_style), Paragraph("<b>Type</b>", body_style), Paragraph("<b>Cle Primaire</b>", body_style), Paragraph("<b>Attributs et Mesures Cles</b>", body_style)],
        [Paragraph("<b>dim_client</b>", body_style), Paragraph("Dimension", body_style), Paragraph("id_client_sk (INT auto)", body_style), Paragraph("code_client, nom, prenom, nom_complet, ville, email, segment_marketing, date_inscription, points_fidelite, type_carte.", body_style)],
        [Paragraph("<b>dim_produit</b>", body_style), Paragraph("Dimension", body_style), Paragraph("id_produit_sk (INT auto)", body_style), Paragraph("code_produit, nom_produit, categorie, sous_categorie, marque, prix_achat, prix_vente, fournisseur, pays_fournisseur, statut.", body_style)],
        [Paragraph("<b>dim_magasin</b>", body_style), Paragraph("Dimension", body_style), Paragraph("id_magasin_sk (INT auto)", body_style), Paragraph("code_magasin, nom_magasin, ville, region, pays, surface_m2, date_ouverture, chiffre_affaires_annuel, nb_employes.", body_style)],
        [Paragraph("<b>dim_temps</b>", body_style), Paragraph("Dimension", body_style), Paragraph("id_temps (INT yyyyMMdd)", body_style), Paragraph("date_complete, jour, mois, nom_mois, trimestre, annee, semestre, jour_semaine, annee_universitaire.", body_style)],
        [Paragraph("<b>fait_ventes</b>", body_style), Paragraph("Table de Faits", body_style), Paragraph("id_vente_sk (INT auto)", body_style), Paragraph("Cles etrangeres : id_client_fk, id_produit_fk, id_magasin_fk, id_temps_fk.<br/>Mesures : quantite_vendue, prix_unitaire, montant_total, mode_paiement.", body_style)]
    ]
    t_dwh = Table(dwh_data, colWidths=[75, 65, 110, 255])
    t_dwh.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), secondary_color),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, light_bg])
    ]))
    story.append(t_dwh)

    story.append(Spacer(1, 4))
    story.append(Paragraph("2.2 Le Pattern Architectural Multi-Sources", h2_style))
    story.append(Paragraph(
        "Afin de garantir l'exhaustivite et l'integrite de chaque entite, l'architecture implementee sous Talaxie repose sur un patron en trois etapes :",
        body_style
    ))
    story.append(Paragraph("1. <b>Convergence et Unification (tUnite) :</b> Extraction simultanee des identifiants depuis la table de reference et depuis la table des transactions, puis fusion via <code>tUnite</code>.", bullet_style))
    story.append(Paragraph("2. <b>Deduplication Stricte (tUniqRow) :</b> Filtrage des cles uniques pour garantir zero redondance avant le chargement dimensionnel.", bullet_style))
    story.append(Paragraph("3. <b>Enrichissement Croise Multi-Sources (tMap Lookups) :</b> Le flux de cles uniques sert de flux principal dans un <code>tMap</code> effectuant des jointures gauches (Left Outer Joins) vers des sources heterogenes (Excel, CSV, XML avec Dom4j).", bullet_style))

    ref_img_path = os.path.join(img_dir, 'referentiel_projet.png')
    if os.path.exists(ref_img_path):
        story.append(Spacer(1, 2))
        story.append(Image(ref_img_path, width=160, height=270))
        story.append(Paragraph("Figure 1 : Arborescence du referentiel TP2_BI_VENTES sous Talaxie Open Studio montrant les 5 Jobs.", caption_style))

    story.append(PageBreak())

    # ==========================================
    # PAGE 4 : JOB DIM_CLIENT
    # ==========================================
    story.append(Paragraph("3. Job 1 : Dimension Client (Job_Dim_Client_Ventes)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=8, spaceBefore=2))

    story.append(Paragraph("3.1 Conception et Execution du Flux Client", h2_style))
    story.append(Paragraph(
        "Le job <b>Job_Dim_Client_Ventes</b> integre et deduplique les donnees clients issues de <code>clients_base_50.xlsx</code> (Excel), <code>clients_online_50.csv</code> (CSV) et <code>clients_fidelite_50.xml</code> (XML) :",
        body_style
    ))
    story.append(Paragraph("- <b>Double extraction :</b> 50 codes depuis la base clients et 50 codes depuis les ventes sont unifies par <code>tUnite</code> (100 lignes traitees), puis dedupliques par <code>tUniqRow</code>.", bullet_style))
    story.append(Paragraph("- <b>Lookups croises :</b> Le tMap central <code>Relier clients</code> realise 3 jointures gauches vers Excel, CSV et XML (Dom4j) pour recuperer noms, villes, emails, segments et points fidelite.", bullet_style))
    story.append(Paragraph("- <b>Chargement MySQL :</b> Ecriture dans <code>dim_client</code> sous la cle de substitution <code>id_client_sk</code>.", bullet_style))

    client_exec = os.path.join(img_dir, 'job_dim_client_exec.jpg')
    if os.path.exists(client_exec):
        story.append(Spacer(1, 4))
        story.append(Image(client_exec, width=460, height=360))
        story.append(Paragraph("Figure 2 : Conception et execution reussie du Job DimClient sous Talaxie Open Studio (100 lignes traitees, [Code de sortie = 0]).", caption_style))

    story.append(PageBreak())

    # ==========================================
    # PAGE 5 : JOB DIM_PRODUIT
    # ==========================================
    story.append(Paragraph("4. Job 2 : Dimension Produit (Job_Dim_Produit_Ventes)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=8, spaceBefore=2))

    story.append(Paragraph("4.1 Conception et Execution du Flux Produit", h2_style))
    story.append(Paragraph(
        "Le job <b>Job_Dim_Produit_Ventes</b> consolide le referentiel catalogue en croisant les articles vendus avec les donnees d'approvisionnement des fournisseurs :",
        body_style
    ))
    story.append(Paragraph("- <b>Unification des references :</b> Extraction simultanee depuis <code>produits_catalogue.xlsx</code> et <code>ventes_synthese.xlsx</code>, fusionnees par <code>tUnite</code> (100 lignes) et filtrees par <code>tUniqRow</code>.", bullet_style))
    story.append(Paragraph("- <b>Double Lookup relationnel :</b> Dans <code>Lier produits</code> (tMap), jointure gauche vers le catalogue Excel (prix, categorie, marque) et vers <code>produits_fournisseurs.csv</code> (fournisseur, pays, delai, cout transport).", bullet_style))
    story.append(Paragraph("- <b>Chargement MySQL :</b> Insertion dans <code>dim_produit</code> sous la cle surrogate <code>id_produit_sk</code>.", bullet_style))

    prod_exec = os.path.join(img_dir, 'job_dim_produit_exec.jpg')
    if os.path.exists(prod_exec):
        story.append(Spacer(1, 4))
        story.append(Image(prod_exec, width=460, height=335))
        story.append(Paragraph("Figure 3 : Conception et execution reussie du Job DimProduit sous Talaxie Open Studio (100 lignes traitees, [Code de sortie = 0]).", caption_style))

    story.append(PageBreak())

    # ==========================================
    # PAGE 6 : JOB DIM_MAGASIN
    # ==========================================
    story.append(Paragraph("5. Job 3 : Dimension Magasin (Job_Dim_Magasin_Ventes)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=8, spaceBefore=2))

    story.append(Paragraph("5.1 Conception et Execution du Flux Magasin", h2_style))
    story.append(Paragraph(
        "Le job <b>Job_Dim_Magasin_Ventes</b> synchronise la localisation spatiale des points de vente avec leurs donnees de gestion financiere et humaine :",
        body_style
    ))
    story.append(Paragraph("- <b>Flux Principal :</b> Lecture de <code>magasins_localisation (2).csv</code> apportant les codes magasins, noms, villes, regions geographiques et pays (50 magasins).", bullet_style))
    story.append(Paragraph("- <b>Lookup de Gestion :</b> Lecture de <code>magasins_ventes (1).xlsx</code> apportant surface commerciale, date d'ouverture, effectif et chiffre d'affaires annuel.", bullet_style))
    story.append(Paragraph("- <b>Jointure et Ecriture :</b> <code>Lier magasins</code> (tMap) enrichit les enregistrements et alimente <code>dim_magasin</code> sous MySQL.", bullet_style))

    mag_exec = os.path.join(img_dir, 'job_dim_magasin_exec.jpg')
    if os.path.exists(mag_exec):
        story.append(Spacer(1, 4))
        story.append(Image(mag_exec, width=460, height=325))
        story.append(Paragraph("Figure 4 : Conception et execution reussie du Job DimMagasin sous Talaxie Open Studio (50 magasins charges, [Code de sortie = 0]).", caption_style))

    story.append(PageBreak())

    # ==========================================
    # PAGE 7 : JOB DIM_TEMPS
    # ==========================================
    story.append(Paragraph("6. Job 4 : Dimension Temps Multi-Sources (Job_Dim_Temps_Ventes)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=8, spaceBefore=2))

    story.append(Paragraph("6.1 Collecte Multi-Sources et Decompilation Calendaire", h2_style))
    story.append(Paragraph(
        "La dimension temporelle consolide l'ensemble des dates d'evenements operationnels pour eviter toute rupture calendaire :",
        body_style
    ))
    story.append(Paragraph("1. <b>Cinq flux sources simultanes :</b> Inscriptions clients (Excel), premier achat web (CSV), insertion catalogue (Excel), ouverture magasin (CSV) et date vente (Excel).", bullet_style))
    story.append(Paragraph("2. <b>Agregation exhaustive (tUnite) :</b> Regroupement des 5 flux en un ensemble chronologique totalisant 250 dates lues.", bullet_style))
    story.append(Paragraph("3. <b>Deduplication absolue (tUniqRow) :</b> Filtrage strict supprimant les redondances pour isoler 240 dates distinctes.", bullet_style))
    story.append(Paragraph("4. <b>Decomposition Calendaire :</b> <code>Mois et trimestre</code> (tMap) calcule <code>id_temps</code> (yyyyMMdd), <code>jour</code>, <code>mois</code>, <code>nom_mois</code>, <code>trimestre</code>, <code>semestre</code>, <code>annee</code> et <code>annee_universitaire</code>.", bullet_style))
    story.append(Paragraph("5. <b>Insertion MySQL :</b> Chargement dans <code>dim_temps</code> sans doublon.", bullet_style))

    temps_exec = os.path.join(img_dir, 'job_dim_temps_exec.jpg')
    if os.path.exists(temps_exec):
        story.append(Spacer(1, 4))
        story.append(Image(temps_exec, width=460, height=350))
        story.append(Paragraph("Figure 5 : Conception et execution reussie du Job DimTemps sous Talaxie Open Studio (250 lues, 240 uniques inserees, [Code de sortie = 0]).", caption_style))

    story.append(PageBreak())

    # ==========================================
    # PAGE 8 : JOB FAIT_VENTES
    # ==========================================
    story.append(Paragraph("7. Job 5 : Table de Faits Centrale (Job_Fait_Ventes)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=8, spaceBefore=2))

    story.append(Paragraph("7.1 Resolution des Cles Dimensionnelles et Calcul des Indicateurs", h2_style))
    story.append(Paragraph(
        "Le job <b>Job_Fait_Ventes</b> constitue le centre de l'architecture decisionnelle en reliant les faits aux dimensions :",
        body_style
    ))
    story.append(Paragraph("- <b>Flux Transactionnel :</b> Lecture de <code>ventes_synthese.xlsx</code> portant 50 transactions d'achat avec quantites et prix.", bullet_style))
    story.append(Paragraph("- <b>Quatre Lookups Dimensionnels MySQL :</b> Resolution en memoire de <code>dim_client</code> (101 lignes), <code>dim_produit</code> (101 lignes), <code>dim_magasin</code> (51 lignes) et <code>dim_temps</code> (240 lignes).", bullet_style))
    story.append(Paragraph("- <b>Securite Referentielle Robuste :</b> En cas d'identifiant absent, une condition ternaire Java attribue automatiquement la cle artificielle <code>1</code> (`C_INCONNU`, `P_INCONNU`, etc.), garantissant zero rejet de cle etrangere :", bullet_style))
    story.append(Paragraph("<code>id_client_fk = (client != null &amp;&amp; client.id_client_sk &gt; 0) ? client.id_client_sk : 1;</code><br/><code>id_produit_fk = (produit != null &amp;&amp; produit.id_produit_sk &gt; 0) ? produit.id_produit_sk : 1;</code><br/><code>id_magasin_fk = (magasin != null &amp;&amp; magasin.id_magasin_sk &gt; 0) ? magasin.id_magasin_sk : 1;</code>", code_style))
    story.append(Paragraph("- <b>Mesures et Sortie :</b> Calcul du montant total (<code>quantite * prix_unitaire</code>) et ecriture dans <code>fait_ventes</code>.", bullet_style))

    fait_exec = os.path.join(img_dir, 'job_fait_ventes_exec.jpg')
    if os.path.exists(fait_exec):
        story.append(Spacer(1, 4))
        story.append(Image(fait_exec, width=460, height=335))
        story.append(Paragraph("Figure 6 : Conception et execution reussie du Job FaitVente sous Talaxie Open Studio (50 transactions integrees, [Code de sortie = 0]).", caption_style))

    story.append(PageBreak())

    # ==========================================
    # PAGE 9 : VALIDATION DWH & ANALYSES OLAP
    # ==========================================
    story.append(Paragraph("8. Validation du Data Warehouse et Analyses Decisionnelles OLAP", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=8, spaceBefore=2))

    story.append(Paragraph("8.1 Controle de Volumetrie dans MySQL (dwh_ventes)", h2_style))
    story.append(Paragraph(
        "A l'issue des executions des cinq flux ETL sous Talaxie, le controle de conformite volumetrique confirme le parfait peuplement des tables de l'entrepot :",
        body_style
    ))

    vol_data = [
        [Paragraph("<b>Table du Data Warehouse</b>", th_style), Paragraph("<b>Type</b>", th_style), Paragraph("<b>Nombre de Lignes</b>", th_style), Paragraph("<b>Statut de Conformite</b>", th_style)],
        [Paragraph("dim_client", body_style), Paragraph("Dimension", body_style), Paragraph("101 lignes (100 sources + 1 inconnu)", body_style), Paragraph("Conforme (integrite respectee)", body_style)],
        [Paragraph("dim_produit", body_style), Paragraph("Dimension", body_style), Paragraph("101 lignes (100 sources + 1 inconnu)", body_style), Paragraph("Conforme (catalogue enrichi)", body_style)],
        [Paragraph("dim_magasin", body_style), Paragraph("Dimension", body_style), Paragraph("51 lignes (50 sources + 1 inconnu)", body_style), Paragraph("Conforme (localisation et gestion)", body_style)],
        [Paragraph("dim_temps", body_style), Paragraph("Dimension", body_style), Paragraph("240 dates distinctes", body_style), Paragraph("Conforme (calendrier sans rupture)", body_style)],
        [Paragraph("fait_ventes", body_style), Paragraph("Table de Faits", body_style), Paragraph("50 transactions consolidees", body_style), Paragraph("Conforme (100% cles resolues)", body_style)]
    ]
    t_vol = Table(vol_data, colWidths=[120, 80, 130, 175])
    t_vol.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), primary_color),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, light_bg])
    ]))
    story.append(t_vol)

    story.append(Spacer(1, 4))
    story.append(Paragraph("8.2 Requetes Analytiques Decisionnelles (Indicateurs OLAP)", h2_style))

    story.append(Paragraph("<b>KPI 1 : Chiffre d'Affaires par Region Administrative et par Magasin</b>", body_style))
    story.append(Paragraph(
        "<code>SELECT m.region, m.nom_magasin, COUNT(f.id_vente_sk) AS nb_ventes, SUM(f.quantite_vendue) AS volume_articles, ROUND(SUM(f.montant_total), 2) AS ca_total_dh FROM fait_ventes f JOIN dim_magasin m ON f.id_magasin_fk = m.id_magasin_sk GROUP BY m.region, m.nom_magasin ORDER BY ca_total_dh DESC;</code>",
        code_style
    ))

    story.append(Spacer(1, 3))
    story.append(Paragraph("<b>KPI 2 : Analyse des Ventes par Categorie de Produit et Annee</b>", body_style))
    story.append(Paragraph(
        "<code>SELECT t.annee, p.categorie, SUM(f.quantite_vendue) AS articles_vendus, ROUND(SUM(f.montant_total), 2) AS ca_dh FROM fait_ventes f JOIN dim_produit p ON f.id_produit_fk = p.id_produit_sk JOIN dim_temps t ON f.id_temps_fk = t.id_temps GROUP BY t.annee, p.categorie ORDER BY t.annee DESC, ca_dh DESC;</code>",
        code_style
    ))

    story.append(Spacer(1, 3))
    story.append(Paragraph("<b>KPI 3 : Repartition des Ventes par Mode de Reglement et Panier Moyen</b>", body_style))
    story.append(Paragraph(
        "<code>SELECT mode_paiement, COUNT(*) AS transactions, ROUND(SUM(montant_total), 2) AS total_encaisse, ROUND(AVG(montant_total), 2) AS panier_moyen FROM fait_ventes GROUP BY mode_paiement ORDER BY total_encaisse DESC;</code>",
        code_style
    ))

    story.append(Spacer(1, 4))
    story.append(Paragraph("8.3 Resultats des Agregations Extraites de MySQL", h2_style))
    story.append(Paragraph(
        "L'execution des requetes analytiques sur les 50 transactions consolidees produit les agregats decisionnels suivants :",
        body_style
    ))

    kpi_res_data = [
        [Paragraph("<b>Axe Analytique</b>", th_style), Paragraph("<b>Segment Majeur</b>", th_style), Paragraph("<b>Volume Ventes</b>", th_style), Paragraph("<b>Chiffre d'Affaires (DH)</b>", th_style)],
        [Paragraph("Top Region 1", body_style), Paragraph("Fes-Meknes", body_style), Paragraph("341 articles", body_style), Paragraph("<b>404 680,56 DH</b>", body_style)],
        [Paragraph("Top Region 2", body_style), Paragraph("Rabat-Sale-Kenitra", body_style), Paragraph("237 articles", body_style), Paragraph("<b>264 949,36 DH</b>", body_style)],
        [Paragraph("Top Region 3", body_style), Paragraph("Tanger-Tetouan-Al Hoceima", body_style), Paragraph("185 articles", body_style), Paragraph("<b>208 647,15 DH</b>", body_style)],
        [Paragraph("Mode Reglement 1", body_style), Paragraph("Especes (12 trans.)", body_style), Paragraph("374 articles", body_style), Paragraph("<b>415 737,62 DH</b>", body_style)],
        [Paragraph("Mode Reglement 2", body_style), Paragraph("Paiement mobile (9 trans.)", body_style), Paragraph("280 articles", body_style), Paragraph("<b>324 712,24 DH</b>", body_style)]
    ]
    t_kpi_res = Table(kpi_res_data, colWidths=[110, 160, 95, 140])
    t_kpi_res.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), primary_color),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, light_bg])
    ]))
    story.append(t_kpi_res)

    story.append(PageBreak())

    # ==========================================
    # PAGE 10 : RESTITUTION POWER BI & CONCLUSION
    # ==========================================
    story.append(Paragraph("9. Restitution Decisionnelle sous Microsoft Power BI", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=8, spaceBefore=2))

    story.append(Paragraph("9.1 Modelisation Semantique et Formules DAX", h2_style))
    story.append(Paragraph(
        "Afin d'offrir une restitution visuelle interactive et dynamique aux decideurs, les donnees du Data Warehouse ont ete connectees a <b>Microsoft Power BI</b>. Le modele semantique en etoile est valorise par des mesures analytiques DAX dediees :",
        body_style
    ))

    pbi_dax_data = [
        [Paragraph("<b>Indicateur DAX</b>", th_style), Paragraph("<b>Formule de Calcul</b>", th_style), Paragraph("<b>Valeur Mesuree</b>", th_style)],
        [Paragraph("Chiffre d'Affaires Total", body_style), Paragraph("<code>SUM(fait_ventes[montant_total])</code>", code_style), Paragraph("<b>1 520 231,31 DH</b>", body_style)],
        [Paragraph("Volume Total Vendu", body_style), Paragraph("<code>SUM(fait_ventes[quantite_vendue])</code>", code_style), Paragraph("<b>1 320 unites</b>", body_style)],
        [Paragraph("Panier Moyen", body_style), Paragraph("<code>DIVIDE([CA Total], [Nb Transactions], 0)</code>", code_style), Paragraph("<b>30 404,63 DH</b>", body_style)],
        [Paragraph("Transactions Realisees", body_style), Paragraph("<code>COUNTROWS(fait_ventes)</code>", code_style), Paragraph("<b>50 ventes</b>", body_style)]
    ]
    t_dax = Table(pbi_dax_data, colWidths=[140, 230, 135])
    t_dax.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), primary_color),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, light_bg])
    ]))
    story.append(t_dax)

    story.append(Spacer(1, 4))
    story.append(Paragraph("9.2 Tableau de Bord Analytique et Synthese Metier", h2_style))

    pbi_img_path = os.path.join(img_dir, 'dashboard_power_bi.png')
    if os.path.exists(pbi_img_path):
        story.append(Image(pbi_img_path, width=505, height=270))
        story.append(Paragraph("<i>Figure 9 : Tableau de Bord Decisionnel interactif concu sous Power BI (Indicateurs cles, CA par Region, Modalites de Reglement et Tendance)</i>", caption_style))

    story.append(Spacer(1, 3))
    story.append(Paragraph("10. Conclusion Generale du Projet", h2_style))
    story.append(Paragraph(
        "Ce projet a permis de maitriser avec succes l'integralite de la chaine decisionnelle BI : de l'analyse des besoins et de la modelisation multidimensionnelle en schema en etoile, jusqu'a la construction de flux ETL modulaires et robustes sous Talaxie Open Studio, et la restitution visuelle executive sous Microsoft Power BI.",
        body_style
    ))
    story.append(Paragraph(
        "L'architecture mise en oeuvre assure l'interoperabilite multi-sources (Excel, CSV, XML), une deduplication stricte et une tracabilite exemplaire des donnees au service de la prise de decision strategique.",
        body_style
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print("PDF genere avec succes :", pdf_path)

if __name__ == '__main__':
    build_pdf()
