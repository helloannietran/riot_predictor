#Annie Tran
#riot analysis using random forest

install.packages("randomForest")
require(randomForest)
require("gdata")
fulldata = read.xls('/Users/isarasuntichotinun/Desktop/ANNIE/CSC 591/riot_predictor/completedata.xlsx',sheet=1,header=T)
# fulldata = fulldata[1:6100,]
fulldata$X<-NULL
fulldata$X.1<-NULL
fulldata$Duration<-NULL
colnames(fulldata)[7] <- "violence.rating"

fulldata$target<-as.factor(fulldata$target)
fulldata$npart<-as.factor(fulldata$npart)
fulldata$issue<-as.factor(fulldata$issue)
fulldata$riot<-as.factor(fulldata$riot)

table(fulldata$riot)/nrow(fulldata)

#split to train and test
#randomize the rows
randomizeddata <- fulldata[sample(nrow(fulldata)),]
randomizeddata$locality<-NULL
randomizeddata$country<-NULL

train = randomizeddata[1:4302,]
train$X<-NULL
test = randomizeddata[4303:nrow(randomizeddata),]
test$X<-NULL
#make sure it's similar distribution of 1 and 0 for train and test
table(test$riot)/nrow(test)
table(train$riot)/nrow(train) 

varNames <- names(train)
varNames <- varNames[!varNames %in% c("riot")] #exclude the target

# add + sign between exploratory variables
varNames1 <- paste(varNames, collapse = "+")
# Add response variable and convert to a formula object
rf.form <- as.formula(paste("riot", varNames1, sep = " ~ "))



riot.model <- randomForest(rf.form,train,ntree=200,importance=T)
plot(riot.model) #error doesn't decrease much after 100 trees
#green line is error rate for 1
#red line is error rate for 0
#black line is out of bag error
  #each observation has an error rate by feeding it to the trees that were not built from it
  #out of bag error is the mean error rate of the error rates of all the observations

riot.model$err.rate
#install.packages('party')
library(party)
#looking at variable importance
varImpPlot(riot.model,sort=T,main="Variable Importance",n.var=6)
var.imp <- data.frame(importance(riot.model,type=1))
var.imp$Variables <- row.names(var.imp)
var.imp[order(var.imp$MeanDecreaseAccuracy,decreasing = T),]
var.imp[order(var.imp$MeanDecreaseGini,decreasing = T),]

#another implementation of random forest
cf1 <- cforest(riot ~ . , data= train, control=cforest_unbiased(mtry=2,ntree=50)) # fit the random forest
varimp(cf1) # get variable importance, based on mean decrease in accuracy
varimpAUC(cf1)  # more robust towards class imbalance.


# Predicting response variable
train$predicted.response <- predict(riot.model ,train)

#output probabilities instead
train$predicted.response <- predict(riot.model ,train,type="prob")
train$predicted.response <- 1-train$predicted.response 

#confusion matrix
library(e1071)
library(caret)
# Create Confusion Matrix
#train (89% accuracy), 91% without duration
confusionMatrix(data=train$predicted.response,
                reference=train$riot,
                positive='1')

#test (82% accuracy), 84% without duration
test$predicted.response <- predict(riot.model ,test)
#prob
test$predicted.response <- predict(riot.model ,test, type="prob")




test$predicted.response<-1-test$predicted.response
#confusion matrix, #82% accuracy with Duration, #84% accuracy without duration
confusionMatrix(data=test$predicted.response,
                reference=test$riot,
                positive='1')
# cor(randomizeddata[,1],randomizeddata[,7])

#cross validation for feature selection
rf.cv <- rfcv(train[,1:6], train[,7], cv.fold=10)
with(rf.cv, plot(n.var, error.cv))

#run if gets "error in plot.new(): figure margins too large
dev.off()
par("mar")
#par(mar=c(5.1,4.1, 4.1, 2.1))

#feature selection
#creates a fake variable to make sure boruta works
train['fakevar'] = runif(nrow(train))
train = train[c(1,2,3,4,5,6,8,7)] #reorder the columns
#install.packages("Boruta")
library(Boruta)
boruta.train<-Boruta(train[,1:7], train[,8])
print(boruta.train)

#another way to look at importance of variable
#install.packages('relaimpo')


#code for plotting tree
# 
# options(repos='http://cran.rstudio.org')
# have.packages <- installed.packages()
# cran.packages <- c('devtools','plotrix','randomForest','tree')
# to.install <- setdiff(cran.packages, have.packages[,1])
# if(length(to.install)>0) install.packages(to.install)
# 
# library(devtools)
# if(!('reprtree' %in% installed.packages())){
#   install_github('araastat/reprtree')
# }
# for(p in c(cran.packages, 'reprtree')) eval(substitute(library(pkg), list(pkg=p)))
# #plot
# reprtree:::plot.getTree(riot.model)


#covariance matrix
library(corrplot)
#only between numeric variables not categorical
randomizeddata$target<-as.numeric(randomizeddata$target)
randomizeddata$npart<-as.numeric(randomizeddata$npart)
randomizeddata$issue<-as.numeric(randomizeddata$issue)
randomizeddata$crime.rate<-as.numeric(randomizeddata$crime.rate)
randomizeddata$deaths<-as.numeric(randomizeddata$deaths)
randomizeddata$violence.rating<-as.numeric(randomizeddata$violence.rating)
#visualize correlation matrix
corrplot(cor(randomizeddata[,1:6]), order = "hclust")

                   
