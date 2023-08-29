# Derrière PandaScan 🐼 ( L'histoire )

## Table des Matières
- [Introduction](#introduction)
- [Idée 💡](#idée-💡)
- [Défis ⛔️](#défis-⛔️)
- [Développement 🏗️](#développement-🏗️)
- [Leçons tirées ✍️](#leçons-tirées-✍️)
- [Remerciements](#remerciements)

#

## **Introduction**

Bonjour 👋, je m'appelle Charles, j'ai 22 ans et je suis en dernière année d'école d'ingénieur à ECAM-EPMI Cergy en 🇫🇷 

Depuis quelques années je suis passionné par l'informatique et la programmation en général ! Comme tout étudiant classique j'ai eu à apprendre de nombreux langages de programmation durant mon cursus comme HTML, CSS, JavaScript , C etc.. 

Cependant je me suis davantage plu à l'apprentissage de Python 🐍 qui est un langage dont la simplicité et l'efficacité est assez remarquable. Machine Learning, Automatisation, Création d'applications etc.. Les possibilités avec ce langage sont vastes et variées. J'ai donc sauter dans le bain et depuis quelques années je ne cesse d'apprendre de nouvelles choses, que ce soit à travers des projets personnels, des formations ou des vidéos Youtube !

Dans ce document, nous plongerons dans le parcours de création de PandaScan 🐼, un projet qui me tient énormément à coeur, depuis son idée initiale jusqu'à sa mise en œuvre et au-delà. L'histoire qui va suivre a pour but de vous transmettre ma passion, vous faire connaître les défis que j'ai pu rencontrer et les enseignements qui ont façonné ce projet.

#

## Idée 💡
C'est en regardant des vidéos sur Tiktok que m'est venu l'idée ! Des comptes diffusaient des pages de scans de mes mangas favoris et je me suis demander comment ils le faisaient vu que la plupart si ce n'est tous les sites de lecture de manga en ligne qui ne nous permettent pas de télécharger ces pages automatiquement. Je me suis dit que si je voulais faire la même chose j'allais perdre un temps énorme à sélectionner chaque page de chapitres de manga pour les télécharger. Le besoin de créer une solution qui me permette de télécharger automatiquement les chapitres de manga que je voulais provient aussi du fait que ces derniers ne sont accessibles qu'à travers une connexion internet ce qui est dommage lorsque nous voulons y accéder même Hors ligne ou en région reculée, loin de tout. 
#

## Défis ⛔️
Comme tout projet et tout développeur qui se respecte, j'ai bien évidemment fais face à de nombreux problèmes ce qui m'a fallu de nombreux jours de debuggage. Les principaux défis auxquels j'ai fait face sont  principalement liés aux syntaxes obsolètes de certaines bibliothèques, la récupération des données pour les sites et la création d'une interface utilisateur simple et facile à prendre en main. J'ai passer beaucoup de temps à tester , débugger et fouiller. Savoir fouiller au bon endroit et trouver la solution à un problème spécifique procure énormément de satisfaction !

#

## Développement 🏗️
Avant de commencer mon projet, il fallait vérifier que le problème 'avait pas encore été résolu. À ma grande surprise il existait bel et bien des outils pour le faire mais qui ne prenaient pas en compte le côté francophone ! J'ai donc décider de me lancer dans l'aventure. Je savais qu'il me fallait un moyen d'**aller sur les sites de lecture de manga en ligne**, **récupérer les pages => du chapitre => d'un manga** que je voulais et le **stocker dans un dossier** sur mon ordinateur ! Sur le papier ça avait l'air simple à faire étant donné que j'avais déjà eu à faire au scraping web auparavant.

1. Le test
   
Dans cette étape, il fallait tester l'accès au site et le téléchargement d'une page pour s'assurer qu'il était possible de réaliser le projet.
L'accès était possible avec Request ou avec Selenium néanmoins j'avais besoin de voir ce qui se passait lorsque mon script s'exécutait, j'ai donc opter pour la combinaison Sélénium + Request. J'accédais à la page de mon manga et j'envoyais une requête pour télécharger le manga et le tour était joué. Trop simple, les développeurs du site avaient compliqué la tâche et avaient cacher l'adresse qui contenait l'image dans une autre page. J'ai pu rapidement contourner cette restriction mais le serveur refusait mes requêtes j'ai donc décider de chercher un autre moyen de récupérer l'image. Après quelques jours de réflexions il m'est venu à l'esprit l'idée de prendre tout simplement un screenshot de l'image en question ! C'était à ma grande surprise possible avec Sélénium. Le script n'était pas parfait mais il fonctionnait ! Par ailleurs je n'aimais pas les zones sombres que la capture d'écran téléchargait, je voulais l'image seule, propre , à la taille originale et qui prenait peu d'espace parce que oui, les captures d'écrans prenient de la place ( 3 Mo/capture en moyenne ). J'ai donc chercher un moyen de "crop" l'image après capture mais je me heurtait à un autre problème : les pages ne sont pas toutes de la même taille et ne sont pas toutes au même format ( certaines etaient verticales et d'autres à l'horizontale ). Après quelques nuits de test j'ai pu réaliser le script qui me permettait de "crop" l'image à la bonne taille et au bon format !  

3. À l'action
   
Dans cette étape il fallait automatiser le processus : accéder à la première page du manga, télécharger cette page et la stocker dans un dossier qui aurait "Le nom du manga" et qui contiendrait le "nom du chapitre en cours de téléchargement", puis il fallait accéder à la page suivante et ajouter cette dernière au sous-dossier créé. Il fallait le faire jusqu'à ce que tout le chapitre soit télécharger ! L'utilisation de boucles était indispensable, Il fallait trouver un "pattern" qui me permette d'accéder aux pages suivantes en incrémentant une valeur ce qui était assez facile car les sites suivaient tous la même architecture : " site/nom_du_manga/N°chapitre/page " je n'avais qu'à incrémenter "page" et le tour était joué. Le script fonctionnait à merveille ! Malheureusement celà ne suffisait pas ..

4. Tout Automatiser

Bien que tout fonctionnait parfaitement , Il était pénible de saisir à chaque fois l'adresse du manga dans mon script, trouver le pattern pour ensuite télécharger le manga. Il me fallait un moyen plus simple d'accéder au manga que je voulais, mais aussi au chapitre que je voulais ! D'où la nécessité de récupérer les données concernant tous les numéros de chapitre et tous les noms de mangas disponibles du site. Cette étape était pénible mais utile pour la suite.

5. L'interface Graphique

Pour permettre l'utilisation à d'autres de cet outil, il me fallait mettre à l'épreuve mes compétences de designer et de développeur. Je remercie "" Pour avoir développer le superbe outil qu'est [tkinter-designer]() qui m'a considérablement accélérer le processus de développement ! J'ai découvert le super outil qu'est Figma et l'application prenait enfin forme ..

6. Le drame

Mon script n'était basé que sur un seul site web à l'époque et ce que je redoutais arriva : CloudFlare ! L'énnemie juré des scrapeurs web, la barrière à l'automatisation de tâches était arrivée sur Japscan. J'ai passer énormément de temps à chercher un moyen de contourner cette restriction : Utilisation de proxys, Changement d'User Agent, Undetected-chromedriver .. Tous sans succès. La solution la plus simple était de changer de site et de recommencer le processus.

7. Rescapé

J'ai pu trouver dans mes recherches des sites ayant une bonne structure , un catalogue assez large de mangas et accessibles avec de simples requêtes ! Le Graal du scrapeur. après avoir passer quelques nuits blanches à développer des scriptes de scraping pour les sites en question, j'ai pu enfin les intégrer à mon application !

8. Développer et améliorer

Comme tout bon perfectionniste qui se respecte je ne pouvais pas m'arrêter à cette tâche, il me fallait absolument rendre le script disponible, compréhensible et organisé. Je vous passe les détails, je suis encore entrain de me casser la tête .. Néanmoins la version de test est disponible [ici]()

9. Une feature de luxe

Pour atteindre l'automatisation ultime, il me fallait un moyen de rendre les données à jour et éviter à l'utilisateur de lancer manuellement le script pour mettre à jour les mangas ou les chapitres disponibles au téléchargement. J'ai donc gérer l'exécution de ces scripts en créant un fichier JSON de configuration qui permette de coisir entre une mise à jour manuelle ou automatique au lancement de l'application. J'ai aussi mis en place un système qui permette de traquer chaque changement dans les données de chaque site : Les mangas et chapitres ajoutés ou supprimés, la date et l'heure de la mise à jour. 

## Leçons tirées ✍️
Partagez les leçons précieuses que vous avez tirées de votre travail sur PandaScan. Réfléchissez à ce qui s'est bien passé et à ce qui aurait pu être fait différemment. Offrez des idées aux développeurs en herbe ou à ceux intéressés par des projets similaires.

#

## Remerciements
Exprimez votre gratitude envers les individus, les communautés ou les ressources qui ont soutenu et contribué au projet PandaScan. Cela pourrait inclure des mentors, des bibliothèques open source ou des collaborateurs.

---

*Ce document vise à fournir un récit approfondi de la création de PandaScan 🐼, capturant le dévouement et la passion investis pour concrétiser ce projet.*
