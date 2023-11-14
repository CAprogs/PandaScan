# Derrière PandaScan 🐼 (L'histoire)

## Table des Matières
- [Introduction](https://github.com/CAprogs/PandaScan/blob/main/docs/FR/LEARN.fr.md#introduction)
- [Idée 💡](https://github.com/CAprogs/PandaScan/blob/main/docs/FR/LEARN.fr.md#id%C3%A9e-)
- [Défis ⛔️](https://github.com/CAprogs/PandaScan/blob/main/docs/FR/LEARN.fr.md#d%C3%A9fis-%EF%B8%8F)
- [Développement 🏗️](https://github.com/CAprogs/PandaScan/blob/main/docs/FR/LEARN.fr.md#d%C3%A9veloppement-%EF%B8%8F)
- [Leçons tirées ✍️](https://github.com/CAprogs/PandaScan/blob/main/docs/FR/LEARN.fr.md#le%C3%A7ons-tir%C3%A9es-%EF%B8%8F)
- [Remerciements](https://github.com/CAprogs/PandaScan/blob/main/docs/FR/LEARN.fr.md#remerciements)

#

## **Introduction**

Bonjour 👋, je m'appelle Charles, j'ai 22 ans et je suis en dernière année d'école d'ingénieur à ECAM-EPMI Cergy en 🇫🇷.

Depuis quelques années, je suis passionné par l'informatique et la programmation en général ! Comme tout étudiant classique, j'ai dû apprendre de nombreux langages de programmation durant mon cursus, tels que HTML, CSS, JavaScript, C, etc.

Cependant, je me suis davantage plu à l'apprentissage de Python 🐍, qui est un langage dont la simplicité et l'efficacité sont assez remarquables. Machine Learning, Automatisation, Création d'applications, etc. Les possibilités avec ce langage sont vastes et variées. J'ai donc sauté dans le bain et depuis quelques années, je ne cesse d'apprendre de nouvelles choses, que ce soit à travers des projets personnels, des formations ou des vidéos Youtube !

Dans ce document, nous plongerons dans le parcours de création de PandaScan 🐼, un projet qui me tient énormément à cœur, depuis son idée initiale jusqu'à sa mise en œuvre et au-delà. L'histoire qui va suivre a pour but de vous transmettre ma passion, de vous faire connaître les défis que j'ai pu rencontrer et les enseignements qui ont façonné ce projet.

## Idée 💡
C'est en regardant des vidéos sur Tiktok que m'est venue l'idée ! Des comptes diffusaient des pages de scans de mes mangas favoris et je me suis demandé comment ils le faisaient, vu que la plupart, si ce n'est tous les sites de lecture de manga en ligne, ne nous permettent pas de télécharger ces pages automatiquement. Je me suis dit que si je voulais faire la même chose, j'allais perdre un temps énorme à sélectionner chaque page de chapitre de manga pour les télécharger. Le besoin de créer une solution qui me permette de télécharger automatiquement les chapitres de manga que je voulais provient aussi du fait que ces derniers ne sont accessibles qu'à travers une connexion internet, ce qui est dommage lorsque nous voulons y accéder même hors ligne ou en région reculée, loin de tout.

## Défis ⛔️
Comme tout projet et tout développeur qui se respecte, j'ai bien évidemment fait face à de nombreux problèmes, ce qui m'a demandé de nombreux jours de débogage. Les principaux défis auxquels j'ai fait face sont principalement liés à la mauvaise utilisation de certaines bibliothèques, à la récupération des données pour les sites et à la création d'une interface utilisateur simple et facile à prendre en main. J'ai passé beaucoup de temps à tester, déboguer et fouiller. 

Savoir fouiller au bon endroit et trouver la solution à un problème spécifique procure énormément de satisfaction !

## Développement 🏗️
Avant de commencer mon projet, il fallait vérifier que le problème n'avait pas encore été résolu. À ma grande surprise, il existait bel et bien des outils pour télécharger des scans de mangas, mais qui ne prenaient pas en compte le côté francophone ! J'ai donc décidé de sauter le pas. 

Je savais qu'il me fallait un moyen :
- d'aller sur les sites de lecture de manga en ligne 
- récupérer les pages ➡️ du chapitre ➡️ d'un manga que je voulais 
- Les stocker dans un dossier sur mon ordinateur ! 

Sur le papier, cela avait l'air simple à faire étant donné que j'avais déjà eu à faire au scraping web auparavant.

1. **Le test**

Dans cette étape, il fallait tester l'accès au site et le téléchargement d'une page pour s'assurer qu'il était possible de récupérer la donnée souhaitée ( ici une page de manga ). Cela fu possible grâce à **Request** et plus tard **Selenium** : j'accédais à la page de mon manga et j'envoyais une requête pour télécharger le manga et le tour était joué. Trop simple pour être vrai, les administrateurs du site avaient compliqué la tâche en cachant l'adresse qui contenait l'image dans une autre page. J'ai pu rapidement contourner cette restriction, mais le serveur refusait mes requêtes, j'ai donc décidé de chercher un autre moyen de récupérer l'image. Après quelques jours de réflexion, l'idée de prendre tout simplement un screenshot de l'image en question m'est venue à l'esprit ! C'était à ma grande surprise possible avec Selenium. Le script n'était pas parfait, mais il fonctionnait ! Par ailleurs, je n'aimais pas les zones sombres que la capture d'écran téléchargeait, je voulais l'image seule, propre, à la taille originale et qui prenait peu d'espace, car oui, les captures d'écran prennent de la place (3 Mo/capture en moyenne). J'ai donc cherché un moyen de "cropper" l'image après capture, mais je me heurtais à un autre problème : les pages ne sont pas toutes de la même taille et ne sont pas toutes au même format (certaines étaient verticales et d'autres à l'horizontale). Après quelques nuits de test, j'ai pu réaliser le script qui me permettait de "cropper" l'image à la bonne taille et au bon format !

3. **À l'action**

Dans cette étape, il fallait automatiser le processus : 
- accéder à la première page du manga
- télécharger cette page 
- la stocker dans un dossier qui aurait "Le nom du manga" et qui contiendrait le "nom du chapitre en cours de téléchargement"
- puis il fallait accéder à la page suivante et ajouter cette dernière au sous-dossier créé. 

Il fallait le faire jusqu'à ce que tout le chapitre soit téléchargé ! L'utilisation de boucles était indispensable, il fallait trouver un "pattern" qui me permette d'accéder aux pages suivantes en incrémentant une valeur ce qui était assez facile car les sites suivaient tous la même architecture : " site/nom_du_manga/N°chapitre/page " je n'avais qu'à incrémenter "page" et le tour était joué. Le script fonctionnait à merveille ! Malheureusement, cette victoire fût de courte durée ..

4. **Tout Automatiser**

Bien que tout fonctionnait parfaitement, il était pénible de :
- saisir à chaque fois l'adresse du manga dans mon script
- trouver le pattern pour ensuite télécharger le manga. 

Il me fallait un moyen plus simple d'accéder au manga que je voulais, mais aussi au chapitre que je voulais ! D'où la nécessité de récupérer les données concernant tous les numéros de chapitre et tous les noms de mangas disponibles du site. Cette étape était pénible mais utile pour la suite ..

5. **L'interface Graphique**

Pour permettre l'utilisation à d'autres de cet outil, il me fallait mettre à l'épreuve mes compétences de designer et de développeur. Je remercie [@ParthJadhav](https://github.com/ParthJadhav) pour avoir développé le superbe outil qu'est [tkinter-designer]() qui m'a considérablement accéléré le processus de création de l'interface graphique ! J'ai également découvert le super outil qu'est Figma et l'application prenait enfin forme...

6. **Le drame**

Mon script n'était basé que sur un seul site web à l'époque et ce que je redoutais arriva : **CloudFlare** ! 

L'ennemi juré des scrapeurs web, la barrière à l'automatisation de tâches était arrivée sur **Japscan**. J'ai passé énormément de temps à chercher un moyen de contourner cette restriction : utilisation de **proxys**, changement d'**User Agent**, **Undetected-chromedriver**... Tous sans succès. La solution la plus simple était de changer de site et de recommencer le processus.

7. **Rescapé**

J'ai pu trouver dans mes recherches des sites ayant une bonne structure, un catalogue assez large de mangas et accessibles avec de simples requêtes : **Le Graal du scrapeur**. 

Après avoir passé quelques nuits blanches à développer des scripts de scraping pour les sites en question, j'ai enfin pu les intégrer à mon application !

8. **Développer et améliorer**

Comme tout bon perfectionniste qui se respecte, je ne pouvais pas m'arrêter à cette tâche, il me fallait absolument rendre le script disponible, compréhensible et organisé. Je vous passe les détails, je suis encore en train de me casser la tête pour rendre l'application finale disponible sur toutes les plateformes et facilement installable.

Néanmoins, la version de test est disponible [ici](https://github.com/CAprogs/PandaScan/releases).

9. **Une feature essentielle**

Pour atteindre l'automatisation ultime, il me fallait un moyen de rendre les données à jour et d'éviter à l'utilisateur de lancer manuellement les scripts pour mettre à jour les mangas ou les chapitres disponibles au téléchargement. 
- J'ai donc géré l'exécution de ces scripts en créant un fichier JSON de configuration qui permette de choisir entre une mise à jour manuelle ou automatique au lancement de l'application. 
- J'ai aussi mis en place un système qui permette de traquer chaque changement dans les données de chaque site en sauvegardant un fichier .txt qui contient : 
  - le numéro de la mise à jour
  - la date et l'heure d'exécution de cette dernière
  - les mangas et chapitres ajoutés ou supprimés


## Leçons tirées ✍️

En développant PandaScan 🐼, j'ai beaucoup appris de Github, j'ai même pu réaliser mon premier pull request sur le projet [MISST](https://github.com/Frikallo/MISST). J'ai aussi beaucoup appris en développement d'applications et en design d'interface graphique avec Python ! Les erreurs que j'ai rencontrées, la façon de développer, j'en ai appris beaucoup et je sais désormais comment entamer un projet de la sorte et le mener en toute autonomie. Néanmoins, j'aurais aimé pouvoir travailler en équipe, même si le feedback de mon entourage m'a beaucoup aidé. Seul on va plus vite, mais à plusieurs on va plus loin. Raison pour laquelle, si vous êtes intéressés à améliorer le projet, je vous invite à consulter la rubrique [CONTRIBUTION]() pour savoir comment apporter du nouveau à PandaScan 🐼 !

## Remerciements

Je tiens à exprimer ma gratitude envers tous les acteurs proches ou lointains qui ont permis la réalisation de ce projet ! Il n'aurait jamais vu le jour sans l'Open Source, raison pour laquelle ce projet restera Libre d'accès à quiconque voudra en faire usage, dans le respect des limites de son utilisation, bien entendu. 

Merci encore de m'avoir lu et je vous retrouve dans de prochaines histoires encore plus passionnantes, je l'espère 😋.

_Charles_

---

*Ce document vise à fournir un récit approfondi de la création de PandaScan 🐼, capturant le dévouement et la passion investis pour concrétiser ce projet.*
