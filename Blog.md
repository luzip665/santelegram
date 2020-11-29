# SanTelegram Bot

Cet hiver 2020, il est plus important que jamais de garder le contact avec ceux qui nous sont proches. Contact à distance évidemment, vu que l'hiver est marqué par : 1) le froid (logique) et 2) une pandémie mortelle. Pas facile donc de se préparer avec ses proches et sa famille à fêter Noël sereinement. Et pour éviter de réduire Noël à un simple envoi de cadeaux achetés en ligne à des entreprises payant plus ou moins leurs impôts, en discutant avec un ami (bien que collègue), on a eu cette idée de faire un **Bot Telegram "calendrier de l'Avent"**. 

> Ce post de blog a pour but de vous aider à faire votre en bot rapidement. Je m'adresse à des gens qui ont peu ou pas codé du tout. 
>
> Si ce n'est pas votre cas, ou si vous êtes pressés, vous pouvez copier-coller les fichiers qui sont à la fin du post ou [sur mon GitHub](https://github.com/RduMarais/santelegram) et rentrer dans les 10 minutes promises par le titre.

##### Telegram, c'est quoi ? 

Pour ceux qui ne connaissent pas [Telegram](https://telegram.org/), il s'agit d'une messagerie chiffrée, exactement comme WhatsApp. Les quelques différences avec WhatsApp sont : 

 * la possibilité de créer des canaux de conversation chiffrés de bout-en-bout ;
 * le fait que l'application soit développée en source ouverte ; 
 * la possibilité de créer des Bots ; 

Concrètement, c'est comme WhatsApp, mais avec quelques options en plus pour préserver sa vie privée des [companies comme WhatsApp](https://fr.wikipedia.org/wiki/Facebook_(entreprise)). Je ne dis pas que c'est le [Graal de la vie privée](https://www.signal.org/fr/) mais c'est déjà pas mal.

##### Le Bot

Donc l'idée du bot est simple : dans un chat de groupe, tous les jours, quelqu'un ouvre la "case" du jour. Pour réunir les gens autour du bot, tout le monde peut essayer de l'ouvrir, mais une seule personne, déterminée aléatoirement, peut réussir.
Une fois la "case" ouverte, le bot envoie une image, une citation, un lien, qui vient d'une liste prédéterminée.

Si le projet vous plaît, voilà comment faire !

## La Recette

### Ingrédients

Pour faire un Bot Telegram, il vous faut : 

 * un compte Telegram ;
 * un groupe sur lequel faire votre Bot ; 
 * Un ordinateur ;
 * avoir quelques bases en Python (un _hello world_ suffit)
 * Un serveur.

**Par serveur, j'entends** un ordinateur qui pourra rester allumé tant que vous voulez faire fonctionner votre bot, et qui peut faire des requêtes web. Donc il faut avoir suffisamment confiance en la connexion pour pas qu'elle flanche en pleine conversation avec le Bot. Pour les plus _esthètes_, il s'agira donc d'un vrai serveur, éventuellement dans le _cloud_ pour faire chic. Mais pour ce projet, **un vieux PC pentium 4 qui traîne dans un grenier fera très bien l'affaire**.

### Créer le Bot

Pour créer le bot, d'innombrables tutoriels existent. J'ai utilisé [celui-là](https://blog.usejournal.com/part-1-how-to-create-a-telegram-bot-in-python-under-10-minutes-145e7f4e6e40?gi=322a274e6e6c), que je reprends ci-dessous dans les grandes lignes.

 * Il faut se connecter sur Telegram. 
 * Chercher dans la barre de recherche un compte qui s'appelle BotFather ou @botfather de son username.

![Ledit BotFather, petit pères des bots.](https://miro.medium.com/max/1400/1*fV8qxeAoRT8xhVW9-l6g3Q.png)

 * Pour lancer la conversation, cliquez sur le gros bouton `START`.
 * BotFather va vous proposer une série d'options pour gérer votre bot. 
 * Dans le cas présent, nous allons en créer un avec la commande `/newbot`.
 	 * vous allez vite le voir : dans Telegram, les intercations avec les bots se font par "commandes" prédéfinies. Pour indiquer au bot qu'on lui envoie une commande, il faut utiliser ce caractère `/`
 * Donc l'échange avec BotFather devrait se dérouler comme ça : 
 	 * `/newbot`
 	 * `<le nom affiché que vous voulez donner à votre bot>`
 	 * `<l'identifiant de votre bot>`
 * La contrainte sur l'identifiant de votre bot est simple :
 	 * ne pas être déjà pris
 	 * finir avec 'bot'.
 * Si c'est bon, votre bot est créé ! 
 * Vous recevez alors un message contenant alors une chaine de caractères aléatoire. C'est votre clé API, gardez-là bien précieusement !
 * BotFather reste disponible pour vous aider à customiser votre bot avec différentes commandes pour changer sa description, sa photo, etc.

![Récupération de la clé API d'un nouveau bot](https://miro.medium.com/max/1400/1*5Ws-d5E_W_QMu4qQsLrGHA.jpeg)

### Configurer son bot

> Cette partie vise à expliquer comment créer le programme qui va interagir avec notre bot. Si vous êtes pressés, vous pouvez très bien sauter toute cette partie et récupérer uniquement le programme complet à la fin.

#### Prérequis

Le programme que je vous propose pour interagir avec notre bot est écrit en Python. C'est un langage qui se comprend assez facilement, qui est courant et qui n'a pas besoin de compiler. Tout ça fait qu'il est très pratique pour des petits scripts comme notre bot.

Si vous ne l'avez pas déjà, il faut donc [installer Python](https://www.python.org/downloads/). Faites attention en installant : les versions Python2 et Python3 ne sont pas compatibles entre elles ! Ici, nous allons utiliser Python3 et pas Python2, parce qu'on est bientôt en 2021 et qu'on est pas des barbares quand même.

Pour que le programme soit court et simple à comprendre, il utilise des **bibliothèques**, c'est à dire des bouts de code que beaucoup de gens utilisent, et qu'on a mis en commun pour pas avoir tout à réécrire. Il faut donc installer les bibliothèques susnommées.

Pour gérer facilement ces bibliothèques de code, nous avons besoin de pip, que l'on peut [télécharger ici](https://pip.pypa.io/en/stable/installing/). Si vous venez de télécharger Python3, pip est inclus dedans par défaut. Pip est un gestionnaire de bibliothèques, c'est grâce à cet outil que ajouter, mettre à jour ou supprimer des bibliothèques se gère aussi simplement que des applications que l'on télécharge sur l'App Store ou le Play Store.

Enfin, il faut savoir que si vous utilisez Linux, certains composants sont écrits en Python. Donc modifier les bibliothèques installées peut mettre un peu le bazar si on sait pas faire. Pour éviter cela, nous allons utiliser un **environnement virtuel**. Cela permet de choisir la version exacte de Python, les bibliothèques installées etc. sans modifier directement ce qui est sur votre ordinateur. Pour cela, plusieurs solutions, je vous propose ici d'utiliser `python -m venv` mais vous faites comme vous voulez.

Une fois pip et virtualenv installés, nous pouvons revenir à notre bot !

#### [Pour des raisons de mise en page, le coeur du tutoriel est disponible ici](https://github.com/RduMarais/santelegram/blob/master/Tutoriel.md#pr%C3%A9parer-le-code)

> J'espère que ce petit tuto vous plaira, profitez des fêtes et prenez soin de vos proches !
>
> Peace

## Notes

 * N'oubliez pas de supprimer le bot du groupe à la fin du mois de décembre ! C'est une mauvaise pratique de laisser des systèmes informatiques en place lorsqu'on ne les utilise plus. Comme les objets de la vie quotidienne, ils ont un cycle de vie qui a un début, mais aussi une fin, et il ne faut pas la négliger. Très souvent les vulnérabilités informatiques viennent de vieux accès qu'on a oublié de fermer ou de vieux systèmes qu'on a oublié de débrancher.
 * pour déployer le bot, j'utilise un serveur. Je copie le script avec la commande `scp`, je lance un `screen`, dans lequel j'active mon environnement virtuel et je lance mon script. Je peux quitter le `screen` et le serveur tranquille, le script tournera tranquillement.
 * Une fonction sympa serait de permettre aux utilisateurs d'envoyer leurs messages pour les autres. Mais cela signifie avoir du texte envoyé par un utilisateur qui arrive dans un script sur mon serveur. Autrement dit, il faut que je m'assure avant qu'on ne peut pas injecter de code sur mon serveur (et connaissant mes copains/collègues, je sais qu'ils vont essayer...). Tant que je ne maîtrise pas bien les mécanismes de sécurité des bots Telegram, j'évite. 

## La doc : 

 * API de Telegram : https://core.telegram.org/api#telegram-api
 * Telethon : https://github.com/LonamiWebs/Telethon/
 * choper les IDs : https://stackoverflow.com/questions/33844290/how-to-get-telegram-channel-users-list-with-telegram-bot-api
 * API python : https://python-telegram-bot.readthedocs.io/en/stable/telegram.chat.html#telegram.Chat
 * récupérer le chat ID : https://www.wikihow.com/Know-Chat-ID-on-Telegram-on-Android ou https://www.wikihow.com/Know-a-Chat-ID-on-Telegram-on-PC-or-Mac

