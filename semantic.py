import math


def norm(vec):
    sum_of_squares = 0.0  # floating point to handle large numbers
    for x in vec:
        sum_of_squares += vec[x] * vec[x]
    
    return math.sqrt(sum_of_squares)
    
def euclideannorm(vec1,vec2): 
    vec1words = list(vec1.keys())
    vec2words = list(vec2.keys())
    
    vec1num = list(vec1.values())
    vec2num = list(vec2.values())
    
    sumv1 = 0
    sumv2 = 0 
    
    for m in vec1words:
        if m not in vec2words:
            vec2[m] = 0
    
    for n in vec2words:
        if n not in vec1words:
            vec1[n] = 0
            
    for i in vec1words:
        sumv1 += vec1[i]*vec1[i]
    sumv1 = math.sqrt(sumv1)
    for j in vec2words:
        sumv2 += vec2[j]*vec2[j] 
    sumv2 = math.sqrt(sumv2) 
    
    for k in vec1:
        vec1[k] = vec1[k]/sumv1 
    for l in vec2:
        vec2[l] = vec2[l]/sumv2 
    
    diffvec = {} 
    for z in vec1:
        diffvec[z] = vec1[z]-vec2[z]
    
    return -(norm(diffvec))

def euclidean(vec1, vec2):
    vec1words = list(vec1.keys())
    vec2words = list(vec2.keys())
    
    computed = {}
    for k in vec1words:
        if k not in vec2words:
            vec2[k] = 0
    
    for l in vec2words:
        if l not in vec1words:
            vec1[l] = 0
    
    vec1num = list(vec1.values())
    vec2num = list(vec2.values())
    
    for k in vec1words:
        computed[k] = vec1[k] - vec2[k]
    
    return -(norm(computed))

def cosine_similarity(vec1, vec2):
    vec1words = list(vec1.keys())
    vec2words = list(vec2.keys())
    vec1num = list(vec1.values())
    vec2num = list(vec2.values())
    
    for i in range(len(vec1num)):
        vec1num[i] = vec1num[i]*vec1num[i]
    for j in range(len(vec2num)):
        vec2num[j] = vec2num[j]*vec2num[j]
    
    rootsum = math.sqrt(sum(vec1num)*sum(vec2num))

    cos = 0 
    for k in vec1words:
        if k in vec2words:
            computed = (vec1[k]*vec2[k])
            cos += computed 
    
    return cos/(rootsum)

def build_semantic_descriptors_from_files(filenames):
    compiledtext = ""
    
    for i in range(len(filenames)): 
        text = open(filenames[i], "r", encoding="utf-8")
        text = text.read()
        compiledtext += text 

    compiledtext = compiledtext.replace("!",".").replace("?",".").replace(",","").replace("-","").replace("--","").replace(":","").replace(";","").replace('"',"").replace("'"," ").replace("\n"," ").replace("\n\n", " ")

    compiledtext = compiledtext.lower() 

    compiledtext = compiledtext.split(". ")

    sentenceslist = []

    for j in range(len(compiledtext)):
        editedtext = compiledtext[j].split(" ")
        sentenceslist.append(editedtext)  

    return build_semantic_descriptors(sentenceslist)
   

def build_semantic_descriptors(sentences):
    emptydic = {}
    for sentence in sentences:
        for word in sentence:
            emptydic[word] = {}
    
    for sentence in sentences:
        for word in sentence:
            for word2 in sentence:
                if word2 != word:
                    if word2 != '':
                        if word2 not in emptydic[word]:
                            emptydic[word][word2] = 1
                        else:
                            emptydic[word][word2] += 1
    return emptydic 

def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    firstrun = True 
    comparable = list(semantic_descriptors.keys())
    if word not in comparable:
            return choices[0] 
    for i in choices: 
        if i not in comparable:
            tempscore = -1
        else:
            tempscore = similarity_fn(semantic_descriptors[word],semantic_descriptors[i])
        if firstrun == True:
            firstrun = False
            maxscore = tempscore 
            bestword = i 
        
        elif tempscore > maxscore: 
            maxscore = tempscore
            bestword = i 
    return bestword 
    
def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    cur_score = 0
    text = open(filename, "r", encoding="utf-8")
    text = text.read()
    text = text.split("\n")
    totalscore = len(text)
    
    comparablewords = list(semantic_descriptors.keys())
    
    for i in text:
        if len(i) > 1:
            i = i.split(" ") 
            question = i[0]
            answer = i[1] 
            choices = i[2:len(i)]
            output = most_similar_word(question, choices, semantic_descriptors, similarity_fn)
        if  output == answer:
            cur_score += 1 
            
    return cur_score/totalscore*100

if __name__ == '__main__':
    hi = build_semantic_descriptors_from_files(["Swann.txt","WarPeace.txt"]) 
    test_file = "test.txt"
    print("Cosine Similarity")
    print(run_similarity_test(test_file,hi,cosine_similarity))
    print("Euclidean")
    print(run_similarity_test(test_file,hi,euclidean))
    print("Euclidean Norm")
    print(run_similarity_test(test_file,hi,euclideannorm))