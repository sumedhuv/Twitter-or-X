/* Q3 is a query that returns "how the advertisers target the user;
 i.e., you want to see the top ten targeting types and the number
  of ads of that type".

The query should return a table with a two columns 
labeled "Criteria Category" (text) and "Ad Count" (integer).

The query should not modify the database and 
be a single SQL statement. */
   
SELECT TC.targetingType AS "Criteria Category", COUNT(MTC.criteria) AS "Ad Count"
FROM matchedTargetingCriteria AS MTC
INNER JOIN TargetingCriteria AS TC ON MTC.criteria = TC.id
GROUP BY TC.targetingType
ORDER BY COUNT(MTC.criteria) DESC
LIMIT 10;

