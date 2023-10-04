from rdflib import Graph, Namespace, RDF
graph = Graph()
graph.parse("Nintendo_Assignment2.ttl", format="turtle")

'''
A. For a given item(select a random item from your RDF Graph),provide all its categories and subcategories, and its brand. 
'''
item_info_query = """
SELECT ?category ?subcategory ?brand WHERE {
  ?item rdf:type ns1:Product ;
        ns1:isVariantOf ?subcategory ;
        ns1:brand ?brand .
  ?subcategory ns1:Product ?category .
} LIMIT 1
"""

results = graph.query(item_info_query)
# 打印查询结果
for row in results:
    print("Query A answer:",row)

'''
B. Provide items from different subcategories that have the same brand.
'''
items_query = """
SELECT ?item ?otherItem WHERE {
  ?item rdf:type ns1:Product ;
        ns1:brand ?brand ;
        ns1:isVariantOf ?subcategory .
  FILTER EXISTS {
    ?otherItem rdf:type ns1:Product ;
               ns1:brand ?brand ;
               ns1:isVariantOf ?otherCategory .
    FILTER(?subcategory != ?otherCategory)
  }
}
"""

# Execute the query
items_result = graph.query(items_query)
for row in items_result:
    print("Query B answer:",row)
    

'''
C. Group products by brand and show the average price or rating for each brand.
'''
group_query = """
SELECT ?brand (AVG(?price) AS ?averagePrice) WHERE {
  ?product rdf:type ns1:Product ;
           ns1:brand ?brand ;
           ns1:price ?price .
}
GROUP BY ?brand
"""

# Execute the query
group_result = graph.query(group_query)
for row in group_result:
    print("Query C answer:",row)

'''
D. Sort products in one category according to average brand price or rating.
'''

sort_query = """
SELECT ?product WHERE {
  ?product rdf:type ns1:Product ;
           ns1:brand ?brand ;
           ns1:price ?price ;
           ns1:isVariantOf ?subcategory .
  ?subcategory ns1:Product ?category .
  FILTER(?category = NS:consoles)
}
ORDER BY ?price
"""

# Execute the query
sort_result = graph.query(sort_query)
for row in sort_result:
    print("query D answer:",row)
'''
E. Use an external service point, provide a description of 5 facts about the top brand
from part D (e.g. https://query.wikidata.org/), e.g. location of headquarters. You may return images as one of your facts.
'''
# 参考链接 https://www.wikidata.org/wiki/Q8093
# query link: https://query.wikidata.org/

# PREFIX wd: <http://www.wikidata.org/entity/>

# SELECT ?name ?headquarters ?foundingYear ?logo ?location WHERE {
#   wd:Q8093 wdt:P31 ?name ;
#            wdt:P17 ?headquarters ;
#            wdt:P571 ?foundingYear ;
#            wdt:P154 ?logo ;
#            wdt:P154 ?location.
#   SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
# }

'''
F. Recommend an item which is similar to the item using your linked RDF graph
(i.e., shared properties and categories).
'''
query = '''
SELECT ?similarItem WHERE {
  ?similarItem rdf:type ns1:Product ;
               ns1:isVariantOf ?subcategory ;
               ns1:brand ?brand .
  ?item rdf:type ns1:Product ;
        ns1:isVariantOf ?category ;
        ns1:brand ?brand .
  FILTER(?item = NS:nintendo-switch-oled-model-mario-edition-rood-000000000010011772)
  FILTER(?similarItem != ?item)
}
LIMIT 1
'''
# Execute the query
sort_result = graph.query(query)
for row in sort_result:
    print("query F answer:",row)

'''
G. Write your own question about the webshop in plain English, then translate it to
the corresponding SPARQL query, and run it on the graph. Provide a rationale for why this query would be valuable in a webshop setting, such as for semantic search or other applications.
'''

query = '''
SELECT ?product ?price WHERE {
  ?product ns1:videogame NS:games;  
           ns1:price ?price.
  FILTER(?price > 50 && ?price < 60)
} 
ORDER BY ?price
LIMIT 10

'''
# Execute the query
sort_result = graph.query(query)
for row in sort_result:
    print("query G answer:",row)


