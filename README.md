## 🦠 Covid Tracker : Dashboard Interactif avec Streamlit

#### Contexte

La pandémie de Covid-19 a été marquée par des vagues successives affectant différemment les pays et les périodes de l’année.  
Ce projet vise à construire un dashboard interactif permettant de suivre l’évolution des cas de Covid à partir des données publiées par l’European Centre for Disease Prevention and Control (ECDC).

#### Problématique

Comment analyser et visualiser les vagues de Covid-19 à l’échelle mondiale, et que révèle l’étude du cas français sur la dynamique de l’épidémie ?

#### Objectif du projet

Créer une application web accessible depuis un navigateur, simple à développer et à utiliser, afin de partager un travail d’analyse des données Covid avec d’autres utilisateurs.

#### Fichiers de données

Le projet exploite les données officielles de l'UE/EEE fournies par l'ECDC :
- data.csv : archive regroupant les relevés quotidiens des nouveaux cas sur la période 2020-2022
- Source : [European Centre for Disease Prevention and Control (ECDC)](https://www.ecdc.europa.eu/en/publications-data/data-daily-new-cases-covid-19-eueea-country)

#### Environnement technique

Le projet s’appuie sur deux outils clés pour faciliter le développement et la diffusion de l’analyse :
- **Docker** : sert à créer un environnement de travail autonome. Il garantit que le projet s'exécute de la même manière sur n'importe quel ordinateur, évitant ainsi les erreurs liées aux différences de systèmes ou de versions de logiciels.
- **Streamlit** : permet de convertir le script d'analyse Python en un dashboard web interactif. Cela offre une exploration visuelle des données directement via un navigateur et facilite le partage du projet sans que l'utilisateur n'ait besoin d'installer de logiciels spécifiques.

#### Déploiement et hébergement

L'application est hébergée sur Streamlit Cloud, ce qui permet d'accéder au dashboard directement via un navigateur web sans aucune installation complexe.  
Le projet est relié à ce dépôt GitHub. Cette intégration permet un déploiement continu : toute modification apportée au code source est instantanément mise à jour sur l'application en ligne, garantissant ainsi la transparence et la disponibilité des dernières analyses.

#### Méthodologie

**Préparation de l’environnement de travail**
- Téléchargement du fichier data.csv contenant les données Covid à analyser
- Création du fichier app.py dans le dossier de travail covid_tracker  
Ce fichier correspond au script Python exécuté par Streamlit lors du lancement de l’application et définit l’interface utilisateur de l’application web.

**Environnement Docker**
- Lancement de Docker Desktop
- Lancement d’un conteneur Docker à partir d’une image Docker déjà existante et préconfigurée  
Cette image fournit un environnement prêt à l’emploi comprenant Linux, Python, Streamlit ainsi que les librairies nécessaires au projet.
- La commande docker run est utilisée pour créer et démarrer le conteneur.
Elle permet de configurer :
    - un accès interactif au terminal du conteneur
    - un dossier partagé entre l’ordinateur hôte et le conteneur
    - un port réseau afin d’accéder à l’application via un navigateur web  
Commande utilisée : docker run -it -v "$(pwd):/home/app" -p 4000:4000 jedha/streamlit-fs-image

**Lancement de l’application web**
- L’application Streamlit est lancée depuis le conteneur Docker
- Streamlit démarre un serveur web et exécute le script app.py, générant dynamiquement l’interface utilisateur accessible depuis un navigateur web à l’adresse http://localhost:4000.  
Commande utilisée : streamlit run app.py --server.port 4000 --server.address 0.0.0.0
- Activation de l’option « Run on save » dans les Settings de Streamlit pour le rafraîchissement automatique de l’application

**Initialisation et préparation des données**
- Import du fichier data.csv dans l’application Streamlit
- Mise en cache des données à l’aide du mécanisme @st.cache_data afin d’optimiser les performances et d’éviter les rechargements inutiles
- Création d’un DataFrame interactif permettant l’exploration des données au sein de l’application

**Création des visualisations et analyse des données**
- Préparation du script pour les visualisations du dashboard
- Mise en place des premiers graphiques interactifs afin de visualiser l’évolution des cas de Covid au fil du temps
- Utilisation de filtres interactifs (pays, périodes) pour permettre l’exploration dynamique des données
- Analyse visuelle des différentes vagues de Covid à partir des graphiques générés

**Mise en ligne et déploiement final**
- Création d'un répertoire sur GitHub pour y déposer les fichiers du projet (app.py, data.csv, requirements.txt) et son descriptif (README.md).
- Liaison de ce répertoire à la plateforme Streamlit Cloud pour rendre l'application accessible sur internet.
- Cette étape permet de passer d'un travail sur ordinateur local (via Docker) à un dashboard final disponible en ligne via une simple adresse web.

#### Résultats clés

🌍 **Analyse au niveau mondial**

- **Évolution des cas cumulés** : Le nombre total de cas atteint environ 170 millions sur la période 2020-2022. La progression est restée relativement graduelle jusqu'à fin 2021, avant de connaître une accélération marquée début 2022.
- **Effet Omicron** : Cette accélération coïncide avec la vague Omicron. À elle seule, cette période représente une part significative du volume total de cas enregistrés depuis le début de la pandémie.

🇫🇷 **Analyse spécifique à la France**

- **Intensité des vagues épidémiques** : La vague de janvier 2022 est de loin la plus intense, avec des pics journaliers dépassant les 500 000 cas, soit plusieurs fois le niveau des vagues précédentes (qui culminaient entre 60 000 et 100 000 cas).
- **Dynamique de l'épidémie** : Avec un taux de croissance mensuel de 1,457, les données confirment que l'épidémie était encore en phase de progression à la date de clôture du jeu de données.

📉 **Dissociation entre l’intensité épidémique et l’impact sanitaire**

- **Maîtrise de la mortalité**: Un constat analytique majeur réside dans la dissociation entre le nombre de cas et le nombre de décès. Le pic de mortalité le plus élevé (environ 2 000/jour) se situe au printemps 2020, bien avant la vague de cas la plus massive de 2022.
- **Interprétation** : Ce résultat met en évidence une amélioration progressive de la situation sanitaire. Il s'explique par la protection immunitaire apportée par la campagne de vaccination combinée à la moindre virulence intrinsèque des variants tardifs.

#### Conclusion

Ce dashboard permet une lecture claire et interactive de la crise sanitaire sur la période 2020-2022.  
Si l'analyse mondiale montre une tendance générale, la dynamique de l’épidémie est restée très hétérogène d'un pays à l'autre, ce qui justifie le choix d'un focus spécifique à la France afin d’observer les mécanismes au niveau national.  
L'étude montre que, malgré des vagues de contaminations croissantes, la mortalité a progressivement diminué par rapport au nombre de cas. Ce décalage illustre l’impact combiné de la vaccination, de l’amélioration de la prise en charge médicale et de l’évolution de l’immunité collective.  
Sur le plan technique, Streamlit a permis de transformer une analyse de données en une application web interactive et accessible sans infrastructure complexe, validant ainsi la pertinence de cette approche pour des projets de visualisation exploratoire.


