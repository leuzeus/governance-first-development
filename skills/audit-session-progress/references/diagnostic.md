# Questions et mécanismes de diagnostic

Lire seulement les familles qui peuvent changer la prochaine décision.
Ces familles sont des aides au raisonnement, pas des verdicts automatiques.

## Reconstituer la progression

Un essai peut produire une amélioration, une hypothèse infirmée, une dépendance
localisée ou une mesure nouvelle. Relever ces acquis même lorsque le résultat
final reste incomplet. L'absence de livraison n'établit pas l'absence de progrès.

| Signal | Vérification utile | Explication légitime à examiner |
|---|---|---|
| Même correctif répété | Hypothèse, entrée ou condition pertinente ont-elles changé ? | Confirmation d'un comportement intermittent. |
| Beaucoup de changements, peu d'observations | Le changement permet-il de distinguer les causes ? | Essai couplé justifié par des interactions connues. |
| Résultats corrects localement, objectif inaccessible | La chaîne jusqu'au résultat a-t-elle été exécutée ? | Étape de développement explicitement limitée. |
| Référence reconnue mais résultat différent | Préconditions et contrats sont-ils comparables ? | Différence de plateforme, données ou problème. |
| Paramètres ajustés sans effet | L'opération correspondante est-elle active ? | Effet masqué ou mesure insensible. |
| Méthode rejetée réutilisée | Une nouvelle décision ou observation autorise-t-elle sa réévaluation ? | Consigne ultérieure qui la réintroduit. |
| Suite coûteuse relancée | Le changement invalide-t-il cette preuve ? | Gate requis à une frontière d'intégration. |
| Blocage décrit comme panne produit | Le test produit a-t-il effectivement démarré et échoué ? | Défaut produit réel après préparation réussie. |

## Analyser le transfert d'une référence

Comparer les contrats avant de comparer les paramètres ou le code.

1. Quelle affirmation la référence démontre-t-elle réellement ?
2. Quelles entrées et propriétés accepte-t-elle : unités, repères, topologie,
   qualité, versions, matériel, données et initialisation ?
3. Quelles étapes, fonctions et interventions expertes font fonctionner le cas ?
4. Quelles hypothèses ou contraintes notre projet ajoute-t-il ou modifie-t-il ?
5. Quelle sortie intermédiaire doit rester équivalente pour poursuivre ?
6. Quel cas réussi et quelle variante échouée révèlent les limites ?
7. Quel petit essai conserve la difficulté qui rend le transfert incertain ?

Lorsque cela est possible, comparer le même cas dans le moteur de référence,
via l'interface d'exécution, puis dans le parcours dirigé par l'agent. Localiser
le premier écart. Un moteur non reproductible sur la plateforme disponible
laisse le transfert non établi ; cela ne prouve pas que l'algorithme est faux.

## Extraire les connaissances implicites

Sur une étape difficile d'un cas concret, demander à l'expert ou rechercher
dans les traces : quels indices étaient observables, quelle décision a été
prise, quelles alternatives ont été écartées et quelle erreur était possible ?
L'IA peut identifier des inconnues ; ses réponses hypothétiques ne remplacent
pas un entretien, une trace du mécanisme ou une observation du résultat.

Exemple fictif textile : une comparaison visuelle suggère un défaut de tombé,
mais l'état indique que seule la géométrie de placement a été construite.
Vérifier l'étape exécutée précède le choix de rigidité du tissu. Une fois le
solveur actif, géométrie, attaches, contacts et propriétés physiques peuvent
contribuer ensemble au défaut ; ne pas imposer une cause unique.

## Prioriser les questions

Une question est prioritaire si une réponse plausible change la méthode,
évite un essai coûteux ou révèle une impossibilité avec les contraintes actuelles.
Une question dont aucune réponse ne change la décision peut attendre.

| Champ | Contenu attendu |
|---|---|
| Question | Une inconnue précise ancrée dans le cas. |
| Décision | Ce que les réponses possibles feraient changer. |
| Source | Artefact, code, commande inspectée, observation ou expertise. |
| Test | Le plus petit contrôle représentatif qui sépare les hypothèses. |
| Incertitude | Ce que le contrôle ne pourra pas établir. |

Examiner aussi la compatibilité simultanée des contraintes. Deux exigences
peuvent être incompatibles ou manquer d'une condition de faisabilité. Décrire
le conflit potentiel et la preuve nécessaire ; ne pas assouplir les contraintes
approuvées pour faire réussir un candidat.

## Mesurer la friction de manière utile

Conserver les mesures disponibles avec leur méthode : durée d'un contrôle,
attente externe, nombre d'essais comparables, reprises de contexte, lectures
répétées et critères produit effectivement atteints. Séparer temps mur, temps
actif et attente. Les compteurs de tokens ne sont ni un coût financier ni un
quota consommé sans sémantique vérifiée.

Le coût de l'audit lui-même fait partie du bilan. Un audit redondant, un rapport
sans décision nouvelle ou une exploration inutilement élargie sont des frictions
à examiner. Les bénéfices attendus restent des hypothèses jusqu'à observation.

## Fondements et limites

Cette adaptation combine des pratiques existantes ; elle ne constitue pas une
méthode scientifiquement validée pour les sessions Codex.

- L'analyse des fonctions, entrées, sorties et interfaces s'inspire de
  [NASA Logical Decomposition](https://www.nasa.gov/reference/4-3-logical-decomposition/).
- Les questions sur les indices et décisions expertes s'inspirent d'ACTA,
  décrit dans le [MITRE Cognitive Engineering Toolkit, section 2.1.1](https://www.mitre.org/sites/default/files/2021-11/prs-20-2210-cognitive-engineering-toolkit.pdf).
- La progression et l'état durable sont aussi abordés dans
  [OpenAI Run long horizon tasks with Codex](https://developers.openai.com/blog/run-long-horizon-tasks-with-codex).
