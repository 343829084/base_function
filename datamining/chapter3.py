#-*-coding=utf-8-*-
import math
users2 = {"Amy": {"Taylor Swift": 4, "PSY": 3, "Whitney Houston": 4},
          "Ben": {"Taylor Swift": 5, "PSY": 2},
          "Clara": {"PSY": 3.5, "Whitney Houston": 4},
          "Daisy": {"Taylor Swift": 5, "Whitney Houston": 3}}

users = {"Angelica": {"Blues Traveler": 3.5, "Broken Bells": 2.0,
                      "Norah Jones": 4.5, "Phoenix": 5.0,
                      "Slightly Stoopid": 1.5, "The Strokes": 2.5,
                      "Vampire Weekend": 2.0},
         "Bill":{"Blues Traveler": 2.0, "Broken Bells": 3.5,
                 "Deadmau5": 4.0, "Phoenix": 2.0,
                 "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0},
         "Chan": {"Blues Traveler": 5.0, "Broken Bells": 1.0,
                  "Deadmau5": 1.0, "Norah Jones": 3.0,
                  "Phoenix": 5, "Slightly Stoopid": 1.0},
         "Dan": {"Blues Traveler": 3.0, "Broken Bells": 4.0,
                 "Deadmau5": 4.5, "Phoenix": 3.0,
                 "Slightly Stoopid": 4.5, "The Strokes": 4.0,
                 "Vampire Weekend": 2.0},
         "Hailey": {"Broken Bells": 4.0, "Deadmau5": 1.0,
                    "Norah Jones": 4.0, "The Strokes": 4.0,
                    "Vampire Weekend": 1.0},
         "Jordyn":  {"Broken Bells": 4.5, "Deadmau5": 4.0,
                     "Norah Jones": 5.0, "Phoenix": 5.0,
                     "Slightly Stoopid": 4.5, "The Strokes": 4.0,
                     "Vampire Weekend": 4.0},
         "Sam": {"Blues Traveler": 5.0, "Broken Bells": 2.0,
                 "Norah Jones": 3.0, "Phoenix": 5.0,
                 "Slightly Stoopid": 4.0, "The Strokes": 5.0},
         "Veronica": {"Blues Traveler": 3.0, "Norah Jones": 5.0,
                      "Phoenix": 4.0, "Slightly Stoopid": 2.5,
                      "The Strokes": 3.0}
        }

users3 = {"David": {"Imagine Dragons": 3, "Daft Punk": 5,
                    "Lorde": 4, "Fall Out Boy": 1},
          "Matt":  {"Imagine Dragons": 3, "Daft Punk": 4,
                    "Lorde": 4, "Fall Out Boy": 1},
          "Ben":   {"Kacey Musgraves": 4, "Imagine Dragons": 3,
                    "Lorde": 3, "Fall Out Boy": 1},
          "Chris": {"Kacey Musgraves": 4, "Imagine Dragons": 4,
                    "Daft Punk": 4, "Lorde": 3, "Fall Out Boy": 1},
          "Tori":  {"Kacey Musgraves": 5, "Imagine Dragons": 4,
                    "Daft Punk": 5, "Fall Out Boy": 3}}
def computeSimilarity(band1,band2,userRatings):

    band_avg={}

    for user,bands in userRatings.items():
        sum1 = 0
        n = 0
        for band,score in bands.items():
            sum1+=score
            n+=1
        band_avg.setdefault(user,0)
        band_avg[user]=sum1/float(n)

    # return band_avg
    sum_XY=0
    dem1=0
    dem2=0
    for user,bands in userRatings.items():
        # for band,score in bands.items():
        #     if band==band1:
        #         score-band_avg[user]
        if band1 in bands and band2 in bands:
            sum_XY+=(bands[band1]-band_avg[user])*(bands[band2]-band_avg[user])
            dem1+=(bands[band1]-band_avg[user])**2
            dem2+=(bands[band2]-band_avg[user])**2
    result=sum_XY/(float(math.sqrt(dem1))*float(math.sqrt(dem2)))
    return result


def computeDeviations(users):
    freq={}
    deviation={}

    for user,ratings in users.items():

        for music1, ratings1 in ratings.items():

            deviation.setdefault(music1,{})
            freq.setdefault(music1,{})
            for music2, ratings2 in ratings.items():

                if music1!=music2:
                    deviation[music1].setdefault(music2,0)
                    deviation[music1][music2]+=ratings1-ratings2
                    freq[music1].setdefault(music2,0)
                    freq[music1][music2]+=1
    # print(deviation)
    # print(freq)


    for item1,item2 in deviation.items():
        for  item3,rating in item2.items():
            deviation[item1][item3]=rating/float(freq[item1][item3])

    return deviation,freq


def slopeoneRecommand(userRating):
    deviation,freq=computeDeviations(users2)
    # print(deviation)
    # print(userRating)
    recommand={}
    freqs={}
    for d_user,d_user_item in deviation.items():
        if d_user not in userRating:
            for key,value in userRating.items():
                if key in d_user_item:
                    recommand.setdefault(d_user,0)
                    recommand[d_user]+=(value+d_user_item[key])*freq[key][d_user]
                    freqs.setdefault(d_user,0)
                    freqs[d_user]+=freq[d_user][key]
    r=[(k,v/float(freqs[k]))for k,v in recommand.items()]
    r=sorted(r,key=lambda x:x[1],reverse=True)
    print(r)
# print(computeSimilarity('Blues Traveler','Deadmau5',users3))
# print(computeSimilarity("Fall Out Boy","Daft Punk",users3))
# computeDeviations(users2)
g=users2['Clara']
slopeoneRecommand(g)













