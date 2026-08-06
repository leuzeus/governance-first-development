# Governance-First Development

[Read in English](README.md)

> Proposition expérimentale — expérimentée uniquement sur des projets en cours; aucune application de référence n’a encore couvert un cycle de vie complet.

Governance-First Development (GFD) est une méthode provisoire pour les dépôts logiciels développés par des humains et des agents de programmation IA. Elle conserve les autorités, intentions, décisions, contraintes, exigences de validation et preuves avec le code, sous contrôle de version.

Ce dépôt publie une proposition, pas un standard éprouvé. Ses affirmations restent volontairement limitées. Les questions ouvertes figurent dans [STATUS.md](STATUS.md) et [ROADMAP.md](ROADMAP.md).

## Le problème

Les agents IA peuvent modifier un dépôt plus vite qu’un nouveau contributeur ne peut en reconstruire l’historique. Les règles importantes restent souvent dispersées entre des conversations, des issues, des plans périmés et la mémoire privée d’un agent. Un test réussi peut alors être présenté comme la preuve d’une affirmation plus large. Un agent peut aussi modifier un besoin, un test ou un document jusqu’à ce que sa propre implémentation paraisse conforme.

Ajouter des instructions ne suffit pas. Les fichiers de contexte trop longs et les approbations identiques pour tous les changements peuvent augmenter le coût, masquer la règle utile et retarder une correction locale réversible. GFD traite la friction de gouvernance comme une donnée à mesurer.

## Origine de la proposition

La progression a été pratique :

1. Plusieurs projets en cours assistés par IA ont révélé des pertes de contexte, des contradictions documentaires, des dérives d’agents, des validations faibles et des procédures lentes.
2. Des pratiques existantes ont été étudiées, dont les Architecture Decision Records (ADR), les instructions de dépôt, policy as code, GitOps, le développement axé sur les spécifications et la documentation versionnée.
3. Le propriétaire du projet a créé puis fait évoluer `audit-project-governance`, un skill local destiné à détecter ces problèmes et à proposer des corrections proportionnelles au risque.
4. Le skill a été utilisé comme outil expérimental sur des projets en cours, dont SplatForge.
5. Les idées récurrentes ont été séparées du skill et organisées sous le nom GFD.
6. Ce dépôt rend maintenant la proposition critiquable, mesurable et ouverte aux contre-exemples.

Ces projets sont des terrains d’observation. Aucun ne valide GFD sur un cycle de vie complet.

## Définition de travail

> Governance-First Development est une approche du développement logiciel centrée sur le dépôt, dans laquelle les autorités, intentions, décisions, contraintes, exigences de validation et preuves du projet évoluent avec le code afin que les humains et les agents IA puissent développer, comprendre, vérifier et auditer le projet de manière fiable.

Le dépôt constitue l’unité principale de transmission et d’audit. Des autorités externes peuvent s’appliquer, mais le dépôt doit les identifier, décrire leur périmètre et expliquer leur préséance.

## Ce que les agents changent

Un agent peut lire les règles, modifier l’implémentation, mettre à jour les tests et réécrire les explications pendant la même exécution. Cette concentration crée un risque précis : le même acteur peut altérer une affirmation et la preuve utilisée pour l’accepter.

GFD sépare cinq éléments souvent confondus :

- l’intention : le résultat recherché;
- la décision : l’option choisie par une personne ou un processus autorisé;
- l’implémentation : ce qui a changé dans le dépôt;
- le test : le comportement vérifié;
- la preuve : le résultat qui soutient une affirmation, dans un environnement donné et avec des limites déclarées.

Cette séparation aide un nouvel humain ou un agent tiers à vérifier le projet sans dépendre d’un historique privé. Elle peut aussi faciliter un audit externe, car les affirmations renvoient vers des autorités et des preuves. La valeur nette de cette approche reste à démontrer.

## Intégrité des tentatives et des résultats

GFD propose maintenant un enregistrement additif pour les évaluations bornées. Il sépare le statut d’exécution, le résultat de gate, le statut de preuve, le verdict produit et la classification de l’échec. La règle centrale est simple :

> Ne jamais attribuer au produit l’échec d’un test qui n’a pas été exécuté.

Un échec de préparation, d’opérateur, d’orchestration ou d’environnement peut empêcher l’exécution du gate produit. Il constitue alors une preuve sur la couche observée, pas un verdict d’échec du produit. Les résultats et classifications ultérieures sont ajoutés sans réécrire l’historique. Une évaluation de matérialité détermine les preuves réellement touchées avant d’imposer une nouvelle tentative.

