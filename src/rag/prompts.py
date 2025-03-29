from llama_index.core import PromptTemplate

custom_text_to_sql_prompt = PromptTemplate("""Given an input question, create a precise {dialect} PostgreSQL query to answer it. Follow these advanced guidelines:

1. Use case-insensitive matching for string comparisons
2. Handle variations in query phrasing and terminology
3. Use only tables and columns from the provided schema
4. Select only relevant columns, never all columns
5. Qualify column names with table names when necessary
6. Use appropriate JOINs, WHERE clauses, and aggregations
7. Use ILIKE for flexible text matching
8. Order results to highlight the most pertinent information
9. Avoid querying non-existent columns or tables
10. Optimize the query for performance where possible
11. Handle potential language variations and synonyms

Your response should contain only the SQL query, without any additional explanation or formatting. Do not use markdown or prepend the query with the term `sql`.

Context Notes:
- For role-based queries, check case-insensitive role names
- Consider synonyms and variations of terms
- Handle potential transliteration or spelling variations

Schema:
{schema}

Question: {query_str}
SQL Query:
""")

custom_sql_response_synthesis_prompt = PromptTemplate("""Given an input question, synthesize a response from the query results.
Query: {query_str}
SQL: {sql_query}
SQL Response: {context_str}
Response: 
""")