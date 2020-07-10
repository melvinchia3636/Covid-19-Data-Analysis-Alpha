def ShortScale(n):
    testn=n
    list1 = ["D","V","T","q","Q","s","S","O","N"]
    list2 = ["","U","D","T","q","Q","s","S","O","N"]
    w = ["k","M","B","t","q","Q","s","S","O","N"]

    for a in range(len(list1)):
      for i in range(len(list2)):
        w.append(str(list2[i]+list1[a]))
    w.append("C")

    c=len(str(n))

    if(n>=10**306):
        return str(round(n/(10**(c-1)),1)) + 'E' + str(c-1)
    if(n>=1000):
        if round(n/(10**((c-1)//3*3)),1)>=1000:
            return str(1.0)+w[(c-1)//3]
        return str(round(n/(10**((c-1)//3*3)),1))+w[(c-1)//3-1]
    else:
        return n

print(ShortScale(10**303))
