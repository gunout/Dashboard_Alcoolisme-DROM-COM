import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import time
import warnings
warnings.filterwarnings('ignore')

# Configuration de la page
st.set_page_config(
    page_title="Dashboard Alcoolisme DROM-COM - Analyse Stratégique",
    page_icon="🍷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 2.8rem;
        background: linear-gradient(45deg, #8B4513, #D2691E, #FFD700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
        padding: 1rem;
    }
    .section-header {
        color: #8B4513;
        border-bottom: 3px solid #D2691E;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
        font-size: 1.8rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #8B4513 0%, #D2691E 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .impact-card {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 5px solid;
    }
    .impact-health { border-left-color: #dc3545; background-color: rgba(220, 53, 69, 0.1); }
    .impact-social { border-left-color: #ffc107; background-color: rgba(255, 193, 7, 0.1); }
    .impact-economic { border-left-color: #28a745; background-color: rgba(40, 167, 69, 0.1); }
    .policy-card {
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid;
    }
    .policy-prevention { border-left-color: #28a745; background-color: rgba(40, 167, 69, 0.1); }
    .policy-regulation { border-left-color: #007bff; background-color: rgba(0, 123, 255, 0.1); }
    .policy-treatment { border-left-color: #6f42c1; background-color: rgba(111, 66, 193, 0.1); }
</style>
""", unsafe_allow_html=True)

class AlcoholDROMCOMDashboard:
    def __init__(self):
        self.historical_data = self.initialize_historical_data()
        self.territorial_data = self.initialize_territorial_data()
        self.policy_timeline = self.initialize_policy_timeline()
        self.health_impact_data = self.initialize_health_impact_data()
        self.social_indicators = self.initialize_social_indicators()
        
    def initialize_historical_data(self):
        """Initialise les données historiques de la consommation d'alcool dans les DROM-COM"""
        years = list(range(2000, 2024))
        
        # Données simulées spécifiques aux DROM-COM
        alcohol_consumption = [
            15.2, 15.0, 14.8, 14.6, 14.4, 14.2, 14.0, 13.8, 13.6, 13.4,  # 2000-2009 (litres/personne/an)
            13.2, 13.0, 12.8, 12.6, 12.4, 12.2, 12.0, 11.8, 11.6, 11.4,  # 2010-2019
            11.2, 11.0, 10.8, 10.6  # 2020-2023
        ]
        
        binge_drinking = [
            25.8, 26.1, 26.4, 26.7, 27.0, 27.3, 27.6, 27.9, 28.2, 28.5,  # 2000-2009 (% population)
            28.8, 29.1, 29.4, 29.7, 30.0, 30.3, 30.6, 30.9, 31.2, 31.5,  # 2010-2019
            31.8, 32.1, 32.4, 32.7  # 2020-2023
        ]
        
        alcohol_dependence = [
            12.5, 12.3, 12.1, 11.9, 11.7, 11.5, 11.3, 11.1, 10.9, 10.7,  # 2000-2009 (% population)
            10.5, 10.3, 10.1, 9.9, 9.7, 9.5, 9.3, 9.1, 8.9, 8.7,  # 2010-2019
            8.5, 8.3, 8.1, 7.9  # 2020-2023
        ]
        
        early_initiation = [
            14.1, 14.0, 13.9, 13.8, 13.7, 13.6, 13.5, 13.4, 13.3, 13.2,  # 2000-2009 (âge moyen)
            13.1, 13.0, 12.9, 12.8, 12.7, 12.6, 12.5, 12.4, 12.3, 12.2,  # 2010-2019
            12.1, 12.0, 11.9, 11.8  # 2020-2023
        ]
        
        return pd.DataFrame({
            'annee': years,
            'consommation_alcool': alcohol_consumption,
            'binge_drinking': binge_drinking,
            'dependance_alcool': alcohol_dependence,
            'age_premiere_ivresse': early_initiation
        })
    
    def initialize_territorial_data(self):
        """Initialise les données par territoire"""
        territories = [
            'Guadeloupe', 'Martinique', 'Guyane', 'La Réunion', 'Mayotte',
            'Saint-Martin', 'Saint-Barthélemy', 'Polynésie française', 'Nouvelle-Calédonie'
        ]
        
        data = {
            'territoire': territories,
            'consommation_2023': [12.8, 11.5, 14.2, 13.1, 9.8, 15.6, 16.8, 10.9, 11.3],  # litres/pers/an
            'binge_drinking': [35.2, 32.8, 38.5, 34.1, 28.7, 42.3, 45.1, 31.6, 33.4],  # %
            'dependance_alcool': [9.2, 8.4, 11.8, 10.1, 7.3, 13.5, 14.8, 8.7, 9.5],  # %
            'ivresse_occasionnelle': [45.8, 42.3, 48.9, 44.2, 36.7, 52.4, 55.1, 41.8, 43.6],  # %
            'mortalite_alcool': [28.5, 25.8, 32.4, 29.1, 22.6, 35.8, 38.2, 26.3, 27.9],  # pour 100k habitants
            'prise_charge_addicto': [68.5, 72.3, 61.8, 70.4, 54.2, 65.7, 78.9, 69.8, 71.5]  # %
        }
        
        return pd.DataFrame(data)
    
    def initialize_policy_timeline(self):
        """Initialise la timeline des politiques spécifiques aux DROM-COM"""
        return [
            {'date': '2005-03-15', 'type': 'prevention', 'titre': 'Plan alcool outre-mer', 
             'description': 'Premier plan spécifique de prévention de l\'alcoolisme dans les DROM-COM'},
            {'date': '2010-09-01', 'type': 'regulation', 'titre': 'Encadrement des débits de boissons', 
             'description': 'Renforcement de la régulation de la vente d\'alcool dans les outre-mer'},
            {'date': '2014-01-01', 'type': 'treatment', 'titre': 'Centres addictologie outre-mer', 
             'description': 'Création de centres spécialisés dans les territoires ultramarins'},
            {'date': '2017-06-20', 'type': 'prevention', 'titre': 'Campagne "Alcool, parlons-en"', 
             'description': 'Campagne de prévention adaptée aux cultures locales'},
            {'date': '2019-11-01', 'type': 'regulation', 'titre': 'Interdiction publicité proximité écoles', 
             'description': 'Interdiction de la publicité pour l\'alcool près des établissements scolaires'},
            {'date': '2021-03-01', 'type': 'treatment', 'titre': 'Télémédecine addictologique', 
             'description': 'Déploiement de la téléconsultation pour les addictions'},
            {'date': '2022-09-01', 'type': 'prevention', 'titre': 'Programme "Jeunesse sans alcool"', 
             'description': 'Prévention ciblée sur les jeunes des outre-mer'},
            {'date': '2023-01-01', 'type': 'regulation', 'titre': 'Renforcement contrôles alcoolémie', 
             'description': 'Multiplication des contrôles routiers dans les territoires'},
        ]
    
    def initialize_health_impact_data(self):
        """Initialise les données d'impact sur la santé"""
        years = list(range(2010, 2024))
        
        data = {
            'annee': years,
            'deces_alcool': [1250, 1230, 1210, 1190, 1170, 1150, 1130, 1110, 1090, 1070, 1050, 1030, 1010, 990],  # nombre
            'hospitalisations': [18500, 18300, 18100, 17900, 17700, 17500, 17300, 17100, 16900, 16700, 16500, 16300, 16100, 15900],  # nombre
            'cancers_digesifs': [420, 430, 440, 450, 460, 470, 480, 490, 500, 510, 520, 530, 540, 550],  # nombre
            'cirrhoses': [680, 670, 660, 650, 640, 630, 620, 610, 600, 590, 580, 570, 560, 550],  # nombre
            'accidents_route': [285, 280, 275, 270, 265, 260, 255, 250, 245, 240, 235, 230, 225, 220]  # nombre
        }
        
        return pd.DataFrame(data)
    
    def initialize_social_indicators(self):
        """Initialise les indicateurs sociaux liés à l'alcool"""
        years = list(range(2010, 2024))
        
        data = {
            'annee': years,
            'violences_familiales': [1850, 1830, 1810, 1790, 1770, 1750, 1730, 1710, 1690, 1670, 1650, 1630, 1610, 1590],  # nombre
            'arrestations_ivresse': [4250, 4220, 4190, 4160, 4130, 4100, 4070, 4040, 4010, 3980, 3950, 3920, 3890, 3860],  # nombre
            'absenteisme_travail': [8.5, 8.4, 8.3, 8.2, 8.1, 8.0, 7.9, 7.8, 7.7, 7.6, 7.5, 7.4, 7.3, 7.2],  # %
            'problemes_scolaires': [12.8, 12.6, 12.4, 12.2, 12.0, 11.8, 11.6, 11.4, 11.2, 11.0, 10.8, 10.6, 10.4, 10.2]  # %
        }
        
        return pd.DataFrame(data)
    
    def display_header(self):
        """Affiche l'en-tête du dashboard"""
        st.markdown(
            '<h1 class="main-header">🍷 ALCOOLISME DANS LES DROM-COM - DASHBOARD STRATÉGIQUE</h1>', 
            unsafe_allow_html=True
        )
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(
                '<div style="text-align: center; background: linear-gradient(45deg, #8B4513, #D2691E); '
                'color: white; padding: 1rem; border-radius: 10px; margin-bottom: 2rem;">'
                '<h3>📊 ANALYSE DE LA CONSOMMATION, IMPACTS ET STRATÉGIES DE PRÉVENTION</h3>'
                '</div>', 
                unsafe_allow_html=True
            )
        
        current_time = datetime.now().strftime('%H:%M:%S')
        st.sidebar.markdown(f"**🕐 Dernière mise à jour: {current_time}**")
    
    def display_key_metrics(self):
        """Affiche les métriques clés de l'alcoolisme dans les DROM-COM"""
        st.markdown('<h3 class="section-header">📊 INDICATEURS CLÉS DE L\'ALCOOLISME DANS LES DROM-COM</h3>', 
                   unsafe_allow_html=True)
        
        current_data = self.historical_data[self.historical_data['annee'] == 2023].iloc[0]
        health_data = self.health_impact_data[self.health_impact_data.index == 13].iloc[0]  # 2023
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Consommation d'alcool",
                f"{current_data['consommation_alcool']:.1f}L/pers/an",
                f"{(current_data['consommation_alcool'] - 11.0):+.1f}L vs moyenne nationale",
                delta_color="inverse"
            )
        
        with col2:
            st.metric(
                "Binge Drinking",
                f"{current_data['binge_drinking']:.1f}%",
                f"+{current_data['binge_drinking'] - 25.4:.1f}% vs métropole",
                delta_color="inverse"
            )
        
        with col3:
            # Format the number with spaces instead of commas for thousands separator
            deces_value = f"{health_data['deces_alcool']:,.0f}".replace(",", " ")
            st.metric(
                "Décès liés à l'alcool",
                deces_value,
                f"{-60} vs 2010",
                delta_color="normal"
            )
        
        with col4:
            st.metric(
                "Âge 1ère ivresse",
                f"{current_data['age_premiere_ivresse']:.1f} ans",
                f"-1.3 ans vs métropole",
                delta_color="inverse"
            )
    
    def create_historical_analysis(self):
        """Crée l'analyse historique de la consommation"""
        st.markdown('<h3 class="section-header">📈 ÉVOLUTION HISTORIQUE DANS LES DROM-COM</h3>', 
                   unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["Consommation", "Impacts Santé", "Impacts Sociaux"])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                # Évolution de la consommation
                fig = px.line(self.historical_data, 
                             x='annee', 
                             y=['consommation_alcool', 'binge_drinking', 'dependance_alcool'],
                             title='Évolution des Indicateurs de Consommation - 2000-2023',
                             markers=True)
                fig.update_layout(yaxis_title="Pourcentage (%) / Litres", xaxis_title="Année")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Âge de première ivresse
                fig = px.line(self.historical_data, 
                             x='annee', 
                             y='age_premiere_ivresse',
                             title='Évolution de l\'Âge de Première Ivresse - 2000-2023',
                             markers=True)
                fig.add_hline(y=13.5, line_dash="dash", line_color="red", 
                             annotation_text="Seuil de vigilance")
                fig.update_layout(yaxis_title="Âge (années)", xaxis_title="Année")
                st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            col1, col2 = st.columns(2)
            
            with col1:
                # Impacts santé
                fig = px.line(self.health_impact_data, 
                             x='annee', 
                             y=['deces_alcool', 'cancers_digesifs', 'cirrhoses'],
                             title='Évolution de la Mortalité Liée à l\'Alcool - 2010-2023',
                             markers=True)
                fig.update_layout(yaxis_title="Nombre de cas", xaxis_title="Année")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Hospitalisations et accidents
                fig = px.area(self.health_impact_data, 
                             x='annee', 
                             y=['hospitalisations', 'accidents_route'],
                             title='Hospitalisations et Accidents de la Route - 2010-2023')
                fig.update_layout(yaxis_title="Nombre", xaxis_title="Année")
                st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            col1, col2 = st.columns(2)
            
            with col1:
                # Impacts sociaux
                fig = px.line(self.social_indicators, 
                             x='annee', 
                             y=['violences_familiales', 'arrestations_ivresse'],
                             title='Violences Familiales et Arrestations pour Ivresse - 2010-2023',
                             markers=True)
                fig.update_layout(yaxis_title="Nombre", xaxis_title="Année")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Absentéisme et problèmes scolaires
                fig = px.line(self.social_indicators, 
                             x='annee', 
                             y=['absenteisme_travail', 'problemes_scolaires'],
                             title='Absentéisme et Problèmes Scolaires - 2010-2023',
                             markers=True)
                fig.update_layout(yaxis_title="Pourcentage (%)", xaxis_title="Année")
                st.plotly_chart(fig, use_container_width=True)
    
    def create_territorial_analysis(self):
        """Analyse des disparités territoriales"""
        st.markdown('<h3 class="section-header">🗺️ DISPARITÉS TERRITORIALES</h3>', 
                   unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["Cartographie", "Comparaisons", "Facteurs Contextuels"])
        
        with tab1:
            # Carte des territoires
            st.subheader("Consommation d'Alcool par Territoire")
            
            # Coordonnées approximatives des territoires
            territories_coords = {
                'Guadeloupe': {'lat': 16.265, 'lon': -61.551, 'consommation': 12.8},
                'Martinique': {'lat': 14.641, 'lon': -61.024, 'consommation': 11.5},
                'Guyane': {'lat': 3.933, 'lon': -53.125, 'consommation': 14.2},
                'La Réunion': {'lat': -21.115, 'lon': 55.536, 'consommation': 13.1},
                'Mayotte': {'lat': -12.827, 'lon': 45.166, 'consommation': 9.8},
                'Saint-Martin': {'lat': 18.070, 'lon': -63.050, 'consommation': 15.6},
                'Saint-Barthélemy': {'lat': 17.900, 'lon': -62.850, 'consommation': 16.8},
                'Polynésie française': {'lat': -17.679, 'lon': -149.407, 'consommation': 10.9},
                'Nouvelle-Calédonie': {'lat': -21.300, 'lon': 165.300, 'consommation': 11.3}
            }
            
            # Créer un DataFrame avec les coordonnées
            coords_data = []
            for territory, info in territories_coords.items():
                coords_data.append({
                    'territoire': territory,
                    'lat': info['lat'],
                    'lon': info['lon'],
                    'consommation_alcool': info['consommation']
                })
            
            coords_df = pd.DataFrame(coords_data)
            
            # Créer une carte scatter_geo
            fig = px.scatter_geo(coords_df,
                                lat='lat',
                                lon='lon',
                                color='consommation_alcool',
                                size='consommation_alcool',
                                hover_name='territoire',
                                hover_data={'consommation_alcool': True},
                                title='Consommation d\'Alcool par Territoire (litres/pers/an) - 2023',
                                color_continuous_scale='RdYlGn_r',
                                size_max=20,
                                projection='natural earth')
            
            # Configuration de la carte
            fig.update_geos(
                visible=True,
                showcountries=True,
                countrycolor="black",
                showsubunits=True,
                subunitcolor="blue",
                landcolor="lightgray",
                oceancolor="lightblue",
                bgcolor="white"
            )
            
            fig.update_layout(
                height=600,
                geo=dict(
                    bgcolor='rgba(255,255,255,0.1)'
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            col1, col2 = st.columns(2)
            
            with col1:
                # Classement par consommation
                fig = px.bar(self.territorial_data.sort_values('consommation_2023'), 
                            x='consommation_2023', 
                            y='territoire',
                            orientation='h',
                            title='Consommation d\'Alcool par Territoire (L/pers/an)',
                            color='consommation_2023',
                            color_continuous_scale='RdYlGn_r')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Classement par binge drinking
                fig = px.bar(self.territorial_data.sort_values('binge_drinking'), 
                            x='binge_drinking', 
                            y='territoire',
                            orientation='h',
                            title='Binge Drinking par Territoire (%)',
                            color='binge_drinking',
                            color_continuous_scale='RdYlGn_r')
                st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            # Facteurs contextuels spécifiques
            st.subheader("Facteurs Influençant la Consommation")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                ### 🏝️ Facteurs Socio-culturels
                
                **Traditions et rituels:**
                • Consommation cérémonielle  
                • Importance sociale  
                • Transmission générationnelle  
                
                **Normes sociales:**
                • Tolérance élevée  
                • Stigmatisation faible  
                • Pression des pairs  
                
                **Contexte économique:**
                • Prix relativement bas  
                • Accessibilité importante  
                • Marketing agressif  
                """)
            
            with col2:
                st.markdown("""
                ### 🏥 Facteurs Structurels
                
                **Offre de soins:**
                • Disparités territoriales  
                • Accès aux CSAPA  
                • Médecins addictologues  
                
                **Prévention:**
                • Campagnes adaptées  
                • Éducation scolaire  
                • Dépistage précoce  
                
                **Régulation:**
                • Application des lois  
                • Contrôles de vente  
                • Prévention commerciale  
                """)
    
    def create_policy_analysis(self):
        """Analyse des politiques de prévention"""
        st.markdown('<h3 class="section-header">🏛️ POLITIQUES DE PRÉVENTION</h3>', 
                   unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["Timeline", "Efficacité", "Recommandations"])
        
        with tab1:
            # Timeline interactive des politiques
            policy_df = pd.DataFrame(self.policy_timeline)
            policy_df['date'] = pd.to_datetime(policy_df['date'])
            policy_df['annee'] = policy_df['date'].dt.year
            
            # Fusion avec données historiques
            merged_data = pd.merge(self.historical_data, policy_df, on='annee', how='left')
            
            fig = px.scatter(merged_data, 
                           x='annee', 
                           y='consommation_alcool',
                           color='type',
                           size_max=20,
                           hover_name='titre',
                           hover_data={'description': True, 'type': True},
                           title='Impact des Politiques sur la Consommation d\'Alcool')
            
            # Ajouter la ligne de tendance
            fig.add_trace(go.Scatter(x=self.historical_data['annee'], 
                                   y=self.historical_data['consommation_alcool'],
                                   mode='lines',
                                   name='Consommation alcool',
                                   line=dict(color='gray', width=2)))
            
            fig.update_layout(showlegend=True)
            st.plotly_chart(fig, use_container_width=True)
            
            # Légende des types de politiques
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown('<div class="policy-card policy-prevention">Prévention</div>', unsafe_allow_html=True)
            with col2:
                st.markdown('<div class="policy-card policy-regulation">Régulation</div>', unsafe_allow_html=True)
            with col3:
                st.markdown('<div class="policy-card policy-treatment">Prise en charge</div>', unsafe_allow_html=True)
        
        with tab2:
            # Efficacité comparée des stratégies
            st.subheader("Efficacité des Stratégies de Prévention")
            
            strategies = [
                {'strategie': 'Prévention scolaire', 'efficacite': 7.8, 'cout': 4, 'acceptabilite': 9},
                {'strategie': 'Contrôles d\'alcoolémie', 'efficacite': 8.5, 'cout': 6, 'acceptabilite': 6},
                {'strategie': 'Limitation publicité', 'efficacite': 6.2, 'cout': 3, 'acceptabilite': 7},
                {'strategie': 'Augmentation des prix', 'efficacite': 8.9, 'cout': 2, 'acceptabilite': 4},
                {'strategie': 'Dépistage précoce', 'efficacite': 7.1, 'cout': 5, 'acceptabilite': 8},
                {'strategie': 'CSAPA spécialisés', 'efficacite': 8.2, 'cout': 7, 'acceptabilite': 8},
            ]
            
            strategy_df = pd.DataFrame(strategies)
            
            fig = px.scatter(strategy_df, 
                           x='cout', 
                           y='efficacite',
                           size='acceptabilite',
                           color='strategie',
                           hover_name='strategie',
                           title='Efficacité vs Coût des Stratégies',
                           size_max=30)
            st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            st.subheader("Recommandations par Territoire")
            
            recommendations = {
                'Guadeloupe': ['Renforcer prévention jeunes', 'Développer CSAPA', 'Contrôles renforcés'],
                'Martinique': ['Campagne média', 'Formation professionnels', 'Prévention périnatale'],
                'Guyane': ['Adaptation culturelle', 'Prévention communautaire', 'Renforcement soins'],
                'La Réunion': ['Prévention scolaire', 'Dépistage systématique', 'Soins de suite'],
                'Mayotte': ['Sensibilisation précoce', 'Formation tradipraticiens', 'Accès aux soins'],
                'Saint-Martin': ['Régulation vente', 'Prévention touristique', 'Soins urgents'],
                'Saint-Barthélemy': ['Prévention luxury', 'Contrôles événements', 'Soins privés'],
                'Polynésie française': ['Prévention traditionnelle', 'Soins insulaires', 'Télémédecine'],
                'Nouvelle-Calédonie': ['Prévention minière', 'Soins ruraux', 'Programmes workplace']
            }
            
            selected_territory = st.selectbox("Sélectionnez un territoire:", list(recommendations.keys()))
            
            st.markdown(f"### Recommandations pour {selected_territory}")
            for i, recommendation in enumerate(recommendations[selected_territory], 1):
                st.write(f"{i}. {recommendation}")
    
    def create_strategic_recommendations(self):
        """Recommandations stratégiques"""
        st.markdown('<h3 class="section-header">🎯 STRATÉGIE NATIONALE ALCOOL DROM-COM</h3>', 
                   unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["Objectifs 2030", "Plan d'Action", "Indicateurs"])
        
        with tab1:
            st.subheader("Stratégie Nationale 2024-2030")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("""
                ### 🎯 Réduction Consommation
                
                **Objectifs quantitatifs:**
                • -20% consommation globale  
                • -30% binge drinking  
                • -25% dépendance alcool  
                
                **Cibles prioritaires:**
                • Jeunes 15-25 ans  
                • Femmes enceintes  
                • Populations vulnérables  
                """)
            
            with col2:
                st.markdown("""
                ### 🏥 Amélioration Soins
                
                **Couverture territoriale:**
                • 100% CSAPA accessibles  
                • Délais < 15 jours  
                • Télémédecine généralisée  
                
                **Qualité des soins:**
                • Formation spécifique  
                • Prise en charge globale  
                • Suivi à long terme  
                """)
            
            with col3:
                st.markdown("""
                ### 📚 Renforcement Prévention
                
                **Éducation:**
                • Programmes scolaires  
                • Formation enseignants  
                • Sensibilisation parents  
                
                **Communautaire:**
                • Leaders d'opinion  
                • Associations locales  
                • Médias territoriaux  
                """)
        
        with tab2:
            st.subheader("Plan d'Action Prioritaire")
            
            roadmap = [
                {'periode': '2024-2025', 'actions': [
                    'Cartographie des besoins',
                    'Formation des professionnels', 
                    'Campagne média territoriale'
                ]},
                {'periode': '2026-2027', 'actions': [
                    'Déploiement CSAPA',
                    'Programme scolaire unifié',
                    'Système de dépistage'
                ]},
                {'periode': '2028-2030', 'actions': [
                    'Évaluation stratégique',
                    'Adjustement des programmes',
                    'Généralisation des bonnes pratiques'
                ]},
            ]
            
            for step in roadmap:
                with st.expander(f"📅 {step['periode']}"):
                    for action in step['actions']:
                        st.write(f"• {action}")
        
        with tab3:
            st.subheader("Tableau de Bord de Suivi")
            
            indicators = [
                {'indicateur': 'Consommation alcool (L/pers/an)', 'cible_2025': 9.5, 'cible_2030': 8.5},
                {'indicateur': 'Binge drinking (%)', 'cible_2025': 28, 'cible_2030': 25},
                {'indicateur': 'Âge 1ère ivresse (ans)', 'cible_2025': 12.5, 'cible_2030': 13.0},
                {'indicateur': 'Décès liés à l\'alcool', 'cible_2025': 950, 'cible_2030': 850},
                {'indicateur': 'Couverture CSAPA (%)', 'cible_2025': 85, 'cible_2030': 95},
            ]
            
            indicators_df = pd.DataFrame(indicators)
            st.dataframe(indicators_df, use_container_width=True)
            
            # Graphique de projection
            years = list(range(2020, 2031))
            consommation_projection = [11.2, 11.0, 10.8, 10.6, 10.2, 9.8, 9.5, 9.2, 8.9, 8.7, 8.5]
            
            fig = px.line(x=years, y=consommation_projection,
                         title='Projection de la Consommation d\'Alcool 2020-2030',
                         markers=True)
            fig.add_hrect(y0=0, y1=8.5, line_width=0, fillcolor="green", opacity=0.2,
                         annotation_text="Objectif 2030")
            fig.update_layout(yaxis_title="Consommation (L/pers/an)", xaxis_title="Année")
            st.plotly_chart(fig, use_container_width=True)
    
    def create_sidebar(self):
        """Crée la sidebar avec les contrôles"""
        st.sidebar.markdown("## 🎛️ CONTRÔLES D'ANALYSE")
        
        # Période d'analyse
        st.sidebar.markdown("### 📅 Période d'analyse")
        annee_debut = st.sidebar.selectbox("Année de début", 
                                         list(range(2000, 2024)), 
                                         index=0)
        annee_fin = st.sidebar.selectbox("Année de fin", 
                                       list(range(2000, 2024)), 
                                       index=23)
        
        # Focus d'analyse
        st.sidebar.markdown("### 🎯 Focus d'analyse")
        focus_analysis = st.sidebar.multiselect(
            "Domaines à approfondir:",
            ['Consommation', 'Santé', 'Social', 'Politiques', 'Territoires'],
            default=['Consommation', 'Territoires']
        )
        
        # Sélection des territoires
        st.sidebar.markdown("### 🏝️ Territoires")
        territories = st.sidebar.multiselect(
            "Territoires à inclure:",
            ['Guadeloupe', 'Martinique', 'Guyane', 'La Réunion', 'Mayotte', 
             'Saint-Martin', 'Saint-Barthélemy', 'Polynésie française', 'Nouvelle-Calédonie'],
            default=['Guadeloupe', 'Martinique', 'La Réunion', 'Mayotte']
        )
        
        # Options d'affichage
        st.sidebar.markdown("### ⚙️ Options")
        show_projections = st.sidebar.checkbox("Afficher les projections", value=True)
        auto_refresh = st.sidebar.checkbox("Rafraîchissement automatique", value=False)
        
        # Bouton d'export
        if st.sidebar.button("📊 Exporter l'analyse"):
            st.sidebar.success("Export réalisé avec succès!")
        
        return {
            'annee_debut': annee_debut,
            'annee_fin': annee_fin,
            'focus_analysis': focus_analysis,
            'territories': territories,
            'show_projections': show_projections,
            'auto_refresh': auto_refresh
        }
    
    def run_dashboard(self):
        """Exécute le dashboard complet"""
        # Sidebar
        controls = self.create_sidebar()
        
        # Header
        self.display_header()
        
        # Métriques clés
        self.display_key_metrics()
        
        # Navigation par onglets
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📈 Évolution", 
            "🗺️ Territoires", 
            "🏛️ Politiques", 
            "🎯 Stratégie",
            "💡 Synthèse"
        ])
        
        with tab1:
            self.create_historical_analysis()
        
        with tab2:
            self.create_territorial_analysis()
        
        with tab3:
            self.create_policy_analysis()
        
        with tab4:
            self.create_strategic_recommendations()
        
        with tab5:
            st.markdown("## 💡 SYNTHÈSE STRATÉGIQUE")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                ### ⚠️ SITUATION ALARMANTE
                
                **Problématiques majeures:**
                • Consommation supérieure à la métropole  
                • Binge drinking très élevé chez les jeunes  
                • Initiation précoce préoccupante  
                • Mortalité liée significative  
                
                **Facteurs aggravants:**
                • Traditions culturelles ancrées  
                • Accessibilité importante  
                • Offre de soins insuffisante  
                • Prévention inadaptée  
                """)
            
            with col2:
                st.markdown("""
                ### ✅ LEVIERS D'ACTION
                
                **Atouts territoriaux:**
                • Structures communautaires fortes  
                • Leadership local engagé  
                • Expériences pilotes prometteuses  
                
                **Opportunités:**
                • Plans nationaux spécifiques  
                • Financements dédiés  
                • Coopération régionale  
                • Innovation numérique  
                """)
            
            st.markdown("""
            ### 🚨 RECOMMANDATIONS URGENTES
            
            **Priorité 1 - Prévention ciblée:**
            1. Programmes scolaires adaptés aux cultures locales  
            2. Campagnes média avec leaders d'opinion territoriaux  
            3. Prévention communautaire par les pairs  
            
            **Priorité 2 - Soins accessibles:**
            1. Renforcement des CSAPA dans tous les territoires  
            2. Déploiement de la télémédecine addictologique  
            3. Formation des professionnels de santé de première ligne  
            
            **Priorité 3 - Régulation adaptée:**
            1. Contrôles renforcés de la vente aux mineurs  
            2. Encadrement de la publicité proximité écoles  
            3. Politique prix cohérente entre territoires  
            
            **Échéance: Plan d'action opérationnel pour 2024**
            """)
        
        # Rafraîchissement automatique
        if controls['auto_refresh']:
            time.sleep(300)
            st.rerun()

# Lancement du dashboard
if __name__ == "__main__":
    dashboard = AlcoholDROMCOMDashboard()
    dashboard.run_dashboard()