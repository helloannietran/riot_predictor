setwd('/Users/isarasuntichotinun/Desktop/ANNIE/CSC 591/Data/')
article_data = read.csv('/Users/isarasuntichotinun/Desktop/ANNIE/CSC 591/Data/article_data.csv')
article_data$X <- NULL
#convert categorical to numbers:
#issue: 
#1: Election
#2: Economy, Jobs
#3: Food, Water
#4: Environment Degradation
#5: Ethnic Discrimination
#6: Religion
#7: Education
#8: Foreign Affairs
#9: Domestic War, Violence
#10: Human Rights
#11: Pro-government
#12: Economic Resources/Assets
#13: Sport
unique(article_data$issue)
article_data$'issue1'<-NA
for (i in 1:nrow(article_data)){
  if (article_data$issue[i] == 'election'){
    article_data$issue1[i] = 1
  }
  else if (article_data$issue[i]=='jobs'){
    article_data$issue1[i] = 2
  }
  else if (article_data$issue[i]=='food'){
    article_data$issue1[i] = 3
  }
  else if (article_data$issue[i]=='env'){
    article_data$issue1[i] = 4
  }
  else if (article_data$issue[i]=='religion'){
    article_data$issue1[i] = 6
  }
  else if (article_data$issue[i]=='education'){
    article_data$issue1[i] = 7
  }
  else if (article_data$issue[i]=='foreign_affairs'){
    article_data$issue1[i] = 8
  }
  else if (article_data$issue[i]=='domestic'){
    article_data$issue1[i] = 9
  }
  else if (article_data$issue[i]=='human_rights'){
    article_data$issue1[i] = 10
  }
  else if (article_data$issue[i]=='sport'){
    article_data$issue1[i]= 13
  }
}

#group the number of participants
#1: less than 10
#2: 10-100
#3: 101-1,000
#4: 1,001-10,000
#5: 10,001-100,000
#6: 100,001 - 1,000,000
#7: over 1,000,000

article_data$npart = as.numeric(article_data$npart)
article_data$npart_cat <- NA
for (i in 1:nrow(article_data)){
  if (article_data$npart[i] < 10){
    article_data$npart_cat[i] = 1
  }
  else if (article_data$npart[i] <=100 & article_data$npart[i] >=10){
    article_data$npart_cat[i] = 2
  }
  else if (article_data$npart[i] <=1000 & article_data$npart[i] >=101){
    article_data$npart_cat[i] = 3
  }
  else if (article_data$npart[i] <=10000 & article_data$npart[i] >=1001){
    article_data$npart_cat[i] = 4
  }
  else if (article_data$npart[i] <=100000 & article_data$npart[i] >=10001){
    article_data$npart_cat[i] = 5
  } 
  else if (article_data$npart[i] <=1000000 & article_data$npart[i] >=100001){
    article_data$npart_cat[i] = 6
  } 
  else if (article_data$npart[i] > 1000000){
    article_data$npart_cat[i] = 7
  } 
}

article_data$locality <- NA
#fill in the empty city with state
for (i in 1:nrow(article_data)){
  if (article_data$city[i]==''){
    article_data$locality[i] = as.character(article_data$state[i])
  }
  else{
    article_data$locality[i] = as.character(article_data$city[i])
  }
}

article_data$state<- NULL
article_data$city<-NULL

write.csv(article_data, file = "article_data.csv",row.names=FALSE)

