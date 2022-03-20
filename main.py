import pandas as pd
import numpy as np

df = pd.read_csv('spam_or_not_spam.csv')
# df['split'] = np.random.randn(df.shape[0], 1)
#
# msk = np.random.rand(len(df)) <= 0.8
# test = df[~msk]
#
# train = df[msk]
train = df
#test = df

count_sp = 0
count_hm = 0
count_s_w = {}
count_h_w = {}
#Training using the training data sets
for ind in train.index:
    each_email = train['email']
    each_email =  str(each_email[ind])
    sp_ham = train['label']
    sp_ham = sp_ham[ind]
    words = each_email.split()
    words = set(words)
    total_count = len(each_email)
    if sp_ham == 1:
        count_sp += 1
        for word in words:
            if word in count_s_w:
                count_s_w[word] += 1
            else:
                count_s_w[word] = 1
    if sp_ham == 0:
        count_hm += 1
        for word in words:
            if word in count_h_w:
                count_h_w[word] += 1
            else:
                count_h_w[word] = 1

#print(count_s_w)
#print(count_h_w)
prob_spam = count_s_w
prob_ham = count_h_w


prob_spam.update((x, (y+1)/(count_sp + 2)) for x, y in prob_spam.items())
prob_ham.update((x, (y+1)/(count_hm + 2)) for x, y in prob_ham.items())
#print(prob_ham)
#print(prob_spam)
#print(count)

p_s = count_sp/(count_sp+count_hm)
p_h = count_hm/(count_sp+count_hm)

#Testing Phase
p_w_h = None
p_w_s = None

#new_email = test['email']
#new_email = str(new_email[test.index])
#new_email ='Here is the sale that you were looking for'
#new_email = 'Hi how are you mark? How has it been? Are you doing well?'
#new_email ='click on this link to test Viagra.'
new_email = 'Give me your credit card number'
print(new_email)
words = new_email.split()
for word in words:
    if word in prob_spam.keys():
        if p_w_s is None:
            p_w_s = prob_spam.get(word)
        else:
            p_w_s = p_w_s * prob_spam.get(word)

    if word in prob_ham.keys():
        if p_w_h is None:
            p_w_h = prob_ham.get(word)
        else:
            p_w_h = p_w_h * prob_ham.get(word)

if p_w_s and p_w_h is not None:
    p_s_w = (p_s * p_w_s) / ((p_s * p_w_s) + (p_h * p_w_h))
    print(p_s_w)

    if p_s_w > 0.5:
        print('Email is Spam')
    else:
        print('Email is Ham')

else:
    print("None of the words were seen")
