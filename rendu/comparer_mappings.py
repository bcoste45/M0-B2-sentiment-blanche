
import json


def main():
    with open("rendu/scores_30_avis.json", "r", encoding='utf-8') as f:    
        matConf2A = getMatriceConfusion0()
        #negatif manque = avis attendu negatif, mais predit neutre ou positif
        #fausse alerte = faux negatif
        errPredictA = {"negatifManque":"","fausseAlerte":""}
        matConf2B = getMatriceConfusion0()
        errPredictB = {"negatifManque":"","fausseAlerte":""}
        matConf2C = getMatriceConfusion0()
        errPredictC = {"negatifManque":"","fausseAlerte":""}
        matConf2S = getMatriceConfusion0()
        errPredictS = {"negatifManque":"","fausseAlerte":""}

        for predict in json.load(f):
            #print(predict) # {id, attendu(sentiment), note_client(+ gd etoile), scores_5_stars}            
            regleA(predict,matConf2A,errPredictA)
            regleB(predict,matConf2B,errPredictB)
            regleC(predict,matConf2C,errPredictC)
            regleS(predict,matConf2S,errPredictS)
        
        #la matrice de confusion 3 × 3 (attendu en lignes, prédit en colonnes) ;        
        print("Règle A:")
        printMatriceConfusion(matConf2A,errPredictA)
        print("")    
        print("Règle B:")
        printMatriceConfusion(matConf2B,errPredictB) 
        print("")      
        print("Règle C:")
        printMatriceConfusion(matConf2C,errPredictC)   
        print("")  
        print("Règle S:")
        printMatriceConfusion(matConf2S,errPredictS)



def getMatriceConfusion0():
    return {"négatif_att":{"négatif_pred":0,"neutre_pred":0,"positif_pred":0},
            "neutre_att":{"négatif_pred":0,"neutre_pred":0,"positif_pred":0},
            "positif_att":{"négatif_pred":0,"neutre_pred":0,"positif_pred":0}}
     

def printMatriceConfusion(matConf2,errPredict):
    nbreAvisOK = matConf2["négatif_att"]["négatif_pred"]+matConf2["neutre_att"]["neutre_pred"]+matConf2["positif_att"]["positif_pred"]
    print(f"Nombre d'avis bien classé = {nbreAvisOK}/30")   
    print(" ")
    print("Matrice de confusion : ")        
    print("|attendu\\predit| négatif | neutre  | positif |")
    print("|--------------|---------|---------|---------|")
    for i,m in matConf2.items():
        print(f"|   {i.removesuffix('_att')}    |    {m["négatif_pred"]}    |    {m["neutre_pred"]}    |    {m["positif_pred"]}    |")
    print(" ")
    for k,v in errPredict.items():
        print(v)


def regleA(predict, matConf2,errPredict):
    #1-2 : Négatif
    #3 : Neutre
    #4-5 : Positif
    #note_client = la plus probable ind
    #matConf2 = {"négatif_att":{"négatif_pred":0,"neutre_pred":0,"positif_pred":0},"neutre_att":{"négatif_pred":0,"neutre_pred":0,"positif_pred":0},"positif_att":{"négatif_pred":0,"neutre_pred":0,"positif_pred":0}}
    scores_5_stars = predict["scores_5_stars"]
    sentiment_predit = ""
    match max(scores_5_stars, key=scores_5_stars.get):
        case "1 star" | "2 stars":
            sentiment_predit = "négatif"
        case "3 stars":
            sentiment_predit = "neutre"
        case "4 stars" | "5 stars":
            sentiment_predit = "positif"
        case _:
            print("Unknown Class")

    matConf2[predict["attendu"]+"_att"][sentiment_predit+"_pred"] = matConf2[predict["attendu"]+"_att"][sentiment_predit+"_pred"]+1

    if errPredict["negatifManque"] == "" and predict["attendu"]=="négatif" and sentiment_predit!="négatif":
       errPredict["negatifManque"] = "Avis n°"+str(predict['id'])+" est un négatif manqué"
    if errPredict["fausseAlerte"] =="" and sentiment_predit=="négatif" and predict["attendu"]!="négatif":
        errPredict["fausseAlerte"] = "Avis n°"+str(predict['id']) +" est une fausse alerte."


