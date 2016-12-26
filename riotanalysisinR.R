setwd('/Users/isarasuntichotinun/Desktop/ANNIE/CSC 591/Data')

install.packages("gdata")
require("gdata")
fulldata = read.xls('combineddata.xlsx',sheet=1,header=T)
fulldata$X<-NULL

egypt = fulldata[fulldata$country=='Egypt',]
attach(egypt)

egypt$year =as.numeric(format(as.Date(Start.Date),'%Y'))


uniqueyr = unique(year)

nriot = list()
for (i in 1:length(uniqueyr)){
  nriot[i] <-(sum(riot[year==uniqueyr[i]]))
}
plot(uniqueyr,nriot,col='black')



#countries with the most riots happening
#1st: Egypt: 509
#2nd: Nigeria: 438
#3rd: Haiti: 210
#4th: Mexico: 137, South Africa: 115,...


riot = fuldata[fuldata$riot==1,]
countryfreq=table(riot$country)
plot(countryfreq)
countryfreq
order(countryfreq)

#countries with most protests happening
#1st: Egypt: 440
#2nd: Haiti: 222, Mexico: 236,
#3rd: South Africa: 194
#num of protests in Nigeria is 174 vs 438 riots
protest = fuldata[fuldata$riot==0,]
protestfreq=table(protest$country)

order(protestfreq)
plot(protestfreq)
# statefac <- factor(protest$country,
#                    levels = names(protestfreq[order(protestfreq, decreasing = TRUE)]))

vector<-character()

for (i in 1:length(protestfreq))
{
  #riot minus protest
  diff = countryfreq[i] - protestfreq[i]
  print (diff)
  vector[i] <- diff
}

#weights for the country will be based on this
order(as.numeric(vector),decreasing=T) 
vector[order(as.numeric(vector),decreasing=T)]
countryfreq[89] #Nigeria has the biggest difference 
protestfreq[89]

################Look at the target
rtargettab = table(riot$target)
#no protest targetting fans so have to make sure the table include
#value 0 for "Fans" category (6)
pdata <- factor(protest$target, levels = c(1:8))
ptargettab=table(pdata)

targetvector<-character()
for (i in 1:length(ptargettab))
{
  #riot minus protest
  diff = rtargettab[i] - ptargettab[i]
  print (diff)
  targetvector[i] <- diff
}

order(as.numeric(targetvector),decreasing=T) 
targetvector[order(as.numeric(targetvector),decreasing=T) ]
#ranked target indicators for riot:
#1st: Cititizens (opposition supporters) (1)
#2nd: Religious group (5)
#3rd: Police (3)
#4th: Military (7)
#5th: Corporations (4)
#6th: Fans (6)
#7th: Government (2)


#number of deaths
mean(protest$deaths)
mean(riot$deaths)

#death frequency table of the full data
fulldeathtab = table(fuldata$deaths)
plot(fulldeathtab)
#death table for riot only
riotdeathtab = table(riot$deaths)
#death table for protest only
protestdeathtab = table(protest$deaths)

deathsmorethan13 = fuldata[fuldata$deaths>=13,]
sum(deathsmorethan13$riot==1) #494
sum(deathsmorethan13$riot==0) #5
#maybe more than 13 is 98 more times as important as
#less than 15 in indicating a protest as a riot

deathslessthan13 = fuldata[fuldata$deaths<13,]
sum(deathslessthan13$riot==1) #2411
sum(deathslessthan13$riot==0) #3190

#split dataset####################################################
#randomize the rows
fulldata <- fuldata[sample(nrow(fuldata)),]
rownames(fulldata) <- seq(length=nrow(fulldata))

train = fulldata[1:4302,]
test = fulldata[4303:nrow(fulldata),]

#work with train dataset
riot = train[train$riot==1,]
protest=train[train$riot==0,]

rcountryfreq=table(riot$country)
rcountryfreq
order(rcountryfreq)
rcountryfreq[89]

pcountryfreq=table(protest$country)
pcountryfreq
order(pcountryfreq)
pcountryfreq[89]
#countries with most riots ranking
#1: Egypt: 327
#2: Nigeria: 289
#3: Haiti: 143

ind = order(rcountryfreq)
riotincountries = data.frame(matrix(data=0, ncol = 2, nrow =length(rcountryfreq)))
for (i in 1:length(rcountryfreq)){
  riotincountries$X1[i] = names(rcountryfreq[ind[i]])
  riotincountries$X2[i] = rcountryfreq[ind[i]]
}
 
countryMat = matrix(data=0,nrow=length(unique(fulldata$country)),ncol=length(unique(fulldata$country)))
rownames(countryMat) = unique(unique(fulldata$country))
colnames(countryMat) = unique(unique(fulldata$country))

levels = colnames(countryMat)
for (i in 1:length(rcountryfreq)){
  for (j in 1:length(rcountryfreq)){
    if (rcountryfreq[levels[j]]==0){
      countryMat[i,j] = rcountryfreq[levels[i]]
    }
    else{
    countryMat[i,j] = rcountryfreq[levels[i]]/rcountryfreq[levels[j]]
    }
  }
}

squared = countryMat %*% countryMat
sumrows = rowSums(squared)
sumrows =as.matrix(sumrows)
weights = matrix(data=0, nrow = length(rcountryfreq),ncol = 1)
for (i in 1:length(sumrows)){
  weights[i] =  (sumrows[i]/colSums(sumrows))
}

rownames(weights) = levels


