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
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor("#4A5568"),
        alignment=1,
        spaceBefore=2,
        spaceAfter=6
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
        [Paragraph("<b>Plateformes et Outils :</b>", body_style), Paragraph("Talaxie Open Studio for Data Integration (v8.9), MySQL / MariaDB", body_style)],
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
        "Dans le cadre des activites d'une societe de distribution commerciale, les informations operationnelles sont fragmentees entre de multiples systemes heterogenes : les comptes clients, le catalogue des articles, les points de vente physiques et les ventes effectuees reposent sur des formats disparates (classeurs Excel, fichiers plats CSV et fichiers hierarchiques XML).",
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
    story.append(Paragraph("2.2 Le Pattern Architectural Exige par l'Enseignant", h2_style))
    story.append(Paragraph(
        "L'architecture imposee par l'enseignant pour les dimensions complexes (Client, Produit, Temps) s'appuie sur une sequence d'integration hautement rigoureuse :",
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

    story.append(Paragraph("3.1 Description Fonctionnelle et Flux de Donnees", h2_style))
    story.append(Paragraph(
        "Le job <b>Job_Dim_Client_Ventes</b> integre les donnees clients a partir de trois formats differents (Excel, CSV et XML) conformement a l'architecture de l'enseignant :",
        body_style
    ))
    story.append(Paragraph("- <b>Double extraction d'identifiants :</b> `Codes clients Excel` (depuis <code>clients_base_50.xlsx</code>) et `Clients dans ventes` (depuis <code>ventes_synthese.xlsx</code>) passent chacun par un composant <code>tMap</code> pour extraire les codes clients.", bullet_style))
    story.append(Paragraph("- <b>Unification et Deduplication :</b> `Rassembler codes` (<code>tUnite</code>) fusionne les flux (100 lignes traitees), puis `Codes uniques` (<code>tUniqRow</code>) garantit l'unicite absolue des identifiants clients.", bullet_style))
    story.append(Paragraph("- <b>Trois Lookups Multi-Formats :</b> Dans `Relier clients` (<code>tMap</code>), le flux principal de cles uniques realise 3 jointures gauches : `Base clients` (Excel), `Clients web CSV` (CSV) et `Fidelite XML` (XML parse avec Dom4j).", bullet_style))
    story.append(Paragraph("- <b>Sortie MySQL :</b> Alimentation de la table `dim_client` avec generation de la cle surrogate `id_client_sk`.", bullet_style))

    client_design = os.path.join(img_dir, 'job_dim_client_design.png')
    client_exec = os.path.join(img_dir, 'job_dim_client_exec.jpg')
    if os.path.exists(client_design):
        story.append(Spacer(1, 2))
        story.append(Image(client_design, width=440, height=195))
        story.append(Paragraph("Figure 2 : Architecture du Job DimClient (Modele exact de l'enseignant avec tUnite, tUniqRow et 3 lookups).", caption_style))
    if os.path.exists(client_exec):
        story.append(Spacer(1, 2))
        story.append(Image(client_exec, width=440, height=215))
        story.append(Paragraph("Figure 3 : Execution reussie sous Talaxie (100 lignes traitees, Lookups connectes, Code de sortie = 0).", caption_style))

    story.append(PageBreak())

    # ==========================================
    # PAGE 5 : JOB DIM_PRODUIT
    # ==========================================
    story.append(Paragraph("4. Job 2 : Dimension Produit (Job_Dim_Produit_Ventes)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=8, spaceBefore=2))

    story.append(Paragraph("4.1 Description Fonctionnelle et Flux de Donnees", h2_style))
    story.append(Paragraph(
        "Le job <b>Job_Dim_Produit_Ventes</b> consolide le referentiel catalogue en croisant les articles vendus avec les informations fournisseurs :",
        body_style
    ))
    story.append(Paragraph("- <b>Unification des codes articles :</b> `Codes du catalogue` (Excel) et `Produits dans ventes` (Excel) sont rediriges vers `Reunir codes` (<code>tUnite</code>) pour assurer l'exhaustivite des references vendues.", bullet_style))
    story.append(Paragraph("- <b>Deduplication :</b> `Codes uniques` (<code>tUniqRow</code>) garantit qu'aucun code produit ne soit duplique.", bullet_style))
    story.append(Paragraph("- <b>Enrichissement multi-sources :</b> Le composant `Lier produits` (<code>tMap</code>) effectue une double jointure gauche avec `Details catalogue` (Excel) et `Fournisseurs CSV` (CSV) pour adjoindre le pays du fournisseur, le delai logistique et le cout de transport.", bullet_style))
    story.append(Paragraph("- <b>Chargement MySQL :</b> Ecriture dans `dim_produit` avec generation de la cle surrogate `id_produit_sk`.", bullet_style))

    prod_design = os.path.join(img_dir, 'job_dim_produit_design.png')
    prod_exec = os.path.join(img_dir, 'job_dim_produit_exec.jpg')
    if os.path.exists(prod_design):
        story.append(Spacer(1, 2))
        story.append(Image(prod_design, width=440, height=195))
        story.append(Paragraph("Figure 4 : Architecture du Job DimProduit avec double entree, tUnite, tUniqRow et lookups croises.", caption_style))
    if os.path.exists(prod_exec):
        story.append(Spacer(1, 2))
        story.append(Image(prod_exec, width=440, height=215))
        story.append(Paragraph("Figure 5 : Execution reussie du Job Produit sous Talaxie (100 lignes traitees, Code de sortie = 0).", caption_style))

    story.append(PageBreak())

    # ==========================================
    # PAGE 6 : JOB DIM_MAGASIN
    # ==========================================
    story.append(Paragraph("5. Job 3 : Dimension Magasin (Job_Dim_Magasin_Ventes)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=8, spaceBefore=2))

    story.append(Paragraph("5.1 Description Fonctionnelle et Flux de Donnees", h2_style))
    story.append(Paragraph(
        "Le job <b>Job_Dim_Magasin_Ventes</b> integre le reseau de distribution physique en reliant la geographie des boutiques a leurs donnees de gestion :",
        body_style
    ))
    story.append(Paragraph("- <b>Flux Principal :</b> Lecture du fichier `Localisation CSV` (`magasins_localisation (2).csv`) apportant les codes magasins, noms, villes, regions geographiques et pays.", bullet_style))
    story.append(Paragraph("- <b>Lookup de Gestion :</b> Lecture du classeur `Gestoin magasins Excel` (`magasins_ventes (1).xlsx`) apportant la surface en m2, le chiffre d'affaires annuel moyen, l'effectif salarie et la date d'ouverture.", bullet_style))
    story.append(Paragraph("- <b>Jointure et Harmonisation :</b> Le composant `Lier magasins` (<code>tMap</code>) fusionne les attributs, convertit les types numeriques et transmet le flux `sortie_magasin`.", bullet_style))
    story.append(Paragraph("- <b>Alimentation MySQL :</b> Chargement dans la table `dim_magasin` sous MySQL.", bullet_style))

    mag_design = os.path.join(img_dir, 'job_dim_magasin_design.png')
    mag_exec = os.path.join(img_dir, 'job_dim_magasin_exec.jpg')
    if os.path.exists(mag_design):
        story.append(Spacer(1, 2))
        story.append(Image(mag_design, width=440, height=195))
        story.append(Paragraph("Figure 6 : Conception du Job DimMagasin reliant localisation CSV et gestion Excel.", caption_style))
    if os.path.exists(mag_exec):
        story.append(Spacer(1, 2))
        story.append(Image(mag_exec, width=440, height=215))
        story.append(Paragraph("Figure 7 : Execution reussie du Job Magasin sous Talaxie (50 lignes traitees, Code de sortie = 0).", caption_style))

    story.append(PageBreak())

    # ==========================================
    # PAGE 7 : JOB DIM_TEMPS
    # ==========================================
    story.append(Paragraph("6. Job 4 : Dimension Temps (Job_Dim_Temps_Ventes)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=8, spaceBefore=2))

    story.append(Paragraph("6.1 Collecte Multi-Sources et Decompilation Calendaire", h2_style))
    story.append(Paragraph(
        "Conformement aux exigences du professeur, la dimension temps agrege l'ensemble des dates d'evenements metier du systeme d'information :",
        body_style
    ))
    story.append(Paragraph("1. <b>Cinq flux sources simultanes :</b> `Clients Excel` (date inscription), `Clients web` (premier achat), `Catalogue Excel` (date insertion produit), `Magasins CSV` (date ouverture) et `Ventes Excel` (date vente).", bullet_style))
    story.append(Paragraph("2. <b>Extraction et Standardisation :</b> Cinq composants <code>tMap</code> normalisent les dates d'evenements au format Date Java unifie.", bullet_style))
    story.append(Paragraph("3. <b>Agregation (tUnite) :</b> Le composant `Reunir dates` regroupe les 5 flux en un ensemble chronologique total de 250 lignes.", bullet_style))
    story.append(Paragraph("4. <b>Deduplication Temporelle (tUniqRow) :</b> Le composant `Dates uniques` filtre les doublons et isole 240 dates distinctes.", bullet_style))
    story.append(Paragraph("5. <b>Decomposition Calendaire :</b> `Mois et trimestre` (<code>tMap</code>) calcule <code>id_temps</code> (yyyyMMdd), <code>jour</code>, <code>mois</code>, <code>nom_mois</code>, <code>trimestre</code>, <code>semestre</code>, <code>annee</code> et <code>annee_universitaire</code>.", bullet_style))
    story.append(Paragraph("6. <b>Sortie MySQL :</b> Insertion dans `dim_temps` garantissant un calendrier complet et sans aucune rupture temporelle.", bullet_style))

    temps_design = os.path.join(img_dir, 'job_dim_temps_design.png')
    temps_exec = os.path.join(img_dir, 'job_dim_temps_exec.jpg')
    if os.path.exists(temps_design):
        story.append(Spacer(1, 2))
        story.append(Image(temps_design, width=440, height=195))
        story.append(Paragraph("Figure 8 : Architecture du Job DimTemps agregeant 5 sources distinctes avec deduplication.", caption_style))
    if os.path.exists(temps_exec):
        story.append(Spacer(1, 2))
        story.append(Image(temps_exec, width=440, height=215))
        story.append(Paragraph("Figure 9 : Execution reussie du Job Temps sous Talaxie (250 dates lues, 240 uniques inserees, Code = 0).", caption_style))

    story.append(PageBreak())

    # ==========================================
    # PAGE 8 : JOB FAIT_VENTES
    # ==========================================
    story.append(Paragraph("7. Job 5 : Table de Faits (Job_Fait_Ventes)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=8, spaceBefore=2))

    story.append(Paragraph("7.1 Resolution des Cles Dimensionnelles et Calcul des Indicateurs", h2_style))
    story.append(Paragraph(
        "Le job <b>Job_Fait_Ventes</b> constitue le coeur du Data Warehouse en liant les faits transactionnels a toutes les dimensions :",
        body_style
    ))
    story.append(Paragraph("- <b>Flux Transactionnel Principal :</b> Lecture de `Ventes Excel` (`ventes_synthese.xlsx`) portant 50 transactions commerciales.", bullet_style))
    story.append(Paragraph("- <b>Quatre Lookups Dimensionnels MySQL :</b> `Cles clients` (101 clients resolus), `Cles produits` (101 produits resolus), `Cles magasins` (51 magasins resolus) et `Cles des dates` (240 dates resolues).", bullet_style))
    story.append(Paragraph("- <b>Securite Referentielle Robuste :</b> En cas de reference source orpheline, une condition ternaire Java attribue automatiquement la cle artificielle <code>1</code> (`C_INCONNU`, `P_INCONNU`, etc.), garantissant zero rejet de cle etrangere :", bullet_style))
    story.append(Paragraph("<code>id_client_fk = (client != null &amp;&amp; client.id_client_sk &gt; 0) ? client.id_client_sk : 1;</code><br/><code>id_produit_fk = (produit != null &amp;&amp; produit.id_produit_sk &gt; 0) ? produit.id_produit_sk : 1;</code><br/><code>id_magasin_fk = (magasin != null &amp;&amp; magasin.id_magasin_sk &gt; 0) ? magasin.id_magasin_sk : 1;</code>", code_style))
    story.append(Paragraph("- <b>Calcul des mesures :</b> Calcul precis du montant total de vente (<code>quantite * prix_unitaire</code>) dans `Calc montnat et cles`.", bullet_style))
    story.append(Paragraph("- <b>Sortie MySQL :</b> Insertion directe dans `fait_ventes`.", bullet_style))

    fait_design = os.path.join(img_dir, 'job_fait_ventes_design.png')
    fait_exec = os.path.join(img_dir, 'job_fait_ventes_exec.jpg')
    if os.path.exists(fait_design):
        story.append(Spacer(1, 2))
        story.append(Image(fait_design, width=440, height=195))
        story.append(Paragraph("Figure 10 : Conception du Job FaitVente avec 4 lookups dimensionnels convergents.", caption_style))
    if os.path.exists(fait_exec):
        story.append(Spacer(1, 2))
        story.append(Image(fait_exec, width=440, height=215))
        story.append(Paragraph("Figure 11 : Execution reussie du Job FaitVente sous Talaxie (50 ventes chargees, Code de sortie = 0).", caption_style))

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
        [Paragraph("<b>Table du Data Warehouse</b>", body_style), Paragraph("<b>Type</b>", body_style), Paragraph("<b>Nombre de Lignes</b>", body_style), Paragraph("<b>Statut de Conformite</b>", body_style)],
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

    story.append(Spacer(1, 3))
    story.append(Paragraph("8.2 Requetes Analytiques Decisionnelles (Indicateurs OLAP)", h2_style))

    story.append(Paragraph("<b>KPI 1 : Chiffre d'Affaires par Region Administrative et par Magasin</b>", body_style))
    story.append(Paragraph(
        "<code>SELECT m.region, m.nom_magasin, COUNT(f.id_vente_sk) AS nb_ventes, SUM(f.quantite_vendue) AS volume_articles, ROUND(SUM(f.montant_total), 2) AS ca_total_dh FROM fait_ventes f JOIN dim_magasin m ON f.id_magasin_fk = m.id_magasin_sk GROUP BY m.region, m.nom_magasin ORDER BY ca_total_dh DESC;</code>",
        code_style
    ))

    story.append(Spacer(1, 2))
    story.append(Paragraph("<b>KPI 2 : Analyse des Ventes par Categorie de Produit et Annee</b>", body_style))
    story.append(Paragraph(
        "<code>SELECT t.annee, p.categorie, SUM(f.quantite_vendue) AS articles_vendus, ROUND(SUM(f.montant_total), 2) AS ca_dh FROM fait_ventes f JOIN dim_produit p ON f.id_produit_fk = p.id_produit_sk JOIN dim_temps t ON f.id_temps_fk = t.id_temps GROUP BY t.annee, p.categorie ORDER BY t.annee DESC, ca_dh DESC;</code>",
        code_style
    ))

    story.append(Spacer(1, 2))
    story.append(Paragraph("<b>KPI 3 : Repartition des Ventes par Mode de Reglement et Panier Moyen</b>", body_style))
    story.append(Paragraph(
        "<code>SELECT mode_paiement, COUNT(*) AS transactions, ROUND(SUM(montant_total), 2) AS total_encaisse, ROUND(AVG(montant_total), 2) AS panier_moyen FROM fait_ventes GROUP BY mode_paiement ORDER BY total_encaisse DESC;</code>",
        code_style
    ))

    story.append(Spacer(1, 4))
    story.append(Paragraph("8.3 Conclusion Generale du Projet", h2_style))
    story.append(Paragraph(
        "Ce projet a permis de maitriser l'ensemble de la chaine decisionnelle BI : de l'analyse des besoins et de la modelisation multidimensionnelle en schema en etoile, jusqu'a la construction de flux ETL modulaires et robustes sous Talaxie Open Studio, et la validation des indicateurs metier via des requetes SQL complexes.",
        body_style
    ))
    story.append(Paragraph(
        "L'utilisation combinee des composants <code>tUnite</code>, <code>tUniqRow</code> et <code>tMap</code> multi-lookups (Excel, CSV, XML) garantit un traitement exhaustif des donnees sans doublon ni perte d'integrite.",
        body_style
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print("PDF genere avec succes :", pdf_path)

if __name__ == '__main__':
    build_pdf()
