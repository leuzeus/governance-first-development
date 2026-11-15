# Évaluer l'audit avant adoption

Statut : protocole proposé, non exécuté pour cette ébauche.

## Question d'évaluation

Le skill identifie-t-il une anomalie matérielle et une prochaine action utile,
sans inventer une cause, créer un faux blocage ou augmenter le coût total ?

Un diagnostic formulé correctement et une session effectivement résolue sont
deux résultats distincts. Mesurer aussi les inconnues levées et les méthodes
raisonnablement écartées.

## Corpus initial

Préparer des épisodes datés avec contexte suffisant, dans l'emplacement local
autorisé. Fournir les traces et artefacts accessibles, pas les conclusions des
audits précédents. Fixer une coupure ; cacher la suite au lecteur de l'épisode.
N'utiliser que les matériaux autorisés. Les fixtures synthétiques servent à
vérifier des limites ; elles ne prouvent pas une efficacité sur des projets réels.

| Cas à préparer | Comportement à observer |
|---|---|
| Mauvaise couche corrigée | Localiser l'étape non exécutée et proposer un test pertinent. |
| Référence aux préconditions différentes | Identifier l'écart sans inventer les gestes experts manquants. |
| Consigne rejetant une méthode ignorée | Respecter la décision courante et la lignée des changements. |
| CI complète répétée sur correctifs comparables | Vérifier la matérialité et conserver les gates requis. |
| Donnée ou matériel nécessaire indisponible | Qualifier la dépendance et éviter les réparations produit gratuites. |
| Investigation longue avec nouvelles observations | Reconnaître la progression et éviter un faux diagnostic de stagnation. |
| Tests logiciels corrects, preuve produit absente | Limiter la conclusion au comportement réellement démontré. |
| Historique incomplet ou artefacts inaccessibles | Restituer l'incertitude et demander la seule preuve déterminante. |

## Lecture indépendante

Lorsque l'évaluation indépendante est autorisée, faire examiner les épisodes
par un humain ou un agent qui n'a pas reçu la solution historique, les causes
supposées ou le rapport précédent. Documenter modèle, version, prompts et
contexte partagé. Un autre agent ne garantit pas l'indépendance.

La personne qui connaît le projet peut ensuite évaluer : exactitude des faits,
solidité de la cause supposée, qualité du test discriminant, faisabilité de
l'action, respects des décisions et risque introduit.

## Mesures

- Constats matériels confirmés et constats rejetés, avec justification.
- Questions dont la réponse change une décision, et questions sans effet.
- Faux blocages et erreurs de causalité ou d'autorité.
- Corrections proposées qui ont reçu une validation réelle ultérieure.
- Temps et coût de lecture, d'audit, d'essai et de reprise, lorsqu'observables.
- Progrès produit, apprentissage utile et répétitions réellement évitées.

Une relecture a posteriori peut évaluer le diagnostic ; elle ne mesure pas le
temps qu'une intervention aurait économisé. L'effet sur la résolution requiert
un essai prospectif, avec une baseline établie avant l'intervention.

Comparer des tâches suffisamment semblables en documentant leur difficulté,
type, plateforme et modèle. La différence entre une session ancienne et récente
ne permet pas seule d'attribuer un gain au skill. Fixer les critères de réussite
et de rejet avant les essais ; ne pas les réécrire après observation.

## Articulation et adoption GFD

Proposition : ajouter le skill comme implémentation expérimentale informative,
avec sa version, sa provenance et un programme d'évaluation. Le proposer
séparément de l'audit de gouvernance : la session est l'unité de diagnostic,
le dépôt et ses autorités restent l'unité de réforme.

Les constats sur une politique alimentent le workflow de réforme du projet.
Les constats techniques alimentent la prochaine expérience ou correction.
Ils ne deviennent pas automatiquement des règles, schémas ou gates GFD.

Réutiliser les outils de distribution lorsque leurs contrats conviennent.
Introduire un schéma ou collecteur exécutable seulement lorsqu'un consommateur
ou un besoin de fiabilité répété le justifie. Aucune analyse globale des chats
privés ni publication des épisodes bruts n'est requise.

Une adoption normative éventuelle doit documenter problème, preuves, alternatives,
bénéfice attendu, friction ajoutée, risques, compatibilité et retrait possible.
Maintenir le statut expérimental tant que l'efficacité n'est pas établie.

Première étape proposée : préparer un épisode réel à une coupure fixée et
examiner si le skill en tire une question et un test qui changent utilement la
prochaine décision. La lecture autonome de l'auteur ne suffit pas à valider
l'efficacité comportementale.