L’extension est définie dans [METHOD.md](METHOD.md#71-attempt-outcome-integrity), illustrée par [huit cas génériques](examples/attempt-lineage/) et contrôlée par des [schémas JSON](schemas/) ainsi qu’un validateur déterministe. Ces artefacts démontrent leur cohérence interne; ils n’établissent pas encore la valeur de l’extension dans un projet réel.

## Méthode proposée

GFD demande à un projet de conserver seulement la gouvernance qu’il peut expliquer et maintenir :

- une carte des autorités avec une règle de préséance;
- les intentions, non-objectifs, contrats et invariants actuels;
- des décisions qui restent visibles lorsqu’elles sont remplacées;
- des contrôles choisis selon le risque;
- des preuves rattachées à des affirmations précises;
- des statuts honnêtes pour les validations indisponibles ou différées;
- une trace de la friction et des faux blocages;
- des audits périodiques du projet et de sa gouvernance.

La description canonique se trouve dans [METHOD.md](METHOD.md). [MANIFESTO.md](MANIFESTO.md) présente les principes initiaux en format court.

## Parcours proportionnés au risque

GFD propose cinq profils. Ils adaptent les cérémonies sans affaiblir les invariants.

| Profil | Usage prévu |
|---|---|
| `EXPLORE` | Enquête en lecture seule ou prototype isolé sans prétention de livraison |
| `FAST` | Changement local, réversible et de faible risque, sans frontière critique |
| `STANDARD` | Comportement interne significatif ou surface publique additive |
| `ASSURED` | Persistance, compatibilité, permissions, secrets, publication, effets destructifs ou preuve matérielle nécessaire |
| `EMERGENCY` | Superposition temporaire avec contrôles compensatoires, rollback, expiration et régularisation |

## Adoption minimale

Un projet personnel peut commencer sans copier tout ce dépôt :

1. nommer l’autorité actuelle pour les besoins et préciser l’ordre de préséance;
2. écrire un objectif courant et ses non-objectifs;
3. consigner les décisions coûteuses à redécouvrir;
4. déclarer les invariants qu’un agent ne peut pas assouplir;
5. choisir `FAST`, `STANDARD` ou `ASSURED` pour chaque changement livré;
6. rattacher les preuves aux affirmations de fin de tâche;
7. enregistrer une mesure de friction, même simple, avec sa méthode de collecte.

Consultez [l’exemple de projet personnel](examples/personal-agent-driven-project.md) et les [templates](templates/).

## Ce que GFD n’est pas

GFD ne remplace ni l’AI Governance, ni Responsible AI, GitOps, DevSecOps, policy as code, compliance as code, les ADR, le développement axé sur les spécifications ou `AGENTS.md`. La méthode peut utiliser ces pratiques lorsqu’elles correspondent au contexte.

GFD ne prétend pas non plus que des fichiers Markdown créent à eux seuls une gouvernance. Une règle n’est utile que si son autorité, son périmètre, son cycle de vie, son contrôle et ses preuves sont compris. Certaines règles doivent devenir des contrôles exécutables. D’autres exigent un jugement humain ou une validation matérielle.

L’expression « governance-first development » et des formulations voisines possèdent des usages publics antérieurs. [L’étude d’antériorité](references/prior-art.md) les consigne et situe cette proposition.

## Maturité actuelle

La version `0.1-draft` est un premier artefact de recherche appliquée.

- Aucun produit terminé n’a utilisé GFD sur un cycle de vie complet.
- Il n’existe aucune comparaison contrôlée avec un projet équivalent sans GFD.
- Les effets sur la qualité, la vitesse, les tokens, la maintenance et l’auditabilité ne sont pas établis.
- Les résultats des projets en cours sont des observations, pas une validation scientifique ou industrielle.
- Les contextes collaboratifs, exploités, réglementés et maintenus longtemps restent à étudier.

La méthode pourra être révisée ou abandonnée si les études prévues ne montrent pas assez de valeur.

## Carte du dépôt

- [METHOD.md](METHOD.md) : méthode canonique `0.1-draft`
- [STATUS.md](STATUS.md) : maturité, preuves manquantes, risques et questions
- [ROADMAP.md](ROADMAP.md) : programme de validation
- [schemas/](schemas/) : contrats exécutables de tentative et de résultat immuable
- [examples/attempt-lineage/](examples/attempt-lineage/) : cas génériques A à H
- [references/prior-art.md](references/prior-art.md) : sources et comparaison
- [skills/audit-project-governance/](skills/audit-project-governance/) : implémentation expérimentale d’audit
- [CONTRIBUTING.md](CONTRIBUTING.md) : corrections, critiques, cas, mesures et changements normatifs

## Contribuer des preuves et contre-exemples

Une contribution utile peut soutenir GFD, en réduire le périmètre ou montrer qu’une pratique coûte plus qu’elle ne rapporte. Toute preuve doit indiquer son contexte, sa méthode, son résultat, ses limites et sa provenance. Un exemple ne constitue pas une preuve. Un audit produit par une autre requête IA n’est pas automatiquement indépendant.

Utilisez [CONTRIBUTING.md](CONTRIBUTING.md) pour contribuer. Les signalements de sécurité suivent [SECURITY.md](SECURITY.md).

## Licence et citation

Ce dépôt est publié sous licence MIT. Elle autorise l’utilisation, la modification, la redistribution et l’usage commercial, à condition de conserver la notice de droit d’auteur et la licence. Voir [LICENSE](LICENSE) et [CITATION.cff](CITATION.cff).
