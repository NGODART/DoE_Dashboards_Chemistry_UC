library(readxl)

#Data	
#ModelData <- read_excel("C:/Users/GodarN30918/OneDrive - Revvity/Desktop/DOE Project/Designs/First Use Case - Optimization of Copper-Mediated 18F-Fluorination Reactions/FactorScreening_Design_skeleton_w_results.xlsx")
ModelData <- SFDesign_w_Results

#Add the log10_RCC column 
ModelData$Log10_RCC <- log10(ModelData$RCC)

#Linear Model (with only the 5 independant variables)
Model <- lm(Log10_RCC ~ Temperature + DMA + Catalyst  + Pyridine + Atmosphere + Block +  I(Catalyst^2) + Atmosphere:Catalyst , data = ModelData)

#Summary of the Model
SummaryModel<-summary(Model)  

#Coefficient table
Coefficients<-data.frame(Predictor=rownames(SummaryModel$coefficients),SummaryModel$coefficients)

############################################################

#Rsquared
Rsquared <- SummaryModel$r.squared


############################################################

# Perform LOOCV
n <- nrow(ModelData)
mse <- 0
for (i in 1:n) {
  # Fit model without observation i
  fit <- lm(Log10_RCC ~ Temperature + DMA + Catalyst  + Pyridine + Atmosphere + Block +  I(Catalyst^2) + Atmosphere:Catalyst, data=ModelData[-i,])
  # Predict value of observation i
  pred <- suppressWarnings(predict(fit, newdata=ModelData[i,]))
  # Calculate squared difference between predicted and actual value
  mse <- mse + (pred - ModelData[i, "Log10_RCC"])^2
}

# Calculate Q2
variance <- var(ModelData$Log10_RCC)
Q2 <- 1 - (mse/n) / variance