from django.http import HttpResponse
from django.shortcuts import render

def index(request):

    data = request.POST.get("inpprods","Not Entered")

    def mainitis():
        import random

        def remove_null_productions(stringi, key):
            lis = []
            for i in range(stringi.count(key)):
                j = i + 1
                for i in range(len(stringi)):
                    if stringi[i] == key:
                        j = j - 1
                        if j == 0:
                            tstring = stringi[:i] + stringi[i + 1:]
                            if tstring not in lis:
                                lis.append(tstring)
                                lis1 = remove_null_productions(tstring, key)

                                for j in lis1:
                                    if j not in lis:
                                        lis.append(j)
                            break
            return lis

        productions = {}
        productionstring = ""
        chardict = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0, 'I': 0, 'J': 0, 'K': 0, 'L': 0,
                    'M': 0, 'N': 0, 'O': 0, 'P': 0, 'Q': 0, 'R': 0, 'S': 0, 'T': 0, 'U': 0, 'V': 0, 'W': 0, 'X': 0,
                    'Y': 0, 'Z': 0}
        charlist = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                    'U', 'V', 'W', 'X', 'Y', 'Z']

        # print("Enter Production")
        # while True:
        #     production = input()
        #     if production == "*":
        #         break
        #     list = production.split("->")
        #     list2 = list[1].split("|")
        #
        #     chardict[list[0]] = 1
        #     if (list[0] in productions):
        #         for i in list2:
        #             productions[list[0]].append(i)
        #     else:
        #         productions[list[0]] = list2
        #     # print(production)
        # productions = {'S': ['AAC'], 'A': ['aAb', '^'], 'C': ['aC', 'a']}

        print("data"+str(data))
        if data!="Not Entered":
            mainstr = data
            productionlist = mainstr.split("\r\n")
            print(productionlist)
            for prods in productionlist:
                tempproduction = prods.split("->")
                prodname = tempproduction[0]
                chardict[tempproduction[0]] = 1
                prodlist = tempproduction[1].split("|")
                productions[prodname] = prodlist
        # else:
        #     productions = {'S': ['AAC'], 'A': ['aAb', '^'], 'C': ['aC', 'a']}
        print("Productions : " + str(productions))

        # Useless production removal
        dictforuseless = {}
        for key, values in productions.items():
            for val in values:
                for prod in productions.keys():
                    if prod in val:
                        if prod != key:
                            dictforuseless[prod] = 1

        # print(dictforuseless)
        tlist = []
        for key, value in productions.items():
            if key != "S":
                if key not in dictforuseless:
                    tlist.append(key)
        for prod in tlist:
            productions.pop(prod)

        print("Productions after Useless Removal : " + str(productions))
        productionstring = "Productions after Useless Removal : " + str(productions) + "\n"

        # Null Production Removal
        productions_withnull = []
        for key, values in productions.items():
            if (("^" in values) and key != 'S'):
                if key not in productions_withnull:
                    productions_withnull.append(key)

        print("Productions with null " + str(productions_withnull))
        productionstring = productionstring + "Productions with null " + str(productions_withnull) + "\n"

        productions_tobechanged = productions_withnull.copy()

        for key, values in productions.items():
            if key in productions_tobechanged:
                continue
            b = False
            for v in values:
                if (b):
                    break
                for prods in productions_withnull:
                    if prods in v:
                        productions_tobechanged.append(key)
                        b = True
                        break

        print("Productions to be changed: " + str(productions_tobechanged))

        for key, values in productions.items():
            mainlis = values
            if key in productions_tobechanged:
                if (("^" in mainlis) and key != "S"):
                    mainlis.remove("^")
                for val in values:
                    for prods in productions_withnull:
                        if val.count(prods) > 0:
                            lis = remove_null_productions(val, prods)
                            for i in lis:
                                if i not in mainlis:
                                    mainlis.append(i)
            # productions[key] = mainlis

        print("Productions after Null Removal : " + str(productions))
        productionstring = productionstring + "Productions after Null Removal : " + str(productions) + "\n"

        # UNIT Production Removal
        for key, values in productions.items():
            for val in values:
                if val in productions.keys() and key != val:
                    for i in productions[val]:
                        values.append(i)
                    values.remove(val)

        print("Productions after Unit Removal : " + str(productions))
        productionstring = productionstring + "Productions after Unit Removal : " + str(productions) + "\n"
        cnf_productions = productions.copy()

        # Solid NT
        # print(productions.values())
        dictadd = {}
        new_productions = {}

        for key, values in productions.items():
            new_values = []
            for val in values:
                for char in val:
                    if ((char not in productions.keys()) and char != "^"):
                        boolcheck = True
                        for k, v in productions.items():
                            if ((len(v) == 1) and (v[0] == char) and (key != k)):
                                val = val.replace(char, k)
                                boolcheck = False
                        if (boolcheck):
                            for k, v in dictadd.items():
                                if ((len(v) == 1) and (v[0] == char)):
                                    val = val.replace(v[0], k)
                                    boolcheck = False
                        if (boolcheck):
                            randno = random.randint(0, 25)
                            while (chardict[charlist[randno]] != 0):
                                randno = random.randint(0, 25)
                            dictadd[charlist[randno]] = [char]
                            chardict[charlist[randno]] = 1
                            val = val.replace(char, charlist[randno])
                new_values.append(val)
            new_productions[key] = new_values

        productions = new_productions.copy()

        print("Production after Solid NT: " + str(productions))
        print("New productions for Solid NT" + str(dictadd))

        productions.update(dictadd)

        print("All Productions after Solid NT: " + str(productions))
        productionstring = productionstring + "Productions after Solid NT: " + str(productions) + "\n"

        # Restricting right production length
        cnt = 0
        dictadd.clear()
        new_productions.clear()

        for key, values in productions.items():
            new_values = []
            for val in values:
                if (len(val) >= 3):
                    tempstr = val[:len(val) - 1]
                    val = 'X' + str(cnt) + val[-1]
                    dictadd['X' + str(cnt)] = [tempstr]
                    cnt = cnt + 1
                new_values.append(val)
            new_productions[key] = new_values

        # print(dictadd)
        productions = new_productions.copy()
        productions.update(dictadd)
        print("Productions after restricting right production length: " + str(productions))
        productionstring = productionstring + "Productions after restricting right production length: " + str(productions) + "\n"
        dictadd.clear()
        new_productions.clear()

        productionstring = productionstring + "\n" +"Final Output: " + "\n"
        for key, value in productions.items():
            if (productionstring != ""):
                productionstring = productionstring + "\n"
            productionstring = productionstring + key + "->"
            for i in range(len(value)):
                if i != 0:
                    productionstring = productionstring + "|"
                productionstring = productionstring + value[i]
                productionstring = productionstring + value[i]

        print(productionstring)

        # lis = remove_null_productions("AaA",'A')
        # print(lis)

        '''
        S->AAC
        A->aAb|^
        C->aC|a

        S->CA|BB
        B->b|SB
        C->b
        A->a

        '''

        # GNF
        def tempme(hehe):
            f_lower = False
            hehe2 = {}
            Mainbool = False

            for keys, values in hehe.items():
                # print(keys)
                newvalues = values.copy()
                for val in values:
                    # print(val)
                    for i in range(len(val)):
                        if (val[i].islower() and i == 0):
                            f_lower = True
                        elif (val[i].islower() and f_lower == True):
                            newvalues.remove(val)
                            check = True
                            for k, v in hehe.items():
                                if len(v) == 1 and v[0] == val[i]:
                                    check = False
                                    val = val.replace(val[i], k)
                                    # print(val)
                                    newvalues.append(val)
                            for k, v in hehe2.items():
                                if len(v) == 1 and v[0] == val[i]:
                                    check = False
                                    val = val.replace(val[i], k)
                                    # print(val)
                                    newvalues.append(val)
                            if (check):
                                randno = random.randint(0, 25)
                                while (chardict[charlist[randno]] != 0):
                                    randno = random.randint(0, 25)
                                chardict[charlist[randno]] = 1
                                hehe2[charlist[randno]] = [val[i]]
                                val = val.replace(val[i], charlist[randno])
                                newvalues.append(val)

                        elif (val[i].isupper() and val[i] == keys[0] and f_lower == False and i == 0):
                            Mainbool = True
                            hehe2[keys + "'"] = [val[i + 1:] + keys + "'", "^"]
                            newvalues.remove(val)
                            for vs in newvalues:
                                vs = vs + keys + "'"
                            hehe2[keys] = newvalues
                            return hehe2, Mainbool

                        elif (val[i].isupper() and val[i] != keys[0] and f_lower == False):
                            Mainbool = True
                            # print(val[i])
                            # print(hehe)
                            for vals in hehe[val[i]]:
                                if (vals + val[i + 1:] not in newvalues):
                                    newvalues.append(vals + val[i + 1:])
                                if val in newvalues:
                                    newvalues.remove(val)
                            hehe2[keys] = newvalues
                            return hehe2, Mainbool

                    # print(newvalues)

                hehe2[keys] = newvalues
            return hehe2, Mainbool

        return productionstring
        # while True:
        #     hehe,booli = tempme(cnf_productions)
        #     print(hehe)
        #     if booli == False:
        #         break

        # print("GNF Productions after null and unit removal: " + str(cnf_productions))
        # def cnf_to_gnf(cnf_productions):

    prods = mainitis()
    trying = {"prods":prods , "data":data}

    return render(request,'index.html',trying)
    # return HttpResponse("hello")