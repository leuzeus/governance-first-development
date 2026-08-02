# Référence — Attempt Outcome Integrity

Lire ce fichier en entier lorsqu’un audit examine des tentatives, gates,
résultats d’exécution, verdicts produit, classifications, corrections, retries
ou invalidations de preuve.

## Invariant

> Never blame the product for a test that never ran.

> Ne jamais attribuer au produit l’échec d’un test qui n’a pas été exécuté.

Un échec de commande n’est pas automatiquement un échec produit. Le rapport doit
identifier la dernière observation réellement obtenue et la couche qu’elle
évalue.

## Frontière entre occurrence et tentative

Une tentative est une exécution bornée, déclarée pour produire une preuve, un
résultat produit ou un verdict de gate. Une lecture, recherche, résolution de
chemin ou commande ad hoc est une occurrence de session. Ne la promouvoir en
tentative que si elle appartient à une tentative déclarée ou si une autorité
consigne l’une des raisons suivantes : impact matériel, récurrence ou importance
causale.

Signaler comme surcharge toute politique qui transforme chaque opération ou
erreur triviale en tentative durable.

## Champs à reconstruire

Pour chaque tentative applicable, relever :

| Élément | Question |
|---|---|
| Identité | Quel identifiant stable et quelle intention bornée ? |
| Autorité | Quelle source impose les gates et critères ? |
| Gouvernance | Quelle version ou empreinte des critères ? |
| Gates planifiés | Quels identifiants, ordre, type et autorité ? |
| Gate produit cible | Quel gate observe réellement le produit ? |
| Progression | Quel dernier gate a réussi et quel gate est terminal ? |
| Exécution | Le gate produit a-t-il réellement été exécuté ? |
| Verdict produit | `passed`, `failed`, `not_executed`, `not_applicable` ou `inconclusive` ? |
| Classification | Produit, opérateur, orchestration, environnement ou inconnue ? |
| Preuve | Quelles observations directes et quelles limites ? |
| Confiance | Haute, moyenne, faible ou inconnue ? |
| Lignée | Cause, correction, retry, supersession, invalidation et validation ? |

## Règles de verdict

- `passed` : le gate produit cible a été exécuté et a réussi.
- `failed` : le gate produit cible a été exécuté et a échoué. La classification
  primaire est `product_failure`.
- `not_executed` : le gate produit n’a pas été exécuté. Une erreur observée se
  classe dans sa couche, jamais `product_failure`.
- `not_applicable` : une autorité ou règle applicable établit que le gate ne
  s’applique pas. Le statut de preuve correspondant est `SKIP`.
- `inconclusive` : le gate a démarré ou produit une observation insuffisante
  pour accepter ou rejeter le produit. Conserver `UNAVAILABLE` pour la preuve.

Le statut d’exécution, le résultat de gate, le statut de preuve, le verdict
produit et la classification ne sont pas interchangeables.

## Routage de la correction

- `product_failure` : corriger le produit seulement si le gate produit exécuté
  démontre l’écart.
- `operator_error` : corriger l’entrée, la procédure, l’instruction ou
  l’ergonomie concernée.
- `orchestration_error` : corriger le harness, workflow, wrapper ou coordination
  réutilisable.
- `environment_failure` : corriger ou rétablir l’environnement, la permission,
  la dépendance ou la capacité matérielle.
- `unclassified` : préserver l’inconnu et demander la plus petite observation
  discriminante. Ne pas choisir la couche la plus commode.

Les facteurs contributifs ne remplacent pas la cause primaire et ne justifient
pas un verdict produit absent.

## Historique append-only

La déclaration et les événements publiés restent immuables. Ajouter un nouvel
événement pour :

- classifier rétrospectivement un résultat ;
- déclarer une correction ;
- relier un retry ou une validation ;
- consigner une matérialité ou invalidation ;
- superséder une conclusion.

Une classification rétrospective cite l’identifiant et l’empreinte du résultat
original, l’auteur, la date, la preuve, la confiance et la justification. Elle
ne prétend pas qu’une nouvelle tentative a eu lieu.

Une correction `applied_not_validated` ne porte pas de relation de validation.
La validation vient d’une tentative ultérieure dont la preuve est liée à la
correction.

## Matérialité

Avant de rendre une preuve obsolète ou de forcer un rerun :

| Classe de changement | Traitement par défaut |
|---|---|
| `editorial` | Conserver la preuve ; décision explicite si un effet matériel est allégué |
| `observational` | Ajouter l’observation sans changer le contrat d’acceptation |
| `normative` | Citer la décision, identifier les gates affectés, invalider leur preuve et créer une nouvelle tentative |
| `implementation_or_material_environment` | Identifier les claims et gates touchés ; ne pas invalider le reste |

Mesurer, ou laisser inconnus, les coûts de reconstruction, classification,
maintenance et rerun. Ne jamais inventer le bénéfice d’un rerun évité.

## Anti-patterns

- `product_failure` alors que le gate produit est `not_executed` ;
- statut global `failed` copié dans le verdict produit ;
- absence du dernier gate réussi ou du gate terminal ;
- résultat historique réécrit après une nouvelle interprétation ;
- correction déclarée validée dès son application ;
- toute erreur opérationnelle routée vers le code produit ;
- toute occurrence de session promue en tentative ;
- toute modification de texte invalidant automatiquement toute preuve ;
- verdict `not_applicable` sans autorité ni critère de scope ;
- métriques reconstruites après coup.

## Verdict de dimension

- `conformant` : les enregistrements applicables satisfont le contrat et aucune
  divergence matérielle n’est trouvée.
- `partially_conformant` : seules des divergences non critiques ou une couverture
  incomplète limitée sont observées.
- `non_conformant` : faux verdict produit, rupture append-only, gate ou lignée
  matérielle manquante, ou autre divergence forte.
- `not_applicable` : le projet n’utilise pas de modèle de tentative applicable
  à la question. Ce verdict n’évalue pas le produit.
- `not_evaluable` : les autorités, schémas, enregistrements ou preuves nécessaires
  sont indisponibles ou incohérents.

Rapporter les faits, inférences et inconnues séparément. Pour chaque divergence,
indiquer la preuve exacte, la sévérité, la confiance, le risque, la correction
bornée et la friction probable sans mesure inventée.
