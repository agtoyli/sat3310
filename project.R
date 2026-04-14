#! /usr/bin/Rscript
#may need to check on location of R download and edit for your local machine
graphics.off()
#load necessary packages
library(data.table)

#capture arguments
args <- commandArgs(trailingOnly = TRUE)

#assign arguments to variables
rPath <- args[1]
dataFile <- args[2]
catVarsRaw <- args[3]
numVarsRaw <- args[4]

#convert column names into vectors
catVars <- trimws(unlist(strsplit(catVarsRaw, ",")))
numVars <- trimws(unlist(strsplit(numVarsRaw, ",")))

#print processing info
cat("Processing file:", dataFile, "\n")
cat("Categorical variables selected:", paste(catVars, collapse=", "), "\n")
cat("Numeric variables selected:", paste(numVars, collapse=", "), "\n")

#load your data
df <- fread(dataFile)

#analyze categorical variables
for(var in catVars){
  #create frequency table
  counts <- table(df[[var]])
  orderedCounts <- sort(counts, decreasing = TRUE) 
  #cut off if more than 10 
  if(length(orderedCounts) > 10){
    orderedCounts <- orderedCounts[1:10]
  }
  #print output
  print(paste0(var, " Frequency Variable"))
  print(orderedCounts)
  
  #create file for plot
  png(filename = paste0(rPath, var, "_barplot.png"),
      width = 1000, height = 600)
  
  #adjust margins to to accomodate labels
  par(mar = c(5, 12, 4, 2)) 
  
  #create barplot
  barplot(orderedCounts, 
          main = paste0("Top 10 - ", var),
          horiz = TRUE, 
          las = 1,           # horizontal labels
          cex.names = 0.8,   # shrink label font
          names.arg = substr(names(orderedCounts), 1, 30)) #limit length of output
  
  dev.off()
}

#analyze numeric variables
for(var in numVars){
  #print summary
  print(paste0(var, " Summary Statistics"))
  print(summary(df[[var]]))
  print(sd(df[[var]], na.rm = TRUE))
  
  #open file
  png(paste0(rPath, var, "_hist.png"))
  #create histogram
  hist(df[[var]], main = paste0("Distribution of ", var),
       xlab = var)
  dev.off()
}