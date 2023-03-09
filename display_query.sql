SELECT tokens.text as token_text, lemma, pos, tag, dep, head, paragraphs.text as paragraph_text, url, author, title, resources.date as publishing_date
FROM tokens
LEFT JOIN paragraphs ON tokens.frn_paragraph_id = paragraphs.id
LEFT JOIN resources ON paragraphs.frn_resource_id = resources.id
LIMIT 100;