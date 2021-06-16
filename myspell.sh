comm -23 <(tr -cs "A-Za-z" "[\n*]" < $1 | tr "A-Z" "a-z" | sort -u) <(tr -cs "A-Za-z" "[\n*]" < sorted.words | tr "A-Z" "a-z" | sort -u)
