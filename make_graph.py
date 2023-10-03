from rdflib import Graph, Literal, Namespace, RDF
import pandas as pd 

graph = Graph()

# 读取TTL文件 
graph.parse("Nintendo.ttl", format="turtle")

schema = Namespace("http://schema.org/")
NS = Namespace('https://store.nintendo.nl/nl/')

# 还原初始图
#--------------Categories--------------------------------
brand = Literal("Nintendo")

console = NS['consoles']
games = NS['games']
merchandise = NS['merchandise'] #周边merchandise
franchise = NS['franchises'] #独家ip 和其它的会重复Exclusive IP and others will be duplicated
new_product = NS['new']

game_system = NS['consoles/nintendo-switch-consoles'] # *和图不一致
switch = NS['consoles/nintendo-switch-consoles/nintendo-switch']
switch_oled_model = NS['consoles/nintendo-switch-consoles/nintendo-switch-oled-model']

switch_bundle = NS['consoles/nintendo-switch-bundles'] #是console的product
accessory = NS['consoles/accessories'] #是switch的配件
apparel = NS['merchandise/apparel']
home_and_gifts = NS['merchandise/home-and-gifts']
plush = NS['merchandise/home-and-gifts/soft-toys'] 
##关系-----------------------------------------------------
product = schema['Product']
isAccessoryOf = schema['isAccessoryOrSparePartFor']
isVariantOf = schema['isVariantOf']
videoGame = schema['videoGame']

graph.bind('NS', NS)
#Define types for Mainpage

graph.add((console, RDF.type, brand)) # add的三个参数："_SubjectType", "_PredicateType", "_ObjectType"
graph.add((games, RDF.type, brand))
graph.add((merchandise, RDF.type, brand))
graph.add((franchise, RDF.type, brand))
graph.add((new_product, RDF.type, brand))

graph.add((game_system, product, console))
graph.add((switch_bundle, product, console))
graph.add((accessory, isAccessoryOf, console))
graph.add((switch, isVariantOf, game_system))
graph.add((switch_oled_model, isVariantOf, game_system))




df = pd.read_excel("output2.xlsx")

for i,row in df.iterrows():
    # 判断URI是否为空 跳过没有爬到的数据
    if not pd.isna(row["Item_URI"]) :
        product = NS[row["Item_URL"].replace("https://store.nintendo.nl/nl/","").replace(" ","")]
        graph.add((product, RDF.type, schema.Product))
        graph.add((product, schema.name, Literal(row["Value_1"])))
        graph.add((product, schema.description, Literal(row["Value_2"])))
        graph.add((product, schema.sku, Literal(row["Value_3"])))
        graph.add((product, schema.price, Literal(row["Value_4"])))
        graph.add((product, schema.brand, Literal("Nintendo"))) # 可能违反要求 *每个商品的商标都不同
    #    graph.add((product, schema[row["link"]],eval(row["type"])))


# 输出最新图
print(graph.serialize('Nintendo_Assignment2.ttl',format='turtle'))