def regleB(predict, matConf2,errPredict):
    #1 : Négatif
    #2-3 : Neutre
    #4-5 : Positif
    #note_client = la plus probable ind
    #matConf2 = {"négatif_att":{"négatif_pred":0,"neutre_pred":0,"positif_pred":0},"neutre_att":{"négatif_pred":0,"neutre_pred":0,"positif_pred":0},"positif_att":{"négatif_pred":0,"neutre_pred":0,"positif_pred":0}}
    scores_5_stars = predict["scores_5_stars"]
    sentiment_predit = ""
    match max(scores_5_stars, key=scores_5_stars.get):
        case "1 star" :
            sentiment_predit = "négatif"
        case  "2 stars" |"3 stars":
            sentiment_predit = "neutre"
        case "4 stars" | "5 stars":
            sentiment_predit = "positif"
        case _:
            print("Unknown Class")

    matConf2[predict["attendu"]+"_att"][sentiment_predit+"_pred"] = matConf2[predict["attendu"]+"_att"][sentiment_predit+"_pred"]+1

    if errPredict["negatifManque"] == "" and predict["attendu"]=="négatif" and sentiment_predit!="négatif":
       errPredict["negatifManque"] = "Avis n°"+str(predict['id'])+" est un négatif manqué"
    if errPredict["fausseAlerte"] =="" and sentiment_predit=="négatif" and predict["attendu"]!="négatif":
        errPredict["fausseAlerte"] = "Avis n°"+str(predict['id']) +" est une fausse alerte."
     

def regleC(predict, matConf2,errPredict):
    #1-2 : Négatif
    #3-4 : Neutre
    #5 : Positif
    #note_client = la plus probable ind
    #matConf2 = {"négatif_att":{"négatif_pred":0,"neutre_pred":0,"positif_pred":0},"neutre_att":{"négatif_pred":0,"neutre_pred":0,"positif_pred":0},"positif_att":{"négatif_pred":0,"neutre_pred":0,"positif_pred":0}}
    scores_5_stars = predict["scores_5_stars"]
    sentiment_predit = ""
    match max(scores_5_stars, key=scores_5_stars.get):
        case "1 star" | "2 stars":
            sentiment_predit = "négatif"
        case "3 stars" | "4 stars" :
            sentiment_predit = "neutre"
        case "5 stars":
            sentiment_predit = "positif"
        case _:
            print("Unknown Class")

    matConf2[predict["attendu"]+"_att"][sentiment_predit+"_pred"] = matConf2[predict["attendu"]+"_att"][sentiment_predit+"_pred"]+1

    if errPredict["negatifManque"] == "" and predict["attendu"]=="négatif" and sentiment_predit!="négatif":
       errPredict["negatifManque"] = "Avis n°"+str(predict['id'])+" est un négatif manqué"
    if errPredict["fausseAlerte"] =="" and sentiment_predit=="négatif" and predict["attendu"]!="négatif":
        errPredict["fausseAlerte"] = "Avis n°"+str(predict['id']) +" est une fausse alerte."
    

def regleS(predict, matConf2,errPredict):
    #1-2 : Négatif
    #3 : Neutre
    #4-5 : Positif
    #note_client = la plus probable regroupé (1+2 et 4+5)
    #matConf2 = {"négatif_att":{"négatif_pred":0,"neutre_pred":0,"positif_pred":0},"neutre_att":{"négatif_pred":0,"neutre_pred":0,"positif_pred":0},"positif_att":{"négatif_pred":0,"neutre_pred":0,"positif_pred":0}}
    scores_5_stars = predict["scores_5_stars"]
    dict = {"négatif":scores_5_stars["1 star"] + scores_5_stars["2 stars"],
            "neutre":scores_5_stars["3 stars"],
            "positif":scores_5_stars["4 stars"] + scores_5_stars["5 stars"]}
    sentiment_predit = max(dict,key=dict.get)
    
    matConf2[predict["attendu"]+"_att"][sentiment_predit+"_pred"] = matConf2[predict["attendu"]+"_att"][sentiment_predit+"_pred"]+1

    if errPredict["negatifManque"] == "" and predict["attendu"]=="négatif" and sentiment_predit!="négatif":
       errPredict["negatifManque"] = "Avis n°"+str(predict['id'])+" est un négatif manqué"
    if errPredict["fausseAlerte"] =="" and sentiment_predit=="négatif" and predict["attendu"]!="négatif":
        errPredict["fausseAlerte"] = "Avis n°"+str(predict['id']) +" est une fausse alerte."
   

main()
